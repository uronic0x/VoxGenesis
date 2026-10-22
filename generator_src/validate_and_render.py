#!/usr/bin/env python3
"""
validate_and_render.py — Full Read-Back Parser Validation & Isometric/Top-Down Renderer (V5.5)
==============================================================================================
1. Parses every .mca region file in region/ and entities/ using nbt_mca.NBTReader.
2. Verifies chunk status, section palettes, 64-bit long array bit-packing lengths,
   block counts, isLightOn=0 lighting triggers, and Heightmaps across all 2,232 full chunks.
3. Confirms zero P0 floating mountain tree/leaf/vine/bamboo residuals across all chunks.
4. Confirms zero entities / armor stands in both region/*.mca and entities/*.mca.
5. Renders high-resolution Top-Down Master Plan, 4 Architectural Elevation / Section
   Views, and 4 V5.5 Detail Verification Sheets to PNG for visual engineering inspection.
"""

import os
import sys
import struct
import zlib
import gzip
import json
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import MANOR_VERSION, CANVAS_BOUNDS, EXPECTED_CANVAS_CHUNKS
from nbt_mca import NBTReader, unpack_section_blocks

def _resolve_display_version():
    return MANOR_VERSION.upper()

def run_validation_and_render(world_dir, out_dir):
    print("=" * 72)
    print("[Validator] Starting Read-Back NBT & Anvil (.mca) Verification...")
    print("=" * 72)

    region_dir = os.path.join(world_dir, "region")
    entities_dir = os.path.join(world_dir, "entities")

    level_dat_path = os.path.join(world_dir, "level.dat")
    with gzip.open(level_dat_path, 'rb') as f:
        _, level_root = NBTReader(f.read()).read_root()
    data_tag = level_root[1]['Data'][1]
    data_version = data_tag['DataVersion'][1]
    spawn_x = data_tag['SpawnX'][1]
    spawn_y = data_tag['SpawnY'][1]
    spawn_z = data_tag['SpawnZ'][1]
    print(f"  [OK] level.dat verified: DataVersion={data_version}, Spawn=({spawn_x}, {spawn_y}, {spawn_z})")

    entity_count_total = 0
    if os.path.isdir(entities_dir):
        for fname in sorted(os.listdir(entities_dir)):
            if not fname.endswith(".mca"):
                continue
            fpath = os.path.join(entities_dir, fname)
            with open(fpath, "rb") as f:
                raw = f.read()
            if len(raw) < 8192:
                continue
            for idx in range(1024):
                loc = struct.unpack(">I", raw[idx * 4 : idx * 4 + 4])[0]
                if loc == 0:
                    continue
                offset = (loc >> 8) * 4096
                length = struct.unpack(">I", raw[offset : offset + 4])[0]
                comp = raw[offset + 4]
                payload = zlib.decompress(raw[offset + 5 : offset + 4 + length]) if comp == 2 else raw[offset + 5 : offset + 4 + length]
                _, root = NBTReader(payload).read_root()
                ents = root[1].get('Entities')
                if ents and len(ents[2]) > 0:
                    entity_count_total += len(ents[2])
    assert entity_count_total == 0, f"Found {entity_count_total} entities in entities/*.mca!"
    print("  [OK] entities/*.mca verified: 0 entities across all entity region files.")

    x_min, x_max = CANVAS_BOUNDS['x_min'], CANVAS_BOUNDS['x_max']
    z_min, z_max = CANVAS_BOUNDS['z_min'], CANVAS_BOUNDS['z_max']
    y_min, y_max = CANVAS_BOUNDS['y_min'], CANVAS_BOUNDS['y_max']
    cx_min, cx_max = x_min >> 4, x_max >> 4
    cz_min, cz_max = z_min >> 4, z_max >> 4
    rx_min, rx_max = x_min >> 9, x_max >> 9
    rz_min, rz_max = z_min >> 9, z_max >> 9

    sx = x_max - x_min + 1
    sz = z_max - z_min + 1
    sy_len = y_max - y_min + 1

    cat_grid = np.zeros((sx, sz, sy_len), dtype=np.uint8)

    def classify_block(bname):
        if bname in ("minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:light"):
            return 0
        if "water" in bname or "kelp" in bname or "seagrass" in bname:
            return 1
        if bname in ("minecraft:grass_block", "minecraft:moss_block", "minecraft:moss_carpet", "minecraft:podzol", "minecraft:mycelium"):
            return 2
        if "leaves" in bname or "log" in bname or "bamboo" in bname or "vine" in bname or "azalea" in bname:
            return 3
        if "sand" in bname or "sandstone" in bname:
            return 4
        if any(k in bname for k in ("quartz", "white_concrete", "calcite", "diorite", "iron_block", "white_terracotta", "snow")):
            return 6
        if any(k in bname for k in ("glass", "ice")):
            return 8
        if any(k in bname for k in ("red_", "crimson", "brick", "terracotta", "coral", "tnt", "campfire")):
            return 10
        if any(k in bname for k in ("froglight", "sea_lantern", "glowstone", "shroomlight", "lantern", "end_rod", "gold_block", "beacon", "yellow_concrete", "orange_concrete")):
            return 11
        if "copper" in bname or "prismarine" in bname or "cyan_" in bname or "light_blue_" in bname or "blue_" in bname:
            return 12
        if any(k in bname for k in ("wheat", "carrots", "potatoes", "beetroots", "farmland", "hay_block", "melon", "pumpkin")):
            return 13
        if any(k in bname for k in ("planks", "wood", "stripped_", "fence", "trapdoor", "door", "slab", "stairs", "lectern", "barrel", "bookshelf")) and "stone" not in bname and "quartz" not in bname and "deepslate" not in bname:
            return 7
        if any(k in bname for k in ("gray_concrete", "black_concrete", "deepslate", "blackstone", "basalt", "obsidian", "coal_block", "anvil")):
            return 9
        return 5

    block_counter = Counter()
    unique_palette_blocks = set()
    full_chunks_verified = 0
    border_chunks_verified = 0
    p0_sky_tree_errors = 0
    chunk_entity_errors = 0
    bitpack_errors = 0
    heightmap_errors = 0

    FORBIDDEN_SKY_BLOCKS = {
        "minecraft:jungle_leaves", "minecraft:jungle_log", "minecraft:vine",
        "minecraft:bamboo", "minecraft:cocoa",
    }

    for rx in range(rx_min, rx_max + 1):
        for rz in range(rz_min, rz_max + 1):
            rfname = f"r.{rx}.{rz}.mca"
            rfpath = os.path.join(region_dir, rfname)
            assert os.path.isfile(rfpath), f"Missing region file {rfname}"
            with open(rfpath, "rb") as f:
                raw = f.read()

            for idx in range(1024):
                loc = struct.unpack(">I", raw[idx * 4 : idx * 4 + 4])[0]
                if loc == 0:
                    continue
                cx = rx * 32 + (idx % 32)
                cz = rz * 32 + (idx // 32)
                offset = (loc >> 8) * 4096
                length = struct.unpack(">I", raw[offset : offset + 4])[0]
                comp = raw[offset + 4]
                payload = zlib.decompress(raw[offset + 5 : offset + 4 + length]) if comp == 2 else raw[offset + 5 : offset + 4 + length]
                _, root = NBTReader(payload).read_root()
                root_val = root[1]

                ents = root_val.get('entities')
                if ents and len(ents[2]) > 0:
                    chunk_entity_errors += len(ents[2])

                in_canvas = (cx_min <= cx <= cx_max) and (cz_min <= cz <= cz_max) and (root_val['Status'][1] == 'minecraft:full')
                if in_canvas:
                    full_chunks_verified += 1
                    hm = root_val.get('Heightmaps')
                    if not hm or 'MOTION_BLOCKING' not in hm[1] or len(hm[1]['MOTION_BLOCKING'][1]) != 37:
                        heightmap_errors += 1
                    is_light_on = root_val.get('isLightOn')
                    assert is_light_on is not None and is_light_on[1] == 0, f"Expected isLightOn=0 in ({cx},{cz})"
                else:
                    border_chunks_verified += 1

                sections = root_val.get('sections')
                if not sections:
                    continue

                for sec in sections[2]:
                    sec_val = sec[1]
                    sy = sec_val['Y'][1]
                    bs = sec_val.get('block_states')
                    if not bs:
                        continue
                    bs_comp = bs[1]
                    pal_list = bs_comp['palette'][2]
                    if len(pal_list) > 1:
                        bpe = max(4, (len(pal_list) - 1).bit_length())
                        epw = 64 // bpe
                        expected_longs = (4096 + epw - 1) // epw
                        actual_longs = len(bs_comp.get('data', ('long_array', []))[1])
                        if actual_longs != expected_longs:
                            bitpack_errors += 1
                            continue
                    pal_list, indices = unpack_section_blocks(bs_comp)
                    names = [p[1]['Name'][1] for p in pal_list]
                    props_list = [p[1].get('Properties', ('compound', {}))[1] for p in pal_list]

                    for n in names:
                        unique_palette_blocks.add(n)

                    idx_arr = np.asarray(indices, dtype=np.int32)

                    if sy >= 6:
                        forb_mask = np.array([n in FORBIDDEN_SKY_BLOCKS for n in names], dtype=bool)
                        leaf_mask = np.array([
                            (n not in FORBIDDEN_SKY_BLOCKS) and n.endswith("_leaves")
                            and (sy >= 7 or props_list[p].get('persistent', ('string', 'false'))[1] == 'false')
                            for p, n in enumerate(names)
                        ], dtype=bool)
                        p0_sky_tree_errors += int(forb_mask[idx_arr].sum() + leaf_mask[idx_arr].sum())

                    if in_canvas and (1 <= sy <= 10):
                        base_x = cx * 16 - x_min
                        base_z = cz * 16 - z_min
                        base_y = sy * 16 - y_min
                        pal_cat = np.array([classify_block(n) for n in names], dtype=np.uint8)
                        is_air = np.array([n == "minecraft:air" for n in names], dtype=bool)
                        pals, cnts = np.unique(idx_arr, return_counts=True)
                        for p, cnt in zip(pals, cnts):
                            if not is_air[p]:
                                block_counter[names[p]] += int(cnt)
                        blk = pal_cat[idx_arr].reshape(16, 16, 16).transpose(2, 1, 0)
                        m = blk > 0
                        sl = cat_grid[base_x:base_x + 16, base_z:base_z + 16, base_y:base_y + 16]
                        sl[m] = blk[m]

    print(f"  [OK] Full canvas chunks verified: {full_chunks_verified}/{EXPECTED_CANVAS_CHUNKS}")
    print(f"  [OK] Border/outer chunks verified: {border_chunks_verified}")
    print(f"  [OK] Bit-packing errors: {bitpack_errors}")
    print(f"  [OK] Heightmap errors: {heightmap_errors}")
    print(f"  [OK] Chunk entity count: {chunk_entity_errors}")
    print(f"  [OK] P0 high-altitude natural leaf/vine residuals: {p0_sky_tree_errors}")
    print(f"  [OK] Unique block types in palettes: {len(unique_palette_blocks)}")
    print(f"  [OK] Total non-air blocks in Y=16..175 canvas: {sum(block_counter.values()):,}")

    assert full_chunks_verified == EXPECTED_CANVAS_CHUNKS, f"Expected {EXPECTED_CANVAS_CHUNKS} full chunks, got {full_chunks_verified}"
    assert bitpack_errors == 0, f"Bitpack errors: {bitpack_errors}"
    assert heightmap_errors == 0, f"Heightmap errors: {heightmap_errors}"
    assert chunk_entity_errors == 0, f"Chunk entity errors: {chunk_entity_errors}"
    assert p0_sky_tree_errors == 0, f"P0 sky tree errors: {p0_sky_tree_errors}"

    zone_checks = {
        "Villa & Estate Core (X=-89..95, Z=-80..80)": ((-89, 95), (-80, 80), (63, 110)),
        "Scenic Woodland & Brook Buffer (X=-133..-90, Z=-95..45)": ((-133, -90), (-95, 45), (60, 85)),
        "Shifted West Agri-Tech Farm (X=-234..-134, Z=-95..45)": ((-234, -134), (-95, 45), (63, 95)),
        "North Golf Course & Canal (X=-110..137, Z=-250..-95)": ((-110, 137), (-250, -95), (60, 95)),
        "Seaside Park & Relocated Lighthouse (X=98..185, Z=-228..-16)": ((98, 185), (-228, -16), (50, 117)),
        "Underwater Viewing Tunnel & Dome (X=142..182, Z=-78..-56)": ((142, 182), (-78, -56), (50, 62)),
        "Cruise Boarding Terminal & Gangway (X=108..186, Z=-170..-134)": ((108, 186), (-170, -134), (64, 82)),
        "Luxury Cruise Ship 'Serenity of the Seas' (X=183..215, Z=-176..-56)": ((183, 215), (-176, -56), (56, 97)),
        "Supercar Showroom & 6 Voxel Supercars (X=-48..-12, Z=62..98)": ((-48, -12), (62, 98), (63, 75)),
        "Underwater Michelin Restaurant 'L'Abysse d'Or' (X=156..180, Z=-57..-28)": ((156, 180), (-57, -28), (50, 62)),
        "Barrel-Vaulted Cellar, Cigar Lounge & Art Vault (X=44..94, Z=-41..-22)": ((44, 94), (-41, -22), (58, 72)),
        "Enlarged North Sports Complex: 3-Block Track, Basketball & Arena (X=-220..128, Z=-396..-252)": ((-220, 128), (-396, -252), (60, 90)),
        "50-Block Coastal & Parkland Transition Belt (X=-220..185, Z=-447..-397)": ((-220, 185), (-447, -397), (58, 85)),
        "Santa Monica State Beach, Pacific Park Pier & East X+ Waterfall Cove (X=24..348, Z=-856..-448)": ((24, 348), (-856, -448), (50, 106)),
        "Palisades Bluff Park, 3rd St Promenade, Venice Canals & Aero Hangar (X=-312..23, Z=-856..-448)": ((-312, 23), (-856, -448), (58, 92)),
    }
    print("\n[Validator] Zone Structural Non-Air/Non-Water Block Audit:")
    zone_stats = {}
    for zname, ((x0, x1), (z0, z1), (y0, y1)) in zone_checks.items():
        sub = cat_grid[x0 - x_min : x1 - x_min + 1, z0 - z_min : z1 - z_min + 1, y0 - y_min : y1 - y_min + 1]
        solid_cnt = int(np.sum((sub > 1)))
        zone_stats[zname] = solid_cnt
        print(f"  - {zname}: {solid_cnt:,} structural/landscape blocks")
        assert solid_cnt > 500, f"Zone {zname} has unexpectedly low block count ({solid_cnt})!"

    summary = {
        "data_version": data_version,
        "spawn": [spawn_x, spawn_y, spawn_z],
        "full_chunks_verified": full_chunks_verified,
        "border_chunks_verified": border_chunks_verified,
        "bitpack_errors": bitpack_errors,
        "heightmap_errors": heightmap_errors,
        "entity_count": entity_count_total + chunk_entity_errors,
        "p0_sky_tree_errors": p0_sky_tree_errors,
        "unique_palette_blocks": len(unique_palette_blocks),
        "total_non_air_blocks": sum(block_counter.values()),
        "zone_structural_counts": zone_stats,
        "top_25_blocks": block_counter.most_common(25),
    }
    with open(os.path.join(out_dir, "validation_report.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n[Renderer] Generating Top-Down Master Plan (render_topdown.png)...")
    palette_rgb = {
        0: (20, 25, 35),
        1: (28, 107, 160),
        2: (88, 165, 70),
        3: (42, 112, 48),
        4: (232, 214, 156),
        5: (130, 134, 140),
        6: (242, 244, 247),
        7: (178, 132, 84),
        8: (145, 218, 238),
        9: (55, 60, 68),
        10: (204, 68, 60),
        11: (250, 218, 94),
        12: (64, 185, 195),
        13: (198, 172, 58),
    }

    lut = np.zeros((14, 3), dtype=np.float32)
    for k, v in palette_rgb.items():
        lut[k] = v

    solid = cat_grid > 0
    has_solid = solid.any(axis=2)
    top_idx = np.where(has_solid, sy_len - 1 - np.argmax(solid[:, :, ::-1], axis=2), 0)
    top_cat = np.take_along_axis(cat_grid, top_idx[..., None], axis=2)[..., 0]

    nonwater = cat_grid > 1
    has_nw = nonwater.any(axis=2)
    nw_idx = np.where(has_nw, sy_len - 1 - np.argmax(nonwater[:, :, ::-1], axis=2), 0)
    nw_cat = np.take_along_axis(cat_grid, nw_idx[..., None], axis=2)[..., 0]

    base = lut[top_cat]
    water_top = (top_cat == 1) & has_solid
    blend = water_top & has_nw & ((nw_idx + y_min) >= 51)
    base = np.where(water_top[..., None], lut[1], base)
    base[blend] = 0.45 * lut[1] + 0.55 * lut[nw_cat[blend]]

    shade = 1.0 + (top_idx + y_min - 64) * 0.008
    base = np.clip(base * shade[..., None], 0, 255)
    base[~has_solid] = (20, 25, 35)

    img_rgb = base.transpose(1, 0, 2)

    fig, ax = plt.subplots(figsize=(16, 22), dpi=160)
    ax.imshow(img_rgb.astype(np.uint8), extent=[x_min, x_max, z_max, z_min])
    ax.set_title(f"Modern Manor {_resolve_display_version()} — Master Plan Top-Down View (X: {x_min}..{x_max}, Z: {z_min}..{z_max})", fontsize=15, fontweight='bold', pad=12)
    ax.set_xlabel("World X Coordinate (West -X Palisades Bluffs  <--->  East +X Santa Monica Beach & Pier)", fontsize=12)
    ax.set_ylabel("World Z Coordinate (North -Z Extended Santa Monica Beach  <--->  South +Z Front Approach)", fontsize=12)

    annotations = [
        (-184, -25, "West Agri-Tech Farm\n(X=-234..-134)", "white", "#2b5b2e"),
        (-111, -25, "44m Woodland &\nBrook Buffer", "white", "#1f4d2b"),
        (0, -10, "Main Modern Villa\n& Courtyard\n(X=-89..95)", "black", "#f0f4f8"),
        (10, -175, "North Golf Course\n& Canal (Z=-250..-95)", "white", "#2e6f40"),
        (-128, -336, "Enlarged Track & Soccer Stadium\n(Widened 5-Lane Z-Stairs & VIP Box)", "white", "#b83b2b"),
        (8, -336, "Outdoor Basketball\nPark (3 Courts)", "black", "#ff9933"),
        (83, -336, "Indoor Sports Arena\n& 50m Natatorium", "black", "#d9e2ec"),
        (10, -422, "50-Block Coastal & Parkland\nTransition Belt (Z=-447..-397)", "white", "#2e6f40"),
        (82, -512, "Original Muscle Beach\n(76, 65, -527)\nRings, Bars & Weights", "black", "#66d9e8"),
        (154, -582, "Santa Monica Pier & Pacific Park\n(36m Pacific Wheel & West Coaster)", "black", "#ffd966"),
        (103, -557, "Looff Hippodrome\nCarousel Dome", "black", "#f3d58d"),
        (208, -536, "Route 66 End of Trail &\nPier-End Seafood Bistro", "white", "#1d6fa5"),
        (43, -618, "Annenberg Beach House &\nDual 3D Water Slides", "black", "#d9e2ec"),
        (88, -660, "4 Santa Monica Beach\nVolleyball Courts", "black", "#f3d58d"),
        (41, -686, "Venice / Santa Monica\nSkatepark Bowls", "white", "#3b4252"),
        (-48, -586, "Santa Monica Palisades Bluffs\n& Camera Obscura Overlook", "white", "#2e6f40"),
        (-144, -540, "3rd Street Promenade\n(Georgian Deco, Casa del Mar,\nSM Place & Criterion Rotunda)", "black", "#f8f0e3"),
        (-168, -693, "Civic Auditorium (Folded Roof),\nTongva Park & Public Library", "white", "#1d6fa5"),
        (-253, -550, "Venice Beach Canals\n(5 Bridges, 6 Gondolas &\n6 Distinct Non-Boxy Villas)", "white", "#0ca678"),
        (-256, -730, "Museum of Flying Hangar (DC-3)\n& Bergamot Sawtooth Art Center", "white", "#5c5f66"),
        (312, -659, "East X+ Faux-Natural Bluffs,\nEmerald Waterfall Cove &\nSea-Stack Arch (343,74,-659)", "white", "#2b8a3e"),
        (-16, -536, "California Incline &\nPCH Highway 1", "white", "#4c566a"),
        (146, -824, "Point Dume / Malibu\nHeadland & Bluff Slope", "black", "#f3d58d"),
        (156, -212, "Relocated & Heightened\nLighthouse (Y=64..116)", "black", "#ffd966"),
        (199, -116, "Luxury Cruise Ship\n'Serenity of the Seas'", "black", "#ffffff"),
    ]
    for ax_x, ax_z, label, fg, bg in annotations:
        ax.text(ax_x, ax_z, label, fontsize=8.0, fontweight='bold', color=fg,
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=bg, alpha=0.88, edgecolor='black', lw=1.0))

    ax.grid(True, linestyle='--', alpha=0.35, color='white')
    plt.tight_layout()
    topdown_path = os.path.join(out_dir, "render_topdown.png")
    plt.savefig(topdown_path, dpi=160)
    plt.close(fig)
    print(f"  [OK] Saved {topdown_path}")

    print("[Renderer] Generating 4 Architectural Elevation & Section Views (render_3d_views.png)...")
    fig, axes = plt.subplots(2, 2, figsize=(18, 13), dpi=150)

    ax1 = axes[0, 0]
    ew_img = np.full((118 - 45, sx, 3), 235, dtype=np.uint8)
    for gx in range(sx):
        for gy in range(45 - y_min, 118 - y_min):
            col_slice = cat_grid[gx, (-220 - z_min):(60 - z_min), gy]
            nz = col_slice[col_slice > 0]
            if len(nz) > 0:
                c_val = int(np.max(nz))
                ew_img[117 - (gy + y_min), gx] = palette_rgb[c_val]
    ax1.imshow(ew_img, extent=[x_min, x_max, 45, 118], aspect='auto')
    ax1.axhline(62, color='#1c6ba0', linestyle='--', lw=1.2, label='Sea Level (Y=62)')
    ax1.set_title("1. West-to-East Estate Elevation (Y=45..118, Including Heightened Y=116 Lighthouse)", fontsize=11, fontweight='bold')
    ax1.set_xlabel("World X")
    ax1.set_ylabel("Elevation Y")
    ax1.legend(loc='upper left', fontsize=8)

    ax2 = axes[0, 1]
    nb_img = np.full((108 - 50, sx, 3), 230, dtype=np.uint8)
    for gx in range(sx):
        for gy in range(50 - y_min, 108 - y_min):
            col_slice = cat_grid[gx, (-605 - z_min):(-525 - z_min), gy]
            nz = col_slice[col_slice > 0]
            if len(nz) > 0:
                c_val = int(np.max(nz))
                nb_img[107 - (gy + y_min), gx] = palette_rgb[c_val]
    ax2.imshow(nb_img, extent=[x_min, x_max, 50, 108], aspect='auto')
    ax2.set_title("2. V5.5 Santa Monica Axis E-W Profile: Palisades Bluffs (Y=72) -> PCH -> Carousel -> Pacific Wheel (Y=104) -> Pier Bistro", fontsize=10.0, fontweight='bold')
    ax2.set_xlabel("World X (Palisades Bluffs & Camera Obscura -> PCH -> Looff Hippodrome -> 36m Pacific Wheel & West Coaster -> Pier End)")
    ax2.set_ylabel("Elevation Y")

    ax3 = axes[1, 0]
    zp_min, zp_max = -228, -15
    yp_min, yp_max = 48, 118
    park_img = np.full((yp_max - yp_min, zp_max - zp_min, 3), 230, dtype=np.uint8)
    for gz_w in range(zp_min, zp_max):
        gz = gz_w - z_min
        for gy_w in range(yp_min, yp_max):
            gy = gy_w - y_min
            row_x = cat_grid[(105 - x_min):(181 - x_min), gz, gy]
            nz = row_x[row_x > 0]
            if len(nz) > 0:
                non_w = nz[nz > 1]
                c_val = int(non_w[-1]) if len(non_w) > 0 else 1
                park_img[yp_max - 1 - gy_w, gz_w - zp_min] = palette_rgb[c_val]
    ax3.imshow(park_img, extent=[zp_min, zp_max, yp_min, yp_max], aspect='auto')
    ax3.set_title("3. Seaside Park Waterfront Profile (Z=-228..-15, Showing Relocated Lighthouse & Clean Z=-225 Junction)", fontsize=10.5, fontweight='bold')
    ax3.set_xlabel("World Z")
    ax3.set_ylabel("Elevation Y")

    ax4 = axes[1, 1]
    zn0, zn1 = -795, -400
    yn0, yn1 = 50, 108
    ns_img = np.full((yn1 - yn0, zn1 - zn0, 3), 230, dtype=np.uint8)
    for gz_w in range(zn0, zn1):
        gz = gz_w - z_min
        for gy_w in range(yn0, yn1):
            gy = gy_w - y_min
            slice_x = cat_grid[(30 - x_min):(190 - x_min), gz, gy]
            nz = slice_x[slice_x > 0]
            if len(nz) > 0:
                non_w = nz[nz > 1]
                c_val = int(non_w[-1]) if len(non_w) > 0 else 1
                ns_img[yn1 - 1 - gy_w, gz_w - zn0] = palette_rgb[c_val]
    ax4.imshow(ns_img, extent=[zn0, zn1, yn0, yn1], aspect='auto')
    ax4.set_title("4. N-S Section: Point Dume Bluff (Z=-795) -> Skate/Volleyball -> Annenberg -> Pacific Park Pier -> Muscle Beach", fontsize=10.0, fontweight='bold')
    ax4.set_xlabel("World Z")
    ax4.set_ylabel("Elevation Y")

    plt.tight_layout()
    views_path = os.path.join(out_dir, "render_3d_views.png")
    plt.savefig(views_path, dpi=150)
    plt.close(fig)
    print(f"  [OK] Saved {views_path}")

    print("[Renderer] Generating Architectural Detail Verification Sheet (render_v4_fixes_detail.png)...")
    fig2, axes2 = plt.subplots(2, 2, figsize=(18, 12), dpi=150)

    ax_a = axes2[0, 0]
    xb0, xb1, yb0, yb1 = 16, 40, 74, 96
    gs_slice = np.full((yb1 - yb0 + 1, xb1 - xb0 + 1, 3), 235, dtype=np.uint8)
    for xw in range(xb0, xb1 + 1):
        for yw in range(yb0, yb1 + 1):
            col_s = cat_grid[xw - x_min, (-42 - z_min):(-30 - z_min), yw - y_min]
            nz = col_s[col_s > 0]
            if len(nz) > 0:
                gs_slice[yb1 - yw, xw - xb0] = palette_rgb[int(np.max(nz))]
    ax_a.imshow(gs_slice, extent=[xb0, xb1, yb0, yb1], aspect='auto')
    ax_a.set_title("A. V5.5 Fix 1: Elevated Belvedere Tower 4F (Y=85..94) Separated Above 3F Roof (Y=84) at (27, 88, -32)", fontsize=10.5, fontweight='bold')
    ax_a.set_xlabel("World X (3F Roof at Y=84 X=4..25  <--->  Elevated 4F Lantern Room Y=85..94 X=26..37)")
    ax_a.set_ylabel("Elevation Y")
    ax_a.grid(True, linestyle=':', alpha=0.4, color='gray')

    ax_b = axes2[0, 1]
    xf0, xf1, yf0, yf1 = 118, 190, 62, 106
    fw_slice = np.full((yf1 - yf0 + 1, xf1 - xf0 + 1, 3), 235, dtype=np.uint8)
    for xw in range(xf0, xf1 + 1):
        for yw in range(yf0, yf1 + 1):
            col_s = cat_grid[xw - x_min, (-586 - z_min):(-578 - z_min), yw - y_min]
            nz = col_s[col_s > 0]
            if len(nz) > 0:
                fw_slice[yf1 - yw, xw - xf0] = palette_rgb[int(np.max(nz))]
    ax_b.imshow(fw_slice, extent=[xf0, xf1, yf0, yf1], aspect='auto')
    ax_b.set_title("B. V5.5 Santa Monica Pier: 36m Pacific Wheel (154, 86, -582) & West Coaster Roller Coaster", fontsize=10.5, fontweight='bold')
    ax_b.set_xlabel("World X")
    ax_b.set_ylabel("Elevation Y")
    ax_b.grid(True, linestyle=':', alpha=0.4, color='gray')

    ax_c = axes2[1, 0]
    xp0, xp1, yp0, yp1 = -310, 350, 52, 92
    pb_slice = np.full((yp1 - yp0 + 1, xp1 - xp0 + 1, 3), 235, dtype=np.uint8)
    for xw in range(xp0, xp1 + 1):
        for yw in range(yp0, yp1 + 1):
            col_s = cat_grid[xw - x_min, (-666 - z_min):(-480 - z_min), yw - y_min]
            nz = col_s[col_s > 0]
            if len(nz) > 0:
                pb_slice[yp1 - yw, xw - xp0] = palette_rgb[int(np.max(nz))]
    ax_c.imshow(pb_slice, extent=[xp0, xp1, yp0, yb1 if False else yp1], aspect='auto')
    ax_c.set_title("C. V5.5 Full E-W Section: Venice Canals -> 3rd St Promenade -> Palisades Bluffs -> Beach/Pier -> X+ Waterfall Cove", fontsize=10.0, fontweight='bold')
    ax_c.set_xlabel("World X (Venice Canals & Villas -> 3rd St Promenade -> Palisades Bluffs -> Santa Monica Beach -> X+ Cove 343,74,-659)")
    ax_c.set_ylabel("Elevation Y")
    ax_c.grid(True, linestyle=':', alpha=0.4, color='gray')

    ax_d = axes2[1, 1]
    bp_rgb = img_rgb[(-856 - z_min):(-448 - z_min + 1), (-310 - x_min):(348 - x_min + 1), :].astype(np.uint8)
    ax_d.imshow(bp_rgb, extent=[-310, 348, -448, -856], aspect='auto')
    ax_d.set_title("D. V5.5 Master Plan: X- Venice Canals & 3rd St Promenade + 416m Santa Monica Beach + X+ Waterfall Cove", fontsize=10.0, fontweight='bold')
    ax_d.set_xlabel("World X (Venice Canals -> 3rd St Promenade -> Palisades Bluffs -> Santa Monica Beach & Pier -> X+ Waterfall Cove)")
    ax_d.set_ylabel("World Z")
    ax_d.grid(True, linestyle=':', alpha=0.4, color='white')

    plt.tight_layout()
    fixes_path = os.path.join(out_dir, "render_v4_fixes_detail.png")
    plt.savefig(fixes_path, dpi=150)
    plt.close(fig2)
    print(f"  [OK] Saved {fixes_path}")

    print("=" * 72)
    print("[Validator] ALL CHECKS PASSED SUCCESSFULLY!")
    print("=" * 72)

if __name__ == "__main__":
    wdir = sys.argv[1] if len(sys.argv) > 1 else "/tmp/mc_build/TEST_BUILDINGS"
    odir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/mc_build"
    run_validation_and_render(wdir, odir)
