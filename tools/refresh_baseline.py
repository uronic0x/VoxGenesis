#!/usr/bin/env python3
"""refresh_baseline.py — 端到端刷新"验证基线"(按代码版本命名)

把整条种子→预生成→生成→校验→验证链跑一遍,把产出的 validation_report.json
按当前代码版本(git describe)命名后落盘到 generator_src/baselines/ 并 git add,
作为该代码版本的回归对比基线。

确定性契约(实测,2026-10-18 两次 fresh-pregen 比对):
  - 字节稳定:full_chunks_verified(1221)、border_chunks_verified、unique_palette_blocks、
    全部 zone_structural_counts(人建结构)与 _baseline_meta——这些字段两次完全一致。
  - 含自然地形噪声(~百块级):pregen(原版服务端地形生成)非字节确定,洞穴雕刻/流体
    沉降/跨区块装饰依赖 tick 时序(日志可见 'Can't keep up! ... ticks behind')。
    故 total_non_air_blocks 与 top_25 中的原版地形方块(stone/ores/dirt/water/moss 等)
    每次会有 ~0.001% 抖动;生成器 generate_estate 本身确定(人建结构零差异)。
  - 历史对照以 zone_structural_counts 为准,不以 total_non_air 为准。
  世界种子不在此重复,统一由 tools/pregen_seed_world.py 的 SEED 常量管控——
  改种子即改代码,基线随之合法刷新。

用法:
  python tools/refresh_baseline.py --java <Java21+可执行文件> --accept-eula [选项]

  --java          Java 21+ 的 java 可执行文件路径(必填,不硬编码)
  --server-jar    官方 1.21.10 minecraft-server.jar(默认 tools/minecraft-server.jar)
  --accept-eula   透传给 pregen,表示已阅读并同意 https://aka.ms/MinecraftEULA
  --no-stage      只写基线文件,不执行 git add(默认会 git add)
  --baselines-dir 基线输出目录(默认 generator_src/baselines)
  --seed-world-out pregen 模板输出目录(默认 seed_world,gitignored)
  --test-out      生成/校验所用测试存档目录(默认 TEST_BUILDINGS,gitignored)

验证确定性的方法:连续跑两次本脚本,对比两次打印的"内容 SHA-256"是否一致。
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def git(*args):
    return subprocess.run(["git", *args], cwd=REPO_ROOT, text=True,
                          capture_output=True)

def git_out(*args):
    r = git(*args)
    if r.returncode != 0:
        sys.exit(f"git {args[0]} 失败: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()

def run(label, cmd):
    print(f"\n=== {label} ===\n$ {' '.join(cmd)}", flush=True)

    r = subprocess.run(cmd, cwd=REPO_ROOT,
                       env={**os.environ, "PYTHONUNBUFFERED": "1"})
    if r.returncode != 0:
        sys.exit(f"[{label}] 失败,退出码 {r.returncode}")
    return r

def main():
    ap = argparse.ArgumentParser(description="端到端刷新验证基线(按代码版本命名)")
    ap.add_argument("--java", required=True,
                    help="Java 21+ 的 java 可执行文件路径(必填,不硬编码)")
    ap.add_argument("--server-jar", default="tools/minecraft-server.jar",
                    help="官方 1.21.10 minecraft-server.jar(默认 tools/minecraft-server.jar)")
    ap.add_argument("--accept-eula", action="store_true",
                    help="已阅读并同意 Minecraft EULA(透传给 pregen)")
    ap.add_argument("--no-stage", action="store_true",
                    help="只写基线文件,不执行 git add")
    ap.add_argument("--baselines-dir", default="generator_src/baselines",
                    help="基线输出目录(默认 generator_src/baselines)")
    ap.add_argument("--seed-world-out", default="seed_world",
                    help="pregen 模板输出目录(默认 seed_world)")
    ap.add_argument("--test-out", default="TEST_BUILDINGS",
                    help="测试存档目录(默认 TEST_BUILDINGS)")
    ap.add_argument("--python", default=sys.executable,
                    help="跑各子脚本用的 Python 解释器(默认当前解释器)")
    args = ap.parse_args()

    sj = args.server_jar
    if not os.path.isabs(sj):
        sj = os.path.join(REPO_ROOT, sj)
    args.server_jar = os.path.abspath(sj)
    if not os.path.isfile(args.server_jar):
        sys.exit(f"找不到 server jar: {args.server_jar}")

    porcelain = git("status", "--porcelain", "--untracked-files=no").stdout.strip()
    dirty = "\n".join(l for l in porcelain.splitlines()
                      if l and "generator_src/baselines/" not in l)
    if dirty:
        sys.exit(
            "工作树有未提交的跟踪文件改动(基线目录除外):\n" + dirty +
            "\n\n请先 commit 再切基线。基线文件名 = 代码版本(git describe),"
            "从脏树切出的基线无法复现,违背确定性契约。"
        )
    describe = git_out("describe", "--tags", "--always")
    full_sha = git_out("rev-parse", "HEAD")
    print(f"代码版本: {describe}   HEAD: {full_sha[:12]}")

    if not args.accept_eula:
        sys.exit("需 --accept-eula(请先阅读 https://aka.ms/MinecraftEULA )")

    py = args.python
    gs = lambda n: os.path.join("generator_src", n)

    run("1/5 pregen seed_world(固定种子,可复现)",
        [py, "tools/pregen_seed_world.py",
         "--java", args.java,
         "--server-jar", args.server_jar,
         "--accept-eula",
         "--out", args.seed_world_out])

    sw_abs = os.path.join(REPO_ROOT, args.seed_world_out)
    test_abs = os.path.join(REPO_ROOT, args.test_out)
    if not os.path.isdir(sw_abs):
        sys.exit(f"pregen 未产出 {args.seed_world_out}/")
    if os.path.isdir(test_abs):
        shutil.rmtree(test_abs)
    shutil.copytree(sw_abs, test_abs)
    print(f"已重建 {args.test_out}/ (region + level.dat)")

    run("2/5 generate_estate",        [py, gs("generate_estate.py"), args.test_out])
    run("3/5 verify_1_21_10_schema",  [py, gs("verify_1_21_10_schema.py"), args.test_out])
    run("4/5 audit_spatial_connectivity", [py, gs("audit_spatial_connectivity.py"), args.test_out])
    run("5/5 validate_and_render",   [py, gs("validate_and_render.py"), args.test_out, "."])

    src_report = os.path.join(REPO_ROOT, "validation_report.json")
    with open(src_report, encoding="utf-8") as f:
        report = json.load(f)
    report["_baseline_meta"] = {
        "git_describe": describe,
        "git_commit": full_sha,
        "pregen_seed_const": "见 tools/pregen_seed_world.py 的 SEED 常量(不在此复制,避免漂移)",
        "server_jar": os.path.basename(args.server_jar),
        "java_runtime": os.path.basename(os.path.dirname(os.path.dirname(args.java))),
        "cut_by": os.path.basename(__file__),
    }
    baselines_abs = os.path.join(REPO_ROOT, args.baselines_dir)
    os.makedirs(baselines_abs, exist_ok=True)
    out_name = f"validation_report_{describe.replace('/', '_')}.json"
    out_path = os.path.join(baselines_abs, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    content_sha = hashlib.sha256(
        json.dumps(report, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    print(f"\n基线已落盘: {os.path.relpath(out_path, REPO_ROOT)}")
    print(f"内容 SHA-256: {content_sha}")

    rel = os.path.relpath(out_path, REPO_ROOT).replace("\\", "/")
    if not args.no_stage:
        r = git("add", rel)
        if r.returncode != 0:
            print(f"git add 失败: {r.stderr.strip()}")
        else:
            print(f"已 git add {rel}")
            print(f'建议提交: git commit -m "chore: 刷新验证基线 {describe}"')
    else:
        print(f"跳过 git add(--no-stage);文件位于 {rel}")

    print('\n注:pregen 含 ~百块级自然地形噪声(见脚本头"确定性契约")。')
    print('   历史对照请以 zone_structural_counts 为准(人建结构,字节稳定)。')

if __name__ == "__main__":
    main()
