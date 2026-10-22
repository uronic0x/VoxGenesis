"""
zone_core_villa.py — Core Estate Terrain Grading (with P0 Sky Cleanup), Paving,
Landscaping (with West Woodland Brook Buffer), Outbuildings, Main 3-Story Villa & Backyard Pool
===============================================================================================
"""

import math, random
from config import Y_BASE, SEA_LEVEL, HARBOR_FLOOR, MAT, SOFT_FLOWERS
from world_canvas import WorldCanvas
from arch_lib import (
    stair, trapdoor,
    place_bed, place_barrel, place_brewing_stand, place_smoker, place_blast_furnace,
    place_lectern, place_tall_flower, place_door, place_double_door,
    build_recessed_ceiling_grid, build_crystal_chandelier, build_illuminated_carpet_rug,
    build_floor_lamp, build_indoor_planter, build_billiards_table, build_home_theater_wall,
    build_ensuite_bathroom,
    build_wall, build_slatted_feature_wall, build_curtain_wall,
    build_flat_roof_and_eaves, build_support_beams_under_cantilever,
    build_pitched_modern_roof, build_spiral_staircase, build_straight_stairs,
    build_tower, build_pergola_colonnade, build_vine_arch, build_lamppost,
    build_infinity_pool, build_fountain, build_topiary_sculpture,
    build_zen_sand_garden, build_hedgerow_line, build_spherical_shrub,
    build_custom_tree, build_patio_umbrella, build_sun_lounger,
    build_outdoor_sofa, build_outdoor_bar, build_seed_variant_outbuilding,
    build_arched_canal_bridge
)

def _rounded_box_dist(x, z, x1, x2, z1, z2, corner_r=24.0):
    ix1, ix2 = x1 + corner_r, x2 - corner_r
    iz1, iz2 = z1 + corner_r, z2 - corner_r
    dx = max(0.0, ix1 - x, x - ix2)
    dz = max(0.0, iz1 - z, z - iz2)
    return max(0.0, math.hypot(dx, dz) - corner_r)

def step1_flatten_and_grade_terrain(c: WorldCanvas):
    stone_id = c.get_or_register(MAT['stone'])
    dirt_id = c.get_or_register(MAT['dirt'])
    grass_id = c.get_or_register(MAT['grass_block'])
    sand_id = c.get_or_register('minecraft:sand')
    sandstone_id = c.get_or_register('minecraft:smooth_sandstone')
    water_id = c.get_or_register(MAT['water'])
    sea_lantern_id = c.get_or_register(MAT['light_sea'])
    air_id = c.air_id

    smoothed_orig_y = {}
    for z in range(c.z_min, c.z_max + 1):
        for x in range(c.x_min, c.x_max + 1):
            acc = 0
            cnt = 0
            for dz in (-2, 0, 2):
                for dx in (-2, 0, 2):
                    ny = c.orig_surface_y.get((x + dx, z + dz), Y_BASE)
                    acc += min(76, ny)
                    cnt += 1
            smoothed_orig_y[(x, z)] = int(round(acc / cnt))

    for z in range(c.z_min, c.z_max + 1):
        for x in range(c.x_min, c.x_max + 1):
            if 113 <= x <= 223 and 22 <= z <= 106:
                orig_top = c.orig_top_block.get((x, z), 'minecraft:water')
                if x <= 216 and 24 <= z <= 102 or orig_top == 'minecraft:water':
                    for y in range(63, c.y_max + 1):
                        c.set_block_id(x, y, z, air_id)
                    for y in range(46, 59):
                        c.set_block_id(x, y, z, stone_id)
                    c.set_block_id(x, 59, z, sand_id)
                    c.set_block_id(x, 60, z, sand_id)
                    c.set_block_id(x, 61, z, water_id)
                    c.set_block_id(x, 62, z, water_id)
                    continue

            in_lighthouse_headland = (132 <= x <= 172 and -228 <= z <= -196 and ((x - 153)**2 / 19.0**2 + (z + 212)**2 / 16.0**2 <= 1.0))
            if x >= 138 and -232 <= z <= 21 and not in_lighthouse_headland:
                for y in range(63, c.y_max + 1):
                    c.set_block_id(x, y, z, air_id)

                if -96 <= z <= -38 and x <= 153:
                    if x <= 141:
                        beach_y = 64
                    elif x <= 147:
                        beach_y = 63
                    elif x <= 150:
                        beach_y = 62
                    else:
                        beach_y = 62 - (x - 150) * 2
                    for y in range(45, beach_y - 3):
                        c.set_block_id(x, y, z, stone_id)
                    for y in range(beach_y - 3, beach_y):
                        c.set_block_id(x, y, z, sandstone_id)
                    c.set_block_id(x, beach_y, z, sand_id)
                    for y in range(beach_y + 1, 63):
                        c.set_block_id(x, y, z, water_id)
                    continue

                if x < 148:
                    seabed_y = max(50, 56 - (x - 138) // 2)
                else:
                    seabed_y = HARBOR_FLOOR
                for y in range(42, seabed_y - 2):
                    c.set_block_id(x, y, z, stone_id)
                c.set_block_id(x, seabed_y - 2, z, sandstone_id)
                c.set_block_id(x, seabed_y - 1, z, sand_id)
                if x >= 152 and -190 <= z <= -40 and (x % 8 == 0 and z % 8 == 0):
                    c.set_block_id(x, seabed_y, z, sea_lantern_id)
                else:
                    c.set_block_id(x, seabed_y, z, sand_id)
                for y in range(seabed_y + 1, 63):
                    c.set_block_id(x, y, z, water_id)
                continue

            d_core = _rounded_box_dist(x, z, -114, 108, -114, 116, corner_r=18.0)
            d_park = _rounded_box_dist(x, z, 96, 138, -234, 22, corner_r=10.0)
            d_lhouse = 0.0 if in_lighthouse_headland else _rounded_box_dist(x, z, 126, 170, -234, -196, corner_r=6.0)
            d_golf = _rounded_box_dist(x, z, -162, 128, -268, -96, corner_r=28.0)
            d_sports = _rounded_box_dist(x, z, -224, 132, -396, -268, corner_r=20.0)
            d_north_exp = _rounded_box_dist(x, z, -312, 340, -856, -396, corner_r=16.0)
            d_farm = _rounded_box_dist(x, z, -234, -94, -150, 102, corner_r=18.0)
            d_heli = _rounded_box_dist(x, z, 80, 112, 26, 96, corner_r=10.0)
            d = min(d_core, d_park, d_lhouse, d_golf, d_sports, d_north_exp, d_farm, d_heli)

            orig_y = smoothed_orig_y.get((x, z), Y_BASE)
            orig_top = c.orig_top_block.get((x, z), 'minecraft:grass_block')

            if d <= 0.0:
                target_y = Y_BASE
                is_core = True
            elif d >= 28.0:
                target_y = orig_y
                is_core = False
            else:
                t = d / 28.0
                s = t * t * (3.0 - 2.0 * t)
                target_y = int(round(Y_BASE * (1.0 - s) + orig_y * s))
                is_core = False

            for y in range(target_y + 1, c.y_max + 1):
                c.set_block_id(x, y, z, air_id)

            fill_start = max(c.y_min, min(46, orig_y - 4))
            for y in range(fill_start, target_y - 3):
                c.set_block_id(x, y, z, stone_id)
            for y in range(max(c.y_min, target_y - 3), target_y):
                c.set_block_id(x, y, z, dirt_id)

            if not is_core and orig_top == 'minecraft:water' and d > 10.0:
                c.set_block_id(x, 60, z, sand_id)
                c.set_block_id(x, 61, z, water_id)
                c.set_block_id(x, 62, z, water_id)
                for wy in range(63, target_y + 1):
                    c.set_block_id(x, wy, z, air_id)
            else:
                c.set_block_id(x, target_y, z, grass_id)

def step2_paving_and_grounds(c: WorldCanvas):
    for x in range(-90, 105):
        for z in range(102, 106):
            c.set_block(x, Y_BASE, z, MAT['stone_pol_and'] if z in (102, 105) else (MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_and']))
    for z in range(-106, 107):
        for x in range(98, 104):
            if x in (98, 103):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
        for x in range(-90, -86):
            c.set_block(x, Y_BASE, z, MAT['stone_pol_and'] if x in (-90, -87) else (MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_smooth']))

    for z in range(-10, 53):
        for x in range(-44, 45):
            if x % 4 == 0 or z % 4 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            elif (x // 4 + z // 4) % 2 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_dio'] if (x + z) % 2 == 0 else MAT['stone_smooth'])

    for z in range(20, 49):
        for x in range(-42, -6):
            diag_dist = abs((x + 36) * 26 - (z - 20) * 30) / math.hypot(26, 30)
            if diag_dist <= 2.3:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            elif abs(diag_dist - 2.8) < 0.6:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                if (x + z) % 6 == 0:
                    c.set_block(x, Y_BASE - 1, z, MAT['light_sea'])
                    c.set_block(x, Y_BASE, z, MAT['glass_gray'])
            else:
                c.set_block(x, Y_BASE, z, MAT['grass_block'])
                if (x * 3 + z * 5) % 4 == 0:
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:short_grass')

    for z in range(28, 49):
        for x in range(10, 43):
            diag_dist = abs((x - 10) * 20 - (48 - z) * 32) / math.hypot(20, 32)
            if diag_dist <= 2.2:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            elif abs(diag_dist - 2.7) < 0.6:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                if (x + z) % 6 == 0:
                    c.set_block(x, Y_BASE - 1, z, MAT['light_sea'])
                    c.set_block(x, Y_BASE, z, MAT['glass_gray'])
            else:
                c.set_block(x, Y_BASE, z, MAT['grass_block'])
                if (x * 7 + z * 3) % 5 == 0:
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:short_grass')

    for z in range(-10, 53):
        for x in range(-3, 4):
            if abs(x) == 3:
                if z % 6 == 0:
                    c.set_block(x, Y_BASE - 1, z, MAT['light_ochre'])
                    c.set_block(x, Y_BASE, z, MAT['glass_gray'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
    for x in range(-46, 47):
        for z in range(13, 18):
            if z in (13, 17):
                if x % 6 == 0:
                    c.set_block(x, Y_BASE - 1, z, MAT['light_ochre'])
                    c.set_block(x, Y_BASE, z, MAT['glass_gray'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    for z in range(4, 12):
        half_w = (12 - z) // 2
        for x in range(2 - half_w, 3 + half_w):
            if x in (2 - half_w, 2 + half_w) or z in (4, 11):
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 1, z, MAT['slab_stone_b'])
            else:
                c.set_block(x, Y_BASE, z, MAT['moss_block'])
                c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x + z) % len(SOFT_FLOWERS)])
    build_lamppost(c, 2, Y_BASE + 1, 6, style='courtyard')

    for dx in range(-4, 5):
        for dz in range(-4, 5):
            if dx * dx + dz * dz <= 14:
                c.set_block(-9 + dx, Y_BASE, 39 + dz, 'minecraft:tuff' if (dx + dz) % 2 == 0 else MAT['stone_and'])
                if dx * dx + dz * dz <= 8:
                    c.set_block(-9 + dx, Y_BASE + 1, 39 + dz, MAT['slab_and_b'] if dx * dx + dz * dz > 3 else 'minecraft:tuff')

    for z in range(52, 65):
        for x in range(-18, 19):
            if x % 4 == 0 or z % 4 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'])

    for z in range(64, 121):
        in_ew_crossroad = (72 <= z <= 78)
        for x in range(-3, 4):
            if not in_ew_crossroad and x == 0 and z % 4 in (0, 1):
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
            elif not in_ew_crossroad and abs(x) == 3:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            elif z in (72, 78) and x in (-2, 0, 2):
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_gray'])
        if not in_ew_crossroad:
            for sx in (-4, 4):
                c.set_block(sx, Y_BASE, z, MAT['wall_quartz'])
                c.set_block(sx, Y_BASE + 1, z, MAT['slab_stone_b'])
            for sx in (-7, -6, -5, 5, 6, 7):
                c.set_block(sx, Y_BASE, z, MAT['stone_smooth'] if (sx + z) % 2 == 0 else MAT['stone_pol_and'])
            for sx in (-8, 8):
                if z in (71, 79):
                    c.set_block(sx, Y_BASE, z, MAT['wall_quartz'])
                    c.set_block(sx, Y_BASE + 1, z, MAT['slab_stone_b'])
                else:
                    c.set_block(sx, Y_BASE, z, MAT['moss_block'])
                    c.set_block(sx, Y_BASE + 1, z, SOFT_FLOWERS[(z + abs(sx)) % len(SOFT_FLOWERS)])
            for sx in (-9, 9):
                c.set_block(sx, Y_BASE, z, MAT['wall_quartz'])
                c.set_block(sx, Y_BASE + 1, z, MAT['slab_stone_b'])
            if z % 10 == 0 and not (70 <= z <= 80):
                build_lamppost(c, -4, Y_BASE + 1, z, style='avenue')
                build_lamppost(c, 4, Y_BASE + 1, z, style='avenue')
        if z in (68, 82):
            build_lamppost(c, -4, Y_BASE + 1, z, style='avenue')
            build_lamppost(c, 4, Y_BASE + 1, z, style='avenue')

    for x in range(4, 105):
        for z in range(72, 79):
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 4, z, 'minecraft:air')
            if x == 4 and z in (73, 75, 77):
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
            elif z == 75 and x >= 6 and x % 4 in (0, 1):
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
            elif z in (72, 78):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_gray'])

    for z in range(58, 83):
        for x in range(38, 79):
            if (x - 38) % 4 == 0 or (z - 58) % 4 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'])

    for z in range(-76, 86):
        for x in (-67, -66, -65):
            c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
    for x in range(-90, -48):
        for z in (-56, -55, -54, 65, 66, 67):
            c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
    for x in range(84, 100):
        for z in (9, 10, 11):
            c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])

    for z in range(-98, -40):
        for x in range(-48, 49):
            if -24 <= x <= 24 and -52 <= z <= -40:
                c.set_block(x, Y_BASE, z, MAT['wood_warm'] if z % 2 == 0 else MAT['wood_dark'])
            else:
                if x % 4 == 0 or z % 4 == 0:
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x // 4 + z // 4) % 2 == 0 else MAT['stone_smooth'])

def step3_landscaping_and_gardens(c: WorldCanvas):
    rng = random.Random(20261017)
    tree_styles = ['oak_mix', 'oak_mix', 'birch_mix', 'spruce_mix', 'ornamental']

    for z in range(-292, 148, 10):
        for x in range(-234, 212, 10):
            jx = x + rng.randint(-2, 2)
            jz = z + rng.randint(-2, 2)
            in_south_belt = (108 <= jz <= 136 and -228 <= jx <= 104 and not (-14 <= jx <= 14))
            in_west_outer = (-236 <= jx <= -228 and -148 <= jz <= 106)
            in_nw_hills = (-234 <= jx <= -166 and -290 <= jz <= -154)
            in_north_belt = (-162 <= jx <= 132 and -292 <= jz <= -264)
            in_seaside_screen = (46 <= jx <= 95 and -15 <= jz <= -7)
            if in_south_belt or in_west_outer or in_nw_hills or in_north_belt or in_seaside_screen:
                gy = None
                for wy in range(92, 58, -1):
                    bn = c.get_block_name(jx, wy, jz)
                    if bn in ('minecraft:grass_block', 'minecraft:dirt', 'minecraft:moss_block'):
                        gy = wy
                        break
                    elif bn != 'minecraft:air':
                        break
                if gy is not None:
                    h = rng.randint(9, 12)
                    st = 'ornamental' if in_seaside_screen and jx % 2 == 0 else rng.choice(tree_styles)
                    t_seed = rng.randint(1, 99999)
                    if not ((in_north_belt and (jz <= -274 or -46 <= jx <= -24 or 14 <= jx <= 36)) or (in_nw_hills and jz <= -274 and jx >= -222)):
                        build_custom_tree(c, jx, gy, jz, height=h, style=st, seed=t_seed)

    for z in range(-104, 102):
        brook_cx = -112 + int(round(4.5 * math.sin(z / 16.0)))
        for x in range(-133, -90):
            dist_b = abs(x - brook_cx)
            if dist_b <= 2:
                c.set_block(x, Y_BASE - 2, z, MAT['light_sea'] if (x + z) % 4 == 0 else MAT['stone_pol_and'])
                c.set_block(x, Y_BASE - 1, z, MAT['water'])
                c.set_block(x, Y_BASE, z, MAT['water'])
                if dist_b == 0 and z % 9 == 0 and abs(z - 15) > 5 and abs(z + 55) > 5 and abs(z - 66) > 5:
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:lily_pad')
            elif dist_b == 3:
                c.set_block(x, Y_BASE, z, MAT['moss_block'] if (x + z) % 2 == 0 else 'minecraft:tuff')
                if (x + z) % 5 == 0 and abs(z - 15) > 5 and abs(z + 55) > 5 and abs(z - 66) > 5:
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:sugar_cane' if z % 2 == 0 else 'minecraft:fern')
            else:
                if (x * 3 + z * 7) % 11 == 0:
                    c.set_block(x, Y_BASE, z, MAT['moss_block'])
                if (x * 5 + z * 3) % 13 == 0 and abs(z - 15) > 5 and abs(z + 55) > 5 and abs(z - 66) > 5:
                    c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x + z) % len(SOFT_FLOWERS)])

    for bz in (-55, 15, 66):
        brook_cx = -112 + int(round(4.5 * math.sin(bz / 16.0)))
        for x in range(-135, -88):
            for z in range(bz - 2, bz + 3):
                if abs(z - bz) == 2:
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['wall_quartz'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
        build_arched_canal_bridge(c, brook_cx, Y_BASE, bz, width=5, span=10, axis='x')
        build_vine_arch(c, -90, Y_BASE, bz, span=6, height=5, axis='z')
        build_vine_arch(c, -134, Y_BASE, bz, span=6, height=5, axis='z')

    for z in range(-96, 96, 12):
        if abs(z - 15) <= 7 or abs(z + 55) <= 7 or abs(z - 66) <= 7:
            continue
        brook_cx = -112 + int(round(4.5 * math.sin(z / 16.0)))
        for tx in (brook_cx - 9, brook_cx + 9, -94):
            if -131 <= tx <= -92:
                build_custom_tree(c, tx, Y_BASE, z, height=rng.randint(8, 11),
                                  style=rng.choice(['birch_mix', 'ornamental', 'oak_mix']), seed=abs(tx * 37 + z))

    build_hedgerow_line(c, -44, Y_BASE, 50, -5, 50, height=2, gap_every=6)
    build_hedgerow_line(c, 5, Y_BASE, 50, 44, 50, height=2, gap_every=6)
    build_hedgerow_line(c, -44, Y_BASE, -8, -44, 12, height=2, gap_every=6)
    build_hedgerow_line(c, -44, Y_BASE, 18, -44, 50, height=2, gap_every=6)
    build_hedgerow_line(c, 44, Y_BASE, -8, 44, 12, height=2, gap_every=6)
    build_hedgerow_line(c, 44, Y_BASE, 18, 44, 50, height=2, gap_every=6)

    for idx, x in enumerate(range(-40, 41, 8)):
        if abs(x) >= 8:
            build_spherical_shrub(c, x, Y_BASE, 47, radius=1, tone='light' if idx % 2 == 0 else 'dark')
    for idx, z in enumerate(range(-4, 46, 8)):
        if abs(z - 15) >= 5:
            build_spherical_shrub(c, -41, Y_BASE, z, radius=1, tone='light' if idx % 2 == 0 else 'dark')
            build_spherical_shrub(c, 41, Y_BASE, z, radius=1, tone='dark' if idx % 2 == 0 else 'light')

    build_vine_arch(c, 0, Y_BASE, 36, span=6, height=5, axis='x')
    build_vine_arch(c, 0, Y_BASE, 6, span=6, height=5, axis='x')
    build_vine_arch(c, -44, Y_BASE, 15, span=6, height=5, axis='z')
    build_vine_arch(c, 44, Y_BASE, 15, span=6, height=5, axis='z')

    build_fountain(c, 0, Y_BASE, 22, radius=5)
    build_topiary_sculpture(c, -24, Y_BASE, 15)
    build_lamppost(c, -16, Y_BASE + 1, 22, style='courtyard')
    build_lamppost(c, -17, Y_BASE + 1, 4, style='courtyard')
    build_lamppost(c, 14, Y_BASE + 1, 22, style='courtyard')
    build_zen_sand_garden(c, 16, Y_BASE, 5, 37, 24)

    build_custom_tree(c, -22, Y_BASE, 34, height=8, style='ornamental', seed=11, max_radius=2)
    build_custom_tree(c, 26, Y_BASE, 34, height=8, style='ornamental', seed=22, max_radius=2)
    build_custom_tree(c, -41, Y_BASE, -2, height=8, style='birch_mix', seed=33, max_radius=2)
    build_custom_tree(c, 43, Y_BASE, -13, height=8, style='ornamental', seed=44, max_radius=2)

    build_pergola_colonnade(c, -35, Y_BASE, 6, -31, 36, axis='z', lamp_step=8)
    build_pergola_colonnade(c, -51, Y_BASE, -10, -47, 42, axis='z', lamp_step=8)
    build_pergola_colonnade(c, -86, Y_BASE, 13, -52, 17, axis='x', lamp_step=8)

    for x in range(-78, -57):
        for z in range(-14, 11):
            if x in (-78, -58) or z in (-14, 10):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                c.set_block(x, Y_BASE + 1, z, MAT['slab_stone_b'])
            else:
                c.set_block(x, Y_BASE - 2, z, MAT['pool_deep_1'] if (x + z) % 2 == 0 else MAT['light_sea'])
                c.set_block(x, Y_BASE - 1, z, MAT['water'])
                c.set_block(x, Y_BASE, z, MAT['water'])
                if (x * 5 + z * 7) % 19 == 0:
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:lily_pad')

    for z in range(-14, 11):
        for x_clear in range(-71, -61):
            if c.get_block_name(x_clear, Y_BASE + 1, z) == 'minecraft:lily_pad':
                c.set_block(x_clear, Y_BASE + 1, z, 'minecraft:air')

        if z in (-14, 10):
            for x_th in (-68, -67, -66, -65, -64):
                c.set_block(x_th, Y_BASE, z, MAT['wall_quartz'] if x_th in (-68, -64) else MAT['wood_dark'])
                c.set_block(x_th, Y_BASE + 1, z, MAT['slab_dark_b'] if x_th in (-68, -64) else 'minecraft:air')
            continue

        if z in (-11, -7, -4, 0, 3, 7):
            for px_pile in (-68, -64):
                c.fill(px_pile, Y_BASE - 2, z, px_pile, Y_BASE - 1, z, MAT['beam_dark_y'])

        for x_dk in (-67, -66, -65):
            if x_dk == -66 and z % 4 == 0:
                c.set_block(x_dk, Y_BASE, z, MAT['light_ochre'])
            else:
                c.set_block(x_dk, Y_BASE, z, MAT['wood_warm'] if x_dk == -66 else MAT['wood_dark'])
            c.set_block(x_dk, Y_BASE + 1, z, 'minecraft:air')

        if not (-4 <= z <= 0):
            for x_edge in (-68, -64):
                c.set_block(x_edge, Y_BASE, z, MAT['wood_dark'])
                c.set_block(x_edge, Y_BASE + 1, z, MAT['slab_dark_b'])
                if z in (-11, -7, 3, 7):
                    c.set_block(x_edge, Y_BASE + 1, z, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
                    c.set_block(x_edge, Y_BASE + 2, z, MAT['lantern_stand'])

    for z in range(-4, 1):
        for x in range(-70, -61):
            is_outer_ring = (x in (-70, -62) or z in (-4, 0))
            if is_outer_ring:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['wood_dark'])
                if not (-67 <= x <= -65 and z in (-4, 0)):
                    c.set_block(x, Y_BASE + 1, z, MAT['slab_dark_b'])
            else:
                if (x in (-68, -64) and z == -2):
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (x + z) % 2 == 0 else MAT['wood_dark'])
                c.set_block(x, Y_BASE + 1, z, 'minecraft:air')

    for z_bench in (-3, -2, -1):
        c.set_block(-69, Y_BASE + 1, z_bench, stair('spruce', 'east', 'bottom'))
        c.set_block(-63, Y_BASE + 1, z_bench, stair('spruce', 'west', 'bottom'))

    for px_c in (-70, -62):
        for pz_c in (-4, 0):
            c.fill(px_c, Y_BASE - 2, pz_c, px_c, Y_BASE + 3, pz_c, MAT['beam_dark_y'])
            c.set_block(px_c, Y_BASE + 1, pz_c, MAT['wall_quartz'])
            c.fill(px_c, Y_BASE + 2, pz_c, px_c, Y_BASE + 3, pz_c, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
    for x in range(-70, -61):
        for z in range(-4, 1):
            if x in (-70, -62) or z in (-4, 0):
                c.set_block(x, Y_BASE + 4, z, MAT['slab_dark_b'])
            else:
                c.set_block(x, Y_BASE + 4, z, MAT['slab_spruce_b'] if (x + z) % 2 == 0 else trapdoor('dark_oak', 'north', 'top', 'false'))
    c.set_block(-66, Y_BASE + 4, -2, MAT['light_ochre'])
    c.set_block(-66, Y_BASE + 5, -2, MAT['slab_quartz_b'])

    c.fill(-72, Y_BASE, 20, -56, Y_BASE, 36, MAT['wood_warm'])
    build_patio_umbrella(c, -67, Y_BASE, 25)
    build_patio_umbrella(c, -60, Y_BASE, 31)
    build_outdoor_sofa(c, -69, Y_BASE, 29, length=5, facing='north')
    build_outdoor_sofa(c, -63, Y_BASE, 23, length=5, facing='south')

    c.fill(48, Y_BASE, -20, 84, Y_BASE, 40, MAT['stone_smooth'])
    quads = [(51, -17, 64, 8), (68, -17, 81, 8), (51, 12, 64, 37), (68, 12, 81, 37)]
    for q_idx, (qx1, qz1, qx2, qz2) in enumerate(quads):
        for x in range(qx1, qx2 + 1):
            for z in range(qz1, qz2 + 1):
                dx = min(x - qx1, qx2 - x)
                dz = min(z - qz1, qz2 - z)
                ring = min(dx, dz)
                if ring == 0:
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if (x + z) % 4 == 0 else MAT['moss_block'])
                    c.set_block(x, Y_BASE + 1, z, MAT['leaf_azalea'])
                    c.set_block(x, Y_BASE + 2, z, MAT['leaf_oak'])
                elif ring in (1, 2):
                    c.set_block(x, Y_BASE, z, MAT['stone_dio'])
                elif ring == 3:
                    c.set_block(x, Y_BASE, z, MAT['moss_block'])
                    c.set_block(x, Y_BASE + 1, z, MAT['leaf_oak'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['moss_block'])
                    c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x + z + q_idx) % len(SOFT_FLOWERS)])
        mx, mz = (qx1 + qx2) // 2, (qz1 + qz2) // 2
        for x in (qx1, qx2):
            c.fill(x, Y_BASE + 1, mz - 1, x, Y_BASE + 2, mz + 1, 'minecraft:air')
        for z in (qz1, qz2):
            c.fill(mx - 1, Y_BASE + 1, z, mx + 1, Y_BASE + 2, z, 'minecraft:air')
        build_spherical_shrub(c, mx, Y_BASE, mz, radius=2, tone='light' if q_idx % 2 == 0 else 'dark')

    for z in range(-17, 38):
        if 9 <= z <= 11:
            continue
        c.set_block(65, Y_BASE, z, MAT['wall_quartz'])
        c.set_block(67, Y_BASE, z, MAT['wall_quartz'])
        c.set_block(66, Y_BASE - 1, z, MAT['light_sea'] if z % 3 == 0 else MAT['pool_deep_1'])
        c.set_block(66, Y_BASE, z, MAT['water'])

    build_hedgerow_line(c, 48, Y_BASE, -20, 96, -20, height=3, gap_every=0)

def step4_gates_garage_and_outbuildings(c: WorldCanvas):
    """
    4. Build Zone A Entrance Gate & Landscape Walls, Zone G Garage/Tool House/Recycling,
       and Seed-Driven Outbuildings with upgraded interior lighting and furnishings.
    """
    c.fill(-4, Y_BASE + 1, 51, -3, Y_BASE + 5, 53, MAT['wall_white'])
    c.fill(3, Y_BASE + 1, 51, 4, Y_BASE + 5, 53, MAT['wall_white'])
    c.fill(-5, Y_BASE + 5, 50, 5, Y_BASE + 5, 54, MAT['wood_dark'])
    c.fill(-5, Y_BASE + 6, 50, 5, Y_BASE + 6, 54, MAT['wall_white'])
    for x in range(-5, 6):
        c.set_block(x, Y_BASE + 7, 50, MAT['slab_quartz_b'])
        c.set_block(x, Y_BASE + 7, 54, MAT['slab_quartz_b'])
        if x % 2 == 0:
            c.set_block(x, Y_BASE + 5, 52, MAT['light_ochre'])
    c.fill(-2, Y_BASE + 1, 52, -2, Y_BASE + 4, 52, MAT['glass_black'])
    c.fill(2, Y_BASE + 1, 52, 2, Y_BASE + 4, 52, MAT['glass_black'])
    c.fill(-1, Y_BASE + 4, 52, 1, Y_BASE + 4, 52, MAT['pane_black'])
    build_lamppost(c, -6, Y_BASE + 1, 55, style='courtyard')
    build_lamppost(c, 6, Y_BASE + 1, 55, style='courtyard')

    c.fill(-17, Y_BASE + 1, 52, -6, Y_BASE + 4, 52, MAT['wall_white'])
    c.fill(-16, Y_BASE + 2, 52, -7, Y_BASE + 3, 52, MAT['wall_lgray'])
    c.fill(-17, Y_BASE + 5, 52, -6, Y_BASE + 5, 52, MAT['slab_quartz_b'])
    for x in range(-16, -6, 3):
        c.set_block(x, Y_BASE + 1, 53, MAT['light_ochre'])
        build_spherical_shrub(c, x, Y_BASE, 55, radius=1, tone='light' if x % 2 == 0 else 'dark')

    c.fill(6, Y_BASE + 1, 52, 17, Y_BASE + 4, 52, MAT['wall_white'])
    c.fill(7, Y_BASE + 2, 52, 16, Y_BASE + 3, 52, MAT['wall_lgray'])
    c.fill(6, Y_BASE + 5, 52, 17, Y_BASE + 5, 52, MAT['slab_quartz_b'])
    for x in range(7, 17, 3):
        c.set_block(x, Y_BASE + 1, 53, MAT['light_ochre'])
        build_spherical_shrub(c, x, Y_BASE, 55, radius=1, tone='dark' if x % 2 == 0 else 'light')

    build_seed_variant_outbuilding(c, 19, Y_BASE, 50, w=7, d=6, h=5, seed=202, role='casita')

    gx1, gx2, gz1, gz2, gy_top = 42, 53, 60, 69, Y_BASE + 6
    c.fill(gx1, Y_BASE, gz1, gx2, Y_BASE, gz2, MAT['stone_pol_and'])
    c.fill(gx1, Y_BASE + 1, gz1, gx2, gy_top - 1, gz2, MAT['wall_white'])
    c.fill(gx1 + 1, Y_BASE + 1, gz1 + 1, gx2 - 1, gy_top - 1, gz2 - 1, 'minecraft:air')
    for x in range(gx1 + 1, gx2):
        for z in range(gz1 + 1, gz2):
            if (x - gx1) % 3 == 0 and (z - gz1) % 3 == 0:
                c.set_block(x, Y_BASE, z, MAT['light_sea'])
                c.set_block(x, Y_BASE + 1, z, MAT['carpet_lgray'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'] if (x + z) % 2 == 0 else MAT['wall_lgray'])
            if z in (gz1 + 2, gz1 + 5, gz2 - 2) and x % 2 == 0:
                c.set_block(x, gy_top - 1, z, MAT['light_sea'])
    for bay_x1, bay_x2 in [(43, 45), (47, 48), (50, 52)]:
        for x in range(bay_x1, bay_x2 + 1):
            for y in range(Y_BASE + 1, Y_BASE + 4):
                c.set_block(x, y, gz2, MAT['wall_lgray'] if y % 2 == 0 else 'minecraft:chiseled_stone_bricks')
            c.set_block(x, Y_BASE + 4, gz2, MAT['glass_black'])
    c.fill(gx1 + 2, Y_BASE + 3, gz1, gx2 - 2, Y_BASE + 4, gz1, MAT['glass_black'])
    place_barrel(c, gx1 + 1, Y_BASE + 1, gz1 + 1, 'south')
    c.set_block(gx1 + 2, Y_BASE + 1, gz1 + 1, 'minecraft:crafting_table')
    c.set_block(gx1 + 3, Y_BASE + 1, gz1 + 1, 'minecraft:smithing_table')
    build_flat_roof_and_eaves(c, gx1, gy_top, gz1, gx2, gz2, overhang=1,
                              roof_mat=MAT['wall_white'], soffit_mat=MAT['wood_dark'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)

    build_seed_variant_outbuilding(c, 57, Y_BASE, 62, w=6, d=6, h=5, seed=101, role='tool_house')

    rx1, rx2, rz1, rz2 = 65, 72, 62, 67
    c.fill(rx1, Y_BASE, rz1, rx2, Y_BASE, rz2, MAT['stone_pol_and'])
    for x in range(rx1, rx2 + 1):
        for z in range(rz1, rz2 + 1):
            if x in (rx1, rx2) or z in (rz1, rz2):
                if z == rz2 and rx1 + 3 <= x <= rx1 + 4:
                    continue
                c.set_block(x, Y_BASE + 1, z, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
                c.set_block(x, Y_BASE + 2, z, MAT['slab_dark_b'])
    place_barrel(c, rx1 + 1, Y_BASE + 1, rz1 + 1, 'up')
    place_barrel(c, rx1 + 2, Y_BASE + 1, rz1 + 1, 'up')
    c.set_block(rx1 + 4, Y_BASE + 1, rz1 + 1, 'minecraft:cauldron')
    c.set_block(rx1 + 5, Y_BASE + 1, rz1 + 1, 'minecraft:water_cauldron[level=3]')
    c.set_block(rx1 + 6, Y_BASE + 1, rz1 + 1, 'minecraft:composter[level=6]')
    c.set_block(rx1 + 1, Y_BASE + 1, rz2 - 1, 'minecraft:cauldron')
    c.set_block(rx2 - 1, Y_BASE + 2, rz1 + 1, MAT['lantern_stand'])

    build_seed_variant_outbuilding(c, 44, Y_BASE, 84, w=10, d=8, h=5, seed=404, role='casita')
    build_seed_variant_outbuilding(c, 86, Y_BASE, 4, w=10, d=14, h=6, seed=303, role='art_pavilion')
    build_seed_variant_outbuilding(c, -83, Y_BASE, 20, w=10, d=12, h=5, seed=505, role='casita')
    build_seed_variant_outbuilding(c, -10, Y_BASE, -94, w=20, d=8, h=5, seed=606, role='casita')

    c.fill(-80, Y_BASE, -76, -56, Y_BASE, -36, MAT['stone_smooth'])
    for x in range(-80, -55):
        for z in range(-76, -35):
            if (x - (-80)) % 4 == 0 or (z - (-76)) % 4 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
    build_hedgerow_line(c, -80, Y_BASE, -76, -56, -76, height=2, gap_every=6)
    build_hedgerow_line(c, -80, Y_BASE, -36, -56, -36, height=2, gap_every=6)
    build_hedgerow_line(c, -80, Y_BASE, -76, -80, -36, height=2, gap_every=6)
    build_seed_variant_outbuilding(c, -76, Y_BASE, -70, w=12, d=10, h=5, seed=707, role='art_pavilion')
    build_fountain(c, -66, Y_BASE, -48, radius=4)
    build_patio_umbrella(c, -76, Y_BASE, -46)
    build_outdoor_sofa(c, -78, Y_BASE, -52, length=5, facing='south')

    c.fill(-80, Y_BASE, 48, -52, Y_BASE, 86, MAT['stone_smooth'])
    for x in range(-80, -51):
        for z in range(48, 87):
            if (x - (-80)) % 4 == 0 or (z - 48) % 4 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
    build_hedgerow_line(c, -80, Y_BASE, 86, -52, 86, height=2, gap_every=6)
    build_hedgerow_line(c, -80, Y_BASE, 48, -80, 86, height=2, gap_every=6)
    build_hedgerow_line(c, -52, Y_BASE, 48, -52, 86, height=2, gap_every=6)
    build_seed_variant_outbuilding(c, -76, Y_BASE, 54, w=14, d=10, h=6, seed=808, role='art_pavilion')
    for bx1, bz1, bx2, bz2 in [(-75, 68, -67, 80), (-64, 68, -56, 80)]:
        c.fill(bx1, Y_BASE, bz1, bx2, Y_BASE, bz2, MAT['moss_block'])
        for x in range(bx1, bx2 + 1):
            for z in range(bz1, bz2 + 1):
                if x in (bx1, bx2) or z in (bz1, bz2):
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if (x + z) % 3 == 0 else MAT['moss_block'])
                    c.set_block(x, Y_BASE + 1, z, MAT['slab_quartz_b'])
                elif (x + z) % 2 == 0:
                    place_tall_flower(c, x, Y_BASE + 1, z, 'minecraft:peony' if x % 2 == 0 else 'minecraft:lilac')
                else:
                    c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x + z) % len(SOFT_FLOWERS)])

def step5_main_villa_complex(c: WorldCanvas):
    """
    5. Build Zone C: The Core 3-Story Modern Minimalist Villa Complex with
       COMPREHENSIVE INTERIOR LIGHTING & DETAILED ROOM FURNISHING UPGRADES.
    """
    wx1, wx2, wz1, wz2 = -36, -8, -38, -12
    y_1f = Y_BASE
    y_2f = Y_BASE + 6
    y_3f = Y_BASE + 13

    for x in range(-35, -9):
        for z in range(-11, -5):
            if x in (-35, -10) or z in (-11, -6):
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 1, z, MAT['slab_quartz_b'])
            else:
                c.set_block(x, Y_BASE - 2, z, MAT['light_sea'] if (x + z) % 2 == 0 else MAT['pool_deep_1'])
                c.set_block(x, Y_BASE - 1, z, MAT['water'])
                c.set_block(x, Y_BASE, z, MAT['water'])
    for z in range(-11, -5):
        c.set_block(-22, Y_BASE, z, MAT['wall_quartz'])
        c.set_block(-21, Y_BASE, z, MAT['wall_quartz'])
        c.set_block(-22, Y_BASE + 1, z, 'minecraft:air')
        c.set_block(-21, Y_BASE + 1, z, 'minecraft:air')

    c.fill(wx1, y_1f, wz1, wx2, y_1f, wz2, MAT['wood_dark'])
    c.fill(wx1, y_1f + 1, wz1, wx2, y_2f - 1, wz2, MAT['wall_white'])
    c.fill(wx1 + 1, y_1f + 1, wz1 + 1, wx2 - 1, y_2f - 1, wz2 - 1, 'minecraft:air')

    build_curtain_wall(c, wx1 + 2, y_1f + 1, wz2, wx2 - 2, y_2f - 1, wz2,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, wx1 + 3, y_1f + 1, wz1, wx2 - 3, y_2f - 1, wz1,
                       MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, wx1, y_1f + 1, wz1 + 3, wx1, y_2f - 1, wz2 - 3,
                       MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    place_double_door(c, -22, y_1f + 1, wz2, 'dark_oak', 'north', 'true')

    c.fill(wx1, y_2f, wz1, wx2, y_2f, wz2 + 4, MAT['wood_dark'])
    build_support_beams_under_cantilever(c, wx1, y_2f - 1, wz2, wx2, wz2 + 4, axis='z', step=5)
    for col_x in (-35, -16, -9):
        c.fill(col_x, y_1f + 1, wz2 + 3, col_x, y_2f - 1, wz2 + 3, MAT['wall_white'])
    for x in range(wx1, wx2 + 1):
        c.set_block(x, y_2f, wz2 + 4, MAT['wall_white'])
        c.set_block(x, y_2f + 1, wz2 + 4, MAT['pane_black'])
        if x in (-33, -30, -14, -11):
            c.set_block(x, y_2f, wz2 + 3, MAT['light_ochre'])
            c.set_block(x, y_2f + 1, wz2 + 3, 'minecraft:moss_block')
            c.set_block(x, y_2f + 2, wz2 + 3, MAT['leaf_azalea'])
    for z in range(wz2, wz2 + 5):
        c.set_block(wx1, y_2f, z, MAT['wall_white'])
        c.set_block(wx1, y_2f + 1, z, MAT['pane_black'])

    build_recessed_ceiling_grid(c, wx1 + 2, y_2f, wz1 + 2, wx2 - 2, wz2 - 2, step_x=4, step_z=4, light_mat=MAT['light_ochre'])

    c.fill(wx1, y_2f + 1, wz1, wx2, y_3f - 1, wz2, MAT['wall_white'])
    c.fill(wx1 + 1, y_2f + 1, wz1 + 1, wx2 - 1, y_3f - 1, wz2 - 1, 'minecraft:air')
    c.fill(-31, y_2f, -20, -20, y_2f, -14, 'minecraft:air')
    for x in range(-32, -18):
        for z_edge in (-21, -13):
            c.set_block(x, y_2f, z_edge, MAT['light_ochre'] if x % 3 == 0 else MAT['wall_quartz'])
            c.set_block(x, y_2f + 1, z_edge, MAT['pane_black'])
    for z in range(-20, -13):
        for x_edge in (-32, -19):
            c.set_block(x_edge, y_2f, z, MAT['light_ochre'] if z % 2 == 0 else MAT['wall_quartz'])
            c.set_block(x_edge, y_2f + 1, z, MAT['pane_black'])

    build_curtain_wall(c, wx1 + 3, y_2f + 1, wz2, wx2 - 3, y_3f - 1, wz2,
                       MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, wx1 + 3, y_2f + 1, wz1, wx2 - 3, y_3f - 1, wz1,
                       MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, wx1, y_2f + 1, -22, wx1, y_3f - 1, wz2 - 2,
                       MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    place_double_door(c, -15, y_2f + 1, wz2, 'dark_oak', 'north', 'false')
    build_sun_lounger(c, -26, y_2f, -10, facing='south')
    build_sun_lounger(c, -22, y_2f, -10, facing='south')

    build_pitched_modern_roof(c, wx1, y_3f, wz1, wx2, wz2, ridge_offset=10)

    build_illuminated_carpet_rug(c, -31, y_1f, -25, -23, -18, MAT['carpet_white'], MAT['carpet_lgray'])
    build_outdoor_sofa(c, -30, y_1f, -25, length=7, facing='south')
    build_outdoor_sofa(c, -32, y_1f, -23, length=4, facing='east')
    c.fill(-28, y_1f + 1, -22, -25, y_1f + 1, -21, MAT['slab_quartz_t'])
    c.set_block(-27, y_1f, -22, MAT['light_sea'])
    c.set_block(-27, y_1f + 2, -22, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    c.set_block(-26, y_1f + 2, -21, 'minecraft:flower_pot')
    c.fill(wx1 + 1, y_1f + 1, -27, wx1 + 2, y_2f - 1, -19, MAT['stone_pol_and'])
    c.fill(wx1 + 1, y_1f + 1, -24, wx1 + 1, y_1f + 2, -22, 'minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]')
    c.fill(wx1 + 1, y_1f + 3, -24, wx1 + 1, y_1f + 3, -22, MAT['light_shroom'])
    c.fill(wx1 + 2, y_1f + 1, -24, wx1 + 2, y_1f + 2, -22, MAT['iron_bars'])
    for fz in (-26, -20):
        c.set_block(wx1 + 1, y_1f + 2, fz, MAT['light_ochre'])
        c.set_block(wx1 + 2, y_1f + 2, fz, 'minecraft:bookshelf')
        c.set_block(wx1 + 2, y_1f + 3, fz, 'minecraft:bookshelf')
    build_floor_lamp(c, -33, y_1f, -15, 'modern')
    build_floor_lamp(c, -33, y_1f, -28, 'modern')

    build_illuminated_carpet_rug(c, -17, y_1f, -21, -12, -15, MAT['carpet_lgray'], MAT['carpet_white'])
    c.fill(-16, y_1f + 1, -20, -13, y_1f + 1, -17, MAT['slab_deep_t'])
    c.fill(-16, y_1f + 2, -20, -13, y_1f + 2, -18, MAT['carpet_black'])
    c.set_block(-14, y_1f + 1, -16, stair('smooth_quartz', 'north', 'bottom'))
    build_floor_lamp(c, -11, y_1f, -15, 'modern')
    build_indoor_planter(c, -11, y_1f, -21, tall=True)

    build_home_theater_wall(c, -32, y_1f, -37, width=7, facing='south')
    build_illuminated_carpet_rug(c, -32, y_1f, -34, -26, -30, MAT['carpet_gray'], MAT['carpet_lgray'])
    build_outdoor_sofa(c, -31, y_1f, -31, length=5, facing='north')
    build_floor_lamp(c, -34, y_1f, -35, 'modern')

    build_billiards_table(c, -18, y_1f, -35, y_ceil=y_2f)
    for bz in range(-35, -29):
        c.set_block(-11, y_1f, bz, MAT['light_ochre'] if bz % 2 == 0 else MAT['wood_dark'])
        c.set_block(-11, y_1f + 1, bz, MAT['wood_dark'])
        c.set_block(-11, y_1f + 2, bz, MAT['slab_quartz_b'])
        if bz % 2 == 0:
            c.set_block(-13, y_1f + 1, bz, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
            c.set_block(-13, y_1f + 2, bz, MAT['carpet_white'])
    build_indoor_planter(c, -21, y_1f, -36, tall=True)

    build_crystal_chandelier(c, -26, y_3f, -17, drop=4, style='grand')
    build_crystal_chandelier(c, -27, y_2f, -23, drop=2, style='grand')
    build_crystal_chandelier(c, -15, y_2f, -19, drop=2, style='grand')
    build_crystal_chandelier(c, -28, y_2f, -33, drop=2, style='pearl')

    build_illuminated_carpet_rug(c, -33, y_2f, -35, -25, -28, MAT['carpet_white'], MAT['carpet_lgray'])
    c.fill(-33, y_2f + 1, -36, -25, y_2f + 4, -36, MAT['wood_dark'])
    for hx in (-32, -29, -26):
        c.fill(hx, y_2f + 2, -36, hx, y_2f + 3, -36, MAT['light_ochre'])
        c.fill(hx, y_2f + 2, -35, hx, y_2f + 3, -35, trapdoor('dark_oak', 'south', 'bottom', 'true'))
    place_bed(c, -30, y_2f + 1, -33, facing='north', color='white')
    place_bed(c, -29, y_2f + 1, -33, facing='north', color='white')
    for nx in (-32, -27):
        c.set_block(nx, y_2f + 1, -34, MAT['wall_quartz'])
        c.set_block(nx, y_2f + 2, -34, MAT['lantern_stand'] if nx == -32 else 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    c.fill(-31, y_2f + 1, -31, -28, y_2f + 1, -31, MAT['slab_quartz_b'])
    for wz_i in range(-32, -23):
        if wz_i % 3 == 0:
            place_barrel(c, -35, y_2f + 1, wz_i, 'east')
            c.set_block(-35, y_2f + 2, wz_i, MAT['light_ochre'])
            c.set_block(-35, y_2f + 3, wz_i, 'minecraft:bookshelf')
        else:
            c.fill(-35, y_2f + 1, wz_i, -35, y_2f + 3, wz_i, 'minecraft:bookshelf')
    build_floor_lamp(c, -34, y_2f, -23, 'modern')
    build_crystal_chandelier(c, -29, y_3f + 2, -31, drop=3, style='grand')

    build_ensuite_bathroom(c, -20, y_2f, -37, -9, -29, door_side='south')

    build_illuminated_carpet_rug(c, -17, y_2f, -24, -11, -16, MAT['carpet_lgray'], MAT['carpet_white'])
    build_outdoor_sofa(c, -16, y_2f, -18, length=5, facing='north')
    place_lectern(c, -11, y_2f + 1, -24, 'south')
    build_floor_lamp(c, -17, y_2f, -25, 'modern')
    build_indoor_planter(c, -10, y_2f, -15, tall=True)
    build_crystal_chandelier(c, -14, y_3f + 1, -20, drop=2, style='pearl')

    mx1, mx2, mz1, mz2 = -8, 12, -36, -12

    c.fill(mx1, y_1f, mz1, mx2, y_1f, mz2, MAT['wall_quartz'])
    c.fill(mx1, y_1f + 1, mz1, mx2, y_2f - 1, mz2, MAT['wall_white'])
    c.fill(mx1 + 1, y_1f + 1, mz1 + 1, mx2 - 1, y_2f - 1, mz2 - 1, 'minecraft:air')
    c.fill(mx1, y_1f + 1, -32, mx1, y_2f - 2, -18, 'minecraft:air')
    c.fill(mx2, y_1f + 1, -32, mx2, y_2f - 2, -18, 'minecraft:air')

    build_curtain_wall(c, -6, y_1f + 1, mz2, 1, y_2f - 1, mz2, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=3)
    place_double_door(c, -3, y_1f + 1, mz2, 'dark_oak', 'north', 'true')
    build_slatted_feature_wall(c, 2, y_1f + 1, mz2, 10, y_2f - 1, mz2, MAT['wall_white'], MAT['glass_black'])

    build_curtain_wall(c, mx1 + 2, y_1f + 1, mz1, mx2 - 2, y_2f - 1, mz1, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    place_double_door(c, 0, y_1f + 1, mz1, 'dark_oak', 'south', 'true')

    build_recessed_ceiling_grid(c, mx1 + 2, y_2f, mz1 + 2, mx2 - 2, mz2 - 2, step_x=4, step_z=4, light_mat=MAT['light_pearl'])

    build_illuminated_carpet_rug(c, -3, y_1f, -34, 1, -14, MAT['carpet_white'], MAT['carpet_lgray'])
    build_outdoor_bar(c, -5, y_1f, -32, length=6)
    build_illuminated_carpet_rug(c, 4, y_1f, -33, 10, -27, MAT['carpet_lgray'], MAT['carpet_white'])
    build_outdoor_sofa(c, 5, y_1f, -33, length=4, facing='south')
    build_outdoor_sofa(c, 5, y_1f, -27, length=4, facing='north')
    c.fill(6, y_1f + 1, -30, 8, y_1f + 1, -30, MAT['slab_dark_t'])
    c.set_block(7, y_1f + 2, -30, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    c.fill(5, y_1f + 1, -18, 7, y_1f + 1, -16, MAT['frame_dark'])
    c.set_block(6, y_1f + 2, -17, MAT['wall_quartz'])
    c.set_block(6, y_1f + 3, -17, MAT['light_ochre'])
    c.set_block(6, y_1f + 4, -17, MAT['end_rod_up'])
    for bx in (9,):
        build_indoor_planter(c, bx, y_1f, -13, tall=False)
    for x in range(-7, -3):
        for z in range(-24, -19):
            c.set_block(x, y_1f - 1, z, MAT['light_sea'])
            c.set_block(x, y_1f, z, MAT['water'] if (x + z) % 2 == 0 else MAT['moss_block'])
    build_crystal_chandelier(c, 0, y_2f, -20, drop=2, style='grand')
    build_crystal_chandelier(c, 6, y_2f, -22, drop=2, style='pearl')

    c.fill(mx1, y_2f, mz1, mx2, y_2f, mz2, MAT['wood_dark'])
    c.fill(mx1, y_2f + 1, mz1, mx2, y_3f - 1, -18, MAT['wall_white'])
    c.fill(mx1 + 1, y_2f + 1, mz1 + 1, mx2 - 1, y_3f - 1, -19, 'minecraft:air')
    c.fill(mx1, y_2f + 1, -30, mx1, y_3f - 2, -22, 'minecraft:air')
    c.fill(mx2, y_2f + 1, -30, mx2, y_3f - 2, -22, 'minecraft:air')
    build_curtain_wall(c, mx1, y_2f + 1, -18, mx2, y_3f - 1, -18, MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, mx1 + 1, y_2f + 1, mz1, mx2 - 1, y_3f - 1, mz1, MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    place_double_door(c, 1, y_2f + 1, -18, 'dark_oak', 'north', 'false')

    build_illuminated_carpet_rug(c, -7, y_2f, -29, 11, -23, MAT['carpet_white'], MAT['carpet_lgray'])
    build_straight_stairs(c, -6, y_1f + 1, -18, width=3, height=y_2f - y_1f, direction='north', stair_prefix='smooth_quartz', hidden_lights=True)
    for bx in range(-2, 9):
        c.set_block(bx, y_2f, mz1 + 1, MAT['light_ochre'])
        c.fill(bx, y_2f + 1, mz1 + 1, bx, y_2f + 4, mz1 + 1, MAT['light_ochre'] if bx in (0, 6) else 'minecraft:bookshelf')
    c.fill(0, y_2f + 1, -26, 4, y_2f + 1, -25, MAT['slab_dark_t'])
    c.set_block(2, y_2f, -25, MAT['light_ochre'])
    c.set_block(1, y_2f + 2, -25, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    place_lectern(c, 3, y_2f + 1, -25, 'north')
    c.set_block(2, y_2f + 1, -27, stair('smooth_quartz', 'south', 'bottom'))
    c.set_block(1, y_2f + 1, -23, stair('smooth_quartz', 'north', 'bottom'))
    c.set_block(3, y_2f + 1, -23, stair('smooth_quartz', 'north', 'bottom'))
    build_floor_lamp(c, -2, y_2f, -20, 'modern')
    build_floor_lamp(c, 9, y_2f, -20, 'modern')
    build_flat_roof_and_eaves(c, mx1, y_3f, mz1, mx2, -18, overhang=1, hidden_lights=True)
    build_crystal_chandelier(c, 2, y_3f, -26, drop=2, style='grand')
    build_crystal_chandelier(c, 7, y_3f, -26, drop=2, style='pearl')

    c.fill(7, y_2f, -17, 11, y_2f + 1, -13, MAT['wall_qbrick'])
    c.fill(8, y_2f + 1, -16, 10, y_2f + 1, -14, MAT['moss_block'])
    c.set_block(8, y_2f + 1, -16, MAT['light_ochre'])
    c.set_block(10, y_2f + 1, -14, MAT['light_ochre'])
    build_spherical_shrub(c, 9, y_2f + 1, -15, radius=1, tone='light')
    for x in range(mx1, mx2 + 1):
        c.set_block(x, y_2f, mz2, MAT['wall_quartz'])
        c.set_block(x, y_2f + 1, mz2, MAT['pane_black'])

    ex1, ex2, ez1, ez2 = 12, 36, -40, -8
    y_roof_3f = Y_BASE + 19

    c.fill(ex1, y_1f, ez1, ex2, y_1f, ez2, MAT['wood_warm'])
    c.fill(ex1, y_1f + 1, ez1, ex2, y_2f - 1, ez2, MAT['wall_white'])
    c.fill(ex1 + 1, y_1f + 1, ez1 + 1, ex2 - 1, y_2f - 1, ez2 - 1, 'minecraft:air')
    c.fill(ex1, y_1f + 1, -32, ex1, y_2f - 2, -18, 'minecraft:air')

    build_curtain_wall(c, ex1 + 1, y_1f + 1, ez2, ex2 - 1, y_2f - 1, ez2,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, ex1, y_1f + 1, -18, ex1, y_2f - 1, ez2 - 1,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, ex2, y_1f + 1, ez1 + 2, ex2, y_2f - 1, ez2 - 2,
                       MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, ex1 + 2, y_1f + 1, ez1, ex2 - 2, y_2f - 1, ez1,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    place_double_door(c, 27, y_1f + 1, ez2, 'dark_oak', 'north', 'true')

    build_illuminated_carpet_rug(c, 21, y_1f, -18, 33, -11, MAT['carpet_lgray'], MAT['carpet_white'])
    c.fill(23, y_1f + 1, -15, 31, y_1f + 1, -14, MAT['slab_quartz_t'])
    for tx in (23, 27, 31):
        c.set_block(tx, y_1f, -15, MAT['light_ochre'])
        c.set_block(tx, y_1f + 1, -15, MAT['wall_quartz'])
        c.set_block(tx, y_1f + 2, -15, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    for cx_chair in (23, 25, 27, 29, 31):
        c.set_block(cx_chair, y_1f + 1, -17, stair('dark_oak', 'south', 'bottom'))
        c.set_block(cx_chair, y_1f + 1, -12, stair('dark_oak', 'north', 'bottom'))
    for z_buf in range(-15, -10):
        c.set_block(14, y_1f, z_buf, MAT['light_ochre'] if z_buf % 2 == 0 else MAT['wood_dark'])
        c.set_block(14, y_1f + 1, z_buf, MAT['wood_dark'])
        c.set_block(14, y_1f + 2, z_buf, MAT['slab_quartz_b'])
    build_floor_lamp(c, 15, y_1f, -17, 'modern')
    build_indoor_planter(c, 34, y_1f, -10, tall=True)
    for lx in range(23, 32, 2):
        c.set_block(lx, y_2f - 1, -15, MAT['chain_y'])
        c.set_block(lx, y_2f - 2, -15, MAT['light_ochre'])
        c.set_block(lx, y_2f - 3, -15, MAT['end_rod_down'])

    for x in range(14, 35):
        for z in range(-30, -19):
            if (x + z) % 4 == 0:
                c.set_block(x, y_1f, z, MAT['light_sea'])
            else:
                c.set_block(x, y_1f, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
    for kz in range(-29, -20):
        c.set_block(34, y_1f + 1, kz, MAT['stone_pol_and'])
        c.set_block(34, y_1f + 4, kz, MAT['wood_dark'])
        if kz % 2 == 0:
            c.set_block(34, y_1f + 3, kz, MAT['light_ochre'])
    place_smoker(c, 34, y_1f + 1, -28, facing='west', lit='true')
    place_smoker(c, 34, y_1f + 1, -27, facing='west', lit='true')
    place_blast_furnace(c, 34, y_1f + 1, -26, facing='west', lit='false')
    c.fill(33, y_1f + 3, -28, 34, y_1f + 4, -26, MAT['stone_pol_and'])
    c.set_block(33, y_1f + 3, -27, MAT['light_sea'])
    c.set_block(34, y_1f + 1, -24, 'minecraft:water_cauldron[level=3]')
    c.set_block(34, y_1f + 1, -23, 'minecraft:water_cauldron[level=3]')
    c.fill(34, y_1f + 1, -22, 34, y_1f + 3, -21, 'minecraft:iron_block')
    c.fill(18, y_1f + 1, -27, 29, y_1f + 1, -26, MAT['wall_quartz'])
    c.set_block(21, y_1f + 1, -27, 'minecraft:water_cauldron[level=3]')
    place_brewing_stand(c, 25, y_1f + 2, -27)
    c.set_block(27, y_1f + 2, -27, 'minecraft:flower_pot')
    c.fill(18, y_1f + 1, -23, 29, y_1f + 1, -22, MAT['wall_quartz'])
    c.fill(18, y_1f + 2, -23, 29, y_1f + 2, -22, MAT['carpet_white'])
    for bx in range(19, 29, 2):
        c.set_block(bx, y_1f + 1, -20, stair('dark_oak', 'north', 'bottom'))
        c.set_block(bx, y_2f - 1, -25, MAT['chain_y'])
        c.set_block(bx, y_2f - 2, -25, MAT['light_ochre'])

    for x in range(13, 36):
        if x in (18, 19, 20, 29, 30, 31):
            continue
        for y in range(y_1f + 1, y_2f):
            c.set_block(x, y, -31, MAT['frame_dark'] if y in (y_1f + 1, y_2f - 1) or x % 4 == 0 else MAT['glass_tinted'])
    for x in range(14, 27):
        if x % 2 == 0:
            place_barrel(c, x, y_1f + 1, -39, 'south')
            place_barrel(c, x, y_1f + 2, -39, 'south')
            c.set_block(x, y_1f + 3, -39, MAT['light_ochre'])
            c.set_block(x, y_1f + 4, -39, 'minecraft:bookshelf')
        else:
            c.fill(x, y_1f + 1, -39, x, y_1f + 4, -39, 'minecraft:bookshelf')
    build_illuminated_carpet_rug(c, 16, y_1f, -37, 24, -33, MAT['carpet_lgray'], MAT['carpet_white'])
    c.fill(18, y_1f + 1, -35, 22, y_1f + 1, -35, MAT['slab_dark_t'])
    c.set_block(20, y_1f + 2, -35, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    build_crystal_chandelier(c, 20, y_2f, -35, drop=2, style='grand')

    c.fill(ex1, y_2f, ez1, ex2 + 3, y_2f, ez2 + 4, MAT['wood_dark'])
    build_support_beams_under_cantilever(c, ex1, y_2f - 1, ez2, ex2 + 3, ez2 + 4, axis='z', step=4)
    build_support_beams_under_cantilever(c, ex2, y_2f - 1, ez1, ex2 + 3, ez2 + 4, axis='x', step=4)
    build_recessed_ceiling_grid(c, ex1 + 2, y_2f, ez1 + 2, ex2 - 2, ez2 - 2, step_x=4, step_z=4, light_mat=MAT['light_ochre'])

    c.fill(14, y_2f + 1, -38, 36, y_3f - 1, -12, MAT['wall_white'])
    c.fill(15, y_2f + 1, -37, 35, y_3f - 1, -13, 'minecraft:air')
    c.fill(14, y_2f + 1, -30, 14, y_3f - 2, -22, 'minecraft:air')

    build_curtain_wall(c, 15, y_2f + 1, -12, 34, y_3f - 1, -12, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 14, y_2f + 1, -35, 14, y_3f - 1, -14, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    c.fill(14, y_2f + 1, -30, 14, y_3f - 2, -22, 'minecraft:air')
    build_curtain_wall(c, 16, y_2f + 1, -38, 34, y_3f - 1, -38, MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    place_double_door(c, 22, y_2f + 1, -12, 'dark_oak', 'north', 'false')

    for x in range(12, 40):
        c.set_block(x, y_2f, -4, MAT['wall_white'])
        c.set_block(x, y_2f + 1, -4, MAT['pane_black'])
    for z in range(-40, -3):
        c.set_block(12, y_2f, z, MAT['wall_white'])
        if z >= -12:
            c.set_block(12, y_2f + 1, z, MAT['pane_black'])
        c.set_block(39, y_2f, z, MAT['wall_white'])
        c.set_block(39, y_2f + 1, z, MAT['pane_black'])

    build_ensuite_bathroom(c, 15, y_2f, -37, 23, -31, door_side='south')
    build_illuminated_carpet_rug(c, 26, y_2f, -35, 34, -24, MAT['carpet_white'], MAT['carpet_lgray'])
    c.fill(35, y_2f + 1, -32, 35, y_2f + 4, -26, MAT['wood_dark'])
    c.set_block(35, y_2f + 2, -31, MAT['light_ochre'])
    c.set_block(35, y_2f + 2, -27, MAT['light_ochre'])
    place_bed(c, 33, y_2f + 1, -29, facing='east', color='white')
    place_bed(c, 33, y_2f + 1, -28, facing='east', color='white')
    c.set_block(34, y_2f + 1, -31, MAT['wall_quartz'])
    c.set_block(34, y_2f + 2, -31, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    c.set_block(34, y_2f + 1, -26, MAT['wall_quartz'])
    c.set_block(34, y_2f + 2, -26, MAT['lantern_stand'])
    c.fill(24, y_2f + 1, -37, 26, y_2f + 3, -37, 'minecraft:bookshelf')
    build_floor_lamp(c, 26, y_2f, -23, 'modern')
    build_illuminated_carpet_rug(c, 20, y_2f, -20, 28, -14, MAT['carpet_lgray'], MAT['carpet_white'])
    build_outdoor_sofa(c, 21, y_2f, -15, length=5, facing='north')
    build_indoor_planter(c, 15, y_2f, -14, tall=True)
    build_outdoor_sofa(c, 20, y_2f, -8, length=5, facing='north')

    c.fill(26, y_2f, -8, 38, y_2f, 10, MAT['wood_dark'])
    build_support_beams_under_cantilever(c, 26, y_2f - 1, -8, 38, 10, axis='x', step=4)
    for cz_col in (-2, 4, 9):
        c.fill(37, y_1f + 1, cz_col, 38, y_2f - 1, cz_col, MAT['wall_white'])
        c.fill(31, y_1f + 1, cz_col, 31, y_2f - 1, cz_col, MAT['stone_pol_and'])
    c.fill(30, y_2f + 1, -8, 38, y_3f - 1, 6, MAT['wall_white'])
    c.fill(31, y_2f + 1, -7, 37, y_3f - 1, 5, 'minecraft:air')
    build_curtain_wall(c, 30, y_2f + 1, -6, 30, y_3f - 1, 4, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 38, y_2f + 1, -6, 38, y_3f - 1, 4, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 31, y_2f + 1, 6, 37, y_3f - 1, 6, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=3)
    c.fill(31, y_2f + 1, -12, 37, y_3f - 1, -8, MAT['wall_white'])
    c.fill(32, y_2f + 1, -12, 36, y_3f - 2, -8, 'minecraft:air')
    place_door(c, 30, y_2f + 1, 0, 'dark_oak', 'east', 'left', 'false')
    build_illuminated_carpet_rug(c, 32, y_2f, -6, 36, 4, MAT['carpet_white'], MAT['carpet_lgray'])
    c.fill(33, y_2f + 1, -2, 35, y_2f + 1, 0, MAT['slab_quartz_t'])
    place_lectern(c, 34, y_2f + 1, 1, 'north')
    c.set_block(34, y_2f + 2, -1, MAT['lantern_stand'])
    build_indoor_planter(c, 32, y_2f, 4, tall=True)
    build_indoor_planter(c, 36, y_2f, 4, tall=True)
    for z in range(-8, 11):
        c.set_block(26, y_2f, z, MAT['wall_white'])
        c.set_block(26, y_2f + 1, z, MAT['pane_black'])
    for x in range(26, 39):
        c.set_block(x, y_2f, 10, MAT['wall_white'])
        c.set_block(x, y_2f + 1, 10, MAT['pane_black'])
    c.set_block(28, y_2f + 1, 2, MAT['slab_dark_t'])
    c.set_block(28, y_2f + 1, 1, stair('smooth_quartz', 'north', 'bottom'))
    c.set_block(28, y_2f + 1, 3, stair('smooth_quartz', 'south', 'bottom'))
    build_flat_roof_and_eaves(c, 26, y_3f, -8, 38, 10, overhang=1, hidden_lights=True)
    build_crystal_chandelier(c, 34, y_3f, -1, drop=2, style='grand')

    c.fill(0, y_3f, -36, 36, y_3f, -10, MAT['wood_dark'])
    build_support_beams_under_cantilever(c, 0, y_3f - 1, -18, 14, -10, axis='z', step=4)
    build_recessed_ceiling_grid(c, 16, y_3f, -36, 34, -14, step_x=4, step_z=4, light_mat=MAT['light_ochre'])
    build_crystal_chandelier(c, 24, y_3f, -18, drop=2, style='grand')
    build_crystal_chandelier(c, 30, y_3f, -28, drop=2, style='grand')

    c.fill(6, y_3f + 1, -34, 34, y_roof_3f - 1, -15, MAT['wall_white'])
    c.fill(7, y_3f + 1, -33, 33, y_roof_3f - 1, -16, 'minecraft:air')
    build_curtain_wall(c, 7, y_3f + 1, -15, 32, y_roof_3f - 1, -15, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=5)
    build_curtain_wall(c, 6, y_3f + 1, -32, 6, y_roof_3f - 1, -16, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 8, y_3f + 1, -34, 32, y_roof_3f - 1, -34, MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 34, y_3f + 1, -32, 34, y_roof_3f - 1, -17, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    c.fill(1, y_3f + 1, -35, 5, y_3f + 3, -11, 'minecraft:air')
    place_door(c, 6, y_3f + 1, -20, 'dark_oak', 'east', 'left', 'false')
    place_double_door(c, 20, y_3f + 1, -15, 'dark_oak', 'north', 'false')

    for x in range(0, 37):
        c.set_block(x, y_3f, -10, MAT['wall_white'])
        c.set_block(x, y_3f + 1, -10, MAT['pane_black'])
        c.set_block(x, y_3f, -36, MAT['wall_white'])
        c.set_block(x, y_3f + 1, -36, MAT['pane_black'])
    for z in range(-36, -9):
        c.set_block(0, y_3f, z, MAT['wall_white'])
        c.set_block(0, y_3f + 1, z, MAT['pane_black'])
        c.set_block(36, y_3f, z, MAT['wall_white'])
        c.set_block(36, y_3f + 1, z, MAT['pane_black'])
    for px, pz in [(2, -12), (16, -12), (33, -12), (2, -34)]:
        c.set_block(px, y_3f, pz, MAT['light_ochre'])
        c.set_block(px, y_3f + 1, pz, MAT['moss_block'])
        c.set_block(px, y_3f + 2, pz, MAT['leaf_azalea'])
        c.set_block(px, y_3f + 3, pz, MAT['leaf_fl_azalea'])

    build_illuminated_carpet_rug(c, 8, y_3f, -21, 18, -16, MAT['carpet_white'], MAT['carpet_lgray'])
    build_outdoor_sofa(c, 9, y_3f, -19, length=5, facing='south')
    build_outdoor_bar(c, 19, y_3f, -31, length=6)
    build_straight_stairs(c, 15, y_2f + 1, -22, width=3, height=y_3f - y_2f, direction='north', stair_prefix='smooth_quartz', hidden_lights=True)
    build_illuminated_carpet_rug(c, 25, y_3f, -26, 32, -18, MAT['carpet_lgray'], MAT['carpet_white'])
    c.fill(27, y_3f + 1, -24, 30, y_3f + 1, -20, MAT['slab_quartz_t'])
    c.set_block(28, y_3f + 2, -22, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    c.set_block(29, y_3f + 2, -22, 'minecraft:flower_pot')
    for z_ch in (-24, -22, -20):
        c.set_block(25, y_3f + 1, z_ch, stair('dark_oak', 'east', 'bottom'))
        c.set_block(32, y_3f + 1, z_ch, stair('dark_oak', 'west', 'bottom'))
    build_floor_lamp(c, 8, y_3f, -32, 'modern')
    build_floor_lamp(c, 32, y_3f, -32, 'modern')
    build_indoor_planter(c, 32, y_3f, -17, tall=True)

    build_flat_roof_and_eaves(c, 4, y_roof_3f, -35, 36, -9, overhang=2,
                              roof_mat=MAT['wall_white'], soffit_mat=MAT['wood_dark'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)
    for lx in (11, 20, 29):
        build_crystal_chandelier(c, lx, y_roof_3f, -22, drop=2, style='grand')

    build_spiral_staircase(c, 4, y_1f, y_3f, -14, radius=2)

    build_tower(c, 28, y_1f, -41, size=8, height=28)

    c.fill(29, y_1f + 1, -35, 34, y_1f + 3, -32, 'minecraft:air')
    c.fill(26, y_1f + 1, -39, 28, y_1f + 3, -36, 'minecraft:air')
    c.fill(29, y_2f + 1, -35, 34, y_2f + 3, -33, 'minecraft:air')
    c.fill(25, y_2f + 1, -37, 28, y_2f + 3, -35, 'minecraft:air')

    c.fill(24, y_3f, -39, 28, y_3f, -35, MAT['wall_quartz'])
    for z_t in range(-39, -35):
        c.set_block(24, y_3f + 1, z_t, MAT['pane_black'])
    for x_t in range(24, 28):
        c.set_block(x_t, y_3f + 1, -39, MAT['pane_black'])
    c.fill(29, y_3f + 1, -35, 34, y_3f + 3, -33, 'minecraft:air')
    c.fill(25, y_3f + 1, -38, 28, y_3f + 3, -36, 'minecraft:air')

def step6_backyard_pool_and_resort(c: WorldCanvas):
    """
    6. Build Zone F: Backyard Timber Deck, Infinity Pool, Sun Loungers, Umbrellas,
       Outdoor Bar, and Sunken Fire-Pit Lounge.
    """
    build_infinity_pool(c, -26, Y_BASE, -76, 26, -56)
    build_outdoor_bar(c, -18, Y_BASE, -46, length=6)
    build_outdoor_sofa(c, 6, Y_BASE, -45, length=6, facing='north')
    build_outdoor_sofa(c, -4, Y_BASE, -48, length=5, facing='south')

    umbrella_coords = [(-20, -51), (0, -51), (20, -51), (-32, -66), (32, -66), (0, -82)]
    for ux, uz in umbrella_coords:
        build_patio_umbrella(c, ux, Y_BASE, uz)

    for lx in range(-22, 23, 5):
        build_sun_lounger(c, lx, Y_BASE, -80, facing='south')
    for lz in (-72, -66, -60):
        build_sun_lounger(c, -30, Y_BASE, lz, facing='east')
        build_sun_lounger(c, 30, Y_BASE, lz, facing='west')

    fx1, fx2, fz1, fz2 = -44, -34, -72, -62
    c.fill(fx1, Y_BASE - 1, fz1, fx2, Y_BASE - 1, fz2, MAT['wood_dark'])
    c.fill(fx1 + 1, Y_BASE, fz1 + 1, fx2 - 1, Y_BASE, fz2 - 1, 'minecraft:air')
    for x in range(fx1 + 2, fx2 - 1):
        c.set_block(x, Y_BASE, fz1 + 1, stair('smooth_quartz', 'north', 'bottom'))
        c.set_block(x, Y_BASE, fz2 - 1, stair('smooth_quartz', 'south', 'bottom'))
    for z in range(fz1 + 2, fz2 - 1):
        c.set_block(fx1 + 1, Y_BASE, z, stair('smooth_quartz', 'west', 'bottom'))
        c.set_block(fx2 - 1, Y_BASE, z, stair('smooth_quartz', 'east', 'bottom'))
    fcx, fcz = (fx1 + fx2) // 2, (fz1 + fz2) // 2
    c.fill(fcx - 1, Y_BASE, fcz - 1, fcx + 1, Y_BASE, fcz + 1, MAT['stone_pol_and'])
    c.set_block(fcx, Y_BASE, fcz, 'minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]')

    for lx in (-46, -28, 0, 28, 46):
        build_lamppost(c, lx, Y_BASE + 1, -54, style='courtyard')
        build_lamppost(c, lx, Y_BASE + 1, -84, style='courtyard')
