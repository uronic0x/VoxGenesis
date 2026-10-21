"""
zone_cruise_ship.py — Expansion 5: The Offshore Luxury Cruise Ship (海上豪华游轮)
=================================================================================
"""

import math
from config import Y_BASE, SEA_LEVEL, MAT
from world_canvas import WorldCanvas
from arch_lib import (
    stair, trapdoor,
    place_bed, place_barrel, place_brewing_stand, place_lectern, place_door,
    build_recessed_ceiling_grid, build_crystal_chandelier, build_illuminated_carpet_rug,
    build_floor_lamp, build_curtain_wall, build_spiral_staircase, build_straight_stairs,
    build_patio_umbrella, build_sun_lounger, build_outdoor_sofa, build_outdoor_bar
)

def _hull_half_width(z, y):
    if y < 60:
        flare = 0.82 + 0.04 * (y - 56)
    elif y < 64:
        flare = 0.96 + 0.01 * (y - 60)
    else:
        flare = 1.0

    if -150 <= z <= -86:
        base_hw = 13.0
    elif z > -86:
        bow_tip_z = -59.0 + (y - 56) * 0.28
        if z > bow_tip_z:
            return -1
        t = max(0.0, (bow_tip_z - z) / max(1.0, (bow_tip_z - (-86.0))))
        base_hw = 13.0 * (t ** 0.68)
    else:
        stern_end_z = -173.0 - max(0, (y - 58)) * 0.25
        if z < stern_end_z:
            return -1
        t = max(0.0, (z - stern_end_z) / max(1.0, (-150.0 - stern_end_z)))
        base_hw = 4.5 + 8.5 * (t ** 0.55)

    return int(round(base_hw * flare))

def step11_luxury_cruise_ship(c: WorldCanvas):
    xc = 199
    z_stern, z_bow = -176, -56

    for y in range(56, 69):
        for z in range(z_stern, z_bow + 1):
            hw = _hull_half_width(z, y)
            if hw < 0:
                continue
            x1, x2 = xc - hw, xc + hw
            for x in range(x1, x2 + 1):
                is_shell = (x in (x1, x2) or z in (z_stern, z_bow) or abs(x - xc) >= hw - 1)
                if y == 56:
                    c.set_block(x, y, z, MAT['frame_dark'])
                elif y == 64:
                    if is_shell:
                        c.set_block(x, y, z, MAT['wall_white'])
                    else:
                        c.set_block(x, y, z, MAT['light_ochre'] if (x % 4 == 0 and z % 4 == 0) else MAT['wood_dark'])
                elif is_shell:
                    if y < 60:
                        c.set_block(x, y, z, MAT['frame_dark'])
                    elif y == 60:
                        c.set_block(x, y, z, MAT['red_concrete'])
                    elif y <= 63:
                        if y == 62 and z % 4 == 0 and -164 <= z <= -70:
                            c.set_block(x, y, z, MAT['light_sea'])
                        else:
                            c.set_block(x, y, z, MAT['wall_dark'])
                    else:
                        if y == 68:
                            c.set_block(x, y, z, MAT['light_ochre'] if z % 3 == 0 else MAT['wall_quartz'])
                        elif y in (66, 67) and z % 4 in (1, 2) and -166 <= z <= -72:
                            c.set_block(x, y, z, MAT['glass_black'])
                        else:
                            c.set_block(x, y, z, MAT['wall_white'])
                else:
                    if y == 60 and x % 5 == 0 and z % 5 == 0:
                        c.set_block(x, y, z, MAT['light_sea'])
                    else:
                        c.set_block(x, y, z, 'minecraft:air')

    for z in range(-56, -51):
        rad = 2 if z <= -54 else 1
        for dx in range(-rad, rad + 1):
            for dy in range(57, 61):
                if dx * dx + (dy - 58.5) ** 2 <= (rad + 0.5) ** 2:
                    c.set_block(xc + dx, dy, z, MAT['red_concrete'] if dy >= 59 else MAT['frame_dark'])
    c.set_block(xc, 59, -52, MAT['light_sea'])

    for px in (xc - 5, xc + 5):
        c.fill(px, 58, -176, px, 58, -173, MAT['frame_dark'])
        c.set_block(px, 58, -176, MAT['light_ochre'])
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            c.set_block(px + dx, 58 + dy, -176, MAT['gold_block'])
    c.fill(xc, 56, -176, xc, 60, -174, MAT['frame_dark'])

    c.fill(186, 65, -142, 187, 67, -140, 'minecraft:air')
    build_illuminated_carpet_rug(c, xc - 8, 64, -124, xc + 8, -106, MAT['carpet_white'], MAT['carpet_cyan'])
    build_outdoor_bar(c, xc - 4, 64, -122, length=8)
    build_outdoor_sofa(c, xc - 7, 64, -110, length=5, facing='north')
    build_outdoor_sofa(c, xc + 2, 64, -110, length=5, facing='north')
    build_illuminated_carpet_rug(c, xc - 8, 64, -164, xc + 8, -148, MAT['carpet_red'], MAT['carpet_white'])
    for tx in (xc - 5, xc + 5):
        for tz in (-162, -156, -150):
            c.fill(tx - 1, 65, tz, tx + 1, 65, tz, MAT['slab_quartz_t'])
            c.set_block(tx, 64, tz, MAT['light_ochre'])
            c.set_block(tx, 66, tz, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
            c.set_block(tx - 1, 65, tz - 1, stair('dark_oak', 'north', 'bottom'))
            c.set_block(tx + 1, 65, tz + 1, stair('dark_oak', 'south', 'bottom'))

    for z in range(z_stern + 2, z_bow + 1):
        hw = _hull_half_width(z, 68)
        if hw < 0:
            continue
        for x in range(xc - hw, xc + hw + 1):
            if z > -74:
                if abs(x - xc) == hw or z == z_bow:
                    c.set_block(x, 69, z, MAT['wall_quartz'])
                    c.set_block(x, 70, z, MAT['pane_white'])
                else:
                    c.set_block(x, 69, z, MAT['light_ochre'] if (x == xc and z % 4 == 0) else (MAT['wood_warm'] if (x + z) % 2 == 0 else MAT['wood_dark']))
            else:
                c.set_block(x, 69, z, MAT['light_ochre'] if (x % 4 == 0 and z % 4 == 0) else MAT['wood_dark'])

    for wx in (xc - 3, xc + 3):
        c.set_block(wx, 70, -66, MAT['frame_dark'])
        c.set_block(wx, 71, -66, MAT['iron_trap_b'])
        c.fill(wx, 64, -62, wx, 69, -62, MAT['chain_y'])
    c.fill(xc, 70, z_bow, xc, 74, z_bow, MAT['end_rod_up'])

    for z in range(-170, -73):
        for x in (186, 212):
            c.set_block(x, 69, z, MAT['light_ochre'] if z % 4 == 0 else MAT['wall_quartz'])
            if not (x == 186 and -143 <= z <= -139):
                c.set_block(x, 70, z, MAT['pane_black'])
        for x in (187, 188, 210, 211):
            c.set_block(x, 69, z, MAT['wood_warm'])

    c.fill(189, 70, -168, 209, 73, -74, MAT['wall_white'])
    c.fill(190, 70, -167, 208, 73, -75, 'minecraft:air')
    build_curtain_wall(c, 189, 70, -166, 189, 73, -76, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 209, 70, -166, 209, 73, -76, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 191, 70, -74, 207, 73, -74, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 191, 70, -168, 207, 73, -168, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    c.fill(189, 70, -142, 189, 72, -140, 'minecraft:air')

    for lb_z in (-132, -116, -100):
        for side_x, davit_x in [(186, 188), (212, 210)]:
            for dz_d in (-3, 3):
                c.fill(davit_x, 70, lb_z + dz_d, side_x, 73, lb_z + dz_d, MAT['iron_bars'])
                c.set_block(side_x, 73, lb_z + dz_d, MAT['wall_quartz'])
            for dz_b in range(-2, 3):
                c.set_block(side_x, 71, lb_z + dz_b, MAT['orange_wool'])
                if abs(dz_b) <= 1:
                    c.set_block(side_x, 72, lb_z + dz_b, MAT['light_ochre'] if dz_b == 0 else MAT['wall_white'])
                else:
                    c.set_block(side_x, 72, lb_z + dz_b, MAT['slab_quartz_b'])

    c.fill(xc - 5, 69, -120, xc + 5, 69, -108, 'minecraft:air')
    for x in range(xc - 6, xc + 7):
        for z in (-121, -107):
            c.set_block(x, 69, z, MAT['light_ochre'] if x % 3 == 0 else MAT['wall_quartz'])
            c.set_block(x, 70, z, MAT['pane_black'])
    for z in range(-120, -107):
        for x in (xc - 6, xc + 6):
            c.set_block(x, 69, z, MAT['light_ochre'] if z % 3 == 0 else MAT['wall_quartz'])
            c.set_block(x, 70, z, MAT['pane_black'])

    for sz_room in (-160, -150, -96, -86):
        place_bed(c, 192, 70, sz_room, facing='north', color='white')
        place_bed(c, 206, 70, sz_room, facing='north', color='white')
        build_floor_lamp(c, 194, 69, sz_room, 'modern')
        build_floor_lamp(c, 204, 69, sz_room, 'modern')

    c.fill(188, 74, -166, 210, 74, -74, MAT['wood_dark'])
    build_recessed_ceiling_grid(c, 190, 74, -166, 208, -76, step_x=4, step_z=4, light_mat=MAT['light_ochre'])

    for z in range(-166, -73):
        for bx_bal in (188, 210):
            c.set_block(bx_bal, 74, z, MAT['light_ochre'] if z % 4 == 0 else MAT['wall_quartz'])
            c.set_block(bx_bal, 75, z, MAT['pane_cyan'])
        if z % 8 == 0:
            c.fill(188, 75, z, 189, 77, z, MAT['wall_white'])
            c.fill(209, 75, z, 210, 77, z, MAT['wall_white'])

    c.fill(190, 75, -164, 208, 78, -76, MAT['wall_white'])
    c.fill(191, 75, -163, 207, 78, -77, 'minecraft:air')
    build_curtain_wall(c, 190, 75, -162, 190, 78, -78, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 208, 75, -162, 208, 78, -78, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 192, 75, -76, 206, 78, -76, MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 192, 75, -164, 206, 78, -164, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)

    c.fill(xc - 4, 74, -118, xc + 4, 74, -110, 'minecraft:air')
    for x in range(xc - 5, xc + 6):
        for z in (-119, -109):
            c.set_block(x, 74, z, MAT['wall_quartz'])
            c.set_block(x, 75, z, MAT['pane_black'])
    for z in range(-118, -109):
        for x in (xc - 5, xc + 5):
            c.set_block(x, 74, z, MAT['wall_quartz'])
            c.set_block(x, 75, z, MAT['pane_black'])

    c.fill(xc - 5, 75, -82, xc + 5, 75, -78, MAT['wood_dark'])
    c.set_block(xc - 5, 76, -80, 'minecraft:jukebox')
    c.set_block(xc + 5, 76, -80, 'minecraft:jukebox')
    c.set_block(xc, 75, -80, MAT['light_ochre'])
    for sz_th in (-92, -88, -85):
        build_outdoor_sofa(c, xc - 4, 74, sz_th, length=9, facing='north')

    for sz_s in (-156, -144, -132):
        place_bed(c, 193, 75, sz_s, facing='north', color='cyan')
        place_bed(c, 205, 75, sz_s, facing='north', color='cyan')

    c.fill(188, 79, -164, 210, 79, -68, MAT['wood_warm'])
    build_recessed_ceiling_grid(c, 191, 79, -162, 207, -78, step_x=4, step_z=4, light_mat=MAT['light_ochre'])

    build_spiral_staircase(c, xc, 64, 79, -130, radius=2)

    c.fill(183, 79, -76, 215, 79, -70, MAT['wall_white'])
    c.fill(184, 79, -74, 185, 79, -72, MAT['glass_clear'])
    c.fill(213, 79, -74, 214, 79, -72, MAT['glass_clear'])
    for y in range(80, 83):
        for x in range(183, 216):
            for z in range(-76, -69):
                if x in (183, 215) or z in (-76, -70):
                    if (x in (183, 188, 210, 215) and z in (-76, -70)):
                        c.set_block(x, y, z, MAT['wall_white'])
                    else:
                        c.set_block(x, y, z, MAT['glass_black'] if y == 81 else MAT['glass_clear'])
                else:
                    c.set_block(x, y, z, 'minecraft:air')
    c.fill(182, 83, -77, 216, 83, -69, MAT['wall_white'])
    c.fill(183, 84, -76, 215, 84, -70, MAT['slab_quartz_b'])
    c.set_block(183, 84, -73, MAT['red_concrete'])
    c.set_block(183, 85, -73, MAT['end_rod_up'])
    c.set_block(215, 84, -73, MAT['green_concrete'])
    c.set_block(215, 85, -73, MAT['end_rod_up'])
    for hx in (xc - 4, xc, xc + 4):
        place_lectern(c, hx, 80, -71, 'south')
        c.set_block(hx, 80, -73, stair('smooth_quartz', 'north', 'bottom'))
        c.set_block(hx, 83, -73, MAT['light_ochre'])
    c.fill(xc - 2, 80, -75, xc + 2, 80, -75, MAT['light_sea'])
    c.set_block(185, 80, -73, 'minecraft:lectern[facing=west,has_book=false,powered=false]',
                {'id': ('string', 'minecraft:lectern'), 'x': ('int', 185), 'y': ('int', 80), 'z': ('int', -73), 'keepPacked': ('byte', 0)})
    c.set_block(213, 80, -73, 'minecraft:lectern[facing=east,has_book=false,powered=false]',
                {'id': ('string', 'minecraft:lectern'), 'x': ('int', 213), 'y': ('int', 80), 'z': ('int', -73), 'keepPacked': ('byte', 0)})

    for z in range(-164, -76):
        for x in (188, 210):
            c.set_block(x, 79, z, MAT['light_ochre'] if z % 4 == 0 else MAT['wall_quartz'])
            c.set_block(x, 80, z, MAT['pane_cyan'])

    for x in range(195, 204):
        for z in range(-124, -103):
            if x in (195, 203) or z in (-124, -104):
                c.set_block(x, 78, z, MAT['pool_shallow_1'])
                c.set_block(x, 79, z, MAT['wall_quartz'])
                c.set_block(x, 80, z, MAT['slab_quartz_b'])
            else:
                c.set_block(x, 77, z, MAT['light_sea'] if (x + z) % 2 == 0 else MAT['pool_deep_1'])
                c.set_block(x, 78, z, MAT['water'])
                c.set_block(x, 79, z, MAT['water'])

    for jx1 in (190, 205):
        for x in range(jx1, jx1 + 4):
            for z in range(-98, -94):
                if x in (jx1, jx1 + 3) or z in (-98, -95):
                    c.set_block(x, 79, z, MAT['wall_quartz'])
                    c.set_block(x, 80, z, MAT['slab_quartz_b'])
                else:
                    c.set_block(x, 79, z, MAT['light_sea'])
                    c.set_block(x, 80, z, MAT['water'])

    build_outdoor_bar(c, 196, 79, -86, length=7)
    for lz in range(-122, -104, 5):
        build_sun_lounger(c, 191, 79, lz, facing='east')
        build_sun_lounger(c, 207, 79, lz, facing='west')
    build_patio_umbrella(c, 191, 79, -114)
    build_patio_umbrella(c, 207, 79, -114)

    c.fill(190, 80, -160, 208, 83, -136, MAT['wall_white'])
    c.fill(191, 80, -159, 207, 83, -137, 'minecraft:air')
    build_curtain_wall(c, 190, 80, -158, 190, 83, -138, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 208, 80, -158, 208, 83, -138, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, 192, 80, -160, 206, 83, -160, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    c.fill(196, 80, -136, 202, 82, -136, 'minecraft:air')
    build_illuminated_carpet_rug(c, 193, 79, -156, 205, -140, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_sofa(c, 195, 79, -154, length=9, facing='south')

    c.fill(192, 84, -94, 206, 84, -76, MAT['wall_white'])
    for x in range(192, 207):
        for z in (-94, -76):
            c.set_block(x, 85, z, MAT['pane_cyan'])
    for z in range(-94, -75):
        for x in (192, 206):
            c.set_block(x, 85, z, MAT['pane_cyan'])

    for rx_dome in (195, 203):
        c.set_block(rx_dome, 85, -82, MAT['frame_dark'])
        for dx in range(-1, 2):
            for dy in range(86, 89):
                for dz in range(-1, 2):
                    if abs(dx) + abs(dy - 87) + abs(dz) <= 2:
                        c.set_block(rx_dome + dx, dy, -82 + dz, MAT['light_sea'] if (dx == 0 and dy == 87 and dz == 0) else MAT['wall_quartz'])

    for y in range(85, 95):
        c.set_block(xc, y, -78, MAT['wall_white'] if y < 91 else MAT['iron_bars'])
        if y in (88, 92):
            span = 4 if y == 88 else 3
            c.fill(xc - span, y, -78, xc + span, y, -78, MAT['slab_quartz_b'])
            c.set_block(xc - span, y + 1, -78, MAT['end_rod_up'])
            c.set_block(xc + span, y + 1, -78, MAT['end_rod_up'])
    c.set_block(xc, 95, -78, MAT['light_ochre'])
    c.fill(xc, 96, -78, xc, 97, -78, MAT['end_rod_up'])

    c.fill(190, 84, -160, 208, 84, -136, MAT['wall_white'])
    build_recessed_ceiling_grid(c, 192, 84, -158, 206, -138, step_x=4, step_z=4, light_mat=MAT['light_ochre'])

    for y in range(85, 97):
        rel_y = y - 85
        z_front = -137 - rel_y // 2
        z_back = -149 - rel_y // 3
        hw_f = 4 if rel_y < 8 else 3
        for z in range(z_back, z_front + 1):
            for x in range(xc - hw_f, xc + hw_f + 1):
                is_edge = (x in (xc - hw_f, xc + hw_f) or z in (z_back, z_front))
                if y >= 95:
                    c.set_block(x, y, z, MAT['frame_dark'] if is_edge else MAT['light_shroom'])
                elif rel_y in (5, 6):
                    c.set_block(x, y, z, MAT['light_ochre'] if z == z_front else MAT['red_concrete'])
                else:
                    c.set_block(x, y, z, MAT['wall_white'] if is_edge else MAT['light_ochre'])
        if rel_y in (5, 6):
            for wx_fin in (xc - hw_f - 2, xc - hw_f - 1, xc + hw_f + 1, xc + hw_f + 2):
                for z in range(z_back + 1, z_front):
                    c.set_block(wx_fin, y, z, MAT['red_concrete'] if rel_y == 5 else MAT['slab_quartz_b'])
