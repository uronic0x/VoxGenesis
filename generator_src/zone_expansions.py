"""
zone_expansions.py — Southeast Helipad, North Championship Golf Course, and
Relocated West High-End Agri-Tech Farm (shifted farther from the Villa Area)
===========================================================================
"""

import math
from config import Y_BASE, MAT, SOFT_FLOWERS
from world_canvas import WorldCanvas
from arch_lib import (
    stair, trapdoor,
    place_barrel, place_beehive, place_lectern, place_tall_flower, place_door, place_double_door,
    build_recessed_ceiling_grid, build_crystal_chandelier, build_illuminated_carpet_rug,
    build_floor_lamp, build_curtain_wall, build_flat_roof_and_eaves,
    build_straight_stairs, build_vine_arch, build_lamppost,
    build_fountain, build_hedgerow_line, build_custom_tree,
    build_outdoor_sofa, build_outdoor_bar,
    build_executive_helicopter, build_windsock_tower,
    build_golf_flag_and_cup, build_golf_cart, build_golf_gazebo, build_arched_canal_bridge,
    build_smart_greenhouse, build_irrigation_boom, build_cylindrical_silo,
    build_modern_windmill_tower, build_farm_tractor
)

def step7_helipad_and_aviation_complex(c: WorldCanvas):
    """
    7. EXPANSION 1: EXECUTIVE WATERFRONT HELIPAD & VIP AVIATION TERMINAL (Southeast Bay, X in [78, 158], Z in [28, 96])
    """

    for x in range(80, 113):
        for z in range(28, 97):
            if x == 112:
                c.fill(x, 60, z, x, Y_BASE, z, MAT['stone_pol_and'])
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 1, z, MAT['pane_black'])
                if z % 6 == 0:
                    c.set_block(x, Y_BASE + 1, z, MAT['wall_quartz'])
                    c.set_block(x, Y_BASE + 2, z, MAT['light_ochre'])
                    c.set_block(x, Y_BASE + 3, z, MAT['slab_quartz_b'])
            elif (x - 80) % 4 == 0 or (z - 28) % 4 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    for z in range(18, 29):
        for x in range(89, 94):
            c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
        if z % 6 == 0:
            build_lamppost(c, 88, Y_BASE + 1, z, style='courtyard')
            build_lamppost(c, 94, Y_BASE + 1, z, style='courtyard')

    tx1, tx2, tz1, tz2, ty_top = 84, 102, 56, 84, Y_BASE + 6
    c.fill(tx1, Y_BASE, tz1, tx2, Y_BASE, tz2, MAT['wood_dark'])
    c.fill(tx1, Y_BASE + 1, tz1, tx2, ty_top - 1, tz2, MAT['wall_white'])
    c.fill(tx1 + 1, Y_BASE + 1, tz1 + 1, tx2 - 1, ty_top - 1, tz2 - 1, 'minecraft:air')
    build_curtain_wall(c, tx2, Y_BASE + 1, tz1 + 2, tx2, ty_top - 1, tz2 - 2,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, tx1, Y_BASE + 1, tz1 + 2, tx1, ty_top - 1, tz2 - 2,
                       MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, tx1 + 2, Y_BASE + 1, tz2, tx2 - 2, ty_top - 1, tz2,
                       MAT['glass_black'], MAT['glass_gray'], MAT['frame_dark'], bay_width=4)
    place_double_door(c, tx1, Y_BASE + 1, 68, 'dark_oak', 'east', 'true')
    place_double_door(c, tx2, Y_BASE + 1, 68, 'dark_oak', 'west', 'true')

    build_illuminated_carpet_rug(c, tx1 + 3, Y_BASE, tz1 + 3, tx2 - 3, tz2 - 3, MAT['carpet_white'], MAT['carpet_lgray'])
    build_outdoor_sofa(c, tx1 + 5, Y_BASE, 62, length=6, facing='south')
    build_outdoor_sofa(c, tx1 + 5, Y_BASE, 75, length=6, facing='north')
    build_outdoor_bar(c, tx1 + 4, Y_BASE, 80, length=6)
    c.fill(tx1 + 4, Y_BASE + 2, tz1 + 1, tx2 - 4, Y_BASE + 4, tz1 + 1, MAT['wall_black'])
    c.set_block(tx1 + 6, Y_BASE + 3, tz1 + 1, MAT['light_sea'])
    c.set_block(tx1 + 9, Y_BASE + 3, tz1 + 1, MAT['light_verdant'])
    c.set_block(tx1 + 12, Y_BASE + 3, tz1 + 1, MAT['light_ochre'])
    place_lectern(c, tx1 + 9, Y_BASE + 1, tz1 + 2, 'south')
    build_floor_lamp(c, tx1 + 2, Y_BASE, tz1 + 2, 'modern')
    build_floor_lamp(c, tx2 - 2, Y_BASE, tz1 + 2, 'modern')
    build_floor_lamp(c, tx2 - 2, Y_BASE, tz2 - 2, 'modern')
    build_flat_roof_and_eaves(c, tx1, ty_top, tz1, tx2, tz2, overhang=2, hidden_lights=True)
    build_crystal_chandelier(c, (tx1 + tx2) // 2, ty_top, 64, drop=2, style='grand')
    build_crystal_chandelier(c, (tx1 + tx2) // 2, ty_top, 74, drop=2, style='grand')

    c.fill(88, Y_BASE, 44, 98, Y_BASE + 1, 54, MAT['stone_pol_and'])
    for y in range(Y_BASE + 1, Y_BASE + 14):
        c.fill(90, y, 46, 96, y, 52, MAT['wall_white'])
        c.fill(91, y, 47, 95, y, 51, 'minecraft:air')
        if (y - Y_BASE) % 3 == 0:
            c.fill(90, y, 52, 96, y, 52, MAT['glass_black'])
            c.set_block(93, y, 49, MAT['light_ochre'])
    c.fill(88, Y_BASE + 14, 44, 98, Y_BASE + 14, 54, MAT['wood_dark'])
    build_recessed_ceiling_grid(c, 89, Y_BASE + 14, 45, 97, 53, step_x=3, step_z=3, light_mat=MAT['light_ochre'])
    for y in range(Y_BASE + 15, Y_BASE + 19):
        for x in range(88, 99):
            for z in range(44, 55):
                if x in (88, 98) or z in (44, 54):
                    if (x in (88, 98) and z in (44, 54)):
                        c.set_block(x, y, z, MAT['frame_dark'])
                    else:
                        c.set_block(x, y, z, MAT['glass_black'] if y < Y_BASE + 18 else MAT['glass_clear'])
    place_lectern(c, 95, Y_BASE + 15, 48, 'east')
    place_lectern(c, 95, Y_BASE + 15, 50, 'east')
    c.set_block(93, Y_BASE + 15, 49, MAT['light_sea'])
    build_flat_roof_and_eaves(c, 88, Y_BASE + 19, 44, 98, 54, overhang=1, hidden_lights=True)
    c.fill(92, Y_BASE + 21, 48, 94, Y_BASE + 22, 50, MAT['stone_pol_and'])
    c.fill(91, Y_BASE + 23, 49, 95, Y_BASE + 24, 49, MAT['wall_quartz'])
    c.set_block(90, Y_BASE + 23, 48, MAT['iron_bars'])
    c.set_block(96, Y_BASE + 23, 48, MAT['iron_bars'])
    c.set_block(93, Y_BASE + 25, 49, MAT['light_shroom'])
    c.set_block(93, Y_BASE + 26, 49, MAT['glass_red'])
    c.set_block(93, Y_BASE + 27, 49, MAT['end_rod_up'])

    build_windsock_tower(c, 108, Y_BASE, 44)

    hcx, hcz, hy_pad, h_rad = 130, 68, Y_BASE + 2, 17

    for x in range(103, hcx - h_rad + 2):
        y_br = Y_BASE + (1 if x >= 106 else 0) + (1 if x >= 109 else 0)
        for z in range(64, 73):
            if z in (64, 72):
                c.set_block(x, y_br, z, MAT['wall_quartz'])
                c.set_block(x, y_br + 1, z, MAT['pane_black'])
                if x % 3 == 0:
                    c.set_block(x, y_br, z, MAT['light_ochre'])
            else:
                c.set_block(x, y_br, z, MAT['stone_pol_and'] if (x + z) % 2 == 0 else MAT['wall_gray'])

    for px in (hcx - 12, hcx, hcx + 12):
        for pz in (hcz - 12, hcz, hcz + 12):
            if abs(px - hcx) + abs(pz - hcz) <= 20:
                c.fill(px - 1, 58, pz - 1, px + 1, hy_pad - 2, pz + 1, MAT['frame_dark'])
                c.fill(px - 1, 62, pz - 1, px + 1, 63, pz + 1, MAT['wall_white'])
                c.set_block(px, 63, pz - 2, MAT['light_sea'])
                c.set_block(px, 63, pz + 2, MAT['light_sea'])

    for dx in range(-h_rad - 1, h_rad + 2):
        for dz in range(-h_rad - 1, h_rad + 2):
            oct_d = max(abs(dx), abs(dz), (abs(dx) + abs(dz) + 1) * 5 // 7)
            x, z = hcx + dx, hcz + dz
            if oct_d == h_rad + 1:
                c.set_block(x, hy_pad - 1, z, MAT['iron_bars'])
            elif oct_d == h_rad:
                c.set_block(x, hy_pad - 1, z, MAT['wall_white'])
                if (dx + dz) % 3 == 0:
                    c.set_block(x, hy_pad - 1, z, MAT['light_verdant'] if (dx + dz) % 6 == 0 else MAT['light_ochre'])
                    c.set_block(x, hy_pad, z, MAT['glass_green'] if (dx + dz) % 6 == 0 else MAT['glass_yellow'])
                else:
                    c.set_block(x, hy_pad, z, MAT['wall_quartz'])
                    c.set_block(x, hy_pad + 1, z, MAT['slab_quartz_b'] if abs(dz) > 4 or dx > 0 else 'minecraft:air')
            elif oct_d < h_rad:
                c.set_block(x, hy_pad - 1, z, MAT['stone_pol_and'])
                if oct_d == 13:
                    if (dx + dz) % 2 == 0:
                        c.set_block(x, hy_pad - 1, z, MAT['light_ochre'])
                        c.set_block(x, hy_pad, z, MAT['glass_yellow'])
                    else:
                        c.set_block(x, hy_pad, z, MAT['yellow_concrete'])
                elif oct_d == 9 and (abs(dx) <= 4 or abs(dz) <= 4):
                    c.set_block(x, hy_pad, z, MAT['wall_quartz'])
                else:
                    if dx % 6 == 0 and dz % 6 == 0:
                        c.set_block(x, hy_pad - 1, z, MAT['light_sea'])
                        c.set_block(x, hy_pad, z, MAT['glass_gray'])
                    else:
                        c.set_block(x, hy_pad, z, MAT['wall_gray'] if (dx + dz) % 2 == 0 else MAT['frame_dark'])

    for dz in range(-6, 7):
        for dx in (-5, -4, 4, 5):
            c.set_block(hcx + dx, hy_pad - 1, hcz + dz, MAT['light_sea'])
            c.set_block(hcx + dx, hy_pad, hcz + dz, MAT['wall_quartz'] if dz % 2 == 0 else MAT['glass_white'])
    for dx in range(-3, 4):
        for dz in (-1, 0, 1):
            c.set_block(hcx + dx, hy_pad - 1, hcz + dz, MAT['light_sea'])
            c.set_block(hcx + dx, hy_pad, hcz + dz, MAT['wall_quartz'] if dx % 2 == 0 else MAT['glass_white'])

    for ax in range(hcx + h_rad + 3, 166, 4):
        for az in (hcz - 5, hcz, hcz + 5):
            c.fill(ax, 58, az, ax, 64, az, MAT['frame_dark'])
            c.set_block(ax, 65, az, MAT['light_sea'] if az == hcz else MAT['light_verdant'])
            c.set_block(ax, 66, az, MAT['end_rod_up'])

    build_executive_helicopter(c, hcx, hy_pad, hcz)

def step8_golf_course_and_clubhouse(c: WorldCanvas):
    """
    8. EXPANSION 2: CHAMPIONSHIP 3-HOLE GOLF COURSE, DRIVING RANGE & CLUBHOUSE
       (Northeast & Grand North Expansion: X in [-160, 118], Z in [-268, -32])
    """

    for x in range(-90, 137):
        for z in range(-114, -105):
            if z in (-114, -106) or x == -90:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 1, z, MAT['slab_stone_b'])
            else:
                c.set_block(x, Y_BASE - 2, z, MAT['light_sea'] if (x + z) % 4 == 0 else MAT['pool_deep_1'])
                c.set_block(x, Y_BASE - 1, z, MAT['water'])
                c.set_block(x, Y_BASE, z, MAT['water'])
    build_arched_canal_bridge(c, -55, Y_BASE, -110, width=5, span=12, axis='z')
    build_arched_canal_bridge(c, 0, Y_BASE, -110, width=7, span=12, axis='z')
    build_arched_canal_bridge(c, 62, Y_BASE, -110, width=5, span=12, axis='z')
    build_arched_canal_bridge(c, 100, Y_BASE, -110, width=7, span=12, axis='z')

    for x in range(44, 96):
        for z in range(-92, -38):
            if (x - 44) % 4 == 0 or (z - (-92)) % 4 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['wall_quartz'])

    cx1, cx2, cz1, cz2 = 46, 66, -76, -44
    y_c2f, y_croof = Y_BASE + 6, Y_BASE + 12
    c.fill(cx1, Y_BASE, cz1, cx2, Y_BASE, cz2, MAT['wood_dark'])
    c.fill(cx1, Y_BASE + 1, cz1, cx2, y_c2f - 1, cz2, MAT['wall_white'])
    c.fill(cx1 + 1, Y_BASE + 1, cz1 + 1, cx2 - 1, y_c2f - 1, cz2 - 1, 'minecraft:air')
    build_curtain_wall(c, cx1, Y_BASE + 1, cz1 + 2, cx1, y_c2f - 1, cz2 - 2, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, cx2, Y_BASE + 1, cz1 + 2, cx2, y_c2f - 1, cz2 - 2, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, cx1 + 2, Y_BASE + 1, cz1, cx2 - 2, y_c2f - 1, cz1, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    place_double_door(c, cx1, Y_BASE + 1, -60, 'dark_oak', 'east', 'true')
    place_double_door(c, 56, Y_BASE + 1, cz1, 'dark_oak', 'south', 'true')

    build_recessed_ceiling_grid(c, cx1 + 2, y_c2f, cz1 + 2, cx2 - 2, cz2 - 2, step_x=4, step_z=4, light_mat=MAT['light_ochre'])
    build_illuminated_carpet_rug(c, 49, Y_BASE, -55, 63, -47, MAT['carpet_green'], MAT['moss_carpet'])
    c.set_block(56, Y_BASE, -51, MAT['light_sea'])
    c.set_block(56, Y_BASE + 1, -51, MAT['end_rod_up'])
    build_illuminated_carpet_rug(c, 49, Y_BASE, -73, 63, -60, MAT['carpet_white'], MAT['carpet_lgray'])
    build_outdoor_bar(c, 52, Y_BASE, -71, length=6)
    build_outdoor_sofa(c, 51, Y_BASE, -62, length=6, facing='north')
    build_crystal_chandelier(c, 56, y_c2f, -66, drop=2, style='grand')
    build_crystal_chandelier(c, 56, y_c2f, -51, drop=2, style='pearl')

    c.fill(cx1, y_c2f, cz1, cx2, y_c2f, cz2, MAT['wood_dark'])
    c.fill(cx1, y_c2f + 1, cz1, cx2, y_croof - 1, -54, MAT['wall_white'])
    c.fill(cx1 + 1, y_c2f + 1, cz1 + 1, cx2 - 1, y_croof - 1, -55, 'minecraft:air')
    build_curtain_wall(c, cx1 + 1, y_c2f + 1, cz1, cx2 - 1, y_croof - 1, cz1, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, cx1, y_c2f + 1, cz1 + 1, cx1, y_croof - 1, -55, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    place_door(c, 59, y_c2f + 1, -54, 'dark_oak', 'north', 'left', 'true')
    build_illuminated_carpet_rug(c, 49, y_c2f, -73, 60, -58, MAT['carpet_lgray'], MAT['carpet_white'])
    build_straight_stairs(c, 62, Y_BASE + 1, -58, width=2, height=y_c2f - Y_BASE, direction='north', stair_prefix='smooth_quartz', hidden_lights=True)
    build_outdoor_sofa(c, 51, y_c2f, -68, length=6, facing='north')
    build_flat_roof_and_eaves(c, cx1, y_croof, cz1, cx2, -54, overhang=1, hidden_lights=True)
    build_crystal_chandelier(c, 55, y_croof, -65, drop=2, style='grand')
    for x in range(cx1, cx2 + 1):
        c.set_block(x, y_c2f, cz2, MAT['wall_quartz'])
        c.set_block(x, y_c2f + 1, cz2, MAT['pane_black'])
    for z in range(-54, cz2 + 1):
        c.set_block(cx1, y_c2f, z, MAT['wall_quartz'])
        c.set_block(cx1, y_c2f + 1, z, MAT['pane_black'])
        c.set_block(cx2, y_c2f, z, MAT['wall_quartz'])
        c.set_block(cx2, y_c2f + 1, z, MAT['pane_black'])

    c.fill(70, Y_BASE, -76, 94, Y_BASE, -64, MAT['stone_pol_and'])
    c.fill(69, Y_BASE + 5, -77, 95, Y_BASE + 5, -63, MAT['wood_dark'])
    c.fill(69, Y_BASE + 6, -77, 95, Y_BASE + 6, -63, MAT['wall_white'])
    for bx in range(71, 94, 4):
        c.fill(bx, Y_BASE + 1, -65, bx, Y_BASE + 4, -65, MAT['wall_white'])
        c.set_block(bx, Y_BASE + 5, -70, MAT['light_ochre'])
        c.fill(bx + 1, Y_BASE, -74, bx + 3, Y_BASE, -71, MAT['light_ochre'])
        c.fill(bx + 1, Y_BASE + 1, -74, bx + 3, Y_BASE + 1, -71, MAT['carpet_green'])
        c.set_block(bx + 1, Y_BASE + 1, -70, 'minecraft:cauldron')
        c.set_block(bx + 2, Y_BASE + 1, -75, MAT['end_rod_up'])
        c.set_block(bx + 2, Y_BASE + 1, -67, stair('smooth_quartz', 'north', 'bottom'))

    for t_idx, tz in enumerate([-135, -165, -195]):
        tx = 86
        for dx in range(-6, 7):
            for dz in range(-6, 7):
                d2 = dx*dx + dz*dz
                if d2 <= 36:
                    c.set_block(tx + dx, Y_BASE, tz + dz, MAT['light_ochre'] if d2 in (0, 16) else MAT['moss_block'])
                    c.set_block(tx + dx, Y_BASE + 1, tz + dz, MAT['carpet_white'] if 12 <= d2 <= 18 else MAT['moss_carpet'])
        build_golf_flag_and_cup(c, tx, Y_BASE, tz, hole_num=t_idx + 1)

    def paint_fairway_segment(ax, az, bx, bz, radius):
        min_x, max_x = int(min(ax, bx) - radius - 4), int(max(ax, bx) + radius + 4)
        min_z, max_z = int(min(az, bz) - radius - 4), int(max(az, bz) + radius + 4)
        abx, abz = bx - ax, bz - az
        ab_len2 = max(1.0, abx*abx + abz*abz)
        for z in range(min_z, max_z + 1):
            for x in range(min_x, max_x + 1):
                t = max(0.0, min(1.0, ((x - ax)*abx + (z - az)*abz) / ab_len2))
                px, pz = ax + t * abx, az + t * abz
                dist = math.hypot(x - px, z - pz)
                if dist <= radius:
                    stripe = ((x + z) // 4) % 2 == 0
                    if x % 9 == 0 and z % 9 == 0:
                        c.set_block(x, Y_BASE, z, MAT['light_ochre'])
                        c.set_block(x, Y_BASE + 1, z, MAT['moss_carpet'] if stripe else MAT['carpet_green'])
                    else:
                        c.set_block(x, Y_BASE, z, MAT['moss_block'] if stripe else MAT['grass_block'])
                        c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
                elif dist <= radius + 3.0:
                    if (x * 5 + z * 3) % 4 == 0:
                        c.set_block(x, Y_BASE + 1, z, 'minecraft:short_grass')

    def build_sand_bunker(cx, cz, rx, rz, angle_deg=0):
        ang = math.radians(angle_deg)
        ca, sa = math.cos(ang), math.sin(ang)
        m = max(rx, rz) + 2
        for dz in range(-m, m + 1):
            for dx in range(-m, m + 1):
                ux = (dx * ca - dz * sa) / rx
                uz = (dx * sa + dz * ca) / rz
                ux_k = ux + 0.25 * (uz * uz - 0.5)
                d2 = ux_k * ux_k + uz * uz
                x, z = cx + dx, cz + dz
                if d2 <= 0.72:
                    c.set_block(x, Y_BASE - 1, z, MAT['light_ochre'] if (dx + dz) % 4 == 0 else 'minecraft:smooth_sandstone')
                    c.set_block(x, Y_BASE, z, 'minecraft:sandstone_slab[type=bottom,waterlogged=false]' if d2 <= 0.35 else 'minecraft:sand')
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
                elif d2 <= 1.0:
                    c.set_block(x, Y_BASE, z, 'minecraft:sand')
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
                elif d2 <= 1.25:
                    c.set_block(x, Y_BASE, z, MAT['moss_block'])

    def build_putting_green(cx, cz, rx, rz, hole_num=1):
        m = max(rx, rz) + 3
        for dz in range(-m, m + 1):
            for dx in range(-m, m + 1):
                d2 = (dx / rx) ** 2 + (dz / rz) ** 2
                x, z = cx + dx, cz + dz
                if d2 <= 1.0:
                    if dx % 4 == 0 and dz % 4 == 0:
                        c.set_block(x, Y_BASE, z, MAT['light_sea'])
                    else:
                        c.set_block(x, Y_BASE, z, MAT['moss_block'])
                    c.set_block(x, Y_BASE + 1, z, MAT['carpet_green'] if d2 <= 0.78 else MAT['moss_carpet'])
                elif d2 <= 1.25:
                    c.set_block(x, Y_BASE, z, MAT['moss_block'])
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
        build_golf_flag_and_cup(c, cx, Y_BASE + 1, cz, hole_num=hole_num)

    def build_tee_box(cx, cz, facing='north'):
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                x, z = cx + dx, cz + dz
                if abs(dx) == 4 or abs(dz) == 4:
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                    c.set_block(x, Y_BASE + 1, z, MAT['slab_quartz_b'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if (dx + dz) % 3 == 0 else MAT['moss_block'])
                    c.set_block(x, Y_BASE + 1, z, MAT['carpet_green'])
        c.set_block(cx - 2, Y_BASE + 2, cz, MAT['lantern_stand'])
        c.set_block(cx + 2, Y_BASE + 2, cz, MAT['lantern_stand'])
        c.set_block(cx - 3, Y_BASE + 2, cz + 2, stair('smooth_quartz', facing, 'bottom'))
        c.set_block(cx - 3, Y_BASE + 2, cz + 3, stair('smooth_quartz', facing, 'bottom'))
        c.set_block(cx + 3, Y_BASE + 2, cz + 2, 'minecraft:water_cauldron[level=3]')

    paint_fairway_segment(62, -128, 46, -182, radius=15)
    paint_fairway_segment(46, -182, 16, -242, radius=14)
    build_tee_box(62, -128, facing='north')
    build_sand_bunker(64, -172, 7, 5, angle_deg=20)
    build_sand_bunker(28, -195, 6, 4, angle_deg=-25)
    build_sand_bunker(32, -238, 6, 5, angle_deg=15)
    build_sand_bunker(0, -244, 5, 4, angle_deg=-15)
    build_putting_green(16, -242, 12, 10, hole_num=1)

    lcx, lcz = 5, -184
    for z in range(-208, -160):
        for x in range(-22, 32):
            ux = (x - lcx) / 25.0
            uz = (z - lcz) / 21.0
            d2 = ux*ux + uz*uz + 0.15 * math.sin(x * 0.2) * math.cos(z * 0.2)
            if d2 <= 0.85:
                c.set_block(x, Y_BASE - 2, z, MAT['light_sea'] if (x + z) % 5 == 0 else MAT['pool_deep_2'])
                c.set_block(x, Y_BASE - 1, z, MAT['water'])
                c.set_block(x, Y_BASE, z, MAT['water'])
                c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
            elif d2 <= 1.0:
                c.set_block(x, Y_BASE - 1, z, MAT['pool_deep_1'])
                c.set_block(x, Y_BASE, z, 'minecraft:sand' if (x + z) % 2 == 0 else MAT['stone_pol_and'])
                c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
    c.fill(lcx - 1, Y_BASE - 1, lcz - 1, lcx + 1, Y_BASE, lcz + 1, MAT['wall_quartz'])
    c.set_block(lcx, Y_BASE + 1, lcz, MAT['light_sea'])
    c.fill(lcx, Y_BASE + 2, lcz, lcx, Y_BASE + 4, lcz, MAT['water'])
    c.set_block(lcx, Y_BASE + 5, lcz, MAT['end_rod_up'])

    paint_fairway_segment(-10, -248, -70, -236, radius=15)
    paint_fairway_segment(-70, -236, -128, -212, radius=14)
    build_tee_box(-10, -248, facing='west')
    build_golf_gazebo(c, -58, Y_BASE, -256)
    build_sand_bunker(-48, -222, 8, 5, angle_deg=10)
    build_sand_bunker(-88, -244, 7, 4, angle_deg=-15)
    build_sand_bunker(-114, -226, 6, 4, angle_deg=30)
    build_sand_bunker(-142, -206, 6, 5, angle_deg=-20)
    build_putting_green(-128, -212, 13, 11, hole_num=2)

    build_tee_box(-128, -172, facing='east')
    paint_fairway_segment(-128, -172, -102, -162, radius=10)
    icx, icz = -62, -154
    for z in range(-184, -125):
        for x in range(-98, -27):
            ux = (x - icx) / 33.0
            uz = (z - icz) / 27.0
            d2 = ux*ux + uz*uz
            if d2 <= 0.92:
                c.set_block(x, Y_BASE - 2, z, MAT['light_sea'] if (x + z) % 4 == 0 else MAT['pool_deep_1'])
                c.set_block(x, Y_BASE - 1, z, MAT['water'])
                c.set_block(x, Y_BASE, z, MAT['water'])
                c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
            elif d2 <= 1.02:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                c.set_block(x, Y_BASE + 1, z, MAT['slab_stone_b'] if (x + z) % 2 == 0 else 'minecraft:air')
    for dz in range(-15, 16):
        for dx in range(-17, 18):
            d2 = (dx / 15.0) ** 2 + (dz / 13.0) ** 2
            x, z = icx + dx, icz + dz
            if d2 <= 1.18:
                c.fill(x, Y_BASE - 2, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
                if d2 > 1.0:
                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                    c.set_block(x, Y_BASE + 1, z, MAT['slab_dark_b'] if (dx + dz) % 2 == 0 else MAT['slab_quartz_b'])
                    if (dx + dz) % 4 == 0:
                        c.set_block(x, Y_BASE, z, MAT['light_ochre'])
    build_putting_green(icx, icz, 12, 10, hole_num=3)
    build_sand_bunker(icx - 8, icz + 5, 4, 3, angle_deg=0)
    build_arched_canal_bridge(c, icx, Y_BASE, -133, width=5, span=14, axis='z')

    cart_waypoints = [
        (62, -92), (62, -122), (76, -145), (60, -195), (28, -252),
        (-8, -256), (-58, -250), (-136, -226), (-136, -172), (-106, -140),
        (-62, -122), (0, -120), (100, -120)
    ]
    for i in range(len(cart_waypoints) - 1):
        x1, z1 = cart_waypoints[i]
        x2, z2 = cart_waypoints[i + 1]
        steps = int(max(abs(x2 - x1), abs(z2 - z1)))
        for s in range(steps + 1):
            t = s / max(1, steps)
            px = int(round(x1 + (x2 - x1) * t))
            pz = int(round(z1 + (z2 - z1) * t))
            for dx in range(-1, 3):
                for dz in range(-1, 3):
                    if dx*dx + dz*dz <= 3:
                        b_cur = c.get_block_name(px + dx, Y_BASE, pz + dz)
                        if b_cur != 'minecraft:water':
                            c.set_block(px + dx, Y_BASE, pz + dz, MAT['stone_smooth'] if (px + dx + pz + dz) % 2 == 0 else MAT['stone_pol_and'])
            if s % 10 == 0:
                build_lamppost(c, px + 3, Y_BASE + 1, pz, style='bollard')

    build_golf_cart(c, 58, Y_BASE, -84, facing='north')
    build_golf_cart(c, 70, Y_BASE, -128, facing='north')
    build_golf_cart(c, -2, Y_BASE, -254, facing='west')
    build_golf_cart(c, -135, Y_BASE, -180, facing='east')

    golf_trees = [
        (36, -142, 'ornamental'), (74, -162, 'birch_mix'), (48, -218, 'oak_mix'),
        (-8, -225, 'ornamental'), (-35, -258, 'birch_mix'), (-95, -258, 'oak_mix'),
        (-102, -202, 'ornamental'), (-148, -192, 'spruce_mix'), (-112, -148, 'ornamental'),
        (-20, -142, 'birch_mix'), (24, -142, 'ornamental'),
    ]
    for idx, (gtx, gtz, gst) in enumerate(golf_trees):
        build_custom_tree(c, gtx, Y_BASE, gtz, height=10, style=gst, seed=900 + idx)

def step9_high_end_agri_farm(c: WorldCanvas):
    """
    9. EXPANSION 3 (RELOCATED FARTHER WEST — Requirement 1):
       HIGH-END AGRI-TECH & ORGANIC ESTATE FARM (X in [-234, -134], Z in [-142, 94])
       Shifted westward by 18-24 blocks so that a 44-block Scenic Woodland & Meandering
       Country Brook Buffer (X = -133..-90) separates the Farm from the Villa Area!
    """
    S = -18

    for z in range(-142, -94):
        for x in range(-163 + S, -158 + S):
            c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else (MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and']))
    for x in range(-163 + S, -104):
        for z in range(-124, -119):
            c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else (MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and']))
    build_fountain(c, -161 + S, Y_BASE, -122, radius=5)
    build_golf_gazebo(c, -190 + S, Y_BASE, -122)
    for ox, oz in [(-180 + S, -136), (-142 + S, -136), (-180 + S, -108), (-142 + S, -108), (-204 + S, -122)]:
        build_custom_tree(c, ox, Y_BASE, oz, height=9, style='ornamental', seed=abs(ox * 17 + oz))

    for z in range(-94, 93):
        for x in range(-163 + S, -158 + S):
            if x in (-163 + S, -159 + S):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
        if z % 12 == 0:
            build_lamppost(c, -164 + S, Y_BASE + 1, z, style='courtyard')
            build_lamppost(c, -158 + S, Y_BASE + 1, z, style='courtyard')

    for bz in (-55, 15, 44, 66):
        for x in range(-214 + S, -116 + S):
            for z in range(bz - 2, bz + 3):
                if abs(z - bz) == 2:
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['wall_quartz'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])

    build_hedgerow_line(c, -216 + S, Y_BASE, -94, -216 + S, 94, height=2, gap_every=8)
    build_hedgerow_line(c, -216 + S, Y_BASE, -94, -116 + S, -94, height=2, gap_every=8)
    build_hedgerow_line(c, -216 + S, Y_BASE, 94, -116 + S, 94, height=2, gap_every=8)
    build_hedgerow_line(c, -116 + S, Y_BASE, -94, -116 + S, -60, height=2, gap_every=8)
    build_hedgerow_line(c, -116 + S, Y_BASE, -50, -116 + S, 10, height=2, gap_every=8)
    build_hedgerow_line(c, -116 + S, Y_BASE, 20, -116 + S, 61, height=2, gap_every=8)
    build_hedgerow_line(c, -116 + S, Y_BASE, 71, -116 + S, 94, height=2, gap_every=8)

    build_smart_greenhouse(c, -156 + S, Y_BASE, -88, -118 + S, -70, variant='hydro_veg')
    build_smart_greenhouse(c, -156 + S, Y_BASE, -64, -118 + S, -46, variant='aeroponic_berry')
    build_smart_greenhouse(c, -156 + S, Y_BASE, -40, -118 + S, -22, variant='orchid_nursery')
    for gz1, gz2 in [(-69, -65), (-45, -41)]:
        for z in range(gz1, gz2 + 1):
            c.fill(-139 + S, Y_BASE, z, -135 + S, Y_BASE, z, MAT['wall_quartz'])
            c.set_block(-137 + S, Y_BASE, z, MAT['light_sea'])
            for y in range(Y_BASE + 1, Y_BASE + 4):
                c.set_block(-139 + S, y, z, MAT['glass_clear'])
                c.set_block(-135 + S, y, z, MAT['glass_clear'])
            c.fill(-139 + S, Y_BASE + 4, z, -135 + S, Y_BASE + 4, z, MAT['slab_quartz_b'])
            c.fill(-138 + S, Y_BASE + 1, gz1 - 1, -136 + S, Y_BASE + 3, gz2 + 1, 'minecraft:air')

    parterre_bands = [
        (-88, -60, [MAT['wheat_full'], MAT['carrots_full']]),
        (-50, -22, [MAT['potatoes_full'], MAT['beetroots_full']]),
        (-18, 10,  [MAT['wheat_full'], MAT['potatoes_full']]),
        (20, 38,   ['melon_pumpkin']),
    ]
    for b_idx, (pz1, pz2, crop_list) in enumerate(parterre_bands):
        for x in range(-214 + S, -165 + S):
            for z in range(pz1, pz2 + 1):
                if x in (-214 + S, -190 + S, -166 + S) or z in (pz1, pz2):
                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                    c.set_block(x, Y_BASE + 1, z, MAT['slab_stone_b'])
                elif (z - pz1) % 6 == 3 or x in (-202 + S, -178 + S):
                    c.set_block(x, Y_BASE - 1, z, MAT['light_sea'] if (x + z) % 2 == 0 else MAT['light_ochre'])
                    c.set_block(x, Y_BASE, z, MAT['water'])
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:lily_pad' if (x + z) % 5 == 0 else 'minecraft:air')
                else:
                    if crop_list[0] == 'melon_pumpkin':
                        c.set_block(x, Y_BASE, z, MAT['moss_block'] if x % 2 == 0 else MAT['farmland_wet'])
                        if (x + z) % 3 == 0:
                            c.set_block(x, Y_BASE + 1, z, MAT['melon_block'] if x % 2 == 0 else MAT['pumpkin_block'])
                        else:
                            c.set_block(x, Y_BASE + 1, z, MAT['carrots_full'])
                    else:
                        c.set_block(x, Y_BASE, z, MAT['farmland_wet'])
                        c.set_block(x, Y_BASE + 1, z, crop_list[((x - (-214 + S)) // 4 + b_idx) % len(crop_list)])

    build_irrigation_boom(c, -214 + S, Y_BASE, -166 + S, -74)
    build_irrigation_boom(c, -214 + S, Y_BASE, -166 + S, -36)
    build_irrigation_boom(c, -214 + S, Y_BASE, -166 + S, -4)

    for vz1, vz2 in [(-16, 10), (20, 40)]:
        for x in range(-156 + S, -135 + S):
            for z in range(vz1, vz2 + 1):
                if (x - (-156 + S)) % 4 == 0:
                    c.set_block(x, Y_BASE, z, MAT['moss_block'])
                    if (z - vz1) % 4 == 0:
                        c.set_block(x, Y_BASE + 1, z, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
                        c.set_block(x, Y_BASE + 2, z, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
                    else:
                        c.set_block(x, Y_BASE + 1, z, 'minecraft:cave_vines[age=22,berries=true]' if z % 2 == 0 else MAT['leaf_azalea'])
                    c.set_block(x, Y_BASE + 3, z, MAT['leaf_fl_azalea'] if (x + z) % 2 == 0 else MAT['leaf_azalea'])
                else:
                    if (x - (-156 + S)) % 4 == 2 and z % 4 == 0:
                        c.set_block(x, Y_BASE, z, MAT['light_ochre'])
                        c.set_block(x, Y_BASE + 1, z, MAT['moss_carpet'])
                    else:
                        c.set_block(x, Y_BASE, z, MAT['grass_block'])

    for ox in (-131 + S, -125 + S, -119 + S):
        for oz in (-12, -4, 4):
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    if abs(dx) == 2 or abs(dz) == 2:
                        c.set_block(ox + dx, Y_BASE + 1, oz + dz, MAT['slab_quartz_b'])
                    else:
                        c.set_block(ox + dx, Y_BASE, oz + dz, MAT['moss_block'])
            build_custom_tree(c, ox, Y_BASE, oz, height=7, style='ornamental' if (ox + oz) % 2 == 0 else 'oak_mix', seed=abs(ox * 31 + oz))
            c.set_block(ox, Y_BASE, oz - 2, MAT['light_ochre'])

    for x in range(-134 + S, -117 + S):
        for z in range(20, 40):
            c.set_block(x, Y_BASE, z, MAT['moss_block'] if (x + z) % 2 == 0 else MAT['grass_block'])
            if (x + z) % 2 == 0:
                c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x * 5 + z * 3) % len(SOFT_FLOWERS)])
    for hx in (-131 + S, -125 + S, -119 + S):
        for hz in (23, 29, 35):
            c.set_block(hx, Y_BASE, hz, MAT['light_ochre'])
            c.set_block(hx, Y_BASE + 1, hz, MAT['wall_quartz'])
            place_beehive(c, hx, Y_BASE + 2, hz, facing='west', honey_level=5)
            c.set_block(hx, Y_BASE + 3, hz, MAT['slab_dark_b'])
            c.set_block(hx, Y_BASE + 2, hz - 1, MAT['lantern_stand'])

    for x in range(-186 + S, -116 + S):
        for z in range(48, 91):
            if (x - (-186 + S)) % 4 == 0 or (z - 48) % 4 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    bx1, bx2, bz1, bz2 = -156 + S, -120 + S, 52, 78
    y_broof = Y_BASE + 8
    c.fill(bx1, Y_BASE, bz1, bx2, Y_BASE, bz2, MAT['wood_warm'])
    c.fill(bx1, Y_BASE + 1, bz1, bx2, y_broof - 1, bz2, MAT['wall_white'])
    c.fill(bx1 + 1, Y_BASE + 1, bz1 + 1, bx2 - 1, y_broof - 1, bz2 - 1, 'minecraft:air')
    for x in range(bx1, bx2 + 1):
        is_frame = (x == bx1 or x == bx2 or (x - bx1) % 6 == 0)
        for z in (bz1, bz2):
            for y in range(Y_BASE + 1, y_broof):
                if is_frame:
                    c.set_block(x, y, z, MAT['beam_dark_y'])
                elif y in (Y_BASE + 1, y_broof - 1):
                    c.set_block(x, y, z, MAT['wood_dark'])
                else:
                    c.set_block(x, y, z, MAT['glass_black'] if (x // 6) % 2 == 0 else MAT['glass_clear'])
    c.fill(bx2, Y_BASE + 1, 62, bx2, Y_BASE + 5, 68, 'minecraft:air')
    c.fill(bx1, Y_BASE + 1, 62, bx1, Y_BASE + 5, 68, 'minecraft:air')
    c.fill(-140 + S, Y_BASE + 1, bz1, -136 + S, Y_BASE + 5, bz1, 'minecraft:air')

    z_ridge = (bz1 + bz2) // 2
    for z in range(bz1 - 1, bz2 + 2):
        dist_r = abs(z - z_ridge)
        dy = int(round((1.0 - dist_r / 14.0) * 5.0))
        ry = y_broof + max(0, dy)
        for x in range(bx1 - 1, bx2 + 2):
            if bx1 <= x <= bx2 and ry > y_broof:
                if x in (bx1, bx2):
                    c.fill(x, y_broof, z, x, ry - 1, z, MAT['wall_white'] if dist_r > 3 else MAT['glass_black'])
                else:
                    c.set_block(x, ry - 1, z, MAT['light_ochre'] if (x % 4 == 0 and z % 3 == 0) else MAT['wood_dark'])
            if dist_r <= 1:
                c.set_block(x, ry, z, MAT['glass_clear'] if x % 2 == 0 else MAT['light_ochre'])
            else:
                c.set_block(x, ry, z, MAT['wall_white'])
                c.set_block(x, ry + 1, z, MAT['slab_quartz_b'])

    for x in range(-153 + S, -141 + S, 3):
        for z in (55, 56, 74, 75):
            place_barrel(c, x, Y_BASE + 1, z, 'up')
            place_barrel(c, x, Y_BASE + 2, z, 'up')
            c.set_block(x, Y_BASE + 3, z, MAT['light_ochre'])
        c.fill(x, Y_BASE + 1, 59, x + 1, Y_BASE + 3, 60, 'minecraft:iron_block')
        c.set_block(x, Y_BASE + 4, 59, MAT['light_sea'])
    c.fill(-154 + S, Y_BASE + 1, 70, -150 + S, Y_BASE + 3, 73, MAT['hay_y'])

    build_illuminated_carpet_rug(c, -138 + S, Y_BASE, 56, -122 + S, 74, MAT['carpet_white'], MAT['carpet_lgray'])
    build_outdoor_bar(c, -135 + S, Y_BASE, 58, length=8)
    c.fill(-135 + S, Y_BASE + 1, 68, -124 + S, Y_BASE + 1, 69, MAT['slab_dark_t'])
    for tx in range(-134 + S, -123 + S, 2):
        c.set_block(tx, Y_BASE, 68, MAT['light_ochre'])
        c.set_block(tx, Y_BASE + 2, 68, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]' if tx % 4 == 0 else 'minecraft:flower_pot')
        c.set_block(tx, Y_BASE + 1, 66, stair('smooth_quartz', 'south', 'bottom'))
        c.set_block(tx, Y_BASE + 1, 71, stair('smooth_quartz', 'north', 'bottom'))
    for cx_ch in (-146 + S, -138 + S, -128 + S):
        build_crystal_chandelier(c, cx_ch, y_broof + 3, 65, drop=3, style='grand')

    build_cylindrical_silo(c, -174 + S, Y_BASE, 56, radius=4, height=18)
    build_cylindrical_silo(c, -174 + S, Y_BASE, 70, radius=4, height=18)
    c.fill(-175 + S, Y_BASE + 16, 60, -173 + S, Y_BASE + 16, 66, MAT['slab_quartz_t'])
    c.fill(-175 + S, Y_BASE + 17, 60, -173 + S, Y_BASE + 17, 66, MAT['iron_bars'])
    build_modern_windmill_tower(c, -174 + S, Y_BASE, 84, height=22)

    for x in range(-202 + S, -186 + S):
        for z in range(58, 75):
            c.set_block(x, Y_BASE, z, MAT['stone_pol_and'] if (x + z) % 2 == 0 else MAT['stone_smooth'])
    build_farm_tractor(c, -194 + S, Y_BASE, 66)

    for z in range(76, 93):
        step_h = 0 if z < 81 else (1 if z < 87 else 2)
        ty = Y_BASE + step_h
        for x in range(-214 + S, -187 + S):
            c.fill(x, Y_BASE, z, x, ty, z, MAT['moss_block'])
            if z in (81, 87) or x in (-214 + S, -188 + S):
                c.set_block(x, ty, z, MAT['light_ochre'] if x % 4 == 0 else MAT['wall_quartz'])
                c.set_block(x, ty + 1, z, MAT['slab_quartz_b'])
            else:
                if step_h == 0:
                    c.set_block(x, ty + 1, z, 'minecraft:allium' if (x + z) % 2 == 0 else 'minecraft:blue_orchid')
                elif step_h == 1:
                    place_tall_flower(c, x, ty + 1, z, 'minecraft:peony' if (x + z) % 2 == 0 else 'minecraft:lilac')
                else:
                    place_tall_flower(c, x, ty + 1, z, 'minecraft:sunflower' if (x + z) % 2 == 0 else 'minecraft:rose_bush')
