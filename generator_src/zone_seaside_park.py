"""
zone_seaside_park.py — Expansion 4: The Seaside Park (海滨公园)
==============================================================
Located on the Ocean Side (+X, X in [98, 185]) at the Rear/Mid-Rear section of the
Villa Area (Z in [-200, -16]), screened from the Villa Front Courtyard (+Z) by the
3-Story East Wing and the Z=-20..40 East Parterre Garden & Ornamental Tree Screen.

Includes all 10 required coastal park landmarks:
  1. Pier / Boardwalk & Marina Yacht (码头/栈桥)
  2. Coastal Boathouse & Speedboat (船屋)
  3. Headland Lighthouse & Keeper's Cottage (灯塔)
  4. Golden Sand Beach & Lifeguard Tower (海滩救生台)
  5. Overwater Panoramic Seafood Restaurant (海鲜餐厅)
  6. Open-Air Seaside Market Street (海边市集)
  7. Offshore Diving Spot & Coral Reef (潜水点)
  8. Submerged Glass Underwater Viewing Tunnel & Dome (水下观景廊)
  9. Resort Swimming Pool + Poolside Bar + Sun Lounger Deck (泳池+池畔酒吧+躺椅区)
 10. Choreographed Musical Fountain Plaza (音乐喷泉)
 11. Cruise Terminal / VIP Boarding & Waiting Hall (邮轮旁登船大厅/候船厅)
"""

import math, random
from config import Y_BASE, SEA_LEVEL, HARBOR_FLOOR, MAT, SOFT_FLOWERS, CORAL_BLOCKS
from world_canvas import WorldCanvas
from arch_lib import (
    stair, trapdoor,
    place_bed, place_barrel, place_brewing_stand, place_smoker, place_blast_furnace,
    place_lectern, place_tall_flower, place_door, place_double_door,
    build_recessed_ceiling_grid, build_crystal_chandelier, build_illuminated_carpet_rug,
    build_floor_lamp, build_indoor_planter,
    build_curtain_wall, build_flat_roof_and_eaves,
    build_spiral_staircase, build_straight_stairs,
    build_lamppost, build_hedgerow_line, build_spherical_shrub,
    build_custom_tree, build_patio_umbrella, build_sun_lounger,
    build_outdoor_sofa, build_outdoor_bar, build_infinity_pool
)

def build_seaside_park_grounds_and_boardwalk(c: WorldCanvas):

    for x in range(48, 104):
        for z in range(-50, -45):
            if z in (-50, -46) and x < 98:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
    for x in range(62, 104):
        for z in range(-90, -85):
            if z in (-90, -86) and x < 98:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
    for x in range(62, 104):
        for z in range(-122, -117):
            if z in (-122, -118) and x < 98:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])

    for z in range(-220, 29):
        in_west_junc = (-50 <= z <= -46) or (-90 <= z <= -86) or (-122 <= z <= -118) or (-34 <= z <= -29)
        in_east_plaza_open = (-215 <= z <= -17) and not (-114 <= z <= -106)
        for x in range(98, 104):
            if x == 98 and not in_west_junc:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['wall_quartz'])
            elif x == 103 and not in_east_plaza_open:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
        if z % 12 == 0 and not (-115 <= z <= -105) and not in_west_junc:
            build_lamppost(c, 97, Y_BASE + 1, z, style='avenue')

    for z in range(-218, -17):
        if -114 <= z <= -106:
            continue
        for x in range(104, 132):
            if (x - 104) % 6 == 0 or (z + 216) % 6 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    for z in range(-170, -15):
        c.fill(137, 54, z, 138, Y_BASE - 1, z, MAT['stone_pol_and'])
        if -114 <= z <= -106:
            arch_dy = 1 if -112 <= z <= -108 else 0
            for x in range(132, 139):
                c.set_block(x, Y_BASE + arch_dy, z, MAT['slab_dark_b'] if arch_dy else MAT['wood_dark'])
                if x in (132, 138):
                    c.set_block(x, Y_BASE + arch_dy, z, MAT['wall_quartz'])
                    c.set_block(x, Y_BASE + arch_dy + 1, z, MAT['pane_black'])
            continue

        for x in range(132, 139):
            if x == 138:
                c.set_block(x, Y_BASE, z, MAT['light_sea'] if z % 4 == 0 else MAT['wall_quartz'])
                if not (-94 <= z <= -40 or -101 <= z <= -93 or -125 <= z <= -107 or -170 <= z <= -134 or -36 <= z <= -18):
                    c.set_block(x, Y_BASE + 1, z, MAT['pane_black'])
            elif x == 132:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 5 == 0 else MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (z // 2) % 2 == 0 else MAT['wood_dark'])

        if z % 10 == 0 and not (-36 <= z <= -18 or -125 <= z <= -107 or -170 <= z <= -134):
            build_lamppost(c, 132, Y_BASE + 1, z, style='courtyard')

def build_seafood_restaurant(c: WorldCanvas):
    rx1, rx2, rz1, rz2 = 108, 144, -36, -18
    y_1f = Y_BASE
    y_2f = Y_BASE + 6
    y_roof = Y_BASE + 11

    for px in (138, 143):
        for pz in (-35, -27, -19):
            c.fill(px, 52, pz, px + 1, y_1f - 1, pz + 1, MAT['frame_dark'])
            c.set_block(px, 62, pz, MAT['light_sea'])

    c.fill(rx1, y_1f, rz1, rx2, y_1f, rz2, MAT['wood_dark'])
    c.fill(rx1, y_1f + 1, rz1, 138, y_2f - 1, rz2, MAT['wall_white'])
    c.fill(rx1 + 1, y_1f + 1, rz1 + 1, 137, y_2f - 1, rz2 - 1, 'minecraft:air')
    c.fill(139, y_1f + 1, rz1, rx2, y_2f + 5, rz2, 'minecraft:air')

    for x in range(rx1 + 1, 138):
        for z in range(rz1 + 1, rz2):
            if (x + z) % 4 == 0:
                c.set_block(x, y_1f, z, MAT['light_ochre'])
            else:
                c.set_block(x, y_1f, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    build_curtain_wall(c, 138, y_1f + 1, rz1 + 2, 138, y_2f - 1, rz2 - 2,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, rx1 + 2, y_1f + 1, rz1, 136, y_2f - 1, rz1,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, rx1 + 2, y_1f + 1, rz2, 136, y_2f - 1, rz2,
                       MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, rx1, y_1f + 1, rz1 + 2, rx1, y_2f - 1, rz2 - 2,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)

    place_double_door(c, rx1, y_1f + 1, -28, 'dark_oak', 'east', 'true')
    place_double_door(c, 138, y_1f + 1, -28, 'dark_oak', 'west', 'true')

    for x in range(139, rx2 + 1):
        for z in range(rz1, rz2 + 1):
            if x == rx2 or z in (rz1, rz2):
                c.set_block(x, y_1f, z, MAT['light_sea'] if (x + z) % 3 == 0 else MAT['wall_quartz'])
                c.set_block(x, y_1f + 1, z, MAT['pane_cyan'])
            else:
                c.set_block(x, y_1f, z, MAT['wood_warm'] if z % 2 == 0 else MAT['wood_dark'])
    for tz in (-32, -23):
        c.set_block(141, y_1f, tz, MAT['light_ochre'])
        c.set_block(141, y_1f + 1, tz, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        c.set_block(141, y_1f + 2, tz, MAT['carpet_white'])
        c.set_block(141, y_1f + 1, tz - 1, stair('smooth_quartz', 'north', 'bottom'))
        c.set_block(141, y_1f + 1, tz + 1, stair('smooth_quartz', 'south', 'bottom'))

    coral_fans = [
        'minecraft:tube_coral_fan[waterlogged=true]',
        'minecraft:brain_coral_fan[waterlogged=true]',
        'minecraft:bubble_coral_fan[waterlogged=true]',
        'minecraft:fire_coral_fan[waterlogged=true]',
        'minecraft:horn_coral_fan[waterlogged=true]',
    ]
    for x in range(112, 123):
        for z in range(-35, -31):
            for y in range(y_1f + 1, y_2f - 1):
                if x in (112, 122) or z in (-35, -32):
                    c.set_block(x, y, z, MAT['frame_dark'] if (x in (112, 122) and z in (-35, -32)) else MAT['glass_clear'])
                else:
                    if y == y_1f + 1:
                        c.set_block(x, y, z, MAT['light_sea'] if (x + z) % 2 == 0 else CORAL_BLOCKS[(x + z) % len(CORAL_BLOCKS)])
                    elif y == y_1f + 2:
                        c.set_block(x, y, z, MAT['sea_pickle_4'] if x % 2 == 0 else coral_fans[x % len(coral_fans)])
                    elif y == y_1f + 3 and (x + z) % 3 == 0:
                        c.set_block(x, y, z, MAT['seagrass'])
                    else:
                        c.set_block(x, y, z, MAT['water'])
        c.fill(112, y_2f - 1, -35, 122, y_2f - 1, -32, MAT['light_sea'])

    for x in range(110, 121):
        c.set_block(x, y_1f, -22, MAT['light_ochre'] if x % 2 == 0 else MAT['wood_dark'])
        c.set_block(x, y_1f + 1, -22, MAT['wall_quartz'])
        c.set_block(x, y_1f + 2, -22, MAT['slab_quartz_b'])
        if x % 2 == 0 and x not in (112, 114):
            c.set_block(x, y_1f + 1, -24, stair('dark_oak', 'north', 'bottom'))
    place_smoker(c, 111, y_1f + 1, -19, facing='north', lit='true')
    place_smoker(c, 112, y_1f + 1, -19, facing='north', lit='true')
    place_blast_furnace(c, 113, y_1f + 1, -19, facing='north', lit='true')
    c.set_block(115, y_1f + 1, -19, 'minecraft:water_cauldron[level=3]')
    c.set_block(116, y_1f + 1, -19, MAT['packed_ice'])
    place_barrel(c, 118, y_1f + 1, -19, 'north')
    place_barrel(c, 119, y_1f + 1, -19, 'north')
    place_brewing_stand(c, 114, y_1f + 2, -22)

    for tx in (126, 133):
        for tz in (-31, -26, -21):
            c.fill(tx - 1, y_1f + 1, tz, tx + 1, y_1f + 1, tz, MAT['slab_quartz_t'])
            c.set_block(tx, y_1f, tz, MAT['light_ochre'])
            c.fill(tx - 1, y_1f + 2, tz, tx + 1, y_1f + 2, tz, MAT['carpet_white'])
            c.set_block(tx, y_1f + 2, tz, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
            for dx in (-1, 1):
                c.set_block(tx + dx, y_1f + 1, tz - 1, stair('dark_oak', 'north', 'bottom'))
                c.set_block(tx + dx, y_1f + 1, tz + 1, stair('dark_oak', 'south', 'bottom'))

    build_recessed_ceiling_grid(c, rx1 + 2, y_2f, rz1 + 2, 136, rz2 - 2, step_x=4, step_z=4, light_mat=MAT['light_ochre'])
    build_crystal_chandelier(c, 125, y_2f, -27, drop=2, style='grand')
    build_crystal_chandelier(c, 133, y_2f, -27, drop=2, style='grand')

    c.fill(110, y_2f, rz1, 138, y_2f, rz2, MAT['wood_dark'])
    c.fill(116, y_2f + 1, -34, 132, y_roof - 1, -20, MAT['wall_white'])
    c.fill(117, y_2f + 1, -33, 131, y_roof - 1, -21, 'minecraft:air')
    place_door(c, 116, y_2f + 1, -27, 'dark_oak', 'east', 'left', 'true')
    build_curtain_wall(c, 132, y_2f + 1, -32, 132, y_roof - 1, -22, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=3)
    build_curtain_wall(c, 118, y_2f + 1, -34, 130, y_roof - 1, -34, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    place_door(c, 132, y_2f + 1, -27, 'dark_oak', 'west', 'left', 'true')
    build_illuminated_carpet_rug(c, 119, y_2f, -31, 129, -23, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_bar(c, 120, y_2f, -31, length=6)
    build_outdoor_sofa(c, 120, y_2f, -24, length=6, facing='north')
    build_flat_roof_and_eaves(c, 116, y_roof, -34, 132, -20, overhang=2, hidden_lights=True)
    build_crystal_chandelier(c, 124, y_roof, -27, drop=2, style='grand')

    for x in range(109, 139):
        for z in (rz1, rz2):
            c.set_block(x, y_2f, z, MAT['wall_quartz'])
            c.set_block(x, y_2f + 1, z, MAT['pane_black'])
    for z in range(rz1, rz2 + 1):
        for x in (109, 138):
            c.set_block(x, y_2f, z, MAT['wall_quartz'])
            c.set_block(x, y_2f + 1, z, MAT['pane_black'])

    build_spiral_staircase(c, 113, y_1f + 1, y_2f, -27, radius=2, start_sector=1, clockwise=True)
    c.set_block(111, y_2f, -26, MAT['slab_quartz_t'])
    for hy_sf in range(y_2f + 1, y_2f + 4):
        c.set_block(111, hy_sf, -26, 'minecraft:air')
    build_patio_umbrella(c, 135, y_2f, -32)
    build_patio_umbrella(c, 135, y_2f, -22)

def build_musical_fountain_plaza(c: WorldCanvas):
    fcx, fcz = 118, -48
    rad = 9
    rainbow_glass = [MAT['glass_cyan'], MAT['glass_magenta'], MAT['glass_yellow'], MAT['glass_blue']]

    for dx in range(-rad, rad + 1):
        for dz in range(-rad, rad + 1):
            d = math.hypot(dx, dz)
            x, z = fcx + dx, fcz + dz
            if d > rad + 0.4:
                continue
            elif d >= rad - 1.0:
                c.set_block(x, Y_BASE - 1, z, MAT['stone_pol_and'])
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                if (abs(dx) in (0, 5, 8) and abs(dz) in (0, 5, 8)):
                    c.set_block(x, Y_BASE, z, 'minecraft:jukebox' if (dx + dz) % 2 == 0 else 'minecraft:note_block')
                    c.set_block(x, Y_BASE + 1, z, MAT['light_ochre'])
                    c.set_block(x, Y_BASE + 2, z, MAT['slab_quartz_b'])
                else:
                    c.set_block(x, Y_BASE + 1, z, MAT['slab_quartz_b'])
            else:
                ring_idx = int(round(d))
                if ring_idx in (2, 4, 6):
                    c.set_block(x, Y_BASE - 3, z, MAT['light_sea'] if ring_idx != 4 else MAT['light_ochre'])
                    c.set_block(x, Y_BASE - 2, z, rainbow_glass[(dx + dz + ring_idx) % len(rainbow_glass)])
                else:
                    c.set_block(x, Y_BASE - 3, z, MAT['pool_deep_1'])
                    c.set_block(x, Y_BASE - 2, z, MAT['pool_shallow_1'] if (dx + dz) % 2 == 0 else MAT['pool_deep_2'])
                c.set_block(x, Y_BASE - 1, z, MAT['water'])
                c.set_block(x, Y_BASE, z, MAT['water'])

    for ang_i in range(8):
        ang = ang_i * math.pi / 4.0
        jx = fcx + int(round(6.0 * math.cos(ang)))
        jz = fcz + int(round(6.0 * math.sin(ang)))
        c.set_block(jx, Y_BASE, jz, MAT['light_sea'])
        c.set_block(jx, Y_BASE + 1, jz, MAT['end_rod_up'])
        c.set_block(jx, Y_BASE + 2, jz, MAT['water'])
        c.set_block(jx, Y_BASE + 3, jz, MAT['end_rod_up'])

    for jx, jz in [(fcx - 3, fcz), (fcx + 3, fcz), (fcx, fcz - 3), (fcx, fcz + 3)]:
        c.set_block(jx, Y_BASE, jz, MAT['light_pearl'])
        c.fill(jx, Y_BASE + 1, jz, jx, Y_BASE + 2, jz, MAT['end_rod_up'])
        c.fill(jx, Y_BASE + 3, jz, jx, Y_BASE + 4, jz, MAT['water'])
        c.set_block(jx, Y_BASE + 5, jz, MAT['end_rod_up'])

    c.fill(fcx - 1, Y_BASE - 1, fcz - 1, fcx + 1, Y_BASE + 1, fcz + 1, MAT['wall_chiseled'])
    c.set_block(fcx, Y_BASE + 1, fcz, MAT['light_ochre'])
    c.fill(fcx, Y_BASE + 2, fcz, fcx, Y_BASE + 4, fcz, MAT['end_rod_up'])
    c.set_block(fcx, Y_BASE + 5, fcz, MAT['light_sea'])
    c.fill(fcx, Y_BASE + 6, fcz, fcx, Y_BASE + 7, fcz, MAT['water'])
    c.set_block(fcx, Y_BASE + 8, fcz, MAT['end_rod_up'])

    for z in range(fcz - 5, fcz + 6, 2):
        c.set_block(fcx - 11, Y_BASE, z, MAT['light_ochre'])
        c.set_block(fcx - 11, Y_BASE + 1, z, stair('smooth_quartz', 'west', 'bottom'))

def build_resort_pool_bar_and_loungers(c: WorldCanvas):
    px1, px2, pz1, pz2 = 116, 131, -90, -66
    build_infinity_pool(c, px1, Y_BASE, pz1, px2, pz2)

    for sz in range(-82, -71, 2):
        c.set_block(117, Y_BASE - 2, sz, MAT['light_sea'])
        c.set_block(117, Y_BASE - 1, sz, MAT['wall_quartz'])
        c.set_block(117, Y_BASE, sz, 'minecraft:water[level=0]')

    bx1, bx2, bz1, bz2 = 105, 115, -84, -70
    c.fill(bx1, Y_BASE, bz1, bx2, Y_BASE, bz2, MAT['wood_dark'])
    for cx_p in (bx1, bx2):
        for cz_p in (bz1, bz2):
            c.set_block(cx_p, Y_BASE + 1, cz_p, MAT['stone_pol_and'])
            c.fill(cx_p, Y_BASE + 2, cz_p, cx_p, Y_BASE + 4, cz_p, MAT['beam_dark_y'])
    build_flat_roof_and_eaves(c, bx1, Y_BASE + 5, bz1, bx2, bz2, overhang=1,
                              roof_mat=MAT['wall_white'], soffit_mat=MAT['wood_dark'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)
    for z in range(-81, -72):
        c.set_block(110, Y_BASE, z, MAT['light_ochre'])
        c.set_block(110, Y_BASE + 1, z, MAT['wall_quartz'])
        if z % 2 == 0:
            place_barrel(c, 110, Y_BASE + 2, z, 'east')
            c.set_block(110, Y_BASE + 3, z, MAT['light_ochre'])
        else:
            c.set_block(110, Y_BASE + 2, z, 'minecraft:bookshelf')
            c.set_block(110, Y_BASE + 3, z, MAT['glass_cyan'])
        c.set_block(110, Y_BASE + 4, z, MAT['slab_dark_b'])

    for z in range(-82, -71):
        for bx_cnt in (107, 114):
            c.set_block(bx_cnt, Y_BASE, z, MAT['light_ochre'] if z % 2 == 0 else MAT['wood_dark'])
            c.set_block(bx_cnt, Y_BASE + 1, z, MAT['wood_dark'])
            c.set_block(bx_cnt, Y_BASE + 2, z, MAT['slab_quartz_b'])
        if z % 2 == 0:
            c.set_block(105, Y_BASE + 1, z, stair('smooth_quartz', 'east', 'bottom'))
    place_brewing_stand(c, 114, Y_BASE + 2, -79)
    place_brewing_stand(c, 107, Y_BASE + 2, -75)
    c.set_block(114, Y_BASE + 2, -74, 'minecraft:white_candle[candles=4,lit=true,waterlogged=false]')
    c.set_block(107, Y_BASE + 2, -80, 'minecraft:flower_pot')

    for lx in range(116, 131, 4):
        build_sun_lounger(c, lx, Y_BASE, -94, facing='south')
        build_sun_lounger(c, lx, Y_BASE, -62, facing='north')
    for ux in (118, 126):
        build_patio_umbrella(c, ux, Y_BASE, -93)
        build_patio_umbrella(c, ux, Y_BASE, -63)
    build_outdoor_sofa(c, 106, Y_BASE, -93, length=6, facing='south')
    build_outdoor_sofa(c, 106, Y_BASE, -63, length=6, facing='north')

def build_golden_beach_and_lifeguard_tower(c: WorldCanvas):
    for sz_base in (-76, -46):
        for dz in range(-2, 3):
            c.set_block(138, Y_BASE, sz_base + dz, stair('smooth_quartz', 'west', 'bottom'))
            c.set_block(139, Y_BASE - 1, sz_base + dz, MAT['wall_quartz'])

    for idx, bz in enumerate(range(-90, -56, 10)):
        bx = 143 if idx % 2 == 0 else 145
        by = 63
        c.set_block(bx, by, bz - 2, MAT['light_ochre'])
        c.set_block(bx, by + 1, bz - 2, MAT['carpet_cyan'] if idx % 2 == 0 else MAT['carpet_yellow'])
        c.set_block(bx, by + 1, bz - 1, stair('smooth_quartz', 'west', 'bottom'))
        build_patio_umbrella(c, bx, by, bz)

    lx1, lx2, lz1, lz2 = 142, 148, -53, -47
    y_sand = 63
    y_deck = 67
    y_roof = 71

    c.fill(lx1 - 1, y_sand - 2, lz1 - 1, lx2 + 1, y_sand, lz2 + 1, 'minecraft:smooth_sandstone')
    c.fill(lx1 - 1, y_sand, lz1 - 1, lx2 + 1, y_sand, lz2 + 1, 'minecraft:sand')

    for sx in (lx1 + 1, lx2 - 1):
        for sz in (lz1 + 1, lz2 - 1):
            c.fill(sx, y_sand + 1, sz, sx, y_deck - 1, sz, MAT['beam_spruce_y'])
            c.set_block(sx, y_sand + 2, (lz1 + lz2) // 2, MAT['iron_bars'])
    c.set_block((lx1 + lx2) // 2, y_deck - 1, (lz1 + lz2) // 2, MAT['light_ochre'])

    c.fill(lx1, y_deck, lz1, lx2, y_deck, lz2, MAT['wall_quartz'])
    for step in range(4):
        sx = lx1 - 3 + step
        sy = y_sand + 1 + step
        for sz in (-51, -50):
            c.set_block(sx, sy, sz, stair('smooth_quartz', 'east', 'bottom'))
            c.set_block(sx, sy - 1, sz, MAT['light_ochre'] if step == 2 else MAT['wall_white'])
    for x in range(lx1, lx2 + 1):
        for z in range(lz1, lz2 + 1):
            if x in (lx1, lx2) or z in (lz1, lz2):
                if x == lx1 and z in (-51, -50):
                    continue
                c.set_block(x, y_deck + 1, z, MAT['iron_bars'])

    c.fill(lx1 + 1, y_deck + 1, lz1 + 1, lx2 - 1, y_roof - 1, lz2 - 1, MAT['wall_white'])
    c.fill(lx1 + 2, y_deck + 1, lz1 + 2, lx2 - 2, y_roof - 1, lz2 - 2, 'minecraft:air')
    for x in range(lx1 + 1, lx2):
        for z in range(lz1 + 1, lz2):
            if x in (lx1 + 1, lx2 - 1) or z in (lz1 + 1, lz2 - 1):
                c.set_block(x, y_deck + 1, z, MAT['red_concrete'] if (x + z) % 2 == 0 else MAT['wall_white'])
                if not (x in (lx1 + 1, lx2 - 1) and z in (lz1 + 1, lz2 - 1)):
                    c.set_block(x, y_deck + 2, z, MAT['pane_clear'])
    place_door(c, lx1 + 1, y_deck + 1, -50, 'spruce', 'east', 'left', 'true')
    place_lectern(c, lx2 - 2, y_deck + 1, -50, 'east')
    c.set_block((lx1 + lx2) // 2, y_roof - 1, -50, MAT['light_ochre'])

    for x in range(lx1, lx2 + 1):
        for z in range(lz1, lz2 + 1):
            mat_r = MAT['red_concrete'] if x % 2 == 0 else MAT['wall_white']
            c.set_block(x, y_roof, z, mat_r)
            if lx1 + 1 <= x <= lx2 - 1 and lz1 + 1 <= z <= lz2 - 1:
                c.set_block(x, y_roof + 1, z, MAT['slab_quartz_b'])
    c.set_block((lx1 + lx2) // 2, y_roof + 1, -50, MAT['light_ochre'])
    c.set_block((lx1 + lx2) // 2, y_roof + 2, -50, MAT['end_rod_up'])

def build_underwater_gallery_and_diving_spot(c: WorldCanvas):
    """
    V4 Upgraded Underwater Aquarium Gallery, Octagonal Dome & Shore Spiral Entry Pavilion:
      - Fixes (135, 53, -59): Expanded 9x9 Shore Entry Pavilion (X=129..137, Z=-63..-55) with solid 1F
        foyer deck at Y=64, smooth 8-sector spiral staircase (center 133, -59), and 3.0m-tall unobstructed
        bottom vestibule (X=134..136, Y=53..55, Z=-60..-58) leading into the underwater tunnel.
      - Fixes (159, 53, -59): Removed the solid cyan_stained_glass wall at X=160 that blocked the tunnel!
        The 3-block-wide glass tunnel now runs continuously from X=136 to X=170 (Z=-60..-58, Y=53..55)
        and opens via a 6-block-wide grand portal (X=165..170, Z=-61, Y=53..56) directly into the
        Octagonal Underwater Viewing Dome (center 168, -68, radius 7).
      - Upgraded Aquarium Scenery: Multi-tiered living coral reef terraces (Y=51..59) placed right outside
        both sides of the glass tunnel (X=139..182, Z=-94..-48) and around the Viewing Dome at eye level,
        with 5 coral block species, waterlogged coral fans, sea pickles, kelp columns, sea lanterns, and
        suspended voxel marine sculptures.
    """
    rng = random.Random(2026888)
    coral_fans = [
        'minecraft:tube_coral_fan[waterlogged=true]',
        'minecraft:brain_coral_fan[waterlogged=true]',
        'minecraft:bubble_coral_fan[waterlogged=true]',
        'minecraft:fire_coral_fan[waterlogged=true]',
        'minecraft:horn_coral_fan[waterlogged=true]',
    ]

    for z in range(-94, -48):
        for x in range(139, 185):
            in_lagoon = (x >= 152) or (-67 <= z <= -51)
            if not in_lagoon:

                if z in (-68, -50) and 139 <= x <= 151:
                    for wy in range(50, 64):
                        c.set_block(x, wy, z, MAT['light_sea'] if (wy in (54, 60) and x % 3 == 0) else (MAT['wall_quartz'] if wy == 63 else MAT['pool_deep_1']))
                continue

            for wy in range(51, 63):
                c.set_block(x, wy, z, MAT['water'])

            if (x * 7 + z * 11) % 7 == 0:
                c.set_block(x, 50, z, MAT['light_sea'])
            elif (x + z) % 3 == 0:
                c.set_block(x, 50, z, MAT['pool_deep_1'])
            else:
                c.set_block(x, 50, z, 'minecraft:sand')

            in_tunnel_struct = (135 <= x <= 171 and -61 <= z <= -57)
            dx_d, dz_d = x - 168, z - (-68)
            oct_d = max(abs(dx_d), abs(dz_d), (abs(dx_d) + abs(dz_d) + 1) * 5 // 7)
            in_dome_struct = (oct_d <= 7)
            if in_tunnel_struct or in_dome_struct:
                continue

            near_tunnel = (139 <= x <= 175 and (-65 <= z <= -62 or -56 <= z <= -52))
            near_dome = (8 <= oct_d <= 11)

            if near_tunnel or near_dome:

                mound_h = 2 + ((x * 3 + z * 5) % 4)
                coral_mat = CORAL_BLOCKS[(x * 2 + z) % len(CORAL_BLOCKS)]
                if (x + z) % 3 == 0:
                    for cy in range(51, 51 + mound_h):
                        c.set_block(x, cy, z, MAT['light_sea'] if (cy == 51 + mound_h - 1 and (x + z) % 6 == 0) else coral_mat)
                    top_y = 51 + mound_h
                    if top_y <= 60:
                        c.set_block(x, top_y, z, MAT['sea_pickle_4'] if (x + z) % 2 == 0 else coral_fans[(x + z) % len(coral_fans)])
                elif (x + z) % 3 == 1:
                    c.set_block(x, 51, z, MAT['light_sea'] if x % 4 == 0 else coral_mat)
                    c.set_block(x, 52, z, coral_fans[(x * 3 + z) % len(coral_fans)])
                else:

                    kelp_top = 56 + ((x + z) % 4)
                    for ky in range(51, kelp_top):
                        c.set_block(x, ky, z, 'minecraft:kelp_plant')
                    c.set_block(x, kelp_top, z, 'minecraft:kelp[age=20]')
            else:
                if rng.random() < 0.26:
                    coral = rng.choice(CORAL_BLOCKS)
                    h_c = rng.randint(1, 5)
                    for cy in range(51, 51 + h_c):
                        c.set_block(x, cy, z, coral)
                    if rng.random() < 0.65:
                        c.set_block(x, 51 + h_c, z, MAT['sea_pickle_4'])
                    elif rng.random() < 0.40:
                        c.set_block(x, 51 + h_c, z, MAT['light_sea'] if rng.random() < 0.5 else MAT['light_pearl'])
                elif rng.random() < 0.30:
                    c.set_block(x, 51, z, MAT['seagrass'])

    for jx, jz, jy, jmat in [
        (145, -64, 57, MAT['glass_magenta']),
        (153, -54, 57, MAT['glass_yellow']),
        (159, -64, 56, MAT['glass_cyan']),
        (164, -54, 57, MAT['glass_magenta']),
        (175, -64, 56, MAT['glass_yellow']),
        (175, -72, 57, MAT['glass_cyan']),
        (162, -77, 56, MAT['glass_magenta']),
    ]:
        c.set_block(jx, jy, jz, MAT['light_pearl'])
        for dx_j, dz_j in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
            c.set_block(jx + dx_j, jy + 1, jz + dz_j, jmat)
        c.set_block(jx, jy - 1, jz, MAT['end_rod_down'])

    for ring_x in (164, 170):
        rcz, rcy = -84, 55
        for dy in range(-2, 3):
            for dz in range(-2, 3):
                if abs(dy) == 2 or abs(dz) == 2:
                    c.set_block(ring_x, rcy + dy, rcz + dz, MAT['light_sea'] if (dy == 0 or dz == 0) else MAT['gold_block'])

    ex1, ex2, ez1, ez2 = 129, 137, -63, -55
    c.fill(ex1, 51, ez1, ex2, Y_BASE, ez2, MAT['wall_white'])
    c.fill(ex1 + 2, 52, ez1 + 2, ex2 - 2, Y_BASE + 4, ez2 - 2, 'minecraft:air')
    c.fill(ex1 + 1, 52, ez1 + 1, ex2 - 1, 52, ez2 - 1, MAT['wall_quartz'])

    c.fill(ex1 + 1, Y_BASE + 1, ez1 + 1, ex2 - 1, Y_BASE + 4, ez2 - 1, 'minecraft:air')
    for y in range(Y_BASE + 1, Y_BASE + 5):
        for x in range(ex1, ex2 + 1):
            for z in range(ez1, ez2 + 1):
                if x in (ex1, ex2) or z in (ez1, ez2):
                    if x in (ex1, ex2) and z in (ez1, ez2):
                        c.set_block(x, y, z, MAT['frame_dark'])
                    else:
                        c.set_block(x, y, z, MAT['glass_clear'] if y in (Y_BASE + 2, Y_BASE + 3) else MAT['glass_cyan'])

    c.fill(ex1, Y_BASE + 1, -60, ex1, Y_BASE + 3, -58, 'minecraft:air')
    build_flat_roof_and_eaves(c, ex1, Y_BASE + 5, ez1, ex2, ez2, overhang=1, hidden_lights=True)

    c.fill(ex1, Y_BASE, ez1, ex2, Y_BASE, ez2, MAT['wall_quartz'])

    build_spiral_staircase(c, 133, 53, Y_BASE, -59, radius=2, start_sector=5, clockwise=False)

    c.set_block(131, Y_BASE, -60, MAT['slab_quartz_t'])
    for hy_w in range(Y_BASE + 1, Y_BASE + 4):
        c.set_block(131, hy_w, -60, 'minecraft:air')

    for sy_l in (54, 58, 62):
        for sx_l in (131, 133, 135):
            c.set_block(sx_l, sy_l, -62, MAT['light_sea'])
            c.set_block(sx_l, sy_l, -56, MAT['light_sea'])
        for sz_l in (-61, -59, -57):
            c.set_block(130, sy_l, sz_l, MAT['light_sea'])
            if not (sy_l == 54 and -60 <= sz_l <= -58):
                c.set_block(136, sy_l, sz_l, MAT['light_sea'])

    for x_rail in range(131, 137):
        c.set_block(x_rail, Y_BASE + 1, -56, MAT['pane_cyan'])
    for z_rail in range(-62, -55):
        c.set_block(136, Y_BASE + 1, z_rail, MAT['pane_cyan'])
    c.fill(129, Y_BASE + 1, -60, 130, Y_BASE + 3, -58, 'minecraft:air')

    for x in range(136, 172):
        is_rib = (x % 6 == 0)
        for z in range(-61, -56):
            c.set_block(x, 51, z, MAT['stone_pol_and'])
            if z == -59:
                c.set_block(x, 52, z, MAT['light_sea'] if x % 2 == 0 else MAT['wall_quartz'])
                c.set_block(x, 53, z, MAT['carpet_cyan'])
            else:
                c.set_block(x, 52, z, MAT['light_sea'] if (x % 4 == 0 and z in (-60, -58)) else MAT['wall_quartz'])

        if x <= 170:
            for z in range(-60, -57):
                for y in range(53, 56):
                    if not (z == -59 and y == 53):
                        c.set_block(x, y, z, 'minecraft:air')
        else:

            for z in range(-61, -56):
                for y in range(53, 57):
                    c.set_block(x, y, z, MAT['frame_dark'] if (y == 56 or z in (-61, -57)) else MAT['glass_clear'])

        for z in (-61, -57):
            for y in range(53, 56):
                if is_rib:
                    c.set_block(x, y, z, MAT['light_sea'] if y == 55 else MAT['glass_cyan'])
                else:
                    c.set_block(x, y, z, MAT['glass_clear'])

        for z in range(-61, -56):
            if is_rib:
                c.set_block(x, 56, z, MAT['light_sea'] if z == -59 else MAT['glass_cyan'])
            else:
                c.set_block(x, 56, z, MAT['glass_clear'] if z in (-60, -59, -58) else MAT['glass_cyan'])

        for z in range(-61, -56):
            for y in range(57, 63):
                if x >= 138:
                    c.set_block(x, y, z, MAT['water'])

    c.set_block(135, 52, -59, MAT['light_sea'])
    c.set_block(135, 53, -59, MAT['carpet_cyan'])

    dcx, dcz, drad = 168, -68, 7
    for dx in range(-drad, drad + 1):
        for dz in range(-drad, drad + 1):
            oct_d = max(abs(dx), abs(dz), (abs(dx) + abs(dz) + 1) * 5 // 7)
            x, z = dcx + dx, dcz + dz
            if oct_d > drad:
                continue
            c.set_block(x, 51, z, MAT['stone_pol_and'])
            if oct_d in (2, 5) and (dx + dz) % 2 == 0:
                c.set_block(x, 52, z, MAT['light_sea'])
            else:
                c.set_block(x, 52, z, MAT['wall_quartz'] if (dx + dz) % 2 == 0 else MAT['pool_shallow_1'])

            if oct_d == drad:
                is_pillar = (dx == 0 or dz == 0 or abs(dx) == abs(dz))
                for y in range(53, 57):
                    c.set_block(x, y, z, MAT['frame_dark'] if is_pillar else (MAT['glass_clear'] if y in (53, 54, 55) else MAT['glass_cyan']))
                c.set_block(x, 57, z, MAT['frame_dark'])
            else:
                for y in range(53, 57):
                    c.set_block(x, y, z, 'minecraft:air')
                if oct_d == drad - 1:
                    c.set_block(x, 57, z, MAT['glass_cyan'] if (dx + dz) % 2 == 0 else MAT['light_sea'])
                else:
                    c.set_block(x, 57, z, 'minecraft:air')
                    c.set_block(x, 58, z, MAT['light_sea'] if oct_d in (0, 3) else MAT['glass_clear'])
                top_dome_y = 57 if oct_d >= drad - 1 else 58
                for y in range(top_dome_y + 1, 63):
                    c.set_block(x, y, z, MAT['water'])

    for x in range(165, 171):
        for z in range(-62, -59):
            c.set_block(x, 52, z, MAT['light_sea'] if (x + z) % 2 == 0 else MAT['wall_quartz'])
            for y in range(53, 56):
                c.set_block(x, y, z, 'minecraft:air')
            c.set_block(x, 56, z, MAT['light_sea'] if x in (166, 169) else MAT['glass_clear'])
        c.set_block(x, 53, -61, MAT['carpet_cyan'])
        c.set_block(x, 53, -62, MAT['carpet_cyan'])

    for z_path in range(-66, -58):
        c.set_block(168, 53, z_path, MAT['carpet_cyan'])

    c.fill(dcx, 53, dcz, dcx, 57, dcz, MAT['light_sea'])
    for d_off in (-3, 3):
        for dz_b in (-1, 0, 1):
            c.set_block(dcx + d_off, 53, dcz + dz_b, stair('smooth_quartz', 'west' if d_off < 0 else 'east', 'bottom'))

    for z in range(-93, -89):
        for x in range(165, 168):
            c.set_block(x, 62, z, MAT['light_sea'] if x == 166 else MAT['wood_dark'])
            c.set_block(x, 63, z, MAT['slab_spruce_b'])

    for x in range(160, 173):
        for z in range(-90, -79):
            is_edge = (x in (160, 172) or z in (-90, -80))
            if is_edge:
                c.set_block(x, 62, z, MAT['light_sea'] if (x + z) % 3 == 0 else MAT['wall_quartz'])
                c.set_block(x, 63, z, MAT['wall_quartz'])
            else:
                c.set_block(x, 62, z, MAT['wood_dark'])
                c.set_block(x, 63, z, MAT['wood_warm'] if (x + z) % 2 == 0 else MAT['wood_dark'])

    for z in range(-88, -82, 2):
        place_barrel(c, 161, 64, z, 'east')
        c.set_block(161, 65, z, MAT['light_ochre'])
        c.set_block(163, 64, z, 'minecraft:iron_block')
        c.set_block(163, 65, z, MAT['end_rod_up'])
    c.set_block(161, 64, -81, 'minecraft:water_cauldron[level=3]')

    for dz_b, bh in [(-86, 65), (-83, 67)]:
        c.fill(171, 64, dz_b, 171, bh, dz_b, MAT['wall_quartz'])
        c.set_block(170, 64, dz_b, stair('smooth_quartz', 'east', 'bottom'))
        c.fill(172, bh, dz_b, 176, bh, dz_b, MAT['slab_quartz_t'])
        c.set_block(176, bh, dz_b, MAT['light_sea'])
        c.set_block(176, bh + 1, dz_b, MAT['carpet_white'])

    c.fill(161, 64, -89, 161, 69, -89, MAT['iron_bars'])
    c.set_block(161, 70, -89, MAT['light_ochre'])
    for fx in range(162, 166):
        for fy in range(67, 70):
            is_diag = ((fx - 162) == (69 - fy))
            c.set_block(fx, fy, -89, MAT['wall_white'] if is_diag else MAT['red_concrete'])

def build_seaside_market(c: WorldCanvas):
    for z in range(-132, -97):
        if -114 <= z <= -106:
            continue
        for x in range(105, 132):
            if x in (116, 121) and z % 4 == 0:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'])
            elif (x + z) % 3 == 0:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_dio'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])

    for z in range(-115, -104):
        for x in range(114, 124):
            if x in (114, 123):
                c.set_block(x, Y_BASE + 1, z, MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 2, z, MAT['pane_black'])
                if z in (-114, -110, -106):
                    c.set_block(x, Y_BASE + 2, z, MAT['light_ochre'])
                    c.set_block(x, Y_BASE + 3, z, MAT['slab_quartz_b'])
            else:
                c.set_block(x, Y_BASE + 1, z, MAT['slab_dark_b'] if -113 <= z <= -107 else MAT['slab_quartz_b'])

    def build_market_stall(sx1, sz1, awning_color, role, facing='east'):
        sx2, sz2 = sx1 + 4, sz1 + 4
        c.fill(sx1, Y_BASE, sz1, sx2, Y_BASE, sz2, MAT['wood_dark'])
        for px in (sx1, sx2):
            for pz in (sz1, sz2):
                c.fill(px, Y_BASE + 1, pz, px, Y_BASE + 3, pz, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        for x in range(sx1 - 1, sx2 + 2):
            for z in range(sz1 - 1, sz2 + 2):
                stripe = ((x + z) % 2 == 0)
                if sx1 <= x <= sx2 and sz1 <= z <= sz2:
                    c.set_block(x, Y_BASE + 4, z, awning_color if stripe else MAT['white_wool'])
                else:
                    c.set_block(x, Y_BASE + 4, z, MAT['slab_quartz_b'])
        c.set_block((sx1 + sx2) // 2, Y_BASE + 3, (sz1 + sz2) // 2, MAT['light_ochre'])

        front_x = sx2 if facing == 'east' else sx1
        back_x = sx1 if facing == 'east' else sx2
        for z in range(sz1 + 1, sz2):
            c.set_block(front_x, Y_BASE, z, MAT['light_ochre'])
            c.set_block(front_x, Y_BASE + 1, z, MAT['wall_quartz'])
            c.set_block(front_x, Y_BASE + 2, z, MAT['carpet_white'])
            place_barrel(c, back_x, Y_BASE + 1, z, 'up')
        if role == 'seafood_grill':
            place_smoker(c, back_x, Y_BASE + 2, sz1 + 1, facing=facing, lit='true')
            c.set_block(back_x, Y_BASE + 2, sz1 + 2, 'minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]')
            c.set_block(front_x, Y_BASE + 2, sz1 + 3, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
        elif role == 'tropical_fruit':
            c.set_block(back_x, Y_BASE + 2, sz1 + 1, MAT['melon_block'])
            c.set_block(back_x, Y_BASE + 2, sz1 + 2, MAT['pumpkin_block'])
            c.set_block(back_x, Y_BASE + 2, sz1 + 3, MAT['hay_y'])
        elif role == 'coral_curio':
            c.set_block(back_x, Y_BASE + 2, sz1 + 1, MAT['coral_tube'])
            c.set_block(back_x, Y_BASE + 2, sz1 + 2, MAT['light_sea'])
            c.set_block(back_x, Y_BASE + 2, sz1 + 3, MAT['coral_brain'])
        elif role == 'gelato_bar':
            place_brewing_stand(c, front_x, Y_BASE + 2, sz1 + 2)
            c.set_block(back_x, Y_BASE + 2, sz1 + 1, MAT['light_pearl'])
            c.set_block(back_x, Y_BASE + 2, sz1 + 3, 'minecraft:water_cauldron[level=3]')
        elif role == 'florist':
            c.set_block(back_x, Y_BASE + 2, sz1 + 1, MAT['leaf_fl_azalea'])
            c.set_block(back_x, Y_BASE + 2, sz1 + 2, MAT['leaf_cherry'])
            c.set_block(front_x, Y_BASE + 2, sz1 + 2, 'minecraft:flower_pot')
        else:
            c.set_block(back_x, Y_BASE + 2, sz1 + 1, MAT['packed_ice'])
            c.set_block(back_x, Y_BASE + 2, sz1 + 2, MAT['packed_ice'])
            c.set_block(back_x, Y_BASE + 2, sz1 + 3, MAT['light_sea'])

    build_market_stall(106, -104, MAT['red_wool'], 'seafood_grill', facing='east')
    build_market_stall(125, -104, MAT['orange_wool'], 'tropical_fruit', facing='west')
    build_market_stall(106, -123, MAT['cyan_wool'], 'coral_curio', facing='east')
    build_market_stall(125, -123, MAT['yellow_wool'], 'gelato_bar', facing='west')
    build_market_stall(106, -131, MAT['pink_wool'], 'florist', facing='east')
    build_market_stall(125, -131, MAT['blue_wool'], 'fish_market', facing='west')

    for z in (-129, -125, -121, -102, -99):
        for x in range(111, 125):
            if x % 3 == 0:
                c.set_block(x, Y_BASE + 5, z, MAT['light_ochre'])
                c.set_block(x, Y_BASE + 6, z, MAT['slab_dark_b'])
            else:
                c.set_block(x, Y_BASE + 5, z, MAT['iron_bars'])
        if z in (-127, -101):
            c.set_block(118, Y_BASE, z, MAT['light_ochre'])
            c.set_block(118, Y_BASE + 1, z, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
            c.set_block(118, Y_BASE + 2, z, MAT['carpet_white'])
            c.set_block(117, Y_BASE + 1, z, stair('smooth_quartz', 'east', 'bottom'))
            c.set_block(119, Y_BASE + 1, z, stair('smooth_quartz', 'west', 'bottom'))

def build_coastal_boathouse(c: WorldCanvas):
    bx1, bx2, bz1, bz2 = 136, 158, -127, -109
    z_mid = (bz1 + bz2) // 2

    for x in range(bx1, bx2 + 1):
        for z in range(bz1, bz2 + 1):
            if -121 <= z <= -115 and x >= 140:
                c.set_block(x, 59, z, MAT['light_sea'] if (x + z) % 4 == 0 else MAT['stone_pol_and'])
                for wy in range(60, 63):
                    c.set_block(x, wy, z, MAT['water'])
                for wy in range(63, Y_BASE + 7):
                    c.set_block(x, wy, z, 'minecraft:air')
            else:
                c.fill(x, 58, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
                c.set_block(x, Y_BASE, z, MAT['wood_dark'] if (x + z) % 2 == 0 else MAT['wood_warm'])

    for y in range(Y_BASE + 1, Y_BASE + 6):
        for x in range(bx1, bx2 + 1):
            for z in (bz1, bz2):
                is_post = (x == bx1 or x == bx2 or (x - bx1) % 4 == 0)
                if is_post:
                    c.set_block(x, y, z, MAT['beam_dark_y'])
                elif y in (Y_BASE + 1, Y_BASE + 5):
                    c.set_block(x, y, z, MAT['stone_pol_and'] if y == Y_BASE + 1 else MAT['wood_dark'])
                else:
                    c.set_block(x, y, z, MAT['glass_clear'] if (x // 4) % 2 == 0 else MAT['wall_white'])
        for z in range(bz1 + 1, bz2):
            if abs(z - z_mid) <= 1 and y <= Y_BASE + 3:
                c.set_block(bx1, y, z, 'minecraft:air')
            else:
                c.set_block(bx1, y, z, MAT['wall_white'] if y < Y_BASE + 5 else MAT['wood_dark'])
            if -122 <= z <= -114:
                if y == Y_BASE + 5:
                    c.set_block(bx2, y, z, MAT['iron_bars'])
                else:
                    c.set_block(bx2, y, z, 'minecraft:air')
            else:
                c.set_block(bx2, y, z, MAT['beam_dark_y'] if z in (-123, -113) else MAT['wall_white'])

    for z in range(bz1 - 1, bz2 + 2):
        dist_z = abs(z - z_mid)
        ry = Y_BASE + 6 + max(0, int(round((1.0 - dist_z / 10.0) * 4.0)))
        for x in range(bx1 - 1, bx2 + 2):
            if bx1 <= x <= bx2 and ry > Y_BASE + 6:
                if x in (bx1, bx2):
                    c.fill(x, Y_BASE + 6, z, x, ry - 1, z, MAT['wall_white'] if dist_z > 2 else MAT['glass_clear'])
                else:
                    c.set_block(x, ry - 1, z, MAT['light_ochre'] if (x % 4 == 0 and z % 3 == 0) else MAT['wood_dark'])
            c.set_block(x, ry, z, MAT['wood_dark'] if dist_z <= 1 else MAT['wall_white'])
            c.set_block(x, ry + 1, z, MAT['slab_quartz_b'] if dist_z <= 1 else MAT['slab_dark_b'])

    for hx in (144, 151):
        c.fill(hx, Y_BASE + 6, -122, hx, Y_BASE + 6, -114, MAT['beam_dark_z'])
        c.set_block(hx, Y_BASE + 5, z_mid, MAT['chain_y'])
        c.set_block(hx, Y_BASE + 4, z_mid, MAT['lantern_hang'])

    for x in range(138, 155, 3):
        place_barrel(c, x, Y_BASE + 1, bz1 + 1, 'south')
        c.set_block(x, Y_BASE + 2, bz1 + 1, MAT['lantern_stand'] if x % 2 == 0 else 'minecraft:air')
    c.set_block(138, Y_BASE + 1, bz2 - 1, 'minecraft:crafting_table')
    c.set_block(139, Y_BASE + 1, bz2 - 1, 'minecraft:smithing_table')
    c.set_block(141, Y_BASE + 1, bz2 - 1, MAT['hay_y'])

    for x in range(143, 154):
        half_w = 1 if x in (143, 152) else (0 if x == 153 else 2)
        for dz in range(-half_w, half_w + 1):
            z = z_mid + dz
            c.set_block(x, 62, z, MAT['wood_dark'])
            if abs(dz) == half_w or x in (143, 153):
                c.set_block(x, 63, z, MAT['wall_quartz'] if x >= 150 else MAT['slab_dark_b'])
            else:
                c.set_block(x, 63, z, MAT['light_ochre'] if x in (146, 150) and dz == 0 else MAT['carpet_white'])
    c.fill(149, 64, z_mid - 1, 149, 64, z_mid + 1, MAT['pane_black'])
    c.set_block(147, 63, z_mid - 1, stair('smooth_quartz', 'west', 'bottom'))
    c.set_block(147, 63, z_mid + 1, stair('smooth_quartz', 'west', 'bottom'))
    c.set_block(142, 63, z_mid, MAT['frame_dark'])
    c.set_block(153, 64, z_mid, MAT['end_rod_up'])

def build_marina_piers_and_yachts(c: WorldCanvas):
    for x in range(138, 179):
        if (x - 138) % 6 == 0:
            for pz in (-101, -94):
                c.fill(x, 50, pz, x, Y_BASE - 1, pz, MAT['frame_dark'])
                c.set_block(x, 62, pz, MAT['light_sea'])
        for z in range(-101, -93):
            if z in (-101, -94) or x == 178:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 4 == 0 else MAT['wall_quartz'])
                if not ((z == -101 and 158 <= x <= 162) or (z == -94 and 165 <= x <= 167)):
                    if x % 6 == 0:
                        c.set_block(x, Y_BASE + 1, z, MAT['wall_deep_post'])
                        c.set_block(x, Y_BASE + 2, z, MAT['lantern_stand'])
                    else:
                        c.set_block(x, Y_BASE + 1, z, MAT['iron_bars'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (x // 2) % 2 == 0 else MAT['wood_dark'])

    ycx, ycz = 161, -105
    for x in range(152, 171):
        dx = x - ycx
        half_w = 0 if abs(dx) >= 8 else (1 if abs(dx) >= 5 else 2)
        for dz in range(-half_w, half_w + 1):
            z = ycz + dz
            c.set_block(x, 61, z, MAT['frame_dark'])
            c.set_block(x, 62, z, MAT['wall_white'])
            if abs(dz) == half_w or abs(dx) >= 7:
                c.set_block(x, 63, z, MAT['wall_quartz'])
                c.set_block(x, 64, z, MAT['slab_quartz_b'])
            else:
                c.set_block(x, 63, z, MAT['light_ochre'] if dx % 3 == 0 and dz == 0 else MAT['wood_warm'])
    c.fill(157, 64, ycz - 1, 164, 64, ycz + 1, MAT['wall_white'])
    c.fill(158, 64, ycz, 163, 64, ycz, MAT['light_sea'])
    c.fill(158, 65, ycz - 1, 163, 65, ycz + 1, MAT['slab_quartz_b'])
    c.fill(ycx, 64, ycz, ycx, 81, ycz, MAT['beam_spruce_y'])
    c.set_block(ycx, 82, ycz, MAT['end_rod_up'])
    c.fill(154, 66, ycz, ycx - 1, 66, ycz, MAT['beam_spruce_x'])
    for y in range(67, 80):
        sail_len = max(1, (80 - y) // 2)
        for sx in range(ycx - sail_len, ycx):
            c.set_block(sx, y, ycz + (1 if y <= 75 else 0), MAT['white_wool'] if (sx + y) % 3 != 0 else MAT['wall_quartz'])
        jib_len = max(1, (78 - y) // 3)
        if y <= 77:
            c.set_block(ycx + jib_len + 1, y, ycz, MAT['white_wool'])

    for x in range(146, 186):
        if (x - 146) % 6 == 0 or x == 185:
            for pz in (-148, -141, -134):
                c.fill(x, 50, pz, x, Y_BASE - 1, pz, MAT['frame_dark'])
                c.set_block(x, 62, pz, MAT['light_sea'])
        for z in range(-148, -133):
            if x == 185:
                c.set_block(x, 62, z, MAT['wall_black'])
                c.set_block(x, 63, z, MAT['wall_black'])
                c.set_block(x, Y_BASE, z, MAT['yellow_concrete'] if z % 2 == 0 else MAT['wall_black'])
            elif z in (-148, -134):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 4 == 0 else MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 1, z, MAT['iron_bars'])
                if x % 8 == 0:
                    build_lamppost(c, x, Y_BASE + 1, z, style='courtyard')
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'] if (x + z) % 2 == 0 else MAT['stone_smooth'])

def build_cruise_boarding_terminal(c: WorldCanvas):
    tx1, tx2, tz1, tz2 = 108, 146, -170, -134
    y_1f = Y_BASE
    y_2f = Y_BASE + 6
    y_roof = Y_BASE + 12
    z_mid = (tz1 + tz2) // 2

    c.fill(tx1, y_1f, tz1, tx2, y_1f, tz2, MAT['wall_quartz'])
    c.fill(tx1, y_1f + 1, tz1, tx2, y_roof - 1, tz2, MAT['wall_white'])
    c.fill(tx1 + 1, y_1f + 1, tz1 + 1, tx2 - 1, y_roof - 1, tz2 - 1, 'minecraft:air')

    for x in range(tx1 + 1, tx2):
        for z in range(tz1 + 1, tz2):
            if (x - tx1) % 4 == 0 and (z - tz1) % 4 == 0:
                c.set_block(x, y_1f, z, MAT['light_sea'])
            elif (x + z) % 2 == 0:
                c.set_block(x, y_1f, z, MAT['wall_quartz'])
            else:
                c.set_block(x, y_1f, z, MAT['stone_dio'])

    build_curtain_wall(c, tx1, y_1f + 1, tz1 + 3, tx1, y_roof - 1, tz2 - 3,
                       MAT['glass_black'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, tx2, y_1f + 1, tz1 + 3, tx2, y_roof - 1, tz2 - 3,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, tx1 + 3, y_1f + 1, tz1, tx2 - 3, y_roof - 1, tz1,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, tx1 + 3, y_1f + 1, tz2, tx2 - 3, y_roof - 1, tz2,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)

    c.fill(104, y_2f, -158, tx1, y_2f, -146, MAT['wood_dark'])
    c.fill(104, y_2f + 1, -158, tx1, y_2f + 1, -146, MAT['wall_white'])
    for pz in (-157, -147):
        c.fill(105, y_1f + 1, pz, 105, y_2f - 1, pz, MAT['wall_quartz'])
        c.set_block(106, y_2f, pz, MAT['light_ochre'])
    c.fill(tx1, y_1f + 1, -154, tx1, y_1f + 4, -150, 'minecraft:air')
    c.fill(tx2, y_1f + 1, -143, tx2, y_1f + 4, -139, 'minecraft:air')
    c.fill(tx1 + 16, y_1f + 1, tz2, tx1 + 20, y_1f + 4, tz2, 'minecraft:air')

    c.fill(113, y_1f + 1, -166, 113, y_1f + 4, -156, MAT['wall_black'])
    for z in range(-165, -156, 2):
        c.set_block(113, y_1f + 3, z, MAT['light_sea'] if z % 4 == 0 else MAT['light_verdant'])
        c.set_block(113, y_1f + 2, z, MAT['light_ochre'])
    for z in range(-166, -155):
        c.set_block(116, y_1f, z, MAT['light_ochre'] if z % 2 == 0 else MAT['wood_dark'])
        c.set_block(116, y_1f + 1, z, MAT['wall_quartz'])
        c.set_block(116, y_1f + 2, z, MAT['slab_quartz_b'])
        if z % 3 == 0:
            place_lectern(c, 115, y_1f + 1, z, 'east')

    for az in (-155, -151, -147):
        c.fill(124, y_1f + 1, az - 1, 124, y_1f + 3, az - 1, MAT['frame_dark'])
        c.fill(124, y_1f + 1, az + 1, 124, y_1f + 3, az + 1, MAT['frame_dark'])
        c.fill(124, y_1f + 4, az - 1, 124, y_1f + 4, az + 1, MAT['light_sea'])

    build_illuminated_carpet_rug(c, 128, y_1f, -166, 143, -154, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_sofa(c, 130, y_1f, -164, length=6, facing='south')
    build_outdoor_sofa(c, 130, y_1f, -156, length=6, facing='north')
    build_outdoor_bar(c, 114, y_1f, -140, length=8)
    build_indoor_planter(c, 142, y_1f, -166, tall=True)
    build_indoor_planter(c, 142, y_1f, -137, tall=True)

    c.fill(127, y_2f, tz1 + 1, tx2 - 1, y_2f, tz2 - 1, MAT['wood_dark'])
    for z in range(tz1 + 1, tz2):
        c.set_block(127, y_2f, z, MAT['light_ochre'] if z % 3 == 0 else MAT['wall_quartz'])
        if not (-147 <= z <= -141):
            c.set_block(127, y_2f + 1, z, MAT['pane_black'])
    build_recessed_ceiling_grid(c, 128, y_2f, tz1 + 3, tx2 - 2, tz2 - 3, step_x=4, step_z=4, light_mat=MAT['light_ochre'])
    build_illuminated_carpet_rug(c, 130, y_2f, -165, 143, -148, MAT['carpet_white'], MAT['carpet_lgray'])
    build_straight_stairs(c, 122, y_1f + 1, -146, width=5, height=y_2f - y_1f, direction='east', stair_prefix='smooth_quartz', hidden_lights=True)

    c.fill(tx2, y_2f + 1, -142, tx2, y_2f + 3, -140, 'minecraft:air')
    build_outdoor_sofa(c, 132, y_2f, -162, length=6, facing='south')
    build_outdoor_sofa(c, 132, y_2f, -152, length=6, facing='north')
    place_lectern(c, 143, y_2f + 1, -143, 'west')
    place_lectern(c, 143, y_2f + 1, -139, 'west')

    for x in range(tx1 - 2, tx2 + 3):
        wave_dy = int(round(0.8 * math.sin((x - tx1) * math.pi / 12.0)))
        ry = y_roof + max(0, wave_dy)
        for z in range(tz1 - 2, tz2 + 3):
            if tx1 <= x <= tx2 and tz1 <= z <= tz2 and abs(z - z_mid) <= 4 and x % 2 == 0:
                c.set_block(x, ry, z, MAT['glass_clear'])
            else:
                c.set_block(x, ry, z, MAT['wall_white'])
                c.set_block(x, ry + 1, z, MAT['slab_quartz_b'])
            if tx1 + 2 <= x <= tx2 - 2 and tz1 + 2 <= z <= tz2 - 2 and x % 4 == 0 and z % 4 == 0:
                c.set_block(x, ry - 1, z, MAT['light_ochre'])

    for cx_ch in (118, 135):
        for cz_ch in (-160, -144):
            build_crystal_chandelier(c, cx_ch, y_roof, cz_ch, drop=3, style='grand')

    for x in range(146, 187):
        if (x - 146) % 8 == 0 and x < 185:
            c.fill(x, Y_BASE + 1, -143, x, y_2f - 1, -143, MAT['frame_dark'])
            c.fill(x, Y_BASE + 1, -139, x, y_2f - 1, -139, MAT['frame_dark'])
        for z in range(-143, -138):
            c.set_block(x, y_2f, z, MAT['light_ochre'] if (x % 3 == 0 and z == -141) else MAT['wall_quartz'])
            c.set_block(x, y_2f + 4, z, MAT['light_sea'] if (x % 4 == 0 and z == -141) else MAT['slab_quartz_b'])
            if z in (-143, -139):
                for y in range(y_2f + 1, y_2f + 4):
                    c.set_block(x, y, z, MAT['frame_dark'] if x % 4 == 0 else MAT['glass_clear'])
            else:
                for y in range(y_2f + 1, y_2f + 4):
                    c.set_block(x, y, z, 'minecraft:air')
                if z == -141:
                    c.set_block(x, y_2f + 1, z, MAT['carpet_red'])
    for z_gw in range(-142, -139):
        c.set_block(187, y_2f - 1, z_gw, MAT['wall_quartz'])
        c.set_block(187, y_2f, z_gw, stair('smooth_quartz', 'west', 'bottom'))
        for y_gw in range(y_2f + 1, y_2f + 4):
            c.set_block(187, y_gw, z_gw, 'minecraft:air')

def build_headland_lighthouse(c: WorldCanvas):
    """
    V5.3 Relocated, Heightened & Base-Optimized Headland Lighthouse & Harbor Master's Cottage:
      - Relocated 26 blocks northward (Z- direction, from Z=-186 to lcz=-212, lcx=156) and separated
        from both the Cruise Boarding Terminal (Z=-170) and the Harbor Master's Cottage (X=114..124, Z=-196..-186),
        opening up a generous 16-to-26 block coastal plaza around (138, 65, -184)!
      - All walkways and headland terraces are built at flush elevation Y = Y_BASE = 64 (walking surface 65.0)
        with ZERO overlapping seawall railings and ZERO white divider lines cutting across walking areas.
      - The 7-block-wide Lighthouse Grand Approach Promenade (Z=-215..-209, centered on Z=-212) aligns 100%
        with the Lighthouse West Main Entrance Portal (150, 65, -212), while the Cottage Approach (Z=-193..-189)
        aligns 100% with the Cottage West Double Door (114, 65, -191).
      - Heightened Lighthouse (y_gal = 105, total pinnacle Y = 116) with an octagonal buttressed plinth base
        (Y = 64..69), 100% solid Y = 64 floor (eliminating the sunken pit), tight 7x7 inner shaft walls
        (max(|dx|, |dz|) == 3) hugging the 5x5 spiral staircase (start_sector=4, clockwise=False, y_bottom=65..105),
        and unobstructed 3-wide x 3-tall West Entrance foyer!
    """

    for z in range(-229, -170):
        for x in range(126 if z < -218 else 132, 146 if z >= -196 else 137):
            c.fill(x, 54, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
            if (x - 132) % 6 == 0 or (z + 216) % 6 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 4, z, 'minecraft:air')

        if z > -197:
            c.set_block(145, Y_BASE, z, MAT['light_sea'] if z % 4 == 0 else MAT['wall_quartz'])
            c.set_block(145, Y_BASE + 1, z, MAT['pane_black'])

    for z in range(-230, -195):
        for x in range(136, 173):
            d_ell = ((x - 153) / 17.0) ** 2 + ((z + 212) / 15.0) ** 2
            if d_ell <= 1.0:
                c.fill(x, 52, z, x, Y_BASE - 1, z, MAT['stone_pol_and'] if d_ell > 0.78 else MAT['stone'])
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
                c.fill(x, Y_BASE + 1, z, x, Y_BASE + 6, z, 'minecraft:air')
                if 0.84 <= d_ell <= 1.0 and x >= 145:
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                    c.set_block(x, Y_BASE + 1, z, MAT['iron_bars'])
            elif x >= 137:

                c.fill(x, 63, z, x, Y_BASE + 6, z, 'minecraft:air')
                c.fill(x, 46, z, x, 55, z, MAT['stone'])
                c.set_block(x, 56, z, 'minecraft:smooth_sandstone')
                c.set_block(x, 57, z, 'minecraft:sand')
                c.fill(x, 58, z, x, 62, z, MAT['water'])

    for z in range(-193, -188):
        for x in range(104, 114):
            if z in (-193, -189):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    for z in range(-215, -208):
        for x in range(104, 151):
            if z in (-215, -209):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['stone_pol_and'])
            elif z == -212:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 8 == 0 else MAT['stone_dio'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
        if z in (-215, -209):
            for lx_p in (108, 120, 132, 144):
                build_lamppost(c, lx_p, Y_BASE + 1, z, style='courtyard')

    kx1, kx2, kz1, kz2, ky = 114, 124, -196, -186, Y_BASE
    c.fill(kx1, ky, kz1, kx2, ky, kz2, MAT['wood_dark'])
    c.fill(kx1, ky + 1, kz1, kx2, ky + 4, kz2, MAT['wall_white'])
    c.fill(kx1 + 1, ky + 1, kz1 + 1, kx2 - 1, ky + 4, kz2 - 1, 'minecraft:air')
    build_illuminated_carpet_rug(c, kx1 + 2, ky, kz1 + 2, kx2 - 2, kz2 - 2, MAT['carpet_white'], MAT['carpet_lgray'])

    place_double_door(c, kx1, ky + 1, -191, 'dark_oak', 'east', 'true')
    place_double_door(c, kx2, ky + 1, -191, 'dark_oak', 'west', 'true')
    c.fill(kx1 + 2, ky + 2, kz1, kx2 - 2, ky + 3, kz1, MAT['glass_clear'])
    c.fill(kx1 + 2, ky + 2, kz2, kx2 - 2, ky + 3, kz2, MAT['glass_clear'])
    place_bed(c, kx1 + 2, ky + 1, kz1 + 2, facing='north', color='red')
    place_lectern(c, kx2 - 2, ky + 1, kz2 - 2, 'north')
    c.set_block((kx1 + kx2) // 2, ky + 4, -191, MAT['light_ochre'])
    build_flat_roof_and_eaves(c, kx1, ky + 5, kz1, kx2, kz2, overhang=1,
                              roof_mat=MAT['red_concrete'], soffit_mat=MAT['wood_dark'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)

    lcx, lcz = 156, -212
    y_floor = Y_BASE
    y_bottom = Y_BASE + 1
    y_gal = 105

    for dx in range(-6, 7):
        for dz in range(-6, 7):
            if math.hypot(dx, dz) <= 6.2:
                c.set_block(lcx + dx, y_floor, lcz + dz, MAT['wall_quartz'] if max(abs(dx), abs(dz)) <= 3 else MAT['stone_pol_and'])

    for y in range(y_bottom, y_gal):
        h_rel = y - y_bottom
        r_outer = 5.2 if h_rel < 3 else (4.7 if h_rel < 6 else (4.4 if h_rel < 20 else 4.1))
        is_red_band = ((h_rel // 5) % 2 == 1)
        wall_mat = MAT['red_concrete'] if is_red_band else MAT['wall_white']
        if h_rel < 3:
            wall_mat = MAT['stone_pol_and'] if h_rel == 0 else MAT['wall_quartz']
        elif h_rel == 3:
            wall_mat = MAT['chiseled_deepslate']

        for dx in range(-6, 7):
            for dz in range(-6, 7):
                cheb = max(abs(dx), abs(dz))
                d = math.hypot(dx, dz)
                if cheb <= 2:
                    c.set_block(lcx + dx, y, lcz + dz, 'minecraft:air')
                elif cheb == 3 or d <= r_outer:
                    if (dx == 0 or dz == 0) and h_rel >= 5 and (h_rel % 5 in (2, 3)):
                        c.set_block(lcx + dx, y, lcz + dz, MAT['glass_clear'])
                    elif cheb == 3 and (dx == 0 or dz == 0) and (h_rel % 5 == 0):
                        c.set_block(lcx + dx, y, lcz + dz, MAT['light_ochre'])
                    else:
                        c.set_block(lcx + dx, y, lcz + dz, wall_mat)

    for dx in range(-5, 6):
        for dz in range(-5, 6):
            d = math.hypot(dx, dz)
            if d <= 5.3:
                c.set_block(lcx + dx, y_gal, lcz + dz, MAT['frame_dark'] if d > 4.2 else MAT['wall_quartz'])
                if 4.2 <= d <= 5.3:
                    c.set_block(lcx + dx, y_gal + 1, lcz + dz, MAT['iron_bars'])
                    if dx == 0 or dz == 0:
                        c.set_block(lcx + dx, y_gal, lcz + dz, MAT['light_ochre'])

    build_spiral_staircase(c, lcx, y_bottom, y_gal, lcz, radius=2, start_sector=4, clockwise=False)

    c.set_block(lcx, y_gal, lcz, MAT['light_sea'])
    c.fill(lcx, y_gal + 1, lcz, lcx, y_gal + 3, lcz, 'minecraft:air')

    c.fill(lcx - 6, y_floor, lcz - 1, lcx - 3, y_floor, lcz + 1, MAT['wall_quartz'])
    c.fill(lcx - 6, y_bottom, lcz - 1, lcx - 3, y_bottom + 2, lcz + 1, 'minecraft:air')

    for pz_trim in (lcz - 2, lcz + 2):
        c.fill(lcx - 6, y_bottom, pz_trim, lcx - 6, y_bottom + 3, pz_trim, MAT['pillar_quartz'])
    c.fill(lcx - 6, y_bottom + 3, lcz - 1, lcx - 6, y_bottom + 3, lcz + 1, MAT['wall_chiseled'])
    c.set_block(lcx - 5, y_bottom + 3, lcz, MAT['light_sea'])

    for y in range(y_gal + 1, y_gal + 5):
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                d = math.hypot(dx, dz)
                if 3.0 <= d <= 3.8:
                    is_door = ((dx == 0 and dz < 0) or (dz == 0 and dx != 0)) and (y <= y_gal + 3)
                    is_corner_mullion = (abs(dx) == 3 and abs(dz) == 2) or (abs(dx) == 2 and abs(dz) == 3)
                    if is_door:
                        c.set_block(lcx + dx, y, lcz + dz, 'minecraft:air')
                    elif is_corner_mullion:
                        c.set_block(lcx + dx, y, lcz + dz, MAT['frame_dark'])
                    else:
                        c.set_block(lcx + dx, y, lcz + dz, MAT['glass_clear'])

    for dx in range(-1, 2):
        for dz in range(-1, 2):
            c.set_block(lcx + dx, y_gal + 4, lcz + dz, MAT['light_sea'] if (dx == 0 or dz == 0) else MAT['glass_yellow'])
    for r_beam in range(4, 9):
        c.set_block(lcx + r_beam, y_gal + 4, lcz, MAT['end_rod_e'])
        c.set_block(lcx - r_beam, y_gal + 4, lcz, MAT['end_rod_w'])
        c.set_block(lcx, y_gal + 4, lcz - r_beam, MAT['end_rod_n'])
        c.set_block(lcx, y_gal + 4, lcz + r_beam, MAT['end_rod_s'])

    for dy, dr in [(5, 3.8), (6, 2.8), (7, 1.8), (8, 1.0)]:
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                if math.hypot(dx, dz) <= dr:
                    c.set_block(lcx + dx, y_gal + dy, lcz + dz, MAT['red_concrete'])
    c.set_block(lcx, y_gal + 9, lcz, MAT['light_shroom'])
    c.fill(lcx, y_gal + 10, lcz, lcx, y_gal + 11, lcz, MAT['end_rod_up'])

def step10_seaside_park_complex(c: WorldCanvas):
    build_seaside_park_grounds_and_boardwalk(c)
    build_seafood_restaurant(c)
    build_musical_fountain_plaza(c)
    build_resort_pool_bar_and_loungers(c)
    build_golden_beach_and_lifeguard_tower(c)
    build_underwater_gallery_and_diving_spot(c)
    build_seaside_market(c)
    build_coastal_boathouse(c)
    build_marina_piers_and_yachts(c)
    build_cruise_boarding_terminal(c)
    build_headland_lighthouse(c)

    park_trees = [
        (104, -39, 'ornamental'), (104, -62, 'birch_mix'),
        (104, -96, 'ornamental'), (104, -135, 'birch_mix'),
        (104, -175, 'ornamental'), (126, -176, 'oak_mix'),
    ]
    for idx, (ptx, ptz, pst) in enumerate(park_trees):
        build_custom_tree(c, ptx, Y_BASE, ptz, height=8, style=pst, seed=7700 + idx, max_radius=2)
