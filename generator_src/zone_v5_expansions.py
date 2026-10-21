"""
zone_v5_expansions.py — Outward V5 Architectural Expansions for Modern Manor
=============================================================================
1. Supercar Showroom (新建超跑展厅，陈列 6 辆体素超跑):
   - Located in the unoccupied South-West Welcome Concourse (X = -48..-12, Z = 62..98, Y = 64..71),
     symmetrically opposite the East Garage Driveway across the Main Welcome Boulevard (X = -9..9).
   - Connected via a flush asphalt & quartz driveway apron (X = -11..-4, Z = 72..78) and a North
     courtyard promenade (X = -32..-28, Z = 50..61).
   - Displays 6 distinct pure-voxel supercars on illuminated quartz & sea-lantern turntables.

2. Luxury Underwater Michelin 3-Star Restaurant (拓展水下展厅，到豪华水下米其林餐厅，注意水下照明):
   - Extends southward from the East end of the Underwater Viewing Tunnel (X = 165..171, Z = -57)
     via a submerged glass gallery (X = 165..171, Z = -57..-49, Y = 52..56) into a 21x21 domed
     underwater Michelin restaurant ("L'Abysse d'Or", center X = 168, Z = -38, radius = 10, Y = 51..59).
   - Features an open chef's tasting & raw bar counter, 6 panoramic reef-side dining tables,
     sommelier wine wall, and multi-layered underwater illumination (luminous seabed mosaic,
     eye-level lit coral reefs, sea pickles, suspended glowing jellyfish/manta sculptures, and
     waterlogged level-15 light blocks throughout the surrounding water column).

3. Barrel-Vaulted Wine Cellar, Cigar Lounge & Private Art Vault (拱顶酒窖、雪茄 lounge 与私人艺术品金库):
   - Located in the unoccupied East Estate Cultural Wing (X = 44..94, Z = -41..-22, Y = 60..71),
     connected directly on the West (X = 36..44, Z = -34..-30) to the Main Villa 1F Wine Room &
     Belvedere Tower, and on the East (X = 94..98, Z = -34..-30) to the Seaside Park Boulevard.
   - Features a true semi-cylindrical barrel vault (`deepslate_tiles` / `deepslate_tile_stairs` /
     `deepslate_tile_slab` ribs alternating with `spruce_planks` / `spruce_stairs` / `spruce_slab`),
     wall-lined `barrel` wine racks (`沿墙排列 barrel 酒架`), and `oxidized_copper_grate` constant-
     temperature ventilation ducts (`恒温通风口`), plus a plush Cigar Lounge with walk-in cedar humidor
     and a high-security Private Art & Bullion Vault (zero entities / zero armor stands).
"""

import math
from config import Y_BASE, SEA_LEVEL, HARBOR_FLOOR, MAT, CORAL_BLOCKS
from world_canvas import WorldCanvas
from arch_lib import (
    stair, trapdoor,
    place_barrel, place_brewing_stand, place_smoker, place_lectern,
    place_door, place_double_door,
    build_recessed_ceiling_grid, build_crystal_chandelier, build_illuminated_carpet_rug,
    build_floor_lamp, build_indoor_planter, build_curtain_wall, build_flat_roof_and_eaves,
    build_lamppost, build_hedgerow_line
)

def _build_voxel_supercar(c: WorldCanvas, cx: int, y_floor: int, cz: int, facing: str,
                          body_block: str, body_stair_prefix: str, body_slab_b: str,
                          body_carpet: str, accent_block: str, has_gt_wing: bool = True):
    """
    Builds a detailed 3-wide x 7-long pure-voxel supercar centered at (cx, cz) on walking
    surface `y_floor + 1` (wheels sit at `y = y_floor + 1`, roof/wing at `y = y_floor + 2`).
    `facing` is 'south' (+Z) or 'north' (-Z).
    """
    s = 1 if facing == 'south' else -1
    f_dir = 'south' if facing == 'south' else 'north'
    r_dir = 'north' if facing == 'south' else 'south'
    y1 = y_floor + 1
    y2 = y_floor + 2

    for dx in range(-3, 4):
        for dz in range(-4, 5):
            if dx * dx + (dz * 0.85) ** 2 <= 11.5:
                if abs(dx) == 3 or abs(dz) == 4:
                    c.set_block(cx + dx, y_floor, cz + dz, MAT['light_sea'] if (dx + dz) % 2 == 0 else MAT['frame_dark'])
                else:
                    c.set_block(cx + dx, y_floor, cz + dz, MAT['light_ochre'] if (dx == 0 and dz in (-2, 2)) else MAT['wall_quartz'])

    for dx in (-1, 0, 1):
        c.set_block(cx + dx, y1, cz + 3 * s, MAT['slab_deep_b'] if dx == 0 else stair(body_stair_prefix, r_dir, 'bottom'))
    c.set_block(cx, y1, cz + 3 * s, accent_block)

    c.set_block(cx - 1, y1, cz + 2 * s, MAT['wall_black'])
    c.set_block(cx + 1, y1, cz + 2 * s, MAT['wall_black'])
    c.set_block(cx, y1, cz + 2 * s, body_block)
    for dx in (-1, 0, 1):
        c.set_block(cx + dx, y2, cz + 2 * s, body_carpet)

    for dx in (-1, 0, 1):
        c.set_block(cx + dx, y1, cz + 1 * s, body_block if dx != 0 else accent_block)
    c.set_block(cx, y2, cz + 1 * s, MAT['glass_black'])
    c.set_block(cx - 1, y2, cz + 1 * s, MAT['pane_black'])
    c.set_block(cx + 1, y2, cz + 1 * s, MAT['pane_black'])

    c.set_block(cx - 1, y1, cz, body_block)
    c.set_block(cx + 1, y1, cz, body_block)
    c.set_block(cx, y1, cz, stair('dark_oak', f_dir, 'bottom'))
    c.set_block(cx, y2, cz, MAT['glass_tinted'])
    c.set_block(cx - 1, y2, cz, trapdoor('dark_oak', 'west', 'bottom', 'true'))
    c.set_block(cx + 1, y2, cz, trapdoor('dark_oak', 'east', 'bottom', 'true'))

    for dx in (-1, 0, 1):
        c.set_block(cx + dx, y1, cz - 1 * s, body_block if dx != 0 else MAT['frame_dark'])
    c.set_block(cx, y2, cz - 1 * s, stair(body_stair_prefix, f_dir, 'bottom'))
    c.set_block(cx - 1, y2, cz - 1 * s, body_carpet)
    c.set_block(cx + 1, y2, cz - 1 * s, body_carpet)

    c.set_block(cx - 1, y1, cz - 2 * s, MAT['wall_black'])
    c.set_block(cx + 1, y1, cz - 2 * s, MAT['wall_black'])
    c.set_block(cx, y1, cz - 2 * s, body_block)
    for dx in (-1, 0, 1):
        c.set_block(cx + dx, y2, cz - 2 * s, body_slab_b if dx == 0 else body_carpet)

    c.set_block(cx - 1, y1, cz - 3 * s, stair('polished_deepslate', f_dir, 'top'))
    c.set_block(cx + 1, y1, cz - 3 * s, stair('polished_deepslate', f_dir, 'top'))
    c.set_block(cx, y1, cz - 3 * s, MAT['light_ochre'])
    if has_gt_wing:
        for dx in (-1, 0, 1):
            c.set_block(cx + dx, y2, cz - 3 * s, MAT['slab_deep_t'] if dx != 0 else body_slab_b)
    else:
        c.set_block(cx, y2, cz - 3 * s, body_carpet)

    lec_x = cx - 3 if cx < -25 else cx + 3
    c.set_block(lec_x, y_floor, cz + 3 * s, MAT['light_sea'])
    place_lectern(c, lec_x, y1, cz + 3 * s, facing=f_dir)

def step12_supercar_showroom(c: WorldCanvas):
    """
    Expansion 1: Glass & Quartz Supercar Showroom (新建超跑展厅，陈列 6 辆体素超跑)
    Footprint: X = -48..-12, Z = 62..98, Y = 64..71
    """
    sx1, sx2, sz1, sz2 = -48, -12, 62, 98
    y_1f = Y_BASE
    y_roof = Y_BASE + 7

    for x in range(-11, -3):
        for z in range(72, 79):
            if x == -4 and z in (73, 75, 77):
                c.set_block(x, y_1f, z, MAT['wall_quartz'])
            elif z == 75 and x <= -6 and x % 3 == 0:
                c.set_block(x, y_1f, z, MAT['wall_quartz'])
            elif z in (72, 78):
                c.set_block(x, y_1f, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, y_1f, z, MAT['wall_gray'])
            c.fill(x, y_1f + 1, z, x, y_1f + 4, z, 'minecraft:air')

    for z in range(51, 62):
        for x in range(-32, -27):
            if x in (-32, -28):
                c.set_block(x, y_1f, z, MAT['light_ochre'] if z % 4 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, y_1f, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            c.fill(x, y_1f + 1, z, x, y_1f + 4, z, 'minecraft:air')

    c.fill(sx1, y_1f - 1, sz1, sx2, y_1f - 1, sz2, MAT['stone_pol_and'])
    for x in range(sx1, sx2 + 1):
        for z in range(sz1, sz2 + 1):
            if (x - sx1) % 6 == 0 and (z - sz1) % 6 == 0:
                c.set_block(x, y_1f, z, MAT['light_sea'])
            elif (x - sx1) % 6 == 0 or (z - sz1) % 6 == 0:
                c.set_block(x, y_1f, z, MAT['frame_dark'])
            else:
                c.set_block(x, y_1f, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    c.fill(sx1, y_1f + 1, sz1, sx2, y_roof - 1, sz2, MAT['wall_white'])
    c.fill(sx1 + 1, y_1f + 1, sz1 + 1, sx2 - 1, y_roof - 1, sz2 - 1, 'minecraft:air')

    build_curtain_wall(c, sx1 + 2, y_1f + 1, sz1, sx2 - 2, y_roof - 1, sz1,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=5)
    build_curtain_wall(c, sx1 + 2, y_1f + 1, sz2, sx2 - 2, y_roof - 1, sz2,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=5)
    build_curtain_wall(c, sx2, y_1f + 1, sz1 + 2, sx2, y_roof - 1, sz2 - 2,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=5)
    build_curtain_wall(c, sx1, y_1f + 1, sz1 + 2, sx1, y_roof - 1, sz2 - 2,
                       MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=5)

    c.fill(sx2, y_1f + 1, 72, sx2, y_1f + 4, 78, MAT['frame_dark'])
    c.fill(sx2, y_1f + 1, 73, sx2, y_1f + 3, 77, 'minecraft:air')
    c.fill(sx2, y_1f + 4, 73, sx2, y_1f + 4, 77, MAT['light_sea'])
    place_double_door(c, -30, y_1f + 1, sz1, 'dark_oak', 'south', 'true')

    build_illuminated_carpet_rug(c, -43, y_1f, 78, -14, 82, MAT['carpet_red'], MAT['carpet_white'], light_mat=MAT['light_ochre'])

    _build_voxel_supercar(c, -40, y_1f, 70, 'south',
                          MAT['red_concrete'], 'smooth_quartz', MAT['slab_quartz_b'],
                          MAT['carpet_red'], MAT['wall_quartz'], has_gt_wing=True)

    _build_voxel_supercar(c, -30, y_1f, 70, 'south',
                          MAT['yellow_concrete'], 'polished_deepslate', MAT['slab_deep_b'],
                          MAT['carpet_yellow'], MAT['wall_black'], has_gt_wing=False)

    _build_voxel_supercar(c, -20, y_1f, 70, 'south',
                          MAT['cyan_concrete'], 'smooth_quartz', MAT['slab_quartz_b'],
                          MAT['carpet_cyan'], MAT['pool_shallow_2'], has_gt_wing=True)

    _build_voxel_supercar(c, -40, y_1f, 90, 'north',
                          MAT['orange_concrete'], 'polished_deepslate', MAT['slab_deep_b'],
                          MAT['carpet_orange'], MAT['wall_black'], has_gt_wing=True)

    _build_voxel_supercar(c, -30, y_1f, 90, 'north',
                          MAT['green_concrete'], 'smooth_quartz', MAT['slab_quartz_b'],
                          MAT['carpet_green'], MAT['lime_concrete'], has_gt_wing=True)

    _build_voxel_supercar(c, -20, y_1f, 90, 'north',
                          MAT['wall_black'], 'polished_deepslate', MAT['slab_deep_b'],
                          MAT['carpet_black'], MAT['gold_block'], has_gt_wing=False)

    for z in range(66, 95, 2):
        if 77 <= z <= 83:
            continue
        c.set_block(sx1 + 1, y_1f + 1, z, MAT['wall_black'])
        c.set_block(sx1 + 1, y_1f + 2, z, MAT['wall_black'])
        c.set_block(sx1 + 1, y_1f + 3, z, MAT['slab_deep_b'])
    c.set_block(sx1 + 1, y_1f + 1, 79, 'minecraft:smithing_table')
    c.set_block(sx1 + 1, y_1f + 1, 80, MAT['gold_block'])
    c.set_block(sx1 + 1, y_1f + 2, 80, MAT['end_rod_up'])
    c.set_block(sx1 + 1, y_1f + 1, 81, 'minecraft:crafting_table')

    for px, pz in [(-46, 64), (-14, 64), (-46, 96), (-14, 96)]:
        build_indoor_planter(c, px, y_1f, pz, tall=True)
    for fx, fz in [(-35, 80), (-25, 80)]:
        build_floor_lamp(c, fx, y_1f, fz, 'modern')

    build_flat_roof_and_eaves(c, sx1, y_roof, sz1, sx2, sz2, overhang=2,
                              roof_mat=MAT['wall_white'], soffit_mat=MAT['wood_dark'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)
    for sky_x in (-40, -30, -20):
        for dx in range(-2, 3):
            for dz in range(-6, 7):
                if abs(dx) == 2 or abs(dz) == 6:
                    c.set_block(sky_x + dx, y_roof, 80 + dz, MAT['light_sea'])
                    c.set_block(sky_x + dx, y_roof + 1, 80 + dz, MAT['wall_quartz'])
                else:
                    c.set_block(sky_x + dx, y_roof, 80 + dz, MAT['glass_clear'])
                    c.set_block(sky_x + dx, y_roof + 1, 80 + dz, MAT['glass_clear'])
        build_crystal_chandelier(c, sky_x, y_roof, 80, drop=2, style='grand')

def step13_underwater_michelin_restaurant(c: WorldCanvas):
    """
    Expansion 2: Luxury Underwater Michelin 3-Star Restaurant ("L'Abysse d'Or")
    Extends southward from the Underwater Viewing Tunnel (X = 165..171, Z = -57)
    into X = 158..178, Z = -48..-28, Y = 51..59, surrounded by an illuminated coral reef lagoon.
    """
    rcx, rcz, rrad = 168, -38, 10
    coral_fans = [
        'minecraft:tube_coral_fan[waterlogged=true]',
        'minecraft:brain_coral_fan[waterlogged=true]',
        'minecraft:bubble_coral_fan[waterlogged=true]',
        'minecraft:fire_coral_fan[waterlogged=true]',
        'minecraft:horn_coral_fan[waterlogged=true]',
    ]
    froglights = [MAT['light_ochre'], MAT['light_pearl'], MAT['light_verdant']]

    for z in range(-56, -23):
        for x in range(150, 187):
            for wy in range(51, 63):
                c.set_block(x, wy, z, MAT['water'])

            if (x + z) % 4 == 0:
                c.set_block(x, 50, z, MAT['light_sea'])
            elif (x * 3 + z * 5) % 5 == 0:
                c.set_block(x, 50, z, froglights[(x + z) % 3])
            elif (x + z) % 2 == 0:
                c.set_block(x, 50, z, MAT['pool_deep_1'])
            else:
                c.set_block(x, 50, z, 'minecraft:sand')

            in_south_tunnel = (165 <= x <= 171 and -57 <= z <= -48)
            dx_r, dz_r = x - rcx, z - rcz
            oct_r = max(abs(dx_r), abs(dz_r), (abs(dx_r) + abs(dz_r) + 1) * 5 // 7)
            if in_south_tunnel or oct_r <= rrad:
                continue

            near_dome = (rrad + 1 <= oct_r <= rrad + 5) or (161 <= x <= 175 and -56 <= z <= -49)
            if near_dome:
                mound_h = 2 + ((x * 5 + z * 3) % 5)
                coral_mat = CORAL_BLOCKS[(x + z * 2) % len(CORAL_BLOCKS)]
                if (x + z) % 3 == 0:
                    for cy in range(51, 51 + mound_h):
                        is_top_glow = (cy == 51 + mound_h - 1 and (x + z) % 2 == 0)
                        c.set_block(x, cy, z, froglights[(x + cy) % 3] if is_top_glow else coral_mat)
                    top_y = 51 + mound_h
                    if top_y <= 60:
                        c.set_block(x, top_y, z, MAT['sea_pickle_4'])
                elif (x + z) % 3 == 1:
                    c.set_block(x, 51, z, MAT['light_sea'])
                    c.set_block(x, 52, z, coral_fans[(x + z) % len(coral_fans)])
                else:
                    kelp_top = 57 + ((x + z) % 4)
                    for ky in range(51, kelp_top):
                        c.set_block(x, ky, z, 'minecraft:kelp_plant')
                    c.set_block(x, kelp_top, z, 'minecraft:kelp[age=20]')

            if (x % 3 == 0 and z % 3 == 0) and oct_r >= rrad + 1:
                for ly_w in (53, 56, 59):
                    if c.get_block_name(x, ly_w, z) == 'minecraft:water':
                        c.set_block(x, ly_w, z, MAT['light_water'])

    for jx, jz, jy, jmat, fl_mat in [
        (154, -44, 56, MAT['glass_magenta'], MAT['light_pearl']),
        (153, -34, 57, MAT['glass_cyan'], MAT['light_verdant']),
        (159, -26, 56, MAT['glass_yellow'], MAT['light_ochre']),
        (177, -26, 57, MAT['glass_magenta'], MAT['light_pearl']),
        (183, -34, 56, MAT['glass_cyan'], MAT['light_verdant']),
        (182, -44, 57, MAT['glass_yellow'], MAT['light_ochre']),
    ]:
        c.set_block(jx, jy, jz, fl_mat)
        for dx_j, dz_j in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
            c.set_block(jx + dx_j, jy + 1, jz + dz_j, jmat)
        c.set_block(jx, jy - 1, jz, MAT['end_rod_down'])
        c.set_block(jx, jy + 2, jz, MAT['light_water'])

    for dx in range(-rrad, rrad + 1):
        for dz in range(-rrad, rrad + 1):
            oct_d = max(abs(dx), abs(dz), (abs(dx) + abs(dz) + 1) * 5 // 7)
            x, z = rcx + dx, rcz + dz
            if oct_d > rrad:
                continue

            c.set_block(x, 51, z, MAT['stone_pol_and'])
            if oct_d in (0, 3, 6, 9) and (dx + dz) % 2 == 0:
                c.set_block(x, 52, z, MAT['light_sea'] if oct_d in (0, 6) else MAT['light_ochre'])
            else:
                c.set_block(x, 52, z, MAT['wall_quartz'] if (dx + dz) % 2 == 0 else MAT['pool_deep_1'])

            if oct_d == rrad:
                is_rib = (dx == 0 or dz == 0 or abs(dx) == abs(dz))
                for y in range(53, 57):
                    c.set_block(x, y, z, MAT['frame_dark'] if is_rib else (MAT['glass_clear'] if y in (53, 54, 55) else MAT['glass_cyan']))
                c.set_block(x, 57, z, MAT['light_sea'] if (dx + dz) % 3 == 0 else MAT['frame_dark'])
            else:
                for y in range(53, 58):
                    c.set_block(x, y, z, 'minecraft:air')
                if oct_d == rrad - 1:
                    c.set_block(x, 57, z, MAT['glass_cyan'] if (dx + dz) % 2 == 0 else MAT['light_sea'])
                    c.set_block(x, 58, z, MAT['frame_dark'])
                    top_y = 58
                elif oct_d >= rrad - 3:
                    c.set_block(x, 58, z, MAT['light_sea'] if (dx + dz) % 4 == 0 else MAT['glass_clear'])
                    top_y = 58
                else:
                    c.set_block(x, 58, z, 'minecraft:air')
                    c.set_block(x, 59, z, MAT['light_pearl'] if oct_d in (0, 2, 4) and (dx == 0 or dz == 0) else MAT['glass_clear'])
                    top_y = 59
                for y in range(top_y + 1, 63):
                    c.set_block(x, y, z, MAT['water'])

    for z in range(-58, -47):
        is_rib = (z % 3 == 0)
        for x in range(165, 172):
            c.set_block(x, 51, z, MAT['stone_pol_and'])
            c.set_block(x, 52, z, MAT['light_sea'] if (x in (166, 168, 170) and z % 2 == 0) else MAT['wall_quartz'])
            if 166 <= x <= 170:
                for y in range(53, 56):
                    c.set_block(x, y, z, 'minecraft:air')
                if x == 168:
                    c.set_block(x, 53, z, MAT['carpet_cyan'])
                elif x in (167, 169):
                    c.set_block(x, 53, z, MAT['carpet_white'])
                c.set_block(x, 56, z, MAT['light_sea'] if (is_rib and x == 168) else MAT['glass_clear'])
            else:
                for y in range(53, 56):
                    c.set_block(x, y, z, MAT['light_sea'] if (is_rib and y == 55) else MAT['glass_clear'])
                c.set_block(x, 56, z, MAT['glass_cyan'])
            for y in range(57, 63):
                if z <= -49:
                    c.set_block(x, y, z, MAT['water'])

    for x in range(166, 171):
        for z in range(-40, -35):
            if x in (166, 170) or z in (-40, -36):
                c.set_block(x, 52, z, MAT['light_ochre'])
                c.set_block(x, 53, z, MAT['wall_quartz'])
                c.set_block(x, 54, z, MAT['carpet_white'])
    c.set_block(168, 53, -38, MAT['frame_dark'])
    c.set_block(168, 54, -38, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    place_smoker(c, 167, 53, -38, facing='north', lit='true')
    place_brewing_stand(c, 169, 54, -38)
    c.set_block(168, 54, -40, 'minecraft:flower_pot')
    c.set_block(168, 54, -36, 'minecraft:flower_pot')

    for sx_s in (166, 168, 170):
        c.set_block(sx_s, 53, -41, stair('dark_oak', 'south', 'bottom'))
        c.set_block(sx_s, 53, -35, stair('dark_oak', 'north', 'bottom'))

    for cx_l in (166, 168, 170):
        c.set_block(cx_l, 58, -38, MAT['chain_y'])
        c.set_block(cx_l, 57, -38, MAT['light_ochre'] if cx_l == 168 else MAT['light_sea'])
        c.set_block(cx_l, 56, -38, MAT['end_rod_down'])

    dining_tables = [
        (161, -42), (161, -34),
        (175, -42), (175, -34),
        (164, -31), (172, -31),
    ]
    for tx, tz in dining_tables:
        c.set_block(tx, 52, tz, MAT['light_sea'])
        c.set_block(tx, 53, tz, MAT['wall_quartz'])
        c.set_block(tx - 1, 53, tz, MAT['slab_quartz_t'])
        c.set_block(tx + 1, 53, tz, MAT['slab_quartz_t'])
        c.set_block(tx, 54, tz, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
        c.set_block(tx - 1, 54, tz, MAT['carpet_white'])
        c.set_block(tx + 1, 54, tz, MAT['carpet_white'])
        c.set_block(tx, 53, tz - 1, stair('dark_oak', 'south', 'bottom'))
        c.set_block(tx, 53, tz + 1, stair('dark_oak', 'north', 'bottom'))

    for wx in (167, 168, 169):
        place_barrel(c, wx, 53, -29, 'north')
        c.set_block(wx, 54, -29, MAT['light_ochre'] if wx == 168 else 'minecraft:bookshelf')
    c.set_block(168, 53, -31, MAT['note_block'])
    c.set_block(168, 53, -32, stair('polished_deepslate', 'south', 'bottom'))

def step14_vaulted_cellar_cigar_and_art_vault(c: WorldCanvas):
    """
    Expansion 3: Barrel-Vaulted Wine Cellar, Cigar Lounge & Private Art Vault
    (拱顶酒窖、雪茄 lounge 与私人艺术品金库：
     `deepslate_tile` 与 `spruce_planks` 筒形拱顶，沿墙排列 `barrel` 酒架、
     `oxidized_copper_grate` 恒温通风口)
    Footprint: X = 44..94, Z = -41..-22, Y = 60..71
    """
    vx1, vx2, vz1, vz2 = 44, 94, -41, -22
    y_floor = 60
    z_mid = -31

    for x in range(36, 44):
        for z in range(-34, -28):
            if z in (-34, -29):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 3 == 0 else MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 1, z, MAT['pane_black'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
            c.fill(x, Y_BASE + 1 if z not in (-34, -29) else Y_BASE + 2, z, x, Y_BASE + 4, z, 'minecraft:air')

    for x in range(95, 99):
        for z in range(-34, -28):
            c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 4, z, 'minecraft:air')

    c.fill(vx1, y_floor - 1, vz1, vx2, y_floor - 1, vz2, MAT['deepslate_tiles'])
    c.fill(vx1, y_floor, vz1, vx2, Y_BASE + 5, vz2, MAT['deepslate_tiles'])
    c.fill(vx1 + 1, y_floor + 1, vz1 + 1, vx2 - 1, Y_BASE + 4, vz2 - 1, 'minecraft:air')

    for x in range(vx1 + 1, vx2):
        for z in range(vz1 + 1, vz2):
            if z in (vz1 + 2, vz2 - 2) and (x - vx1) % 3 == 0:
                c.set_block(x, y_floor - 1, z, MAT['light_ochre'])
                c.set_block(x, y_floor, z, MAT['copper_grate_ox'])
            elif (x - vx1) % 4 == 0:
                c.set_block(x, y_floor, z, MAT['deepslate_tiles'])
            else:
                c.set_block(x, y_floor, z, MAT['wood_warm'] if (x + z) % 2 == 0 else MAT['wood_dark'])

    for x in range(vx1, vx2 + 1):
        is_rib = ((x - vx1) % 4 == 0 or x in (vx1, vx2, 65, 79))
        full_mat = MAT['deepslate_tiles'] if is_rib else MAT['wood_warm']
        stair_pref = 'deepslate_tile' if is_rib else 'spruce'
        slab_b = MAT['slab_dtile_b'] if is_rib else MAT['slab_spruce_b']
        slab_t = MAT['slab_dtile_t'] if is_rib else MAT['slab_spruce_t']

        if vx1 < x < vx2:
            for z in range(vz1 + 1, vz2):
                dz_center = min(z - (vz1 + 1), (vz2 - 1) - z)
                arch_ceil_y = 64 + min(4, (dz_center + 1) // 2)
                for y in range(y_floor + 1, arch_ceil_y):
                    c.set_block(x, y, z, 'minecraft:air')

        c.fill(x, y_floor + 1, vz1 + 1, x, 64, vz1 + 1, full_mat)
        c.fill(x, y_floor + 1, vz2 - 1, x, 64, vz2 - 1, full_mat)

        c.set_block(x, 65, -39, stair(stair_pref, 'north', 'top'))
        c.set_block(x, 65, -24, stair(stair_pref, 'south', 'top'))
        c.set_block(x, 66, -39, full_mat)
        c.set_block(x, 66, -24, full_mat)

        c.set_block(x, 66, -38, stair(stair_pref, 'north', 'top'))
        c.set_block(x, 66, -25, stair(stair_pref, 'south', 'top'))
        c.set_block(x, 67, -38, full_mat)
        c.set_block(x, 67, -25, full_mat)
        c.set_block(x, 67, -37, stair(stair_pref, 'north', 'top'))
        c.set_block(x, 67, -26, stair(stair_pref, 'south', 'top'))
        c.set_block(x, 68, -37, full_mat)
        c.set_block(x, 68, -26, full_mat)

        c.set_block(x, 68, -36, slab_t)
        c.set_block(x, 68, -27, slab_t)
        c.set_block(x, 68, -35, stair(stair_pref, 'north', 'top'))
        c.set_block(x, 68, -28, stair(stair_pref, 'south', 'top'))
        c.set_block(x, 69, -36, full_mat)
        c.set_block(x, 69, -27, full_mat)
        c.set_block(x, 69, -35, full_mat)
        c.set_block(x, 69, -28, full_mat)

        for z_crown in range(-34, -28):
            if not is_rib and z_crown in (-33, -30) and (x % 2 == 0):
                c.set_block(x, 69, z_crown, MAT['copper_grate_ox'])
                c.set_block(x, 70, z_crown, MAT['light_ochre'] if x % 4 == 2 else MAT['light_sea'])
            else:
                c.set_block(x, 69, z_crown, full_mat)
                c.set_block(x, 70, z_crown, slab_b)

        for z_ext in (vz1, vz2):
            c.fill(x, Y_BASE, z_ext, x, 67, z_ext, MAT['deepslate_tiles'] if is_rib else MAT['wall_white'])
            c.set_block(x, 68, z_ext, MAT['slab_dtile_b'] if is_rib else MAT['slab_quartz_b'])

    c.fill(vx1, Y_BASE + 1, -33, vx1, Y_BASE + 3, -30, 'minecraft:air')
    for step_i, sx in enumerate(range(45, 49)):
        sy_step = Y_BASE - step_i
        for z_s in range(-33, -29):
            c.fill(sx, y_floor, z_s, sx, sy_step - 1, z_s, MAT['deepslate_tiles'])
            c.set_block(sx, sy_step, z_s, stair('deepslate_tile', 'west', 'bottom'))
            c.fill(sx, sy_step + 1, z_s, sx, 67, z_s, 'minecraft:air')

    c.fill(vx2, Y_BASE + 1, -33, vx2, Y_BASE + 3, -30, 'minecraft:air')
    for step_i, sx in enumerate(range(93, 89, -1)):
        sy_step = Y_BASE - step_i
        for z_s in range(-33, -29):
            c.fill(sx, y_floor, z_s, sx, sy_step - 1, z_s, MAT['deepslate_tiles'])
            c.set_block(sx, sy_step, z_s, stair('deepslate_tile', 'east', 'bottom'))
            c.fill(sx, sy_step + 1, z_s, sx, 67, z_s, 'minecraft:air')

    for x in range(48, 65):
        is_post = ((x - 48) % 4 == 0)
        for z_wall, face_dir in [(-39, 'south'), (-24, 'north')]:
            if is_post:
                c.fill(x, y_floor + 1, z_wall, x, y_floor + 3, z_wall, MAT['beam_spruce_y'])
                c.set_block(x, y_floor + 4, z_wall, MAT['copper_grate_ox'])
            else:
                for wy in (y_floor + 1, y_floor + 2, y_floor + 3):
                    place_barrel(c, x, wy, z_wall, facing=face_dir)
                c.set_block(x, y_floor + 4, z_wall, MAT['copper_grate_ox'] if x % 2 == 0 else MAT['slab_spruce_b'])
                c.set_block(x, y_floor + 4, z_wall + (-1 if z_wall == -39 else 1), MAT['light_ochre'])

    for rx in (51, 61):
        for z_r in (-37, -36, -27, -26):
            place_barrel(c, rx, y_floor + 1, z_r, facing='east')
            place_barrel(c, rx, y_floor + 2, z_r, facing='west')
            c.set_block(rx, y_floor + 3, z_r, MAT['slab_spruce_b'])

    build_illuminated_carpet_rug(c, 50, y_floor, -34, 63, -29, MAT['carpet_red'], MAT['carpet_brown'], light_mat=MAT['light_ochre'])
    for x in range(54, 59):
        c.set_block(x, y_floor + 1, -32, MAT['wood_warm'] if x in (54, 58) else MAT['slab_spruce_t'])
        c.set_block(x, y_floor + 1, -31, MAT['wood_warm'] if x in (54, 58) else MAT['slab_spruce_t'])
        if x in (54, 56, 58):
            c.set_block(x, y_floor + 1, -34, stair('spruce', 'south', 'bottom'))
            c.set_block(x, y_floor + 1, -29, stair('spruce', 'north', 'bottom'))
    place_brewing_stand(c, 55, y_floor + 2, -32)
    c.set_block(56, y_floor + 2, -32, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    c.set_block(57, y_floor + 2, -31, 'minecraft:flower_pot')
    build_crystal_chandelier(c, 56, 68, -32, drop=2, style='grand')

    for z in range(-39, -23):
        for y in range(y_floor + 1, 66):
            if -33 <= z <= -30 and y <= y_floor + 3:
                c.set_block(65, y, z, 'minecraft:air')
            elif z in (-34, -29) or y == y_floor + 4:
                c.set_block(65, y, z, MAT['deepslate_tiles'])
            else:
                c.set_block(65, y, z, MAT['copper_grate_ox'] if y in (y_floor + 2, y_floor + 3) else MAT['wood_warm'])

    build_illuminated_carpet_rug(c, 67, y_floor, -35, 77, -28, MAT['carpet_brown'], MAT['carpet_orange'], light_mat=MAT['light_ochre'])

    for x in range(66, 71):
        c.fill(x, y_floor + 1, -36, x, y_floor + 3, -36, MAT['glass_tinted'] if x not in (66, 68, 70) else MAT['beam_spruce_y'])
        c.set_block(x, y_floor + 4, -36, MAT['copper_grate_ox'])
    place_door(c, 68, y_floor + 1, -36, 'spruce', 'south', 'left', 'true')
    for x in range(67, 70):
        place_barrel(c, x, y_floor + 1, -39, facing='south')
        place_barrel(c, x, y_floor + 2, -39, facing='south')
        c.set_block(x, y_floor + 3, -39, MAT['copper_grate_ox'])

    c.fill(72, y_floor + 1, -39, 76, y_floor + 4, -38, MAT['deepslate_tiles'])
    c.fill(73, y_floor + 1, -38, 75, y_floor + 2, -38, 'minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]')
    c.fill(73, y_floor + 1, -37, 75, y_floor + 2, -37, MAT['iron_bars'])
    c.set_block(74, y_floor + 3, -38, MAT['copper_grate_ox'])

    for x in range(67, 78):
        if x % 2 == 0:
            place_barrel(c, x, y_floor + 1, -24, facing='north')
            place_barrel(c, x, y_floor + 2, -24, facing='north')
            c.set_block(x, y_floor + 3, -24, MAT['copper_grate_ox'])
        else:
            c.fill(x, y_floor + 1, -24, x, y_floor + 2, -24, 'minecraft:bookshelf')
            c.set_block(x, y_floor + 3, -24, MAT['light_ochre'])
    for x in range(70, 76):
        c.set_block(x, y_floor + 1, -26, MAT['wood_dark'])
        c.set_block(x, y_floor + 2, -26, MAT['carpet_brown'])
    place_brewing_stand(c, 72, y_floor + 2, -26)

    for x in range(71, 75):
        c.set_block(x, y_floor + 1, -34, stair('dark_oak', 'south', 'bottom'))
        c.set_block(x, y_floor + 1, -29, stair('dark_oak', 'north', 'bottom'))
    c.fill(72, y_floor + 1, -32, 73, y_floor + 1, -31, MAT['slab_dark_t'])
    c.set_block(72, y_floor + 2, -32, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    c.set_block(73, y_floor + 2, -31, 'minecraft:flower_pot')
    build_crystal_chandelier(c, 72, 68, -32, drop=2, style='pearl')

    for z in range(-39, -23):
        for y in range(y_floor + 1, 66):
            if -32 <= z <= -31 and y <= y_floor + 3:
                c.set_block(79, y, z, 'minecraft:air')
            elif -33 <= z <= -30 and y <= y_floor + 4:
                c.set_block(79, y, z, 'minecraft:iron_block' if y < y_floor + 4 else MAT['chiseled_deepslate'])
            elif z in (-36, -27) and y in (y_floor + 2, y_floor + 3):
                c.set_block(79, y, z, MAT['copper_grate_ox'])
            else:
                c.set_block(79, y, z, MAT['deepslate_tiles'])

    build_illuminated_carpet_rug(c, 81, y_floor, -34, 89, -29, MAT['carpet_black'], MAT['carpet_white'], light_mat=MAT['light_sea'])

    art_pedestals = [
        (82, -36, MAT['gold_block'], MAT['end_rod_up']),
        (82, -27, MAT['amethyst_block'], MAT['light_pearl']),
        (86, -36, MAT['oxidized_copper'], MAT['copper_grate_ox']),
        (86, -27, MAT['diamond_block'], MAT['emerald_block']),
    ]
    for ax, az, base_art, top_art in art_pedestals:
        c.set_block(ax, y_floor, az, MAT['light_sea'])
        c.set_block(ax, y_floor + 1, az, MAT['wall_quartz'])
        c.set_block(ax, y_floor + 2, az, base_art)
        c.set_block(ax, y_floor + 3, az, top_art)
        c.set_block(ax, y_floor + 4, az, MAT['slab_quartz_b'])
        for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            c.set_block(ax + dx, y_floor + 2, az + dz, MAT['pane_clear'])
            c.set_block(ax + dx, y_floor + 3, az + dz, MAT['pane_clear'])

    for x in range(81, 89):
        for z_w, face_d in [(-39, 'south'), (-24, 'north')]:
            if x in (83, 84, 85):
                c.set_block(x, y_floor + 1, z_w, MAT['chiseled_deepslate'])
                c.set_block(x, y_floor + 2, z_w, MAT['gold_block'] if x == 84 else MAT['amethyst_block'])
                c.set_block(x, y_floor + 3, z_w, MAT['light_pearl'] if x == 84 else MAT['emerald_block'])
                c.set_block(x, y_floor + 4, z_w, MAT['copper_grate_ox'])
            else:
                place_barrel(c, x, y_floor + 1, z_w, facing=face_d)
                c.set_block(x, y_floor + 2, z_w, MAT['gold_block'] if x % 2 == 0 else MAT['copper_grate_ox'])
                c.set_block(x, y_floor + 3, z_w, MAT['copper_grate_ox'])

    build_crystal_chandelier(c, 85, 68, -32, drop=2, style='grand')
