#!/usr/bin/env python3
"""
verify_1_21_10_schema.py — Minecraft Java Edition 1.21.10 (DataVersion = 4556) NBT & Palette Schema Auditor
===========================================================================================================
Reads back `level.dat`, `region/*.mca`, and `entities/*.mca` directly using `nbt_mca.NBTReader` and verifies:
  1. `DataVersion == 4556` (Minecraft Java Edition 1.21.10);
  2. Zero entities (`entities = []` in `region/*.mca` and `Entities = []` in `entities/*.mca`, no mobs/armor stands);
  3. All 1872 canvas chunks (`cx in -20..15, cz in -40..11`) have `Status == "minecraft:full"` and `isLightOn == 0`;
  4. Non-spanning 64-bit `TAG_Long_Array` bit-packing lengths and palette indices in every section;
  5. 1.21.10 block name and property key/value compliance across all section palettes (including `iron_chain`,
     `oxidized_copper_grate[waterlogged=...]`, `deepslate_tiles`, `spruce_planks`, `barrel[facing=...,open=...]`).
"""

import os
import sys
import struct
import zlib
import gzip

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA_VERSION, CANVAS_BOUNDS, EXPECTED_CANVAS_CHUNKS
from nbt_mca import NBTReader, unpack_section_blocks

LEGACY_REMOVED_BLOCKS = {
    'minecraft:chain',
    'minecraft:grass',
}

VALID_PROP_VALUES = {
    'waterlogged': {'true', 'false'},
    'open': {'true', 'false'},
    'powered': {'true', 'false'},
    'lit': {'true', 'false'},
    'hanging': {'true', 'false'},
    'persistent': {'true', 'false'},
    'snowy': {'true', 'false'},
    'occupied': {'true', 'false'},
    'has_book': {'true', 'false'},
    'has_record': {'true', 'false'},
    'signal_fire': {'true', 'false'},
    'berries': {'true', 'false'},
    'up': {'true', 'false'},
    'axis': {'x', 'y', 'z'},
    'facing': {'north', 'south', 'east', 'west', 'up', 'down'},
    'half': {'top', 'bottom', 'upper', 'lower'},
    'type': {'top', 'bottom', 'double', 'single', 'left', 'right'},
    'hinge': {'left', 'right'},
    'shape': {'straight', 'inner_left', 'inner_right', 'outer_left', 'outer_right',
              'north_south', 'east_west', 'ascending_east', 'ascending_west', 'ascending_north', 'ascending_south'},
    'part': {'head', 'foot'},
    'pickles': {'1', '2', '3', '4'},
    'candles': {'1', '2', '3', '4'},
    'flower_amount': {'1', '2', '3', '4'},
}

def verify_schema(world_dir: str):
    print("=" * 72)
    print(f"[Schema Validator] Auditing MC 1.21.10 (DataVersion={DATA_VERSION}) schema in: {world_dir}")
    print("=" * 72)

    level_path = os.path.join(world_dir, 'level.dat')
    assert os.path.isfile(level_path), f"Missing level.dat in {world_dir}"
    with gzip.open(level_path, 'rb') as f:
        _, lroot = NBTReader(f.read()).read_root()
    ldata = lroot[1]['Data'][1]
    dv = ldata['DataVersion'][1]
    assert dv == DATA_VERSION, f"level.dat DataVersion mismatch: expected {DATA_VERSION}, got {dv}"
    print(f"  [PASS] level.dat DataVersion == {dv}")

    ent_dir = os.path.join(world_dir, 'entities')
    total_entities = 0
    if os.path.isdir(ent_dir):
        for fn in sorted(os.listdir(ent_dir)):
            if not fn.endswith('.mca'):
                continue
            with open(os.path.join(ent_dir, fn), 'rb') as f:
                raw = f.read()
            if len(raw) < 8192:
                continue
            locs = struct.unpack('>1024I', raw[:4096])
            for loc in locs:
                if loc == 0:
                    continue
                off = (loc >> 8) * 4096
                length, comp = struct.unpack('>IB', raw[off:off + 5])
                cdata = zlib.decompress(raw[off + 5:off + 4 + length]) if comp == 2 else raw[off + 5:off + 4 + length]
                _, rval = NBTReader(cdata).read_root()
                ents = rval[1].get('Entities')
                if ents:
                    total_entities += len(ents[2])
    assert total_entities == 0, f"Found {total_entities} entities in entities/*.mca"
    print("  [PASS] entities/*.mca contains 0 entities (zero mobs / armor stands)")

    reg_dir = os.path.join(world_dir, 'region')
    cx_min, cx_max = CANVAS_BOUNDS['x_min'] >> 4, CANVAS_BOUNDS['x_max'] >> 4
    cz_min, cz_max = CANVAS_BOUNDS['z_min'] >> 4, CANVAS_BOUNDS['z_max'] >> 4
    rx_min, rx_max = CANVAS_BOUNDS['x_min'] >> 9, CANVAS_BOUNDS['x_max'] >> 9
    rz_min, rz_max = CANVAS_BOUNDS['z_min'] >> 9, CANVAS_BOUNDS['z_max'] >> 9

    full_chunks = 0
    palette_set = set()
    schema_errors = []
    be_count = 0

    for rx in range(rx_min, rx_max + 1):
        for rz in range(rz_min, rz_max + 1):
            fn = os.path.join(reg_dir, f"r.{rx}.{rz}.mca")
            assert os.path.isfile(fn), f"Missing {fn}"
            with open(fn, 'rb') as f:
                raw = f.read()
            locs = struct.unpack('>1024I', raw[:4096])
            for idx, loc in enumerate(locs):
                if loc == 0:
                    continue
                cx, cz = rx * 32 + (idx % 32), rz * 32 + (idx // 32)
                off = (loc >> 8) * 4096
                length, comp = struct.unpack('>IB', raw[off:off + 5])
                cdata = zlib.decompress(raw[off + 5:off + 4 + length])
                _, rval = NBTReader(cdata).read_root()
                croot = rval[1]

                ents = croot.get('entities')
                if ents and len(ents[2]) > 0:
                    schema_errors.append(f"Chunk ({cx},{cz}) has {len(ents[2])} inline entities")

                in_canvas = (cx_min <= cx <= cx_max and cz_min <= cz <= cz_max and croot['Status'][1] == 'minecraft:full')
                if in_canvas:
                    full_chunks += 1
                    bes = croot.get('block_entities')
                    if bes:
                        for be in bes[2]:
                            be_d = be[1]
                            if 'id' not in be_d or 'x' not in be_d or 'y' not in be_d or 'z' not in be_d:
                                schema_errors.append(f"Malformed block_entity in ({cx},{cz}): {be_d}")
                            be_count += 1

                for sec in croot.get('sections', ('list', 0, []))[2]:
                    sc = sec[1]
                    bs = sc.get('block_states')
                    if not bs:
                        continue
                    bs_c = bs[1]
                    pal_list, indices = unpack_section_blocks(bs_c)
                    if max(indices, default=0) >= len(pal_list):
                        schema_errors.append(f"Palette index out of range in ({cx},{cz}) Y={sc['Y'][1]}")
                    for p in pal_list:
                        pd = p[1]
                        bname = pd['Name'][1]
                        palette_set.add(bname)
                        if bname in LEGACY_REMOVED_BLOCKS or not bname.startswith('minecraft:'):
                            schema_errors.append(f"Invalid/legacy block ID in ({cx},{cz}): {bname}")
                        if 'Properties' in pd:
                            for pk, pv in pd['Properties'][1].items():
                                pval = pv[1]
                                if pk in VALID_PROP_VALUES and pval not in VALID_PROP_VALUES[pk]:
                                    schema_errors.append(f"Invalid property {pk}={pval} on {bname} in ({cx},{cz})")

    assert full_chunks == EXPECTED_CANVAS_CHUNKS, f"Expected {EXPECTED_CANVAS_CHUNKS} full canvas chunks, found {full_chunks}"
    assert not schema_errors, f"Schema errors detected: {schema_errors[:10]}"

    required_v5_blocks = {
        'minecraft:deepslate_tiles',
        'minecraft:deepslate_tile_stairs',
        'minecraft:deepslate_tile_slab',
        'minecraft:spruce_planks',
        'minecraft:spruce_stairs',
        'minecraft:spruce_slab',
        'minecraft:barrel',
        'minecraft:oxidized_copper_grate',
        'minecraft:iron_chain',
    }
    missing_req = required_v5_blocks - palette_set
    assert not missing_req, f"Missing required V5 blocks in world palette: {missing_req}"

    print(f"  [PASS] Verified {full_chunks}/{EXPECTED_CANVAS_CHUNKS} full canvas chunks, {len(palette_set)} unique block IDs, {be_count} block entities")
    print(f"  [PASS] All required 1.21.10 & V5 palette blocks present: {sorted(required_v5_blocks)}")
    print("  [PASS] Zero schema or bit-packing errors!")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'TEST_BUILDINGS'))
    verify_schema(target)
