#!/usr/bin/env python3
"""pregen_seed_world.py — 用官方 1.21.10 服务端从种子号无头预生成原始世界模板

流程：
  1. 在临时目录初始化官方服务端（level-seed 固定为庄园种子）；
  2. 启动后通过控制台执行 `forceload add`（拆为 48 个 16×16 区块 = 256 区块的矩形），
       强制把预生成储备范围（12288 个区块）生成到 Status=full；
  3. `save-all` + `stop` 后剥离为极简模板（仅 level.dat + region/）。

设计原则（见 docs/ARCHITECTURE.md）：
  「seed_world 一次备足、CANVAS_BOUNDS 按需扩展」。
  seed_world 的已生成 full 区块范围只需 **包含** CANVAS_BOUNDS 即可；
  生成器只读写 CANVAS_BOUNDS 内的区块，范围外的区块原样保留。

用法：
  python tools/pregen_seed_world.py --accept-eula [--out ./seed_world]

注意：--accept-eula 表示你已阅读并同意《Minecraft 最终用户许可协议》
（https://aka.ms/MinecraftEULA）。
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time

SEED = "-6741035750265810117"

PRESERVE_X_MIN, PRESERVE_X_MAX = -1024, 511
PRESERVE_Z_MIN, PRESERVE_Z_MAX = -1024, 1023

FORCELOAD_RECTS = [
    (x, z, x + 255, z + 255)
    for x in range(PRESERVE_X_MIN, PRESERVE_X_MAX + 1, 256)
    for z in range(PRESERVE_Z_MIN, PRESERVE_Z_MAX + 1, 256)
]

EXPECTED_CANVAS_CHUNKS = 12288

CANVAS_CHUNKS = 1872

DEFAULT_SERVER_JAR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "minecraft-server.jar")
DEFAULT_JAVA = "java"

SERVER_PROPERTIES = f"""\
# Modern Manor 种子世界预生成（自动生成，请勿手改）
level-seed={SEED}
gamemode=creative
difficulty=peaceful
spawn-monsters=false
spawn-animals=false
spawn-npcs=false
generate-structures=true
online-mode=false
enable-command-block=false
view-distance=10
simulation-distance=10
spawn-protection=0
max-tick-time=600000
sync-chunk-writes=false
"""

def iter_region_files(region_dir):
    """枚举 region 目录下所有 .mca，返回 (rx, rz, 文件路径)。"""
    import re
    for fn in sorted(os.listdir(region_dir)):
        m = re.fullmatch(r"r\.(-?\d+)\.(-?\d+)\.mca", fn)
        if m:
            yield int(m.group(1)), int(m.group(2)), os.path.join(region_dir, fn)

def count_full_chunks(region_dir, cx_min=None, cx_max=None, cz_min=None, cz_max=None):
    """统计指定区块矩形内 Status=full 的区块数。

    默认统计整个预生成储备范围（PRESERVE_*）。传入 cx/cz 边界可改为只统计
    CANVAS_BOUNDS 覆盖的那一小块。
    """
    import struct
    import zlib

    if cx_min is None:
        cx_min, cx_max = PRESERVE_X_MIN >> 4, PRESERVE_X_MAX >> 4
        cz_min, cz_max = PRESERVE_Z_MIN >> 4, PRESERVE_Z_MAX >> 4

    total = 0
    for rx, rz, fn in iter_region_files(region_dir):
        with open(fn, "rb") as f:
            raw = f.read()
        if len(raw) < 8192:
            continue
        locs = struct.unpack(">1024I", raw[:4096])
        for idx, loc in enumerate(locs):
            if loc == 0:
                continue
            cx, cz = rx * 32 + idx % 32, rz * 32 + idx // 32
            if not (cx_min <= cx <= cx_max and cz_min <= cz <= cz_max):
                continue
            off = (loc >> 8) * 4096
            length = struct.unpack(">I", raw[off:off + 4])[0]
            if raw[off + 4] != 2:
                continue
            cdata = zlib.decompress(raw[off + 5:off + 4 + length])
            if b"minecraft:full" in cdata[:8192]:
                total += 1
    return total

def log_reader(proc, lines):
    for line in proc.stdout:
        lines.append(line.rstrip())
        print(f"[server] {line.rstrip()}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="seed_world", help="模板输出目录")
    ap.add_argument("--server-jar", default=DEFAULT_SERVER_JAR)
    ap.add_argument("--java", default=DEFAULT_JAVA)
    ap.add_argument("--accept-eula", action="store_true",
                    help="确认已阅读并同意 Minecraft EULA")
    args = ap.parse_args()

    if not args.accept_eula:
        sys.exit("请先阅读 https://aka.ms/MinecraftEULA 并加 --accept-eula 运行。")
    if not os.path.isfile(args.server_jar):
        sys.exit(f"找不到服务端 jar: {args.server_jar}\n"
                 "请将官方 minecraft-server.jar（1.21.10）放入 tools/ 目录，"
                 "或用 --server-jar 指定路径。")

    try:
        out = subprocess.run([args.java, "-version"],
                             capture_output=True, text=True).stderr
        import re
        m = re.search(r'version "(\d+)', out)
        if not m or int(m.group(1)) < 21:
            raise ValueError(out)
    except (FileNotFoundError, ValueError) as e:
        sys.exit(f"需要 Java 21+（当前: {args.java}）。"
                 "请安装 JDK 21+ 并加入 PATH，或用 --java 指定 java 可执行文件。")

    tmp = tempfile.mkdtemp(prefix="manor_seed_server_")
    print(f"服务端工作目录: {tmp}")
    try:
        with open(os.path.join(tmp, "eula.txt"), "w") as f:
            f.write("eula=true\n")
        with open(os.path.join(tmp, "server.properties"), "w") as f:
            f.write(SERVER_PROPERTIES)

        proc = subprocess.Popen(
            [args.java, "-Xmx6G", "-jar", args.server_jar, "nogui"],
            cwd=tmp, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding="utf-8",
            errors="replace", bufsize=1)
        lines = []
        t = threading.Thread(target=log_reader, args=(proc, lines), daemon=True)
        t.start()

        def wait_for(pred, timeout, desc):
            t0 = time.time()
            seen = 0
            while time.time() - t0 < timeout:
                for line in lines[seen:]:
                    if pred(line):
                        return True
                seen = len(lines)
                time.sleep(0.5)
            sys.exit(f"超时：{desc}")

        print("等待服务端初始化完成...")
        wait_for(lambda l: 'Done (' in l and 'For help' in l, 600, "服务端启动")

        region_dir = os.path.join(tmp, "world", "region")
        BATCH_RECTS = 8

        def region_total_bytes():
            total = 0
            if os.path.isdir(region_dir):
                for fn in os.listdir(region_dir):
                    if fn.endswith(".mca"):
                        total += os.path.getsize(os.path.join(region_dir, fn))
            return total

        def cmd(text):
            proc.stdin.write(text + "\n")
            proc.stdin.flush()

        def wait_region_stable(desc, poll=10, need_stable=3, timeout=1800):
            """轮询 region 总大小直至连续 need_stable 次不变。"""
            last, stable, t0 = -1, 0, time.time()
            while True:
                time.sleep(poll)
                cmd("save-all")
                total = region_total_bytes()
                print(f"  [{desc}] region 总大小={total / 1048576:.1f} MB")
                if total == last:
                    stable += 1
                else:
                    stable = 0
                last = total
                if stable >= need_stable:
                    return
                if time.time() - t0 > timeout:
                    sys.exit(f"超时：{desc} 超过 {timeout // 60} 分钟")

        batches = [FORCELOAD_RECTS[i:i + BATCH_RECTS]
                   for i in range(0, len(FORCELOAD_RECTS), BATCH_RECTS)]
        print(f"共 {len(FORCELOAD_RECTS)} 个矩形，分 {len(batches)} 批 "
              f"（每批 {BATCH_RECTS} 个 = {BATCH_RECTS * 256} 区块）...")

        for bi, batch in enumerate(batches, 1):
            print(f"=== 第 {bi}/{len(batches)} 批 forceload ===")
            for (x1, z1, x2, z2) in batch:
                c = f"forceload add {x1} {z1} {x2} {z2}"
                print(f"执行 {c} ...")
                cmd(c)
                time.sleep(0.5)
            wait_region_stable(f"批次 {bi}/{len(batches)}")

            for (x1, z1, x2, z2) in batch:
                cmd(f"forceload remove {x1} {z1} {x2} {z2}")
            time.sleep(1)
            print(f"=== 第 {bi}/{len(batches)} 批完成并已卸载 ===")

        print(f"等待全部 {EXPECTED_CANVAS_CHUNKS} 个储备区块落盘（每 10 秒检查一次）...")
        wait_region_stable("收尾")

        print("保存并关闭服务端...")
        proc.stdin.write("save-all\nstop\n")
        proc.stdin.flush()
        proc.wait(timeout=300)

        world_dir = os.path.join(tmp, "world")
        if os.path.isdir(args.out):
            shutil.rmtree(args.out)
        os.makedirs(os.path.join(args.out, "region"))
        shutil.copy2(os.path.join(world_dir, "level.dat"), args.out)
        for fn in os.listdir(os.path.join(world_dir, "region")):
            if fn.endswith(".mca"):
                shutil.copy2(os.path.join(world_dir, "region", fn),
                             os.path.join(args.out, "region", fn))
        print(f"模板已输出到: {os.path.abspath(args.out)}")

        full = count_full_chunks(os.path.join(args.out, "region"))
        print(f"储备范围 full 区块: {full} / {EXPECTED_CANVAS_CHUNKS}")
        if full < EXPECTED_CANVAS_CHUNKS:
            sys.exit("区块未全部生成，请重跑（或改用游戏内传送补全）")

        sys.path.insert(0, os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "generator_src"))
        from config import CANVAS_BOUNDS
        canvas_full = count_full_chunks(
            os.path.join(args.out, "region"),
            CANVAS_BOUNDS['x_min'] >> 4, CANVAS_BOUNDS['x_max'] >> 4,
            CANVAS_BOUNDS['z_min'] >> 4, CANVAS_BOUNDS['z_max'] >> 4)
        print(f"CANVAS_BOUNDS full 区块: {canvas_full} / {CANVAS_CHUNKS}")
        if canvas_full < CANVAS_CHUNKS:
            sys.exit("CANVAS_BOUNDS 未被 seed_world 完整覆盖，生成器将无法运行！")
        print("OK: 储备范围已完全覆盖 CANVAS_BOUNDS。")
        print("下一步: python generator_src/generate_estate.py "
              "<复制出的测试存档目录>")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
