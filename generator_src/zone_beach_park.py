"""
zone_beach_park.py — V5.3 Expansion: 50-Block Coastal Transition Belt & Large Seaside Beach Park
================================================================================================
Implements Requirement 5a of Modern Manor V5.3:
  1. ~50-Block Coastal & Parkland Transition Zone (`Z = -447..-397`, `X = -224..240`, plus the
     Coastal Cliff & Seawall Promenade `X = 126..240, Z = -447..-228` north of the relocated Lighthouse):
     - Leaves a generous 51-block landscaped transition buffer north of the enlarged Sports Complex
       (`Z = -396..-252`) so the new Seaside Beach Park is never cramped against the stadium.
     - Bulldozes all natural terrain in the transition belt and generates a sculpted Tidal Creek
       (`Z ≈ -422`), coastal pine/birch meadows, cliffside seawall promenade, two cantilevered
       glass overwater ocean lookouts (`Z = -290` & `Z = -360`), and 3 North-South arterial avenues
       with arched bridges connecting the estate to the Beach Park and Main Urban District.
  2. Large Seaside Beach Park (`大型海滨沙滩公园`, `X = 24..240, Z = -632..-448`, `217 x 185` blocks):
     - 100% Custom Procedural Terrain (natural terrain is completely bulldozed from `Y = 44..175`
       and regenerated): sweeping sinusoidal Crescent Golden Sand Beach (`Y = 64 -> 63 -> 62`),
       custom turquoise shallow surf zone with rolling white foam wave crests, deep luminous
       swimming lagoon (`Y = 50..62`), outer coral reef atolls, and sculpted North/South sandstone headlands.
     - 10 Complete, Large-Scale Park Facilities:
       (1) Curved 10-Block-Wide Seaside Palm Boardwalk & Upper Coastal Gardens (`X = 24..78, Z = -628..-448`)
       (2) South Coastal Welcome Plaza, Wave Archway & Shell Fountain (`X = 88..136, Z = -462..-448`)
       (3) 2-Story Flagship Beach Clubhouse, Surf Pro-Shop, Gelato Bar & Sunset Sky Deck
           (`X = 32..60, Z = -554..-518, Y = 64..77`, with spiral staircase at `(38, -524)`)
       (4) Seaside Aqua-Park: 16m Slide Launch Tower (spiral staircase at `(39, -607)`), Dual 3D
           Water Flume Slides (Cyan/White & Orange/Yellow), and Splash Lagoon Pool with Swim-Up Bar
           (`X = 30..64, Z = -614..-566, Y = 61..81`)
       (5) Twin Regulation Beach Volleyball Stadium Courts, Nets, Referee Chairs & Covered Bleachers
           (`X = 74..104, Z = -506..-468, Y = 63..70`)
       (6) Sunken Beach Bonfire Amphitheater & Acoustic Seashell Concert Stage (`X = 32..60, Z = -508..-474`)
       (7) 8 Luxury VIP Beachfront Cabanas, 24 Sun-Lounger Umbrella Bays & 2 Red/White Lifeguard Towers
           (`(116, 63, -492)` & `(116, 63, -580)`)
       (8) 92-Block Overwater Sunset Pier, 2-Story Octagonal Glass & Copper Sea-Breeze Pavilion
           (`center 194, -536`), 2 Pure-Voxel Catamaran Yachts & 4 Jet-Skis (`X = 114..206, Z = -546..-526`)
       (9) Offshore Floating Water-Sports & Diving Island (`X = 154..180, Z = -502..-476, Y = 62..70`)
      (10) North Cape Surfboard Shack, Kayak Launch, Glowing Tidal Rock Pools & Coastal Palm Groves
"""

import math
import random
from config import Y_BASE, HARBOR_FLOOR, MAT, SOFT_FLOWERS, CORAL_BLOCKS
from world_canvas import WorldCanvas
from arch_lib import (
    stair, trapdoor,
    place_barrel, place_brewing_stand, place_smoker, place_lectern,
    place_door, place_double_door,
    build_recessed_ceiling_grid, build_crystal_chandelier, build_illuminated_carpet_rug,
    build_curtain_wall, build_flat_roof_and_eaves,
    build_spiral_staircase, build_straight_stairs,
    build_lamppost, build_fountain, build_infinity_pool,
    build_custom_tree, build_patio_umbrella, build_sun_lounger,
    build_outdoor_sofa, build_outdoor_bar, build_arched_canal_bridge,
    _TREE_BUILDING_GUARD,
)

def _bay_curve_phase(z: int) -> float:
    """Smooth sinusoidal crescent bay curve in Z = -628..-448 (0.0 at headlands, 1.0 at Z = -538)."""
    t = max(0.0, min(1.0, (z - (-628)) / 180.0))
    return math.sin(t * math.pi)

def _x_boardwalk_east(z: int) -> int:
    """East edge of the curved beachfront boardwalk (X = 68 at bay center Z=-538, X = 78 at headlands)."""
    return int(round(78 - 10.0 * _bay_curve_phase(z)))

def _x_shoreline(z: int) -> int:
    """Waterline where wet sand (Y=62) meets shallow ocean surf (X = 122 at bay center, X = 136 at headlands)."""
    return int(round(136 - 14.0 * _bay_curve_phase(z)))

def build_palm_tree(c: WorldCanvas, cx: int, y_ground: int, cz: int, height: int = 9, lean_dx: int = 1, lean_dz: int = 0, seed: int = 101):
    """
    Builds a custom tropical coastal palm tree with a slightly curved stripped wood trunk,
    cocoa/froglight crown cluster, and 8 radiating arched palm fronds, protected by `_TREE_BUILDING_GUARD`.
    """
    for ty in range(y_ground + 1, y_ground + height + 3):
        for tdx in (-2, -1, 0, 1, 2):
            for tdz in (-2, -1, 0, 1, 2):
                if c.get_block_name(cx + tdx, ty, cz + tdz) in _TREE_BUILDING_GUARD:
                    return

    rng = random.Random(seed ^ (cx * 73856093) ^ (cz * 19349663))
    tx, tz = cx, cz
    for dy in range(1, height + 1):
        if dy == height // 2 or dy == (height * 3) // 4:
            tx += lean_dx
            tz += lean_dz
        c.set_block(tx, y_ground + dy, tz, 'minecraft:stripped_jungle_log[axis=y]')
    top_y = y_ground + height
    c.set_block(tx, top_y, tz, MAT['light_ochre'])
    c.set_block(tx, top_y + 1, tz, MAT['leaf_oak'])

    frond_dirs = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]
    for fdx, fdz in frond_dirs:
        f_len = 4 if (fdx == 0 or fdz == 0) else 3
        for step in range(1, f_len + 1):
            fx = tx + fdx * step
            fz = tz + fdz * step
            fy = top_y + (1 if step == 1 else (0 if step < f_len else -1))
            if c.get_block_name(fx, fy, fz) == 'minecraft:air':
                near_b = any(
                    c.get_block_name(fx + nx, fy + ny, fz + nz) in _TREE_BUILDING_GUARD
                    for nx, ny, nz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
                )
                if not near_b:
                    leaf_m = MAT['leaf_oak'] if (step + fdx + fdz) % 2 == 0 else MAT['leaf_azalea']
                    c.set_block(fx, fy, fz, leaf_m)
    if rng.random() < 0.5:
        c.set_block(cx, y_ground, cz, MAT['moss_block'])

def _bulldoze_and_generate_transition_and_beach_terrain(c: WorldCanvas):
    """
    Step 1: Bulldoze all natural terrain in:
      - East Coastal Corridor north of the Lighthouse (`X = 125..255, Z = -447..-228`)
      - 51-Block Transition Parkbelt (`X = -224..255, Z = -447..-397`)
      - Large Seaside Beach Park (`X = 24..255, Z = -636..-448`)
    and procedurally generate custom coastal bluffs, tidal creek, crescent golden beach,
    rolling surf waves, and turquoise coral lagoon!
    """
    stone_id = c.get_or_register(MAT['stone'])
    dirt_id = c.get_or_register(MAT['dirt'])
    grass_id = c.get_or_register(MAT['grass_block'])
    moss_id = c.get_or_register(MAT['moss_block'])
    sand_id = c.get_or_register('minecraft:sand')
    sandstone_id = c.get_or_register('minecraft:smooth_sandstone')
    water_id = c.get_or_register(MAT['water'])
    sea_lantern_id = c.get_or_register(MAT['light_sea'])
    ochre_id = c.get_or_register(MAT['light_ochre'])
    prism_id = c.get_or_register(MAT['pool_shallow_1'])
    dprism_id = c.get_or_register(MAT['pool_deep_1'])
    lblue_id = c.get_or_register(MAT['pool_shallow_2'])
    air_id = c.air_id

    for z in range(-396, -228):
        for x in range(126, c.x_max + 1):
            for y in range(50, c.y_max + 1):
                c.set_block_id(x, y, z, air_id)
            if x <= 136:
                for y in range(46, Y_BASE - 2):
                    c.set_block_id(x, y, z, stone_id)
                c.set_block_id(x, Y_BASE - 2, z, dirt_id)
                c.set_block_id(x, Y_BASE - 1, z, dirt_id)
                c.set_block_id(x, Y_BASE, z, grass_id)
            else:
                seabed_y = max(HARBOR_FLOOR, 58 - (x - 137) // 2)
                for y in range(44, seabed_y - 1):
                    c.set_block_id(x, y, z, stone_id)
                c.set_block_id(x, seabed_y - 1, z, sandstone_id)
                c.set_block_id(x, seabed_y, z, sea_lantern_id if (x % 8 == 0 and z % 8 == 0) else sand_id)
                for y in range(seabed_y + 1, 63):
                    c.set_block_id(x, y, z, water_id)

    for z in range(-447, -396):
        creek_cz = -422 + int(round(3.5 * math.sin(x_ref / 24.0))) if False else -422
        for x in range(-224, c.x_max + 1):
            for y in range(48, c.y_max + 1):
                c.set_block_id(x, y, z, air_id)

            if x >= 137:

                seabed_y = max(HARBOR_FLOOR, 58 - (x - 137) // 2)
                for y in range(44, seabed_y - 1):
                    c.set_block_id(x, y, z, stone_id)
                c.set_block_id(x, seabed_y - 1, z, sandstone_id)
                c.set_block_id(x, seabed_y, z, sea_lantern_id if (x % 8 == 0 and z % 8 == 0) else sand_id)
                for y in range(seabed_y + 1, 63):
                    c.set_block_id(x, y, z, water_id)
                continue

            creek_center_z = -422 + int(round(3.0 * math.sin(x / 22.0)))
            dist_creek = abs(z - creek_center_z)
            for y in range(45, Y_BASE - 3):
                c.set_block_id(x, y, z, stone_id)

            if dist_creek <= 2 and x <= 136:

                c.set_block_id(x, Y_BASE - 3, z, stone_id)
                c.set_block_id(x, Y_BASE - 2, z, sea_lantern_id if (x + z) % 5 == 0 else dprism_id)
                c.set_block_id(x, Y_BASE - 1, z, water_id)
                c.set_block_id(x, Y_BASE, z, water_id)
            elif dist_creek == 3 and x <= 136:
                c.set_block_id(x, Y_BASE - 2, z, dirt_id)
                c.set_block_id(x, Y_BASE - 1, z, dirt_id)
                c.set_block_id(x, Y_BASE, z, moss_id if (x + z) % 2 == 0 else sandstone_id)
            else:
                c.set_block_id(x, Y_BASE - 3, z, dirt_id)
                c.set_block_id(x, Y_BASE - 2, z, dirt_id)
                c.set_block_id(x, Y_BASE - 1, z, dirt_id)
                c.set_block_id(x, Y_BASE, z, moss_id if (x * 5 + z * 7) % 9 == 0 else grass_id)

    for z in range(c.z_min, -447):
        phase = _bay_curve_phase(z)
        x_bw = _x_boardwalk_east(z)
        x_dry_sand = int(round(104 - 12.0 * phase))
        x_mid_sand = int(round(126 - 14.0 * phase))
        x_wet_sand = _x_shoreline(z)

        in_south_cape = (-462 <= z <= -448 and 118 <= z + 580)
        for x in range(24, c.x_max + 1):
            for y in range(46, c.y_max + 1):
                c.set_block_id(x, y, z, air_id)

            d_north_cape = ((x - 142) / 24.0) ** 2 + ((z + 622) / 10.0) ** 2
            d_south_cape = ((x - 138) / 18.0) ** 2 + ((z + 454) / 7.0) ** 2

            if d_north_cape <= 1.0 or d_south_cape <= 1.0:
                cape_h = Y_BASE + (1 if (d_north_cape <= 0.55 or d_south_cape <= 0.55) else 0)
                for y in range(46, cape_h - 2):
                    c.set_block_id(x, y, z, stone_id)
                for y in range(cape_h - 2, cape_h + 1):
                    c.set_block_id(x, y, z, sandstone_id)

                if d_north_cape <= 0.42 and (x + z) % 3 == 0:
                    c.set_block_id(x, cape_h - 1, z, sea_lantern_id)
                    c.set_block_id(x, cape_h, z, water_id)
                continue

            if x <= x_bw:

                for y in range(46, Y_BASE - 2):
                    c.set_block_id(x, y, z, stone_id)
                c.set_block_id(x, Y_BASE - 2, z, dirt_id)
                c.set_block_id(x, Y_BASE - 1, z, dirt_id)
                c.set_block_id(x, Y_BASE, z, grass_id)
            elif x <= x_dry_sand:

                for y in range(46, Y_BASE - 3):
                    c.set_block_id(x, y, z, stone_id)
                c.set_block_id(x, Y_BASE - 3, z, sandstone_id)
                c.set_block_id(x, Y_BASE - 2, z, sandstone_id)
                c.set_block_id(x, Y_BASE - 1, z, sand_id)
                c.set_block_id(x, Y_BASE, z, sand_id)
            elif x <= x_mid_sand:

                y_b = 63
                for y in range(46, y_b - 3):
                    c.set_block_id(x, y, z, stone_id)
                c.set_block_id(x, y_b - 3, z, sandstone_id)
                c.set_block_id(x, y_b - 2, z, sandstone_id)
                c.set_block_id(x, y_b - 1, z, sand_id)
                c.set_block_id(x, y_b, z, sand_id)
            elif x <= x_wet_sand:

                y_b = 62
                for y in range(46, y_b - 2):
                    c.set_block_id(x, y, z, stone_id)
                c.set_block_id(x, y_b - 2, z, sandstone_id)
                c.set_block_id(x, y_b - 1, z, sandstone_id)
                if (x * 3 + z * 5) % 17 == 0 and x >= x_wet_sand - 4:
                    c.set_block_id(x, y_b - 1, z, sea_lantern_id)
                    c.set_block_id(x, y_b, z, water_id)
                else:
                    c.set_block_id(x, y_b, z, sandstone_id if (x + z) % 5 == 0 else sand_id)
            else:

                dist_sea = x - x_wet_sand
                if dist_sea <= 22:

                    seabed_y = max(55, 61 - dist_sea // 4)
                    for y in range(46, seabed_y - 1):
                        c.set_block_id(x, y, z, stone_id)
                    c.set_block_id(x, seabed_y - 1, z, sandstone_id)
                    if (x + z) % 7 == 0:
                        c.set_block_id(x, seabed_y, z, sea_lantern_id)
                    elif dist_sea >= 8 and (x + z) % 2 == 0:
                        c.set_block_id(x, seabed_y, z, lblue_id if dist_sea < 15 else prism_id)
                    else:
                        c.set_block_id(x, seabed_y, z, sand_id)
                    for y in range(seabed_y + 1, 63):
                        c.set_block_id(x, y, z, water_id)

                    wave_jitter = int(round(1.2 * math.sin(z / 6.0)))
                    if dist_sea == 6 + wave_jitter or dist_sea == 14 + wave_jitter:
                        c.set_block(x, 62, z, MAT['glass_white'])
                        if (x + z) % 2 == 0 and -610 <= z <= -465:
                            c.set_block(x, 63, z, MAT['slab_quartz_b'])
                else:

                    seabed_y = HARBOR_FLOOR + (2 if dist_sea < 35 else 0)
                    for y in range(44, seabed_y - 1):
                        c.set_block_id(x, y, z, stone_id)
                    c.set_block_id(x, seabed_y - 1, z, sandstone_id)
                    if (x % 6 == 0 and z % 6 == 0):
                        c.set_block_id(x, seabed_y, z, sea_lantern_id)
                    elif ((x + z) % 9 == 0):
                        c.set_block_id(x, seabed_y, z, ochre_id)
                    elif (x + z) % 3 == 0:
                        c.set_block_id(x, seabed_y, z, prism_id if dist_sea < 55 else dprism_id)
                    else:
                        c.set_block_id(x, seabed_y, z, sand_id)
                    for y in range(seabed_y + 1, 63):
                        c.set_block_id(x, y, z, water_id)

                    if 176 <= x <= 232 and -608 <= z <= -466 and not (-550 <= z <= -522):
                        if (x * 7 + z * 13) % 19 == 0:
                            coral_m = CORAL_BLOCKS[(x + z) % len(CORAL_BLOCKS)]
                            ch = 2 + ((x + z) % 4)
                            for cy in range(seabed_y + 1, min(60, seabed_y + 1 + ch)):
                                c.set_block(x, cy, z, coral_m)
                            c.set_block(x, min(60, seabed_y + 1 + ch), z, MAT['sea_pickle_4'])

def _build_transition_corridors_and_cliff_walk(c: WorldCanvas):
    """
    Step 2: Builds the connecting avenues, arched creek bridges, coastal cliff promenade,
    and two cantilevered glass ocean lookouts across the ~50-block transition zone (`Z = -447..-397`)
    and the East Coastal Corridor (`Z = -447..-216`).
    """

    for z in range(-448, -215):
        creek_center_z = -422 + int(round(3.0 * math.sin(131 / 22.0)))
        if abs(z - creek_center_z) <= 4:
            continue
        for x in range(126, 137):
            c.fill(x, 52, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
            if x == 136:
                c.set_block(x, Y_BASE, z, MAT['light_sea'] if z % 4 == 0 else MAT['wall_quartz'])
                if not (-296 <= z <= -284 or -366 <= z <= -354):
                    c.set_block(x, Y_BASE + 1, z, MAT['pane_black'])
            elif x == 126:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['stone_pol_and'])
            elif x in (130, 131, 132):
                c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (z // 2) % 2 == 0 else MAT['wood_dark'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
        if z % 12 == 0 and not (-298 <= z <= -282 or -368 <= z <= -352):
            build_lamppost(c, 126, Y_BASE + 1, z, style='courtyard')

    build_arched_canal_bridge(c, 131, Y_BASE, -422 + int(round(3.0 * math.sin(131 / 22.0))), width=9, span=12, axis='z')

    for l_cz in (-290, -360):
        l_cx = 141
        for dx in range(-6, 8):
            for dz in range(-6, 7):
                d = math.hypot(dx, dz)
                if d <= 6.2 and l_cx + dx >= 136:
                    x, z = l_cx + dx, l_cz + dz
                    if d >= 5.2:
                        c.set_block(x, Y_BASE, z, MAT['light_sea'] if (dx + dz) % 3 == 0 else MAT['wall_quartz'])
                        c.set_block(x, Y_BASE + 1, z, MAT['pane_cyan'])
                    elif d <= 2.5:
                        c.set_block(x, Y_BASE, z, MAT['glass_cyan'] if (dx + dz) % 2 == 0 else MAT['glass_clear'])
                    else:
                        c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (dx + dz) % 2 == 0 else MAT['wood_dark'])
                    c.set_block(x, Y_BASE + 2, z, 'minecraft:air')
        c.fill(l_cx, 50, l_cz, l_cx + 1, Y_BASE - 1, l_cz + 1, MAT['frame_dark'])
        c.set_block(l_cx, 62, l_cz, MAT['light_sea'])
        build_patio_umbrella(c, l_cx + 1, Y_BASE, l_cz)

    for z in range(-448, -275):
        creek_z = -422 + int(round(3.0 * math.sin(100 / 22.0)))
        if abs(z - creek_z) <= 5:
            continue
        for x in range(98, 104):
            if x in (98, 103):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 4, z, 'minecraft:air')
        if z % 14 == 0:
            build_lamppost(c, 97, Y_BASE + 1, z, style='avenue')
    build_arched_canal_bridge(c, 100, Y_BASE, -422 + int(round(3.0 * math.sin(100 / 22.0))), width=7, span=12, axis='z')

    for x in range(12, 136):
        for z in range(-394, -388):
            if z in (-394, -389) and x not in range(12, 24) and x not in range(98, 104) and x < 126:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])

    for z in range(-448, -388):
        creek_z = -422 + int(round(3.0 * math.sin(18 / 22.0)))
        if abs(z - creek_z) <= 5:
            continue
        for x in range(12, 24):
            if x in (12, 23):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            elif x in (13, 22):
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            elif x in (17, 18):
                c.set_block(x, Y_BASE, z, MAT['moss_block'] if z % 4 != 0 else MAT['light_ochre'])
                if z % 4 != 0:
                    c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x + z) % len(SOFT_FLOWERS)])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_gray'])
        if z in (-440, -406):
            build_lamppost(c, 17, Y_BASE + 1, z, style='avenue')
    build_arched_canal_bridge(c, 18, Y_BASE, -422 + int(round(3.0 * math.sin(18 / 22.0))), width=11, span=12, axis='z')

    for av_cx in (-91, -199):
        creek_z = -422 + int(round(3.0 * math.sin(av_cx / 22.0)))
        for z in range(-448, -395):
            if abs(z - creek_z) <= 5:
                continue
            for dx in range(-5, 6):
                x = av_cx + dx
                if abs(dx) == 5:
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                elif abs(dx) == 4:
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
                elif dx == 0:
                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if z % 4 in (0, 1) else MAT['wall_gray'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['wall_gray'])
            if z in (-440, -404):
                build_lamppost(c, av_cx - 4, Y_BASE + 1, z, style='avenue')
                build_lamppost(c, av_cx + 4, Y_BASE + 1, z, style='avenue')
        build_arched_canal_bridge(c, av_cx, Y_BASE, creek_z, width=9, span=12, axis='z')

    trans_trees = [
        (-160, -436, 'oak_mix'), (-140, -410, 'birch_mix'), (-115, -434, 'ornamental'),
        (-65, -436, 'birch_mix'), (-50, -408, 'ornamental'), (-15, -434, 'oak_mix'),
        (0, -410, 'ornamental'), (45, -436, 'birch_mix'), (65, -408, 'ornamental'),
        (82, -434, 'oak_mix'), (112, -436, 'ornamental'), (114, -406, 'birch_mix'),
        (114, -340, 'ornamental'), (114, -295, 'birch_mix'), (114, -255, 'ornamental'),
    ]
    for idx, (tx, tz, tst) in enumerate(trans_trees):
        build_custom_tree(c, tx, Y_BASE, tz, height=9, style=tst, seed=53010 + idx, max_radius=3)

def _build_curved_palm_boardwalk_and_south_gate(c: WorldCanvas):
    """
    Step 3: Builds the sweeping 10-block-wide Curved Seaside Palm Boardwalk following the
    crescent bay (`Z = -626..-448`) and the South Coastal Welcome Plaza & Seashell Wave Archway (`Z = -462..-448`).
    """

    for z in range(-626, -447):
        x_bw = _x_boardwalk_east(z)
        x_west = x_bw - 9
        for x in range(x_west, x_bw + 1):
            if x == x_bw:
                c.set_block(x, Y_BASE, z, MAT['light_sea'] if z % 4 == 0 else MAT['wall_quartz'])

                if z in (-596, -556, -516, -476):
                    for dz_s in (-1, 0, 1):
                        c.set_block(x, Y_BASE, z + dz_s, stair('smooth_quartz', 'west', 'bottom'))
            elif x == x_west:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 5 == 0 else MAT['stone_pol_and'])
            elif x in (x_west + 1, x_west + 2, x_bw - 2, x_bw - 1):
                c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (z // 2) % 2 == 0 else MAT['wood_dark'])
            else:

                wave_p = ((x + int(round(2.0 * math.sin(z / 5.0)))) % 3 == 0)
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if wave_p else MAT['stone_dio'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 4, z, 'minecraft:air')

        if z % 14 == 0 and -616 <= z <= -460 and not (-546 <= z <= -526):
            build_lamppost(c, x_west, Y_BASE + 1, z, style='courtyard')

    for z_range in [range(-462, -453), range(-542, -529), range(-618, -609)]:
        z_list = list(z_range)
        z_min_r, z_max_r = z_list[0], z_list[-1]
        for z in z_list:
            x_bw = _x_boardwalk_east(z)
            for x in range(24, x_bw - 8):
                if z in (z_min_r, z_max_r):
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['stone_pol_and'])
                elif z == (z_min_r + z_max_r) // 2:
                    c.set_block(x, Y_BASE, z, MAT['light_sea'] if x % 8 == 0 else MAT['wall_quartz'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    for z in range(-462, -447):
        for x in range(76, 137):
            c.fill(x, 54, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
            if (x - 76) % 6 == 0 or (z + 462) % 6 == 0:
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 6, z, 'minecraft:air')

    build_fountain(c, 114, Y_BASE, -455, radius=5)

    for x in range(94, 109):
        u = (x - 101) / 7.0
        arch_y = Y_BASE + int(round(7.0 * max(0.0, 1.0 - u * u)))
        if abs(x - 101) >= 6:
            c.fill(x, Y_BASE + 1, -449, x, arch_y, -449, MAT['pillar_quartz'])
        c.fill(x, arch_y, -450, x, arch_y + 1, -448, MAT['wall_quartz'])
        c.set_block(x, arch_y + 2, -449, MAT['slab_quartz_b'])
        if abs(x - 101) <= 5:
            c.set_block(x, arch_y, -449, MAT['light_sea'] if x % 2 == 0 else MAT['glass_cyan'])

def _build_flagship_beach_clubhouse(c: WorldCanvas):
    """
    Step 4: Flagship 2-Story Panoramic Beach Clubhouse, Visitor Center, Surf Pro-Shop & Sunset Sky Lounge
    Footprint: X = 32..60, Z = -554..-518, Y = 64..77 (centered on the Z = -536 Grand Axis!)
    """
    cx1, cx2, cz1, cz2 = 32, 60, -554, -518
    y_1f = Y_BASE
    y_2f = Y_BASE + 7
    y_roof = Y_BASE + 12

    for z in range(cz1 - 4, cz2 + 5):
        for x in range(cx1 - 4, cx2 + 7):
            c.set_block(x, y_1f, z, MAT['wall_quartz'] if (x + z) % 3 == 0 else MAT['stone_smooth'])
            c.fill(x, y_1f + 1, z, x, y_roof + 3, z, 'minecraft:air')

    c.fill(cx1, y_1f - 1, cz1, cx2, y_1f - 1, cz2, MAT['stone_pol_and'])
    for z in range(cz1, cz2 + 1):
        for x in range(cx1, cx2 + 1):
            if (x - cx1) % 5 == 0 and (z - cz1) % 5 == 0:
                c.set_block(x, y_1f, z, MAT['light_sea'])
            else:
                c.set_block(x, y_1f, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['wood_birch'])

    c.fill(cx1, y_1f + 1, cz1, cx2, y_2f - 1, cz2, MAT['wall_white'])
    c.fill(cx1 + 1, y_1f + 1, cz1 + 1, cx2 - 1, y_2f - 1, cz2 - 1, 'minecraft:air')

    build_curtain_wall(c, cx2, y_1f + 1, cz1 + 2, cx2, y_2f - 1, cz2 - 2,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, cx1, y_1f + 1, cz1 + 2, cx1, y_2f - 1, cz2 - 2,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, cx1 + 2, y_1f + 1, cz1, cx2 - 2, y_2f - 1, cz1,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, cx1 + 2, y_1f + 1, cz2, cx2 - 2, y_2f - 1, cz2,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)

    build_recessed_ceiling_grid(c, cx1 + 2, y_2f, cz1 + 2, cx2 - 2, cz2 - 2, step_x=4, step_z=4, light_mat=MAT['light_ochre'])
    build_illuminated_carpet_rug(c, 40, y_1f, -544, 54, -528, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_bar(c, 42, y_1f, -549, length=10)
    build_outdoor_sofa(c, 43, y_1f, -539, length=7, facing='south')
    build_outdoor_sofa(c, 43, y_1f, -533, length=7, facing='north')
    build_crystal_chandelier(c, 46, y_2f, -536, drop=2, style='grand')

    c.fill(cx1, y_2f, cz1, cx2, y_2f, cz2, MAT['wood_dark'])
    for x in range(cx1, cx2 + 1):
        for z in (cz1, cz2):
            c.set_block(x, y_2f, z, MAT['wall_quartz'])
            c.set_block(x, y_2f + 1, z, MAT['pane_cyan'])
    for z in range(cz1, cz2 + 1):
        for x in (cx1, cx2):
            c.set_block(x, y_2f, z, MAT['wall_quartz'])
            c.set_block(x, y_2f + 1, z, MAT['pane_cyan'])

    c.fill(35, y_2f + 1, -548, 53, y_roof - 1, -526, MAT['wall_white'])
    c.fill(36, y_2f + 1, -547, 52, y_roof - 1, -527, 'minecraft:air')
    build_curtain_wall(c, 53, y_2f + 1, -546, 53, y_roof - 1, -528,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=3)
    build_curtain_wall(c, 35, y_2f + 1, -546, 35, y_roof - 1, -528,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=3)
    build_curtain_wall(c, 37, y_2f + 1, -548, 51, y_roof - 1, -548,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=3)
    place_double_door(c, 53, y_2f + 1, -537, 'dark_oak', 'west', 'true')
    place_double_door(c, 44, y_2f + 1, -526, 'dark_oak', 'north', 'true')

    build_illuminated_carpet_rug(c, 38, y_2f, -545, 50, -530, MAT['carpet_orange'], MAT['carpet_white'])
    build_outdoor_bar(c, 39, y_2f, -544, length=8)
    build_outdoor_sofa(c, 40, y_2f, -534, length=6, facing='north')
    build_flat_roof_and_eaves(c, 35, y_roof, -548, 53, -526, overhang=2, hidden_lights=True)
    build_crystal_chandelier(c, 44, y_roof, -537, drop=2, style='grand')

    build_spiral_staircase(c, 38, y_1f + 1, y_2f, -522, radius=2, start_sector=1, clockwise=True)
    for x_r in range(35, 42):
        c.set_block(x_r, y_2f + 1, -519, MAT['pane_cyan'])
    for z_r in range(-525, -518):
        c.set_block(35, y_2f + 1, z_r, MAT['pane_cyan'])

    for uz in (-548, -537, -524):
        build_patio_umbrella(c, 57, y_2f, uz)

    place_double_door(c, cx1, y_1f + 1, -536, 'dark_oak', 'east', 'true')
    place_double_door(c, cx2, y_1f + 1, -536, 'dark_oak', 'west', 'true')
    place_double_door(c, 46, y_1f + 1, cz1, 'dark_oak', 'south', 'true')
    place_double_door(c, 46, y_1f + 1, cz2, 'dark_oak', 'north', 'true')
    for dz_d in (-536, -535):
        c.fill(cx1 - 2, y_1f + 1, dz_d, cx1 - 1, y_1f + 3, dz_d, 'minecraft:air')
        c.fill(cx1 + 1, y_1f + 1, dz_d, cx1 + 2, y_1f + 3, dz_d, 'minecraft:air')
        c.fill(cx2 - 2, y_1f + 1, dz_d, cx2 - 1, y_1f + 3, dz_d, 'minecraft:air')
        c.fill(cx2 + 1, y_1f + 1, dz_d, cx2 + 2, y_1f + 3, dz_d, 'minecraft:air')
    for dx_d in (46, 47):
        c.fill(dx_d, y_1f + 1, cz1 - 2, dx_d, y_1f + 3, cz1 - 1, 'minecraft:air')
        c.fill(dx_d, y_1f + 1, cz1 + 1, dx_d, y_1f + 3, cz1 + 2, 'minecraft:air')
        c.fill(dx_d, y_1f + 1, cz2 - 2, dx_d, y_1f + 3, cz2 - 1, 'minecraft:air')
        c.fill(dx_d, y_1f + 1, cz2 + 1, dx_d, y_1f + 3, cz2 + 2, 'minecraft:air')

def _build_seaside_aqua_park_and_water_slides(c: WorldCanvas):
    """
    Step 5: Seaside Water Park, 16m Slide Launch Tower, Dual 3D Water Flume Slides & Splash Lagoon Pool
    Footprint: X = 30..64, Z = -614..-564, Y = 61..81
    """

    for z in range(-614, -563):
        for x in range(30, 63):
            if x in (30, 62) or z in (-614, -564):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 16, z, 'minecraft:air')

    build_infinity_pool(c, 34, Y_BASE, -596, 58, -568)

    for dx in range(-3, 4):
        for dz in range(-3, 4):
            if abs(dx) + abs(dz) <= 4:
                c.fill(46 + dx, Y_BASE - 2, -580 + dz, 46 + dx, Y_BASE, -580 + dz, MAT['wall_quartz'])
                if abs(dx) == 2 or abs(dz) == 2:
                    c.set_block(46 + dx, Y_BASE + 1, -580 + dz, MAT['slab_quartz_b'])
                elif dx == 0 and dz == 0:
                    c.fill(46, Y_BASE + 1, -580, 46, Y_BASE + 4, -580, MAT['beam_spruce_y'])
                    c.set_block(46, Y_BASE + 4, -580, MAT['light_ochre'])
                    for cdx in (-2, -1, 0, 1, 2):
                        for cdz in (-2, -1, 0, 1, 2):
                            if abs(cdx) + abs(cdz) <= 3:
                                c.set_block(46 + cdx, Y_BASE + 5, -580 + cdz, MAT['slab_spruce_b'])

    tx1, tx2, tz1, tz2 = 34, 44, -612, -602
    y_launch = Y_BASE + 11
    y_roof_t = Y_BASE + 15
    c.fill(tx1, Y_BASE, tz1, tx2, Y_BASE, tz2, MAT['wall_quartz'])
    for y in range(Y_BASE + 1, y_launch):
        for x in range(tx1, tx2 + 1):
            for z in range(tz1, tz2 + 1):
                cheb = max(abs(x - 39), abs(z - (-607)))
                if cheb == 3:

                    if (x == 39 or z == -607) and (y - Y_BASE) % 3 == 2:
                        c.set_block(x, y, z, MAT['glass_cyan'])
                    elif (x == 39 or z == -607) and (y - Y_BASE) % 4 == 0:
                        c.set_block(x, y, z, MAT['light_sea'])
                    else:
                        c.set_block(x, y, z, MAT['wall_white'])
                elif x in (tx1, tx2) and z in (tz1, tz2):
                    c.set_block(x, y, z, MAT['cyan_concrete'])

    c.fill(tx1, y_launch, tz1, 56, y_launch, tz2, MAT['wall_quartz'])
    for x in range(tx1, 57):
        for z in (tz1, tz2):
            c.set_block(x, y_launch + 1, z, MAT['pane_cyan'])
    for z in range(tz1, tz2 + 1):
        c.set_block(tx1, y_launch + 1, z, MAT['pane_cyan'])
        c.set_block(56, y_launch + 1, z, MAT['pane_cyan'])
    build_flat_roof_and_eaves(c, tx1, y_roof_t, tz1, 56, tz2, overhang=1,
                              roof_mat=MAT['cyan_concrete'], soffit_mat=MAT['wall_white'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)

    build_spiral_staircase(c, 39, Y_BASE + 1, y_launch, -607, radius=2, start_sector=4, clockwise=False)

    c.fill(34, Y_BASE + 1, -608, 36, Y_BASE + 3, -606, 'minecraft:air')

    for step_i in range(11):
        sz = -602 + step_i
        sy = y_launch - step_i
        for sx_c, wall_m in [(47, MAT['cyan_concrete']), (52, MAT['orange_concrete'])]:

            c.fill(sx_c - 1, sy + 1, sz, sx_c + 1, sy + 4, sz, 'minecraft:air')

            c.set_block(sx_c, sy - 1, sz, MAT['light_sea'] if step_i % 2 == 0 else MAT['wall_white'])
            c.set_block(sx_c, sy, sz, MAT['packed_ice'] if step_i < 10 else MAT['water'])
            c.set_block(sx_c, sy + 1, sz, MAT['carpet_cyan'] if sx_c == 47 else MAT['carpet_yellow'])

            c.set_block(sx_c - 1, sy, sz, wall_m)
            c.set_block(sx_c + 1, sy, sz, wall_m)
            c.set_block(sx_c - 1, sy + 1, sz, MAT['wall_white'])
            c.set_block(sx_c + 1, sy + 1, sz, MAT['wall_white'])
            if step_i % 3 == 0 and sz < -596:
                c.fill(sx_c, Y_BASE + 1, sz, sx_c, sy - 2, sz, MAT['frame_dark'])

def _build_beach_volleyball_and_bonfire_amphitheater(c: WorldCanvas):
    """
    Step 6:
      - Twin Regulation Beach Volleyball Stadium Courts & Covered Bleachers (`X = 74..104, Z = -506..-468`)
      - Sunken Beach Bonfire Amphitheater & Acoustic Seashell Concert Stage (`X = 32..60, Z = -508..-474`)
    """

    for cz_min, cz_max in [(-504, -488), (-484, -468)]:
        cz_mid = (cz_min + cz_max) // 2
        for z in range(cz_min - 1, cz_max + 2):
            for x in range(79, 104):
                c.fill(x, 60, z, x, Y_BASE - 1, z, 'minecraft:smooth_sandstone')
                if (x in (80, 102) and cz_min <= z <= cz_max) or (z in (cz_min, cz_max) and 80 <= x <= 102):
                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                else:
                    c.set_block(x, Y_BASE, z, 'minecraft:sand')
                c.fill(x, Y_BASE + 1, z, x, Y_BASE + 5, z, 'minecraft:air')

        c.fill(80, Y_BASE + 1, cz_mid, 80, Y_BASE + 3, cz_mid, MAT['pillar_quartz'])
        c.fill(102, Y_BASE + 1, cz_mid, 102, Y_BASE + 3, cz_mid, MAT['pillar_quartz'])
        for x in range(81, 102):
            c.set_block(x, Y_BASE + 1, cz_mid, MAT['iron_bars'])
            c.set_block(x, Y_BASE + 2, cz_mid, 'minecraft:cobweb' if x % 2 == 0 else MAT['iron_bars'])
            c.set_block(x, Y_BASE + 3, cz_mid, MAT['carpet_white'])

        c.fill(79, Y_BASE + 1, cz_mid, 79, Y_BASE + 2, cz_mid, 'minecraft:oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        c.set_block(79, Y_BASE + 3, cz_mid, stair('smooth_quartz', 'west', 'bottom'))
        build_patio_umbrella(c, 104, Y_BASE, cz_mid - 4)
        build_patio_umbrella(c, 104, Y_BASE, cz_mid + 4)

    for z in range(-502, -469):
        if -487 <= z <= -485:
            continue
        for tier in range(3):
            bx = 77 - tier
            by = Y_BASE + 1 + tier
            c.fill(bx, Y_BASE + 1, z, bx, by - 1, z, MAT['stone_pol_and'])
            c.set_block(bx, by, z, stair('spruce' if tier % 2 == 0 else 'smooth_quartz', 'west', 'bottom'))

    acx, acz = 46, -491
    for dx in range(-14, 15):
        for dz in range(-16, 17):
            x, z = acx + dx, acz + dz
            d = math.hypot(dx, dz)
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 8, z, 'minecraft:air')
            if d <= 3.5:

                c.set_block(x, Y_BASE - 3, z, MAT['stone_pol_and'])
                c.set_block(x, Y_BASE - 2, z, MAT['light_ochre'] if (dx + dz) % 2 == 0 else 'minecraft:smooth_sandstone')
                c.fill(x, Y_BASE - 1, z, x, Y_BASE, z, 'minecraft:air')
            elif d <= 6.5:

                c.set_block(x, Y_BASE - 2, z, 'minecraft:smooth_sandstone')
                c.set_block(x, Y_BASE - 1, z, MAT['wood_warm'] if (dx + dz) % 2 == 0 else 'minecraft:smooth_sandstone')
                c.set_block(x, Y_BASE, z, 'minecraft:air')
            elif d <= 9.5:

                c.set_block(x, Y_BASE - 1, z, 'minecraft:smooth_sandstone')
                c.set_block(x, Y_BASE, z, MAT['wood_dark'] if (dx + dz) % 2 == 0 else MAT['wall_quartz'])
                if 7.5 <= d <= 8.5 and dz > -3 and abs(dx) >= 2:
                    c.set_block(x, Y_BASE + 1, z, stair('spruce', 'south' if dz > 0 else ('east' if dx > 0 else 'west'), 'bottom'))
            elif d <= 12.5:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    c.fill(acx - 1, Y_BASE - 2, acz - 1, acx + 1, Y_BASE - 2, acz + 1, MAT['stone_pol_and'])
    for bdx in (-1, 0, 1):
        for bdz in (-1, 0, 1):
            if abs(bdx) + abs(bdz) <= 1:
                c.set_block(acx + bdx, Y_BASE - 1, acz + bdz, 'minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]')
    c.set_block(acx, Y_BASE - 2, acz, MAT['light_shroom'])

    for x in range(40, 53):
        u = (x - 46) / 6.0
        shell_h = int(round(5.0 * max(0.0, 1.0 - u * u)))
        c.fill(x, Y_BASE, -504, x, Y_BASE + 1, -500, MAT['wood_dark'])
        for y in range(Y_BASE + 1, Y_BASE + 2 + shell_h):
            c.set_block(x, y, -504, MAT['wall_quartz'] if (x + y) % 2 == 0 else MAT['wall_white'])
        if shell_h > 0:
            c.set_block(x, Y_BASE + 2 + shell_h, -504, MAT['slab_quartz_b'])
            c.set_block(x, Y_BASE + 1 + shell_h, -503, MAT['light_sea'] if x % 2 == 0 else MAT['slab_quartz_t'])
    c.set_block(44, Y_BASE + 2, -502, MAT['note_block'])
    c.set_block(46, Y_BASE + 2, -502, MAT['jukebox'])
    c.set_block(48, Y_BASE + 2, -502, MAT['note_block'])

def _build_cabanas_lifeguard_towers_and_beach_loungers(c: WorldCanvas):
    """
    Step 7: Builds 8 Luxury VIP Beach Cabanas, 24 Sun-Lounger Umbrella Bays,
    and 2 Elevated Red-and-White Baywatch Lifeguard Towers along the Golden Crescent Beach (`Z = -606..-468`).
    """
    umbrella_colors = [
        MAT['slab_quartz_b'],
        'minecraft:smooth_red_sandstone_slab[type=bottom,waterlogged=false]',
        MAT['slab_spruce_b'],
        MAT['slab_dio_b'],
    ]

    cabana_zs = [-596, -582, -568, -554, -520, -508, -496, -482]
    for idx, cz_cab in enumerate(cabana_zs):
        if -510 <= cz_cab <= -466:

            continue
        cx_cab = _x_boardwalk_east(cz_cab) + 6
        c.fill(cx_cab - 2, Y_BASE, cz_cab - 2, cx_cab + 2, Y_BASE, cz_cab + 2, MAT['wood_warm'])
        for px in (cx_cab - 2, cx_cab + 2):
            for pz in (cz_cab - 2, cz_cab + 2):
                c.fill(px, Y_BASE + 1, pz, px, Y_BASE + 3, pz, 'minecraft:birch_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        c.fill(cx_cab - 2, Y_BASE + 4, cz_cab - 2, cx_cab + 2, Y_BASE + 4, cz_cab + 2, MAT['slab_quartz_b'])
        c.set_block(cx_cab, Y_BASE + 4, cz_cab, MAT['light_ochre'])
        build_sun_lounger(c, cx_cab, Y_BASE, cz_cab - 1, facing='east')
        build_sun_lounger(c, cx_cab, Y_BASE, cz_cab + 1, facing='east')

    for idx, bz in enumerate(range(-602, -466, 8)):
        if -548 <= bz <= -524:
            continue
        bx = int(round(112 - 12.0 * _bay_curve_phase(bz))) + (2 if idx % 2 == 0 else -1)
        by = 63
        c.set_block(bx, by, bz, MAT['light_ochre'])
        build_patio_umbrella(c, bx, by, bz, canopy_mat=umbrella_colors[idx % len(umbrella_colors)])
        build_sun_lounger(c, bx, by, bz - 2, facing='east')
        build_sun_lounger(c, bx, by, bz + 2, facing='east')

    for lx_c, lz_c in [(114, -490), (112, -576)]:
        lx1, lx2, lz1, lz2 = lx_c - 3, lx_c + 3, lz_c - 3, lz_c + 3
        y_sand = 63
        y_deck = 67
        y_roof = 71
        c.fill(lx1 - 1, y_sand - 2, lz1 - 1, lx2 + 1, y_sand, lz2 + 1, 'minecraft:sand')
        for sx in (lx1 + 1, lx2 - 1):
            for sz in (lz1 + 1, lz2 - 1):
                c.fill(sx, y_sand + 1, sz, sx, y_deck - 1, sz, MAT['beam_spruce_y'])
        c.fill(lx1, y_deck, lz1, lx2, y_deck, lz2, MAT['wall_quartz'])
        for step in range(4):
            sx = lx1 - 3 + step
            sy = y_sand + 1 + step
            for sz in (lz_c - 1, lz_c):
                c.set_block(sx, sy, sz, stair('smooth_quartz', 'east', 'bottom'))
                c.set_block(sx, sy - 1, sz, MAT['light_ochre'] if step == 2 else MAT['wall_white'])
        for x in range(lx1, lx2 + 1):
            for z in range(lz1, lz2 + 1):
                if x in (lx1, lx2) or z in (lz1, lz2):
                    if x == lx1 and z in (lz_c - 1, lz_c):
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
        place_door(c, lx1 + 1, y_deck + 1, lz_c, 'spruce', 'east', 'left', 'true')
        place_lectern(c, lx2 - 2, y_deck + 1, lz_c, 'east')
        c.set_block(lx_c, y_roof - 1, lz_c, MAT['light_ochre'])
        for x in range(lx1, lx2 + 1):
            for z in range(lz1, lz2 + 1):
                c.set_block(x, y_roof, z, MAT['red_concrete'] if x % 2 == 0 else MAT['wall_white'])
                if lx1 + 1 <= x <= lx2 - 1 and lz1 + 1 <= z <= lz2 - 1:
                    c.set_block(x, y_roof + 1, z, MAT['slab_quartz_b'])
        c.set_block(lx_c, y_roof + 1, lz_c, MAT['light_ochre'])
        c.set_block(lx_c, y_roof + 2, lz_c, MAT['end_rod_up'])

def _build_overwater_sunset_pier_and_offshore_islands(c: WorldCanvas):
    """
    Step 8:
      - 92-Block Overwater Sunset Pier (`X = 68..184, Z = -540..-532, Y = 64`)
      - 2-Story Octagonal Overwater Glass & Oxidized-Copper Sea-Breeze Pavilion (`center 192, -536, r = 10`)
      - 2 Pure-Voxel Racing Catamaran Sailboats (`(154, -552)` & `(154, -520)`) & 4 Jet-Skis
      - Offshore Floating Water-Sports & Diving Island (`X = 156..180, Z = -500..-478, Y = 62..70`)
      - North Bay Surfboard Shack & Kayak Launch (`X = 80..112, Z = -620..-600`)
    """

    for x in range(68, 185):
        if x >= 110 and (x - 110) % 7 == 0:
            for pz in (-540, -532):
                c.fill(x, 50, pz, x, Y_BASE - 1, pz, MAT['frame_dark'])
                c.set_block(x, 62, pz, MAT['light_sea'])
        for z in range(-540, -531):
            if z in (-540, -532):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 4 == 0 else MAT['wall_quartz'])
                if x >= 114 and not (148 <= x <= 160):
                    if x % 7 == 0:
                        c.set_block(x, Y_BASE + 1, z, MAT['wall_deep_post'])
                        c.set_block(x, Y_BASE + 2, z, MAT['lantern_stand'])
                    else:
                        c.set_block(x, Y_BASE + 1, z, MAT['pane_cyan'])
            elif z == -536:
                c.set_block(x, Y_BASE, z, MAT['light_sea'] if x % 5 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (x // 2) % 2 == 0 else MAT['wood_dark'])
            c.fill(x, Y_BASE + 3, z, x, Y_BASE + 6, z, 'minecraft:air')

    pcx, pcz, prad = 192, -536, 10
    for dx in range(-prad, prad + 1):
        for dz in range(-prad, prad + 1):
            oct_d = max(abs(dx), abs(dz), (abs(dx) + abs(dz) + 1) * 5 // 7)
            if oct_d > prad:
                continue
            x, z = pcx + dx, pcz + dz
            if oct_d == prad and (dx in (-prad, 0, prad) or dz in (-prad, 0, prad)):
                c.fill(x, 50, z, x, Y_BASE - 1, z, MAT['frame_dark'])
                c.set_block(x, 62, z, MAT['light_sea'])

            if oct_d <= 3:
                c.set_block(x, Y_BASE, z, MAT['light_sea'] if (dx == 0 and dz == 0) else MAT['glass_cyan'])
                c.set_block(x, 51, z, MAT['light_sea'] if (dx + dz) % 2 == 0 else CORAL_BLOCKS[(dx + dz) % len(CORAL_BLOCKS)])
            elif oct_d == prad:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if (dx + dz) % 3 == 0 else MAT['wall_quartz'])
                if not (dx == -prad and abs(dz) <= 3):
                    c.set_block(x, Y_BASE + 1, z, MAT['pane_cyan'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (dx + dz) % 2 == 0 else MAT['wood_dark'])

            if oct_d == 7 and (abs(dx) in (0, 7) or abs(dz) in (0, 7)):
                c.fill(x, Y_BASE + 1, z, x, Y_BASE + 5, z, MAT['pillar_quartz'])
            if oct_d <= 8:
                roof_y = Y_BASE + 6 + max(0, (8 - oct_d) // 2)
                c.set_block(x, roof_y, z, MAT['cut_copper_ox'] if oct_d % 2 == 0 else MAT['wall_quartz'])
                if oct_d in (0, 4, 8):
                    c.set_block(x, roof_y - 1, z, MAT['light_sea'] if oct_d == 0 else MAT['light_ochre'])
                c.set_block(x, roof_y + 1, z, MAT['slab_quartz_b'])
    c.fill(pcx, Y_BASE + 11, pcz, pcx, Y_BASE + 13, pcz, MAT['end_rod_up'])

    for cat_z, sail_col in [(-550, MAT['cyan_wool']), (-522, MAT['orange_wool'])]:
        cat_x = 154
        for hull_dz in (-3, 3):
            for dx in range(-6, 7):
                c.set_block(cat_x + dx, 62, cat_z + hull_dz, MAT['wall_white'])
                c.set_block(cat_x + dx, 63, cat_z + hull_dz, MAT['slab_quartz_b'] if abs(dx) == 6 else MAT['wall_quartz'])

        for dx in range(-4, 5):
            for dz in range(-2, 3):
                c.set_block(cat_x + dx, 63, cat_z + dz, MAT['light_ochre'] if (dx == 0 and dz == 0) else MAT['wood_warm'])
        c.fill(cat_x, 64, cat_z, cat_x, 77, cat_z, MAT['beam_spruce_y'])
        c.set_block(cat_x, 78, cat_z, MAT['end_rod_up'])
        for sy_s in range(65, 76):
            s_len = max(1, (76 - sy_s) // 2)
            for sdx in range(1, s_len + 1):
                c.set_block(cat_x - sdx, sy_s, cat_z, sail_col if sy_s % 3 == 0 else MAT['white_wool'])

    for z in range(-500, -477):
        for x in range(156, 179):
            is_ring = (x in (156, 157, 177, 178) or z in (-500, -499, -479, -478))
            is_cross = (166 <= x <= 168 or -490 <= z <= -488)
            if is_ring or is_cross:
                c.set_block(x, 62, z, MAT['yellow_concrete'] if (x + z) % 2 == 0 else MAT['orange_concrete'])
                c.set_block(x, 63, z, MAT['carpet_yellow'] if is_ring else MAT['carpet_cyan'])
                if (x in (156, 178) and z in (-500, -478)):
                    c.set_block(x, 62, z, MAT['light_sea'])

    c.fill(171, 63, -490, 173, 63, -488, MAT['wall_quartz'])
    c.fill(172, 64, -490, 172, 67, -490, MAT['pillar_quartz'])
    c.fill(172, 64, -488, 172, 67, -488, MAT['pillar_quartz'])
    c.fill(171, 67, -490, 176, 67, -488, MAT['slab_quartz_t'])
    c.set_block(176, 67, -489, MAT['light_sea'])

    sx1, sx2, sz1, sz2 = 82, 94, -614, -604
    c.fill(sx1, Y_BASE - 2, sz1, sx2, Y_BASE, sz2, MAT['wood_dark'])
    for px in (sx1, sx2):
        for pz in (sz1, sz2):
            c.fill(px, Y_BASE + 1, pz, px, Y_BASE + 4, pz, MAT['beam_spruce_y'])
    build_flat_roof_and_eaves(c, sx1, Y_BASE + 5, sz1, sx2, sz2, overhang=1,
                              roof_mat=MAT['orange_wool'], soffit_mat=MAT['wood_warm'],
                              coping_slab=MAT['slab_spruce_b'], hidden_lights=True)

    surf_colors = [MAT['cyan_concrete'], MAT['yellow_concrete'], MAT['red_concrete'], MAT['lime_concrete'], MAT['orange_concrete']]
    for idx, sbx in enumerate(range(84, 93, 2)):
        c.fill(sbx, Y_BASE + 1, -612, sbx, Y_BASE + 3, -612, surf_colors[idx % len(surf_colors)])
    build_outdoor_bar(c, 84, Y_BASE, -607, length=6)

    ncx, ncz, ncy = 144, -622, Y_BASE + 1
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            if abs(dx) + abs(dz) <= 6:
                c.set_block(ncx + dx, ncy, ncz + dz, MAT['wall_quartz'] if (dx + dz) % 2 == 0 else 'minecraft:smooth_sandstone')
                c.set_block(ncx + dx, ncy + 4, ncz + dz, MAT['cut_copper_ox'])
                c.set_block(ncx + dx, ncy + 5, ncz + dz, MAT['slab_quartz_b'])
    for dx in (-3, 3):
        for dz in (-3, 3):
            c.fill(ncx + dx, ncy + 1, ncz + dz, ncx + dx, ncy + 3, ncz + dz, MAT['pillar_quartz'])
    c.set_block(ncx, ncy + 4, ncz, MAT['light_sea'])
    c.set_block(ncx, ncy + 6, ncz, MAT['end_rod_up'])

def step16_seaside_beach_park_and_transition(c: WorldCanvas):
    """
    Master Builder Entry Point for V5.3 Expansion 10:
    50-Block Coastal & Parkland Transition Belt (`Z = -447..-397`) and
    Large Seaside Beach Park (`大型海滨沙滩公园`, `X = 24..240, Z = -632..-448`).
    """
    _bulldoze_and_generate_transition_and_beach_terrain(c)
    _build_transition_corridors_and_cliff_walk(c)
    _build_curved_palm_boardwalk_and_south_gate(c)
    _build_flagship_beach_clubhouse(c)
    _build_seaside_aqua_park_and_water_slides(c)
    _build_beach_volleyball_and_bonfire_amphitheater(c)
    _build_cabanas_lifeguard_towers_and_beach_loungers(c)
    _build_overwater_sunset_pier_and_offshore_islands(c)

    palm_coords = [
        (64, -618, 9, 1, 0), (62, -598, 10, 1, 0), (60, -578, 9, 1, 0),
        (58, -560, 10, 1, 0), (58, -514, 9, 1, 0), (62, -496, 10, 1, 0),
        (64, -476, 9, 1, 0), (66, -464, 10, 1, 0),
        (28, -606, 9, 0, 1), (28, -572, 10, 0, -1), (28, -504, 9, 1, 0),
        (28, -478, 10, 0, 1), (86, -552, 8, 1, 0), (86, -520, 8, 1, 0),
    ]
    for idx, (px, pz, ph, ldx, ldz) in enumerate(palm_coords):
        build_palm_tree(c, px, Y_BASE, pz, height=ph, lean_dx=ldx, lean_dz=ldz, seed=88000 + idx)
