"""
zone_urban_district.py — V5.3 Expansion: Main Urban District Prototype (大型主城区雏形)
=======================================================================================
Located directly in the `X-` (West / inland) direction behind the Large Seaside Beach Park
(`X in [-304, 23], Z in [-632, -448]`), separated from the North Sports Complex (`Z = -396`)
by the 51-block Scenic Parkland Transition Belt (`Z = -447..-397`), and backed by over
700 blocks of pre-generated `seed_world` reserve (`X down to -1024, Z down to -1024`)
for future urban expansion rounds.

Architectural & Urban Components:
  1. Custom Bulldozed & Graded Metropolitan Platform (`X = -304..23, Z = -632..-448, Y = 64`):
     - Bulldozes all natural hills/trees (`Y = 46..175`) and establishes a crisp urban datum.
  2. Primary Metropolitan Arterial Road Grid (Zero Overlapping Dividers, Full Zebra Crosswalks):
     - Oceanfront Metro Avenue (`滨海市政大道`, `X = 12..23, Z = -628..-448`): 12-block-wide
       boulevard with dual asphalt carriageways, central landscaped streetlamp median, sidewalks,
       and crosswalks at `Z = -460`, `-536`, and `-614` linking directly into the Beach Park.
     - Grand Civic Boulevard (`中央市政大道`, `Z = -542..-530, X = -304..23`): 13-block-wide
       central East-West axis aligned with the Beach Clubhouse & Overwater Pier (`Z = -536`),
       extending to the Western Metropolitan Expansion Gateway (`X = -300`).
     - South & North Urban Avenues (`Z = -464..-456` and `Z = -618..-610`, `X = -304..23`).
     - Two North-South Cross Avenues (`X = -96..-86` and `X = -204..-194`, `Z = -628..-448`).
  3. Central Civic Plaza, Metropolitan Obelisk & "Seaside Central" Underground Metro Hub
     (`X = -84..11, Z = -562..-510, Y = 55..78`):
     - Glass-canopy Metro Entrance Pavilion (`X = -38..-16, Z = -556..-546`) with a wide
       straight staircase descending to a vaulted subterranean ticket concourse & twin-track
       subway platform (`Y = 56..61`) featuring a Pure-Voxel Modern Metro Train (`X = -76..-36`).
     - Central Metropolitan Obelisk & Fountain Plaza (`center -56, -536`).
  4. 3-Story Modernist Commercial & Retail Galleria ("The Coastal Galleria",
     `X = -78..-22, Z = -504..-472, Y = 64..82`):
     - 1F Luxury Retail & Café Colonnade, 2F Design Studios (`Y = 70`), 3F Sky Garden (`Y = 77`),
       connected via an 8-sector spiral staircase at `(-28, -478)`.
  5. 4-Story Boutique Seaside Hotel Prototype ("Azure Bay Hotel",
     `X = -78..-22, Z = -600..-568, Y = 64..88`):
     - 1F Grand Lobby, 2F/3F Suites (`Y = 71, 77`), 4F Rooftop Sky Lounge (`Y = 83`),
       connected via an 8-sector spiral staircase at `(-28, -574)`.
  6. Urban Pocket Park, Innovation Hub Pavilion & Reserved Future Expansion Superblocks
     (`X = -300..-98, Z = -608..-466`):
     - Landscaped urban park, modular superblock utility/road stubs, and Western Expansion
       Gateway Arch (`X = -300, Z = -542..-530`) ready for V5.4+ high-rise & civic expansion.
"""

import math
from config import Y_BASE, MAT, SOFT_FLOWERS
from world_canvas import WorldCanvas
from arch_lib import (
    stair,
    place_bed, place_lectern, place_double_door,
    build_recessed_ceiling_grid, build_crystal_chandelier, build_illuminated_carpet_rug,
    build_floor_lamp, build_indoor_planter,
    build_curtain_wall, build_flat_roof_and_eaves,
    build_spiral_staircase, build_straight_stairs,
    build_lamppost, build_fountain, build_hedgerow_line,
    build_custom_tree, build_patio_umbrella,
    build_outdoor_sofa, build_outdoor_bar,
)

def _bulldoze_and_grade_urban_foundation(c: WorldCanvas):
    """
    1. Bulldozes natural terrain in `X = -306..23, Z = -634..-448` (`Y = 46..175`)
       and grades a clean metropolitan foundation at `Y = Y_BASE = 64`.
    """
    stone_id = c.get_or_register(MAT['stone'])
    dirt_id = c.get_or_register(MAT['dirt'])
    grass_id = c.get_or_register(MAT['grass_block'])
    air_id = c.air_id

    for z in range(c.z_min, -447):
        for x in range(c.x_min, 24):
            for y in range(48, c.y_max + 1):
                c.set_block_id(x, y, z, air_id)
            for y in range(46, Y_BASE - 3):
                c.set_block_id(x, y, z, stone_id)
            c.set_block_id(x, Y_BASE - 3, z, dirt_id)
            c.set_block_id(x, Y_BASE - 2, z, dirt_id)
            c.set_block_id(x, Y_BASE - 1, z, dirt_id)
            c.set_block_id(x, Y_BASE, z, grass_id)

def _build_metropolitan_arterial_road_grid(c: WorldCanvas):
    """
    2. Builds the Metropolitan Arterial Road Grid across `X = -304..23, Z = -628..-448`
       with clean 4-way intersections, zebra crosswalks, and zero overlapping divider lines.
    """
    ew_bands = [
        (-464, -456, -460),
        (-542, -530, -536),
        (-618, -610, -614),
    ]
    ns_bands = [
        (12, 23, 17),
        (-96, -86, -91),
        (-204, -194, -199),
    ]

    def in_ew_road(z):
        return any(z0 <= z <= z1 for z0, z1, _ in ew_bands)

    def in_ns_road(x):
        return any(x0 <= x <= x1 for x0, x1, _ in ns_bands)

    for z0, z1, z_mid in ew_bands:
        for z in range(z0, z1 + 1):
            for x in range(c.x_min, 24):
                is_inter = in_ns_road(x)
                if is_inter:

                    c.set_block(x, Y_BASE, z, MAT['wall_gray'])
                    continue
                if z in (z0, z1):
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                elif z in (z0 + 1, z1 - 1):
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
                elif z == z_mid:
                    if z1 - z0 >= 12:

                        c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['moss_block'])
                        if x % 6 != 0 and x % 2 == 0:
                            c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x + z) % len(SOFT_FLOWERS)])
                    else:
                        c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if x % 4 in (0, 1) else MAT['wall_gray'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['wall_gray'])
            if z in (z0 + 1, z1 - 1):
                for lx in range(-296, 10, 18):
                    if not in_ns_road(lx) and not in_ns_road(lx - 2) and not in_ns_road(lx + 2):
                        build_lamppost(c, lx, Y_BASE + 1, z, style='avenue')

    for x0, x1, x_mid in ns_bands:
        for z in range(c.z_min, -447):
            is_inter = in_ew_road(z)
            for x in range(x0, x1 + 1):
                if is_inter:

                    is_ew_edge = any(z in (zb0 + 1, zb1 - 1) for zb0, zb1, _ in ew_bands)
                    is_ns_edge = (x in (x0 + 1, x1 - 1))
                    if is_ew_edge and (x0 + 2 <= x <= x1 - 2) and (x % 2 == 0):
                        c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                    elif is_ns_edge and (z % 2 == 0):
                        c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                    else:
                        c.set_block(x, Y_BASE, z, MAT['wall_gray'])
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
                    continue

                if x in (x0, x1):
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                elif x in (x0 + 1, x1 - 1):
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
                elif (x1 - x0 == 11 and x in (17, 18)) or (x == x_mid):
                    if x1 - x0 == 11:
                        c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['moss_block'])
                        if z % 6 != 0 and z % 2 == 0:
                            c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x + z) % len(SOFT_FLOWERS)])
                    else:
                        c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if z % 4 in (0, 1) else MAT['wall_gray'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['wall_gray'])
            if z % 16 == 0 and not is_inter and not in_ew_road(z - 2) and not in_ew_road(z + 2):
                build_lamppost(c, x0 + 1, Y_BASE + 1, z, style='avenue')
                build_lamppost(c, x1 - 1, Y_BASE + 1, z, style='avenue')

def _build_central_civic_plaza_and_metro_hub(c: WorldCanvas):
    """
    3. Central Civic Plaza, Metropolitan Obelisk & "Seaside Central" Underground Metro Hub
       (`X = -84..10, Z = -564..-508, Y = 55..80`)
    """

    for z in range(-564, -507):
        if -542 <= z <= -530:
            continue
        for x in range(-84, 11):
            if (x + 84) % 6 == 0 or (z + 564) % 6 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 8, z, 'minecraft:air')

    build_fountain(c, -56, Y_BASE, -554, radius=5)
    build_fountain(c, -56, Y_BASE, -518, radius=5)

    for dx in range(-3, 4):
        for dz in range(-3, 4):
            if abs(dx) + abs(dz) <= 4:
                c.set_block(-56 + dx, Y_BASE, -536 + dz, MAT['stone_pol_and'])
                c.set_block(-56 + dx, Y_BASE + 1, -536 + dz, MAT['slab_quartz_b'] if abs(dx) + abs(dz) > 2 else MAT['wall_chiseled'])
    for dy in range(2, 16):
        rad = 1 if dy < 10 else 0
        for dx in range(-rad, rad + 1):
            for dz in range(-rad, rad + 1):
                if abs(dx) + abs(dz) <= 1:
                    c.set_block(-56 + dx, Y_BASE + dy, -536 + dz, MAT['light_sea'] if dy % 4 == 0 else MAT['wall_quartz'])
    c.set_block(-56, Y_BASE + 16, -536, MAT['gold_block'])
    c.set_block(-56, Y_BASE + 17, -536, MAT['light_pearl'])
    c.fill(-56, Y_BASE + 18, -536, -56, Y_BASE + 19, -536, MAT['end_rod_up'])

    mx1, mx2, mz1, mz2 = -80, -16, -560, -545
    y_plat = 57
    y_track = 56
    c.fill(mx1, y_track - 1, mz1, mx2, Y_BASE - 1, mz2, MAT['deepslate_tiles'])
    c.fill(mx1 + 1, y_track, mz1 + 1, mx2 - 1, Y_BASE - 2, mz2 - 1, 'minecraft:air')

    for x in range(mx1 + 1, mx2):
        for z in range(mz1 + 1, mz2):
            if (x - mx1) % 4 == 0:
                c.set_block(x, Y_BASE - 1, z, MAT['deepslate_tiles'])
            else:
                c.set_block(x, Y_BASE - 1, z, MAT['light_sea'] if (x % 4 == 2 and z in (-556, -549)) else MAT['wall_quartz'])

    for x in range(mx1 + 1, mx2):
        for z in range(-554, -545):
            if z == -554:

                c.set_block(x, y_plat, z, MAT['yellow_concrete'] if x % 2 == 0 else MAT['light_ochre'])
            else:
                c.set_block(x, y_plat, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])

        for z in range(-559, -554):
            c.set_block(x, y_track, z, MAT['stone_and'] if z not in (-558, -556) else MAT['iron_block'])

    for x in range(-76, -39):
        is_car_gap = (x == -58)
        if is_car_gap:
            c.fill(x, y_track + 1, -558, x, y_track + 3, -556, MAT['frame_dark'])
            continue
        for z in (-558, -557, -556):
            c.set_block(x, y_track + 1, z, MAT['wall_quartz'] if z != -557 else MAT['light_ochre'])
            c.set_block(x, y_track + 4, z, MAT['slab_quartz_b'] if z != -557 else MAT['cyan_concrete'])

        is_door = (x in (-70, -69, -64, -63, -52, -51, -46, -45))
        for y_t in (y_track + 2, y_track + 3):
            c.set_block(x, y_t, -558, MAT['glass_cyan'] if x % 3 != 0 else MAT['wall_white'])
            if is_door:
                c.set_block(x, y_t, -556, 'minecraft:air')
            else:
                c.set_block(x, y_t, -556, MAT['glass_clear'] if y_t == y_track + 3 else MAT['wall_white'])
        if x in (-76, -40):
            c.fill(x, y_track + 1, -558, x, y_track + 3, -556, MAT['cyan_concrete'])
            c.set_block(x, y_track + 2, -557, MAT['light_sea'])

    c.fill(-32, Y_BASE, -553, -16, Y_BASE + 4, -547, MAT['wall_white'])
    c.fill(-31, Y_BASE, -552, -17, Y_BASE + 4, -548, 'minecraft:air')
    build_curtain_wall(c, -32, Y_BASE + 1, -553, -16, Y_BASE + 4, -553, MAT['glass_cyan'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, -32, Y_BASE + 1, -547, -16, Y_BASE + 4, -547, MAT['glass_cyan'], MAT['glass_clear'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, -32, Y_BASE + 1, -552, -32, Y_BASE + 4, -548, MAT['glass_cyan'], MAT['glass_clear'], MAT['frame_dark'], bay_width=3)
    c.fill(-16, Y_BASE + 1, -551, -16, Y_BASE + 3, -549, 'minecraft:air')
    build_flat_roof_and_eaves(c, -32, Y_BASE + 5, -553, -16, -547, overhang=1,
                              roof_mat=MAT['cyan_concrete'], soffit_mat=MAT['wall_white'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)

    c.fill(-20, Y_BASE, -552, -16, Y_BASE, -548, MAT['wall_quartz'])
    build_straight_stairs(c, -27, y_plat + 1, -551, width=3, height=Y_BASE - y_plat,
                          direction='east', stair_prefix='smooth_quartz', hidden_lights=True)

def _build_commercial_galleria_and_hotel_prototypes(c: WorldCanvas):
    """
    4. Builds the two Flagship Urban Building Prototypes on the East Superblocks (`X = -78..-22`):
       - South Block: 3-Story Modernist Commercial & Retail Galleria ("The Coastal Galleria", `Z = -504..-472, Y = 64..82`)
       - North Block: 4-Story Boutique Seaside Hotel Prototype ("Azure Bay Hotel", `Z = -600..-568, Y = 64..88`)
    """

    gx1, gx2, gz1, gz2 = -78, -22, -504, -472
    y_1f, y_2f, y_3f, y_roof_g = Y_BASE, Y_BASE + 6, Y_BASE + 13, Y_BASE + 18

    for z in range(gz1 - 4, gz2 + 5):
        for x in range(gx1 - 4, gx2 + 6):
            c.set_block(x, y_1f, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            c.fill(x, y_1f + 1, z, x, y_roof_g + 3, z, 'minecraft:air')

    for fy in (y_1f, y_2f, y_3f):
        c.fill(gx1, fy, gz1, gx2, fy, gz2, MAT['wood_dark'] if fy > y_1f else MAT['wall_quartz'])
    c.fill(gx1, y_1f + 1, gz1, gx2, y_roof_g - 1, gz2, MAT['wall_white'])
    c.fill(gx1 + 1, y_1f + 1, gz1 + 1, gx2 - 1, y_2f - 1, gz2 - 1, 'minecraft:air')
    c.fill(gx1 + 1, y_2f + 1, gz1 + 1, gx2 - 1, y_3f - 1, gz2 - 1, 'minecraft:air')
    c.fill(gx1 + 1, y_3f + 1, gz1 + 1, gx2 - 1, y_roof_g - 1, gz2 - 1, 'minecraft:air')

    for fy_low, fy_high in [(y_1f + 1, y_2f - 1), (y_2f + 1, y_3f - 1), (y_3f + 1, y_roof_g - 1)]:
        build_curtain_wall(c, gx1 + 3, fy_low, gz1, gx2 - 3, fy_high, gz1, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=5)
        build_curtain_wall(c, gx1 + 3, fy_low, gz2, gx2 - 3, fy_high, gz2, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=5)
        build_curtain_wall(c, gx1, fy_low, gz1 + 3, gx1, fy_high, gz2 - 3, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
        build_curtain_wall(c, gx2, fy_low, gz1 + 3, gx2, fy_high, gz2 - 3, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)

    build_recessed_ceiling_grid(c, gx1 + 3, y_2f, gz1 + 3, gx2 - 3, gz2 - 3, step_x=5, step_z=5, light_mat=MAT['light_ochre'])
    build_recessed_ceiling_grid(c, gx1 + 3, y_3f, gz1 + 3, gx2 - 3, gz2 - 3, step_x=5, step_z=5, light_mat=MAT['light_pearl'])
    build_flat_roof_and_eaves(c, gx1, y_roof_g, gz1, gx2, gz2, overhang=2, hidden_lights=True)

    build_illuminated_carpet_rug(c, -68, y_1f, -496, -36, -480, MAT['carpet_lgray'], MAT['carpet_white'])
    build_outdoor_bar(c, -64, y_1f, -498, length=10)
    build_outdoor_sofa(c, -56, y_1f, -486, length=8, facing='north')
    build_illuminated_carpet_rug(c, -68, y_2f, -496, -36, -480, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_sofa(c, -56, y_2f, -488, length=8, facing='south')
    build_illuminated_carpet_rug(c, -68, y_3f, -496, -36, -480, MAT['carpet_white'], MAT['carpet_lgray'])
    build_outdoor_bar(c, -62, y_3f, -495, length=8)
    build_crystal_chandelier(c, -50, y_roof_g, -488, drop=2, style='grand')

    build_spiral_staircase(c, -28, y_1f + 1, y_3f, -478, radius=2, start_sector=1, clockwise=True, intermediate_floors=[y_2f])

    place_double_door(c, gx2, y_1f + 1, -488, 'dark_oak', 'west', 'true')
    place_double_door(c, gx1, y_1f + 1, -488, 'dark_oak', 'east', 'true')
    place_double_door(c, -50, y_1f + 1, gz1, 'dark_oak', 'south', 'true')
    place_double_door(c, -50, y_1f + 1, gz2, 'dark_oak', 'north', 'true')

    hx1, hx2, hz1, hz2 = -78, -22, -600, -568
    hy_1f, hy_2f, hy_3f, hy_4f, hy_roof = Y_BASE, Y_BASE + 7, Y_BASE + 13, Y_BASE + 19, Y_BASE + 24

    for z in range(hz1 - 4, hz2 + 5):
        for x in range(hx1 - 4, hx2 + 6):
            c.set_block(x, hy_1f, z, MAT['wall_quartz'] if (x + z) % 3 == 0 else MAT['stone_smooth'])
            c.fill(x, hy_1f + 1, z, x, hy_roof + 3, z, 'minecraft:air')

    for fy in (hy_1f, hy_2f, hy_3f, hy_4f):
        c.fill(hx1, fy, hz1, hx2, fy, hz2, MAT['wood_warm'] if fy > hy_1f else MAT['wall_quartz'])
    c.fill(hx1, hy_1f + 1, hz1, hx2, hy_roof - 1, hz2, MAT['wall_white'])
    for fy_low, fy_high in [(hy_1f + 1, hy_2f - 1), (hy_2f + 1, hy_3f - 1), (hy_3f + 1, hy_4f - 1), (hy_4f + 1, hy_roof - 1)]:
        c.fill(hx1 + 1, fy_low, hz1 + 1, hx2 - 1, fy_high, hz2 - 1, 'minecraft:air')
        build_curtain_wall(c, hx1 + 3, fy_low, hz1, hx2 - 3, fy_high, hz1, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=5)
        build_curtain_wall(c, hx1 + 3, fy_low, hz2, hx2 - 3, fy_high, hz2, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=5)
        build_curtain_wall(c, hx1, fy_low, hz1 + 3, hx1, fy_high, hz2 - 3, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
        build_curtain_wall(c, hx2, fy_low, hz1 + 3, hx2, fy_high, hz2 - 3, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)

    build_recessed_ceiling_grid(c, hx1 + 3, hy_2f, hz1 + 3, hx2 - 3, hz2 - 3, step_x=5, step_z=5, light_mat=MAT['light_ochre'])
    build_recessed_ceiling_grid(c, hx1 + 3, hy_3f, hz1 + 3, hx2 - 3, hz2 - 3, step_x=5, step_z=5, light_mat=MAT['light_pearl'])
    build_recessed_ceiling_grid(c, hx1 + 3, hy_4f, hz1 + 3, hx2 - 3, hz2 - 3, step_x=5, step_z=5, light_mat=MAT['light_ochre'])
    build_flat_roof_and_eaves(c, hx1, hy_roof, hz1, hx2, hz2, overhang=2, hidden_lights=True)

    build_illuminated_carpet_rug(c, -68, hy_1f, -592, -36, -576, MAT['carpet_red'], MAT['carpet_white'])
    build_outdoor_bar(c, -64, hy_1f, -594, length=10)
    build_outdoor_sofa(c, -56, hy_1f, -582, length=8, facing='south')
    build_crystal_chandelier(c, -50, hy_2f, -584, drop=2, style='grand')

    for fy_suite in (hy_2f, hy_3f):
        build_illuminated_carpet_rug(c, -68, fy_suite, -592, -38, -576, MAT['carpet_white'], MAT['carpet_lgray'])
        place_bed(c, -64, fy_suite + 1, -590, facing='south', color='white')
        place_bed(c, -52, fy_suite + 1, -590, facing='south', color='cyan')
        place_bed(c, -42, fy_suite + 1, -590, facing='south', color='white')

    build_illuminated_carpet_rug(c, -68, hy_4f, -592, -38, -576, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_bar(c, -62, hy_4f, -593, length=8)
    build_outdoor_sofa(c, -56, hy_4f, -582, length=8, facing='north')
    build_crystal_chandelier(c, -50, hy_roof, -584, drop=2, style='grand')

    build_spiral_staircase(c, -28, hy_1f + 1, hy_4f, -574, radius=2, start_sector=1, clockwise=True,
                           intermediate_floors=[hy_2f, hy_3f])

    place_double_door(c, hx2, hy_1f + 1, -584, 'dark_oak', 'west', 'true')
    place_double_door(c, hx1, hy_1f + 1, -584, 'dark_oak', 'east', 'true')
    place_double_door(c, -50, hy_1f + 1, hz1, 'dark_oak', 'south', 'true')
    place_double_door(c, -50, hy_1f + 1, hz2, 'dark_oak', 'north', 'true')

def _build_urban_pocket_park_and_expansion_reserve_blocks(c: WorldCanvas):
    """
    5. Builds the Central Urban Pocket Park & Innovation Pavilion (`X = -188..-102, Z = -524..-468`),
       landscaped superblock avenues, and the Western Metropolitan Expansion Gateway Arch at `X = -300`
       so future iterations have a clean, spacious urban framework ready for expansion.
    """

    for z in range(-524, -467):
        for x in range(-188, -101):
            if x in (-188, -102) or z in (-524, -468):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            elif abs(x - (-145)) <= 3 or abs(z - (-496)) <= 3:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            else:
                c.set_block(x, Y_BASE, z, MAT['moss_block'] if (x + z) % 5 == 0 else MAT['grass_block'])
                if (x * 3 + z * 7) % 19 == 0:
                    c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x + z) % len(SOFT_FLOWERS)])

    build_fountain(c, -145, Y_BASE, -496, radius=6)
    build_hedgerow_line(c, -186, Y_BASE, -522, -104, -522, height=2, gap_every=8)
    build_hedgerow_line(c, -186, Y_BASE, -470, -104, -470, height=2, gap_every=8)

    for bx1, bx2, bz1, bz2 in [
        (-188, -102, -604, -548),
        (-296, -208, -524, -468),
        (-296, -208, -604, -548),
    ]:
        bm_x, bm_z = (bx1 + bx2) // 2, (bz1 + bz2) // 2
        for z in range(bz1, bz2 + 1):
            for x in range(bx1, bx2 + 1):
                if x in (bx1, bx2) or z in (bz1, bz2):
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                    if (x + z) % 6 == 0:
                        c.set_block(x, Y_BASE, z, MAT['light_ochre'])
                elif abs(x - bm_x) <= 2 or abs(z - bm_z) <= 2:
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])

        for dx in range(-5, 6):
            for dz in range(-5, 6):
                if abs(dx) + abs(dz) <= 7:
                    c.set_block(bm_x + dx, Y_BASE, bm_z + dz, MAT['wall_quartz'])
                    c.set_block(bm_x + dx, Y_BASE + 1, bm_z + dz, MAT['slab_quartz_b'] if abs(dx) + abs(dz) == 7 else 'minecraft:air')
        c.set_block(bm_x, Y_BASE, bm_z, MAT['light_sea'])

    for pz in (-542, -530):
        c.fill(-301, Y_BASE + 1, pz - 1, -299, Y_BASE + 14, pz + 1, MAT['wall_white'])
        c.fill(-300, Y_BASE + 2, pz, -300, Y_BASE + 13, pz, MAT['light_sea'])
    c.fill(-301, Y_BASE + 14, -543, -299, Y_BASE + 16, -529, MAT['frame_dark'])
    c.fill(-300, Y_BASE + 15, -541, -300, Y_BASE + 15, -531, MAT['light_ochre'])
    for z_g in range(-543, -528):
        c.set_block(-300, Y_BASE + 17, z_g, MAT['slab_quartz_b'])

    urban_trees = [
        (-175, -512, 'ornamental'), (-175, -480, 'birch_mix'),
        (-115, -512, 'birch_mix'), (-115, -480, 'ornamental'),
        (-160, -592, 'oak_mix'), (-130, -592, 'ornamental'),
        (-160, -560, 'birch_mix'), (-130, -560, 'oak_mix'),
        (-275, -512, 'ornamental'), (-225, -512, 'birch_mix'),
        (-275, -592, 'birch_mix'), (-225, -592, 'ornamental'),
    ]
    for idx, (tx, tz, tst) in enumerate(urban_trees):
        build_custom_tree(c, tx, Y_BASE, tz, height=9, style=tst, seed=91000 + idx, max_radius=3)

def step17_main_urban_district_prototype(c: WorldCanvas):
    """
    Master Builder Entry Point for V5.3 Expansion 11:
    Main Urban District Prototype (`大型主城区雏形`) in `X in [-304, 23], Z in [-632, -448]`.
    """
    _bulldoze_and_grade_urban_foundation(c)
    _build_metropolitan_arterial_road_grid(c)
    _build_central_civic_plaza_and_metro_hub(c)
    _build_commercial_galleria_and_hotel_prototypes(c)
    _build_urban_pocket_park_and_expansion_reserve_blocks(c)
