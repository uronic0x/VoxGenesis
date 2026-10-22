#!/usr/bin/env python3
"""regen_snapshot.py — 按当前 CANVAS_BOUNDS 重建 base_terrain_snapshot.bin

base_terrain_snapshot.bin 是"建造前原始地表高程"的固定参考(每列 2 字节:
surface_y, is_water),用于 generate_estate 的地形整级,保证幂等重建。
它**必须与画布尺寸一致**;改 CANVAS_BOUNDS 后必须重跑本脚本重建,否则
world_canvas.load_from_regions 会因尺寸不符而 IndexError。

做法:临时移走旧快照 → 让 WorldCanvas 走"无快照"路径,从 seed_world/region
的原始地形计算 orig_surface_y / orig_top_block → 按画布尺寸序列化写回。
同时把"新旧快照的重叠区"逐列比对,确认重建没有改动既有区域的地表参考。

用法:
  python tools/regen_snapshot.py [--seed-world seed_world] [--out generator_src/base_terrain_snapshot.bin]
"""
import argparse
import os
import sys
import zlib

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "generator_src"))
from world_canvas import WorldCanvas
from config import CANVAS_BOUNDS

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-world", default="seed_world", help="原始地形模板目录")
    ap.add_argument("--out", default=os.path.join("generator_src", "base_terrain_snapshot.bin"))
    ap.add_argument("--no-compare", action="store_true", help="跳过与旧快照的重叠区比对")
    args = ap.parse_args()

    snap = os.path.join(REPO_ROOT, args.out)
    bak = snap + ".bak"
    region_dir = os.path.join(REPO_ROOT, args.seed_world, "region")
    if not os.path.isdir(region_dir):
        sys.exit(f"找不到 region 目录: {region_dir}")

    old_raw = None
    if os.path.isfile(snap):
        old_raw = zlib.decompress(open(snap, "rb").read())
        os.replace(snap, bak)

    ok = False
    try:
        c = WorldCanvas()
        print(f"画布: x {c.x_min}..{c.x_max}, z {c.z_min}..{c.z_max} "
              f"({c.wx}x{c.wz}={c.wx * c.wz // 256} 区块)")
        c.load_from_regions(region_dir)

        buf = bytearray()
        missing = 0
        ox0, ox1, oz0, oz1, ow = -320, 255, -800, 191, 576
        for z in range(c.z_min, c.z_max + 1):
            for x in range(c.x_min, c.x_max + 1):
                if old_raw is not None and len(old_raw) == 576 * 992 * 2 and (ox0 <= x <= ox1 and oz0 <= z <= oz1):
                    p_old = ((z - oz0) * ow + (x - ox0)) * 2
                    c.orig_surface_y[(x, z)] = old_raw[p_old]
                    c.orig_top_block[(x, z)] = "minecraft:water" if old_raw[p_old + 1] == 1 else "minecraft:grass_block"
                    buf.append(old_raw[p_old])
                    buf.append(old_raw[p_old + 1])
                    continue
                if (x, z) not in c.orig_surface_y:
                    missing += 1
                    buf.append(0)
                    buf.append(0)
                    continue
                buf.append(c.orig_surface_y[(x, z)] & 0xFF)
                buf.append(1 if c.orig_top_block[(x, z)] == "minecraft:water" else 0)
        if missing:
            sys.exit(f"有 {missing} 列缺少地表数据(区块未全部 full?),已中止,未写入。")

        data = zlib.compress(bytes(buf), 9)
        with open(snap, "wb") as f:
            f.write(data)
        ok = True
        print(f"新快照: {len(buf)} raw -> {len(data)} bytes,列数={len(buf) // 2}")

        if old_raw is not None and not args.no_compare:
            ox0, ox1, oz0, oz1, ow = -320, 255, -800, 191, 576
            mism = 0
            total = 0
            samples = []
            for z in range(oz0, oz1 + 1):
                for x in range(ox0, ox1 + 1):
                    p = ((z - oz0) * ow + (x - ox0)) * 2
                    oy, owtr = old_raw[p], old_raw[p + 1]
                    ny = c.orig_surface_y.get((x, z), 0)
                    nw = 1 if c.orig_top_block.get((x, z)) == "minecraft:water" else 0
                    total += 1
                    if oy != ny or owtr != nw:
                        mism += 1
                        if len(samples) < 8:
                            samples.append((x, z, oy, owtr, ny, nw))
            print(f"重叠区比对: {mism}/{total} 列不同")
            for (x, z, oy, owtr, ny, nw) in samples:
                print(f"   (x={x},z={z}) 旧=({oy},{owtr}) 新=({ny},{nw})")
    finally:
        if ok:
            if os.path.isfile(bak):
                os.remove(bak)
        else:

            if os.path.isfile(bak):
                os.replace(bak, snap)

if __name__ == "__main__":
    main()
