"""
zone_beach_park.py — V5.4 Flagship Expansion: Los Angeles Santa Monica State Beach & Pacific Park Pier
======================================================================================================
Implements the V5.4 Coastal Expansion & Refinement:
  1. Extended 352-Block Coastline (`Z = -800..-448`, `X = 24..255`, extended 160 blocks further in `Z-`),
     plus the 51-Block Scenic Coastal & Parkland Transition Belt (`Z = -447..-397`) and East Coastal
     Promenade (`X = 126..255, Z = -447..-216`).
  2. 100% Custom Procedural Terrain (`自然地形不能复用，需要推倒自行生成`) & Zero Raw Cut Cliffs (`消除大片裸露石壁`):
     - Completely demolishes all natural terrain (`Y = 44..175`) across the entire zone and regenerates
       a sweeping 350-block-long **Santa Monica Crescent Golden State Beach** (`Y = 64` upper dry sand,
       `Y = 63` sunbathing slope, `Y = 62` wet intertidal sand & sparkling tidepools), dual rolling
       white-foam surf wave lines, luminous turquoise lagoon (`Y = 50..62`), and outer coral reefs.
     - Along the northern (`Z = -800..-760`) and eastern (`X = 224..255`) edges where the seed world's
       coastal mountain range sits outside the canvas, sculpts a natural **Malibu / Point Dume Coastal
       Headland & Vegetated Sandstone Terraces** that seamlessly blend to the exact outer terrain height—
       eliminating 100% of vertical cut cliffs and exposed grey stone walls!
  3. Authentic Los Angeles **Santa Monica Beach & Pier** Landmarks (Zero Matchbox Buildings!):
     - **Ocean Front Walk & The Marvin Braude Bike Trail ("The Strand", `X = 48..78, Z = -768..-448`)**:
       Curved 12-block-wide palm-lined pedestrian boardwalk + dedicated 5-block-wide turquoise & white
       coastal bicycle path with mile markers, vintage streetlamps, beach showers, and surf racks.
     - **Iconic Blue-and-White Santa Monica Yacht Harbor Arch & Pier Ramp (`X = 24..72, Z = -542..-530`)**:
       Bridges across from the California Incline & PCH directly onto the elevated wooden pier deck (`Y = 66`).
     - **Santa Monica Pier & Pacific Park Amusement Pier (`X = 72..228, Z = -608..-516, Y = 66`)**:
       * **Main Pier Promenade & Fishing Decks (`X = 72..228, Z = -544..-528, Y = 66`)** on heavy timber pilings;
       * **Pacific Park Pleasure Pier Deck (`X = 122..188, Z = -604..-544, Y = 66`)**:
         1) **The Pacific Wheel (`center X = 154, Z = -584, Y = 67..105`)**: 36-block-tall solar-powered
            giant Ferris wheel with 2 concentric illuminated neon rings, 8 radial steel spokes, and 12
            walk-in colorful passenger gondolas!
         2) **The "West Coaster" Steel Roller Coaster (`X = 124..186, Z = -602..-546, Y = 69..83`)**:
            Elevated yellow track loop with red tubular steel support trestles, banked ocean turns,
            sinusoidal camelback hills, and a pure-voxel coaster train!
         3) **Looff Hippodrome Carousel Pavilion (`X = 92..114, Z = -568..-546, Y = 66..79`)**:
            Byzantine/Moorish octagonal rotunda with a multi-tiered oxidized-copper & gold dome and
            interior illuminated carousel ring;
         4) **Playland Arcade & Carnival Midway (`X = 126..176, Z = -562..-546, Y = 66..74`)**:
            Striped carnival game booths (Skee-Ball, Ring Toss, Basketball Shootout, Funnel Cake Bar);
       * **Route 66 "End of the Trail" Sign Monument (`(192, 66, -536)`)**;
       * **Pier-End Two-Story Nautical Seafood Bistro & Angler's Lookout (`X = 198..224, Z = -546..-526, Y = 66..78`)**
         with a 2-masted Californian Coastal Schooner & 2 Racing Catamarans moored offshore.
     - **Original Muscle Beach Santa Monica (`X = 64..102, Z = -514..-472, Y = 64`, covering `(76, 65, -527)`!)**:
       - High-bar & parallel-bar gymnastics cages, flying rings frame, outdoor bench-press & squat
         barbell racks, balance beams, acrobatic tumbling turf mat, and shaded spectator pergola!
     - **Santa Monica Open-Air Beach Amphitheater & Seashell Bandstand (`X = 28..56, Z = -512..-476`)**.
     - **Perry's Beach Café, Surf Pro-Shop & Sunset Terrace (`X = 28..56, Z = -576..-548, Y = 64..75`)**:
       Articulated coastal pavilion with wrap-around timber verandas, stepped hipped roofs, and spiral stair `(34, -552)`.
     - **Annenberg Community Beach House & Seaside Aqua-Park (`X = 28..62, Z = -646..-590, Y = 61..80`)**:
       Historic-inspired Spanish-Revival pool club, 16m dual 3D water flume slides, and turquoise splash lagoon.
     - **4 Regulation Santa Monica Beach Volleyball Tournament Courts & Bleachers (`X = 76..106, Z = -682..-612`)**.
     - **Venice / Santa Monica Oceanfront Skatepark Bowls & Half-Pipe (`X = 30..60, Z = -716..-666`)**.
     - **Iconic Powder-Blue & Timber Baywatch Lifeguard Towers (Towers 14, 15, 18, 20)**, 12 VIP Cabanas,
       36 Colorful Beach Umbrella & Lounger Bays, and Offshore Floating Swim Platforms.
"""

import math
import random
from config import Y_BASE, HARBOR_FLOOR, MAT, SOFT_FLOWERS, CORAL_BLOCKS
from world_canvas import WorldCanvas
from arch_lib import (
    stair, trapdoor,
    place_barrel, place_brewing_stand, place_lectern,
    place_door, place_double_door,
    build_recessed_ceiling_grid, build_crystal_chandelier, build_illuminated_carpet_rug,
    build_curtain_wall, build_flat_roof_and_eaves,
    build_spiral_staircase, build_straight_stairs,
    build_lamppost, build_fountain, build_infinity_pool,
    build_custom_tree, build_patio_umbrella, build_sun_lounger,
    build_outdoor_sofa, build_outdoor_bar, build_arched_canal_bridge,
    build_pergola_colonnade,
    _TREE_BUILDING_GUARD,
)

def _bay_curve_phase(z: int) -> float:
    """Smooth sinusoidal crescent bay curve across Z = -768..-448 (0.0 at headlands, 1.0 at Z = -608)."""
    t = max(0.0, min(1.0, (z - (-768)) / 320.0))
    return math.sin(t * math.pi)

def _x_boardwalk_east(z: int) -> int:
    """East edge of the curved Ocean Front Walk boardwalk (X = 64 at bay center Z=-608, X = 76 at headlands)."""
    return int(round(76 - 12.0 * _bay_curve_phase(z)))

def _x_shoreline(z: int) -> int:
    """Waterline where wet sand (Y=62) meets shallow ocean surf (X = 118 at bay center, X = 136 at headlands)."""
    return int(round(136 - 18.0 * _bay_curve_phase(z)))

def build_palm_tree(c: WorldCanvas, cx: int, y_ground: int, cz: int, height: int = 9, lean_dx: int = 1, lean_dz: int = 0, seed: int = 101):
    """
    Builds a custom Californian Washingtonia / Coconut Palm tree with a gracefully curved
    stripped wood trunk, ochre froglight crown cluster, and 8 radiating arched palm fronds.
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
    c.set_block(cx, y_ground, cz, MAT['moss_block'])

def _bulldoze_and_generate_transition_and_beach_terrain(c: WorldCanvas):
    """
    Step 1: Bulldoze 100% of natural terrain in:
      - East Coastal Corridor north of the Lighthouse (`X = 124..255, Z = -447..-219`, including `(134, 65, -225)`)
      - 51-Block Transition Parkbelt (`X = -224..255, Z = -447..-397`)
      - Extended 352-Block Santa Monica State Beach (`X = 24..255, Z = -800..-448`)
    and procedurally generate custom coastal bluffs, tidal creek, 350m crescent golden beach,
    rolling surf waves, turquoise coral lagoon, and natural Point Dume / Malibu northern headland slopes!
    """
    stone_id = c.get_or_register(MAT['stone'])
    dirt_id = c.get_or_register(MAT['dirt'])
    grass_id = c.get_or_register(MAT['grass_block'])
    moss_id = c.get_or_register(MAT['moss_block'])
    sand_id = c.get_or_register('minecraft:sand')
    sandstone_id = c.get_or_register('minecraft:smooth_sandstone')
    cut_sandstone_id = c.get_or_register('minecraft:cut_sandstone')
    calcite_id = c.get_or_register(MAT['wall_calcite'])
    water_id = c.get_or_register(MAT['water'])
    sea_lantern_id = c.get_or_register(MAT['light_sea'])
    ochre_id = c.get_or_register(MAT['light_ochre'])
    prism_id = c.get_or_register(MAT['pool_shallow_1'])
    dprism_id = c.get_or_register(MAT['pool_deep_1'])
    lblue_id = c.get_or_register(MAT['pool_shallow_2'])
    air_id = c.air_id

    for z in range(-396, -218):
        for x in range(124, c.x_max + 1):
            in_lh_ellipse = (z >= -229 and 136 <= x <= 171 and ((x - 153) / 17.0) ** 2 + ((z + 212) / 15.0) ** 2 <= 1.0)
            if in_lh_ellipse:
                continue
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
        x_dry_sand = int(round(102 - 14.0 * phase))
        x_mid_sand = int(round(124 - 16.0 * phase))
        x_wet_sand = _x_shoreline(z)

        for x in range(24, c.x_max + 1):
            for y in range(46, c.y_max + 1):
                c.set_block_id(x, y, z, air_id)

            d_north_cape = ((x - 146) / 30.0) ** 2 + ((z + 772) / 16.0) ** 2
            d_south_cape = ((x - 138) / 18.0) ** 2 + ((z + 453) / 6.5) ** 2

            if z < -764:
                t_n = max(0.0, min(1.0, (-764 - z) / 36.0))
                s_n = t_n * t_n * (3.0 - 2.0 * t_n)

                ridge_wave = int(round(6.0 * math.sin((x - 24) / 35.0) + 8.0 * (1.0 - max(0.0, (x - 120) / 135.0))))
                cape_h = Y_BASE + int(round(s_n * max(2, ridge_wave)))
                for y in range(46, cape_h - 3):
                    c.set_block_id(x, y, z, stone_id)
                c.set_block_id(x, cape_h - 3, z, sandstone_id)
                c.set_block_id(x, cape_h - 2, z, cut_sandstone_id if (x + z) % 2 == 0 else sandstone_id)
                c.set_block_id(x, cape_h - 1, z, dirt_id if cape_h >= 67 else sandstone_id)
                if cape_h >= 67:
                    c.set_block_id(x, cape_h, z, moss_id if (x + z) % 3 == 0 else grass_id)
                    if (x * 5 + z * 7) % 13 == 0:
                        c.set_block(x, cape_h + 1, z, MAT['leaf_azalea'] if (x + z) % 2 == 0 else SOFT_FLOWERS[(x + z) % len(SOFT_FLOWERS)])
                else:
                    c.set_block_id(x, cape_h, z, sand_id if (x + z) % 2 == 0 else sandstone_id)
                continue

            if d_north_cape <= 1.0 or d_south_cape <= 1.0:
                cape_h = Y_BASE + (2 if d_north_cape <= 0.35 else (1 if (d_north_cape <= 0.65 or d_south_cape <= 0.55) else 0))
                for y in range(46, cape_h - 2):
                    c.set_block_id(x, y, z, stone_id)
                for y in range(cape_h - 2, cape_h + 1):
                    c.set_block_id(x, y, z, sandstone_id)
                if d_north_cape <= 0.48 and (x + z) % 3 == 0:
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
                if dist_sea <= 24:
                    seabed_y = max(55, 61 - dist_sea // 4)
                    for y in range(46, seabed_y - 1):
                        c.set_block_id(x, y, z, stone_id)
                    c.set_block_id(x, seabed_y - 1, z, sandstone_id)
                    if (x + z) % 7 == 0:
                        c.set_block_id(x, seabed_y, z, sea_lantern_id)
                    elif dist_sea >= 8 and (x + z) % 2 == 0:
                        c.set_block_id(x, seabed_y, z, lblue_id if dist_sea < 16 else prism_id)
                    else:
                        c.set_block_id(x, seabed_y, z, sand_id)
                    for y in range(seabed_y + 1, 63):
                        c.set_block_id(x, y, z, water_id)

                    wave_jitter = int(round(1.4 * math.sin(z / 6.5)))
                    if dist_sea in (6 + wave_jitter, 14 + wave_jitter, 21 + wave_jitter):
                        c.set_block(x, 62, z, MAT['glass_white'])
                        if (x + z) % 2 == 0 and -756 <= z <= -462 and not (-608 <= z <= -522):
                            c.set_block(x, 63, z, MAT['slab_quartz_b'])
                else:
                    seabed_y = HARBOR_FLOOR + (2 if dist_sea < 38 else 0)
                    for y in range(44, seabed_y - 1):
                        c.set_block_id(x, y, z, stone_id)
                    c.set_block_id(x, seabed_y - 1, z, sandstone_id)
                    if (x % 6 == 0 and z % 6 == 0):
                        c.set_block_id(x, seabed_y, z, sea_lantern_id)
                    elif ((x + z) % 9 == 0):
                        c.set_block_id(x, seabed_y, z, ochre_id)
                    elif (x + z) % 3 == 0:
                        c.set_block_id(x, seabed_y, z, prism_id if dist_sea < 58 else dprism_id)
                    else:
                        c.set_block_id(x, seabed_y, z, sand_id)
                    for y in range(seabed_y + 1, 63):
                        c.set_block_id(x, y, z, water_id)

                    if 172 <= x <= 246 and -752 <= z <= -464 and not (-612 <= z <= -520):
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
    and the East Coastal Corridor (`Z = -447..-216`), with a 100% seamless junction at `(134, 65, -225)`.
    """

    for z in range(-448, -215):
        creek_center_z = -422 + int(round(3.0 * math.sin(131 / 22.0)))
        if abs(z - creek_center_z) <= 4:
            continue
        for x in range(126, 137):
            c.fill(x, 52, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 5, z, 'minecraft:air')
            if x == 136:
                c.set_block(x, Y_BASE, z, MAT['light_sea'] if z % 4 == 0 else MAT['wall_quartz'])

                if z < -226 and not (-296 <= z <= -284 or -366 <= z <= -354):
                    c.set_block(x, Y_BASE + 1, z, MAT['pane_black'])
            elif x == 126:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['stone_pol_and'])
            elif x in (130, 131, 132):
                c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (z // 2) % 2 == 0 else MAT['wood_dark'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
        if z % 12 == 0 and z < -220 and not (-298 <= z <= -282 or -368 <= z <= -352):
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

def _build_ocean_front_walk_and_marvin_braude_bike_trail(c: WorldCanvas):
    """
    Step 3: Builds Santa Monica's signature **Ocean Front Walk** timber & mosaic boardwalk
    and the **Marvin Braude Coastal Bike Trail ("The Strand")** across `Z = -764..-448` (`317` blocks long!),
    plus the South Coastal Welcome Plaza & Seashell Wave Archway (`Z = -462..-448`).
    """

    for z in range(-764, -447):
        x_bw = _x_boardwalk_east(z)
        x_west = x_bw - 9

        for x in range(x_west, x_bw + 1):
            if x == x_bw:
                c.set_block(x, Y_BASE, z, MAT['light_sea'] if z % 4 == 0 else MAT['wall_quartz'])

                if z in (-736, -700, -664, -628, -592, -556, -516, -476):
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

        x_bike_e = x_west - 2
        x_bike_w = x_west - 6
        c.set_block(x_west - 1, Y_BASE, z, MAT['moss_block'] if z % 4 != 0 else MAT['light_ochre'])
        for x in range(x_bike_w, x_bike_e + 1):
            if x in (x_bike_w, x_bike_e):
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
            elif x == (x_bike_w + x_bike_e) // 2:

                c.set_block(x, Y_BASE, z, MAT['yellow_concrete'] if z % 4 in (0, 1) else 'minecraft:cyan_terracotta')
            else:

                c.set_block(x, Y_BASE, z, 'minecraft:cyan_terracotta')
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 4, z, 'minecraft:air')

        if z % 14 == 0 and -752 <= z <= -460 and not (-546 <= z <= -526):
            build_lamppost(c, x_west, Y_BASE + 1, z, style='courtyard')

    for z_range in [range(-462, -455), range(-542, -529), range(-618, -610), range(-695, -687), range(-756, -748)]:
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

def _build_original_muscle_beach_and_amphitheater(c: WorldCanvas):
    """
    Step 4: Directly addresses User Issue 3 (`76 65 -527 海滨沙滩公园，长度不够，细节不丰富`):
      - Builds the world-famous **Original Muscle Beach Santa Monica (`X = 66..102, Z = -528..-472, Y = 64`)**
        right across `(76, 65, -527)`!
        Includes:
        (a) Checkered Turquoise/White Padded Gymnastics & Acrobatic Tumbling Turf (`X = 72..92, Z = -528..-508`)
            with High-Bar & Parallel-Bar Calisthenics Rig, Pull-Up Cage, and Outdoor Barbell Bench-Press & Squat Racks!
        (b) Iconic Giant Wooden/Steel Travelling Rings A-Frame Rig (`X = 74..94, Z = -504..-494, Y = 64..72`)
            with suspended `iron_chain` + quartz/gold gymnastic rings over a soft sand pit!
        (c) Muscle Beach Strongman Stage, Kettlebell/Dumbbell Rack, Balance Beams & Shaded Spectator Pergola (`Z = -490..-474`).
      - Builds the **Sunken Beach Bonfire Amphitheater & Acoustic Seashell Bandstand (`X = 28..54, Z = -512..-476`)**.
    """

    for z in range(-529, -505):
        for x in range(70, 97):
            c.fill(x, 60, z, x, Y_BASE - 1, z, 'minecraft:smooth_sandstone')
            if x in (70, 96) or z in (-529, -506):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if (x + z) % 5 == 0 else MAT['wall_quartz'])
            elif 73 <= x <= 83 and -527 <= z <= -517:

                c.set_block(x, Y_BASE, z, MAT['cyan_concrete'] if (x + z) % 2 == 0 else MAT['pool_shallow_2'])
            elif 85 <= x <= 93 and -527 <= z <= -509:

                c.set_block(x, Y_BASE, z, 'minecraft:sand')
            else:
                c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (x + z) % 2 == 0 else MAT['wall_quartz'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 8, z, 'minecraft:air')

    for bz in (-525, -520):

        c.set_block(76, Y_BASE + 1, bz, stair('smooth_quartz', 'west', 'bottom'))
        c.set_block(77, Y_BASE + 1, bz, MAT['slab_dark_b'])
        c.set_block(78, Y_BASE + 1, bz, MAT['slab_dark_b'])

        c.set_block(76, Y_BASE + 2, bz - 1, MAT['chiseled_deepslate'])
        c.set_block(76, Y_BASE + 2, bz, MAT['end_rod_n'])
        c.set_block(76, Y_BASE + 2, bz + 1, MAT['chiseled_deepslate'])

    for rz in (-524, -522):
        c.fill(81, Y_BASE + 1, rz, 81, Y_BASE + 3, rz, MAT['frame_dark'])
        c.set_block(81, Y_BASE + 3, rz - (1 if rz == -524 else -1), MAT['wall_black'])
    c.set_block(81, Y_BASE + 3, -523, MAT['end_rod_n'])
    c.set_block(81, Y_BASE + 1, -523, MAT['light_ochre'])

    for px in (86, 89, 92):
        for pz in (-526, -522, -518):
            c.fill(px, Y_BASE + 1, pz, px, Y_BASE + 4, pz, MAT['frame_dark'])
            c.set_block(px, Y_BASE + 5, pz, MAT['slab_quartz_b'])
    for px in (86, 89, 92):
        for z_bar in range(-525, -518):
            if z_bar != -522:
                c.set_block(px, Y_BASE + 4, z_bar, MAT['end_rod_n'])
    for pz in (-526, -522, -518):
        for x_bar in (87, 88, 90, 91):
            c.set_block(x_bar, Y_BASE + 4, pz, MAT['end_rod_e'])

    for z_pb in range(-515, -509):
        for px_pb in (87, 89):
            c.set_block(px_pb, Y_BASE + 1, z_pb, MAT['iron_bars'] if z_pb in (-515, -510) else 'minecraft:air')
            c.set_block(px_pb, Y_BASE + 2, z_pb, MAT['end_rod_n'])

        c.set_block(92, Y_BASE + 1, z_pb, MAT['slab_spruce_t'] if z_pb not in (-515, -510) else MAT['beam_spruce_y'])

    for pz in (-528, -518, -508):
        c.fill(71, Y_BASE + 1, pz, 71, Y_BASE + 4, pz, MAT['beam_spruce_y'])
        c.set_block(71, Y_BASE + 5, pz, MAT['light_ochre'])
    for z_can in range(-528, -507):
        c.set_block(71, Y_BASE + 5, z_can, MAT['slab_quartz_b'] if z_can % 2 == 0 else MAT['cyan_concrete'])
        c.set_block(72, Y_BASE + 5, z_can, MAT['slab_spruce_b'])

    for z in range(-504, -487):
        for x in range(74, 97):
            c.fill(x, 60, z, x, Y_BASE - 1, z, 'minecraft:smooth_sandstone')
            if x in (74, 96) or z in (-504, -488):
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, 'minecraft:sand')
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 10, z, 'minecraft:air')

    for tx_r in (76, 94):
        for dz_leg in (-2, 2):
            c.fill(tx_r, Y_BASE + 1, -496 + dz_leg, tx_r, Y_BASE + 6, -496 + dz_leg, MAT['beam_spruce_y'])
        c.fill(tx_r, Y_BASE + 6, -498, tx_r, Y_BASE + 7, -494, MAT['frame_dark'])
    c.fill(76, Y_BASE + 8, -496, 94, Y_BASE + 8, -496, MAT['frame_dark'])
    for rx in range(78, 93, 2):
        c.set_block(rx, Y_BASE + 7, -496, MAT['chain_y'])
        c.set_block(rx, Y_BASE + 6, -496, MAT['chain_y'])
        c.set_block(rx, Y_BASE + 5, -496, MAT['end_rod_down'])
        if rx % 4 == 2:
            c.set_block(rx, Y_BASE + 8, -496, MAT['light_ochre'])

    acx, acz = 42, -494
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

    for x in range(36, 49):
        u = (x - 42) / 6.0
        shell_h = int(round(5.0 * max(0.0, 1.0 - u * u)))
        c.fill(x, Y_BASE, -507, x, Y_BASE + 1, -503, MAT['wood_dark'])
        for y in range(Y_BASE + 1, Y_BASE + 2 + shell_h):
            c.set_block(x, y, -507, MAT['wall_quartz'] if (x + y) % 2 == 0 else MAT['wall_white'])
        if shell_h > 0:
            c.set_block(x, Y_BASE + 2 + shell_h, -507, MAT['slab_quartz_b'])
            c.set_block(x, Y_BASE + 1 + shell_h, -506, MAT['light_sea'] if x % 2 == 0 else MAT['slab_quartz_t'])
    c.set_block(40, Y_BASE + 2, -505, MAT['note_block'])
    c.set_block(42, Y_BASE + 2, -505, MAT['jukebox'])
    c.set_block(44, Y_BASE + 2, -505, MAT['note_block'])

def _build_santa_monica_pier_and_pacific_park(c: WorldCanvas):
    """
    Step 5: Builds the centerpiece **Los Angeles Santa Monica Pier & Pacific Park Amusement Pier**
    (`X = 24..228, Z = -608..-522, Y = 64..105`):
      1. **Iconic Blue-and-White "SANTA MONICA YACHT HARBOR" Pier Entrance Arch (`X = 62, Z = -542..-530`)**
         & Pier Approach Bridge (`X = 24..72, Z = -542..-530, Y = 64 -> 66`).
      2. **Main Timber Pier Promenade & Fishing Decks (`X = 72..226, Z = -544..-528, Y = 66`)**
         supported on heavy dark-oak pilings driven into the seabed (`Y = 50..65`).
      3. **Looff Hippodrome Carousel Pavilion (`X = 90..114, Z = -570..-545, Y = 66..80`)**:
         Historic octagonal/stepped Californian coastal landmark with an oxidized-copper & gold dome,
         arched stained-glass clerestory windows, and an interior illuminated carousel ring!
      4. **Pacific Park Amusement Pier Deck (`X = 118..190, Z = -606..-544, Y = 66`)**:
         - **The Pacific Wheel (`center X = 154, Z = -586, Y = 67..105`)**: 36-block-tall solar-powered
           Ferris wheel with twin steel A-frame support towers, 2 concentric illuminated neon rings
           (`r = 15` and `r = 9`), 8 radial spokes, and 12 colorful walk-in passenger gondolas!
         - **The "West Coaster" Steel Roller Coaster (`X = 122..188, Z = -604..-546, Y = 69..82`)**:
           Elevated yellow/gold coaster track loop on red steel trestle columns with sinusoidal hills,
           banked ocean turns, and a 3-car coaster train!
         - **Playland Arcade & Carnival Midway Booths (`X = 124..180, Z = -562..-546, Y = 66..73`)**:
           Colorful striped carnival game stalls, Skee-Ball lanes, and a Seaside Churro & Funnel Cake Bar!
      5. **Historic Route 66 "End of the Trail" Monument (`(192, 66, -536)`)** & **Pier-End Two-Story
         Nautical Seafood Bistro & Angler's Lookout (`X = 198..224, Z = -545..-527, Y = 66..78`)**.
    """
    y_pier = Y_BASE + 2

    for x in range(24, 73):
        py = Y_BASE if x < 50 else (Y_BASE + 1 if x < 64 else y_pier)
        use_slab = (x in (49, 63))
        for z in range(-542, -529):
            c.fill(x, 54, z, x, py - 1, z, MAT['stone_pol_and'])
            c.fill(x, py + 1, z, x, py + 12, z, 'minecraft:air')
            if z in (-542, -530):
                c.set_block(x, py, z, MAT['light_ochre'] if x % 5 == 0 else MAT['wall_quartz'])
                c.set_block(x, py + 1, z, MAT['pane_white'])
            elif z == -536:
                c.set_block(x, py, z, MAT['light_sea'] if x % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, py, z, MAT['slab_spruce_b'] if use_slab else (MAT['wood_warm'] if (x // 2) % 2 == 0 else MAT['wood_dark']))

    for pz in (-542, -530):
        c.fill(64, y_pier + 1, pz, 64, y_pier + 8, pz, MAT['pillar_quartz'])
        c.set_block(64, y_pier + 9, pz, MAT['light_sea'])
    for z in range(-542, -529):
        u = (z - (-536)) / 6.0
        arch_dy = int(round(2.5 * max(0.0, 1.0 - u * u)))
        ay = y_pier + 8 + arch_dy
        c.set_block(64, ay, z, MAT['blue_concrete'])
        c.set_block(64, ay + 1, z, MAT['wall_white'] if z % 2 == 0 else MAT['light_sea'])
        c.set_block(64, ay + 2, z, MAT['slab_quartz_b'])

    for x in range(72, 227):

        if (x - 72) % 6 == 0:
            for pz in (-544, -536, -528):
                c.fill(x, 50, pz, x, y_pier - 1, pz, MAT['beam_dark_y'])
                c.set_block(x, 62, pz, MAT['light_sea'] if pz == -536 else MAT['beam_dark_y'])
            c.fill(x, y_pier - 1, -544, x, y_pier - 1, -528, MAT['beam_dark_z'])

        for z in range(-544, -527):
            c.fill(x, y_pier + 1, z, x, y_pier + 12, z, 'minecraft:air')
            if z in (-544, -528):
                c.set_block(x, y_pier, z, MAT['light_ochre'] if x % 4 == 0 else MAT['wall_quartz'])

                if not (z == -544 and 92 <= x <= 186):
                    if x % 6 == 0:
                        c.set_block(x, y_pier + 1, z, MAT['wall_deep_post'])
                        c.set_block(x, y_pier + 2, z, MAT['lantern_stand'])
                    else:
                        c.set_block(x, y_pier + 1, z, MAT['pane_white'])
            elif z == -536:
                c.set_block(x, y_pier, z, MAT['light_sea'] if x % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, y_pier, z, MAT['wood_warm'] if (x // 2) % 2 == 0 else MAT['wood_dark'])

    for x in range(90, 189):
        for z in range(-604, -544):

            if (x - 90) % 6 == 0 and (z + 604) % 6 == 0:
                c.fill(x, 50, z, x, y_pier - 1, z, MAT['beam_dark_y'])
                if (x + z) % 12 == 0:
                    c.set_block(x, 62, z, MAT['light_sea'])

            is_edge = (x in (90, 188) or z == -604)
            if is_edge:
                c.set_block(x, y_pier, z, MAT['light_ochre'] if (x + z) % 4 == 0 else MAT['wall_quartz'])
                c.set_block(x, y_pier + 1, z, MAT['pane_cyan'])
            elif (x - 90) % 8 == 0 or (z + 604) % 8 == 0:
                c.set_block(x, y_pier, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, y_pier, z, MAT['wood_warm'] if (x + z) % 2 == 0 else MAT['wood_dark'])

    hcx, hcz, hrad = 103, -557, 10
    for dx in range(-hrad, hrad + 1):
        for dz in range(-hrad, hrad + 1):
            oct_d = max(abs(dx), abs(dz), (abs(dx) + abs(dz) + 1) * 5 // 7)
            if oct_d > hrad:
                continue
            x, z = hcx + dx, hcz + dz
            c.set_block(x, y_pier, z, MAT['wall_quartz'] if (dx + dz) % 2 == 0 else MAT['wood_birch'])
            if oct_d == hrad:

                is_portal = ((abs(dx) <= 2 and dz in (-hrad, hrad)) or (abs(dz) <= 2 and dx in (-hrad, hrad)))
                for y in range(y_pier + 1, y_pier + 7):
                    if is_portal and y <= y_pier + 4:
                        c.set_block(x, y, z, 'minecraft:air')
                    elif y in (y_pier + 1, y_pier + 6):
                        c.set_block(x, y, z, MAT['wall_quartz'])
                    elif (dx + dz) % 2 == 0:
                        c.set_block(x, y, z, MAT['glass_yellow'] if y == y_pier + 5 else MAT['glass_clear'])
                    else:
                        c.set_block(x, y, z, MAT['wall_white'])
            elif oct_d == 5:

                if (dx + dz) % 2 == 0:
                    c.set_block(x, y_pier + 1, z, MAT['gold_block'] if abs(dx) == abs(dz) else MAT['cyan_wool'])
                    c.set_block(x, y_pier + 2, z, stair('smooth_quartz', 'north' if dz < 0 else 'south', 'bottom'))
                    c.fill(x, y_pier + 3, z, x, y_pier + 5, z, MAT['end_rod_up'])
            elif oct_d <= 2:

                c.fill(x, y_pier + 1, z, x, y_pier + 6, z, MAT['gold_block'] if (dx == 0 and dz == 0) else MAT['light_ochre'])

            if oct_d <= hrad:
                roof_y = y_pier + 7 + max(0, (hrad - oct_d) // 2)
                c.set_block(x, roof_y, z, MAT['cut_copper_ox'] if oct_d % 2 == 0 else MAT['wall_quartz'])
                c.set_block(x, roof_y + 1, z, MAT['slab_quartz_b'])
                if oct_d in (0, 4, 8):
                    c.set_block(x, roof_y - 1, z, MAT['light_ochre'])
    c.fill(hcx, y_pier + 13, hcz, hcx, y_pier + 15, hcz, MAT['end_rod_up'])

    stall_specs = [
        (122, 132, MAT['red_wool'], MAT['white_wool'], 'skee_ball'),
        (136, 146, MAT['cyan_wool'], MAT['yellow_wool'], 'hoop_shoot'),
        (150, 160, MAT['orange_wool'], MAT['white_wool'], 'funnel_cake'),
    ]
    for sx1, sx2, stripe_a, stripe_b, s_role in stall_specs:
        sz1, sz2 = -556, -549
        c.fill(sx1, y_pier, sz1, sx2, y_pier, sz2, MAT['wood_dark'])
        for x in range(sx1, sx2 + 1):
            for z in range(sz1, sz2 + 1):

                c.set_block(x, y_pier + 5, z, stripe_a if (x - sx1) % 2 == 0 else stripe_b)
                if x in (sx1, sx2) and z in (sz1, sz2):
                    c.fill(x, y_pier + 1, z, x, y_pier + 4, z, MAT['beam_spruce_y'])
                elif z == sz1:
                    c.fill(x, y_pier + 1, z, x, y_pier + 4, z, MAT['wall_white'] if (x - sx1) % 2 == 0 else stripe_a)
                elif z == sz2 and sx1 + 1 <= x <= sx2 - 1:

                    c.set_block(x, y_pier + 1, z, MAT['wood_warm'])
                    c.set_block(x, y_pier + 2, z, MAT['slab_quartz_b'])
        c.set_block((sx1 + sx2) // 2, y_pier + 4, (sz1 + sz2) // 2, MAT['light_ochre'])
        if s_role == 'hoop_shoot':
            c.set_block((sx1 + sx2) // 2, y_pier + 3, sz1 + 1, 'minecraft:target')
        elif s_role == 'funnel_cake':
            place_brewing_stand(c, sx1 + 3, y_pier + 2, sz2)
            place_barrel(c, sx2 - 2, y_pier + 1, sz1 + 1, 'south')

    track_pts = []
    for x in range(122, 185):
        track_pts.append((x, -562))
    for z in range(-562, -601, -1):
        track_pts.append((184, z))
    for x in range(184, 121, -1):
        track_pts.append((x, -600))
    for z in range(-600, -562):
        track_pts.append((122, z))

    n_pts = len(track_pts)
    for idx, (tx, tz) in enumerate(track_pts):
        angle = (idx / n_pts) * 2.0 * math.pi
        ty = y_pier + 5 + int(round(4.5 * (1.0 + math.sin(angle * 3.0 - 0.6))))

        c.set_block(tx, ty, tz, MAT['yellow_concrete'])
        c.set_block(tx, ty + 1, tz, MAT['carpet_yellow'] if idx % 2 == 0 else MAT['slab_quartz_b'])
        if idx % 5 == 0:
            c.set_block(tx, ty - 1, tz, MAT['light_ochre'])

        if idx % 8 == 0:
            c.fill(tx, y_pier + 1, tz, tx, ty - 1, tz, MAT['red_concrete'])

        if 96 <= idx <= 106 and idx % 2 == 0:
            c.set_block(tx, ty + 1, tz, MAT['red_concrete'] if idx == 96 else MAT['cyan_concrete'])
            c.set_block(tx, ty + 2, tz, stair('smooth_quartz', 'west', 'bottom'))

    fcx, fcz, fcy, frad = 154, -582, 86, 15

    c.fill(fcx - 8, y_pier + 1, fcz - 4, fcx + 8, y_pier + 2, fcz + 4, MAT['wall_quartz'])
    build_straight_stairs(c, fcx - 10, y_pier + 1, fcz - 1, width=3, height=2, direction='east', stair_prefix='smooth_quartz')

    for dy_t in range(0, fcy - (y_pier + 2) + 1):
        wy = (y_pier + 2) + dy_t
        frac = 1.0 - (dy_t / max(1.0, fcy - (y_pier + 2)))
        dx_leg = int(round(9.0 * frac))
        for sz_leg in (fcz - 3, fcz + 3):
            c.set_block(fcx - dx_leg, wy, sz_leg, MAT['wall_white'])
            c.set_block(fcx + dx_leg, wy, sz_leg, MAT['wall_white'])
            if dy_t % 4 == 0:
                c.set_block(fcx - dx_leg, wy, sz_leg, MAT['light_sea'])
                c.set_block(fcx + dx_leg, wy, sz_leg, MAT['light_sea'])

    c.fill(fcx - 1, fcy - 1, fcz - 3, fcx + 1, fcy + 1, fcz + 3, MAT['gold_block'])
    c.set_block(fcx, fcy, fcz - 3, MAT['light_sea'])
    c.set_block(fcx, fcy, fcz + 3, MAT['light_sea'])

    for dx in range(-frad - 1, frad + 2):
        for dy in range(-frad - 1, frad + 2):
            r = math.hypot(dx, dy)
            x, y = fcx + dx, fcy + dy

            if 14.3 <= r <= 15.6:
                for rz in (fcz - 2, fcz + 2):
                    c.set_block(x, y, rz, MAT['light_sea'] if (dx + dy) % 3 == 0 else MAT['wall_white'])

            elif 8.4 <= r <= 9.5:
                for rz in (fcz - 2, fcz + 2):
                    c.set_block(x, y, rz, MAT['light_ochre'] if (dx + dy) % 2 == 0 else MAT['magenta_stained_glass'] if 'magenta_stained_glass' in MAT else MAT['glass_magenta'])

    gondola_colors = [
        MAT['red_concrete'], MAT['orange_concrete'], MAT['yellow_concrete'],
        MAT['lime_concrete'], MAT['cyan_concrete'], MAT['blue_concrete'],
        MAT['purple_concrete'], MAT['red_concrete'], MAT['orange_concrete'],
        MAT['yellow_concrete'], MAT['cyan_concrete'], MAT['blue_concrete'],
    ]
    for i_sp in range(12):
        theta = i_sp * (2.0 * math.pi / 12.0)
        cos_t, sin_t = math.cos(theta), math.sin(theta)

        for step_r in range(2, frad):
            sx = fcx + int(round(step_r * cos_t))
            sy = fcy + int(round(step_r * sin_t))
            for rz in (fcz - 2, fcz + 2):
                c.set_block(sx, sy, rz, MAT['iron_bars'] if step_r % 3 != 0 else MAT['light_pearl'])

        gx = fcx + int(round(frad * cos_t))
        gy = fcy + int(round(frad * sin_t))
        g_col = gondola_colors[i_sp % len(gondola_colors)]
        c.fill(gx - 1, gy - 1, fcz - 1, gx + 1, gy - 1, fcz + 1, g_col)
        c.set_block(gx, gy - 1, fcz, MAT['light_ochre'])
        c.fill(gx - 1, gy + 1, fcz - 1, gx + 1, gy + 1, fcz + 1, MAT['slab_quartz_b'])
        for gdx in (-1, 1):
            c.set_block(gx + gdx, gy, fcz - 1, MAT['pane_clear'])
            c.set_block(gx + gdx, gy, fcz + 1, MAT['pane_clear'])

    c.fill(191, y_pier + 1, -537, 193, y_pier + 1, -535, MAT['wall_quartz'])
    c.fill(192, y_pier + 2, -536, 192, y_pier + 6, -536, MAT['pillar_quartz'])

    for dz_s in (-1, 0, 1):
        c.set_block(192, y_pier + 5, -536 + dz_s, MAT['wall_white'] if dz_s == 0 else MAT['red_concrete'])
        c.set_block(192, y_pier + 6, -536 + dz_s, MAT['blue_concrete'] if dz_s == 0 else MAT['wall_white'])
    c.set_block(192, y_pier + 7, -536, MAT['light_ochre'])

    bx1, bx2, bz1, bz2 = 200, 218, -543, -529
    for x in range(198, 225):
        for z in range(-545, -526):
            if (x - 198) % 6 == 0 and (z + 545) % 6 == 0:
                c.fill(x, 50, z, x, y_pier - 1, z, MAT['frame_dark'])
                c.set_block(x, 62, z, MAT['light_sea'])
            c.set_block(x, y_pier, z, MAT['wood_warm'] if (x + z) % 2 == 0 else MAT['wood_dark'])
            if x in (198, 224) or z in (-545, -527):
                c.set_block(x, y_pier, z, MAT['light_ochre'] if (x + z) % 4 == 0 else MAT['wall_quartz'])
                if not (x == 198 and -540 <= z <= -532):
                    c.set_block(x, y_pier + 1, z, MAT['pane_cyan'])

    for dx_w in (-1, 0, 1):
        for dz_w in (-2, -1, 0, 1, 2):
            c.set_block(221 + dx_w, y_pier, -536 + dz_w, MAT['glass_cyan'])
            c.set_block(221 + dx_w, 51, -536 + dz_w, MAT['light_sea'])

    c.fill(bx1, y_pier, bz1, bx2, y_pier, bz2, MAT['wall_quartz'])
    c.fill(bx1, y_pier + 1, bz1, bx2, y_pier + 5, bz2, MAT['wall_white'])
    c.fill(bx1 + 1, y_pier + 1, bz1 + 1, bx2 - 1, y_pier + 5, bz2 - 1, 'minecraft:air')
    build_curtain_wall(c, bx1, y_pier + 1, bz1 + 2, bx1, y_pier + 5, bz2 - 2, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=3)
    build_curtain_wall(c, bx2, y_pier + 1, bz1 + 2, bx2, y_pier + 5, bz2 - 2, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=3)
    build_curtain_wall(c, bx1 + 2, y_pier + 1, bz1, bx2 - 2, y_pier + 5, bz1, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, bx1 + 2, y_pier + 1, bz2, bx2 - 2, y_pier + 5, bz2, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    place_double_door(c, bx1, y_pier + 1, -536, 'dark_oak', 'east', 'true')
    place_double_door(c, bx2, y_pier + 1, -536, 'dark_oak', 'west', 'true')

    build_illuminated_carpet_rug(c, bx1 + 3, y_pier, bz1 + 2, bx2 - 3, bz2 - 2, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_bar(c, 205, y_pier, -540, length=8)
    build_outdoor_sofa(c, 206, y_pier, -533, length=6, facing='north')

    for step_r in range(4):
        rx1, rx2 = bx1 - 1 + step_r * 2, bx2 + 1 - step_r * 2
        rz1, rz2 = bz1 - 1 + step_r, bz2 + 1 - step_r
        ry = y_pier + 6 + step_r
        c.fill(rx1, ry, rz1, rx2, ry, rz2, MAT['cut_copper_ox'] if step_r % 2 == 0 else MAT['wall_quartz'])
        for x_e in range(rx1, rx2 + 1):
            c.set_block(x_e, ry + 1, rz1, MAT['slab_quartz_b'])
            c.set_block(x_e, ry + 1, rz2, MAT['slab_quartz_b'])
    c.fill(208, y_pier + 10, -537, 210, y_pier + 11, -535, MAT['light_sea'])
    c.set_block(209, y_pier + 12, -536, MAT['end_rod_up'])

def _build_perrys_beach_cafe_and_annenberg_aqua_club(c: WorldCanvas):
    """
    Step 6:
      - **Perry's Beach Café, Surf Pro-Shop & Sunset Veranda (`X = 28..54, Z = -576..-548, Y = 64..76`)**:
        Articulated Californian coastal pavilion with wrap-around timber porch, stepped roof, and spiral stair `(34, -552)`.
      - **Annenberg Community Beach House & Seaside Aqua-Park (`X = 28..60, Z = -648..-590, Y = 61..80`)**:
        16m Slide Launch Tower (spiral staircase at `(37, -641)`), Dual 3D Water Flume Slides, and Splash Lagoon Pool.
    """

    cx1, cx2, cz1, cz2 = 30, 52, -574, -550
    y_1f, y_2f, y_roof = Y_BASE, Y_BASE + 7, Y_BASE + 12

    for z in range(cz1 - 3, cz2 + 4):
        for x in range(cx1 - 3, cx2 + 5):
            c.set_block(x, y_1f, z, MAT['wall_quartz'] if (x + z) % 3 == 0 else MAT['stone_smooth'])
            c.fill(x, y_1f + 1, z, x, y_roof + 3, z, 'minecraft:air')

    c.fill(cx1, y_1f - 1, cz1, cx2, y_1f - 1, cz2, MAT['stone_pol_and'])
    for z in range(cz1, cz2 + 1):
        for x in range(cx1, cx2 + 1):
            c.set_block(x, y_1f, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['wood_birch'])

    c.fill(cx1, y_1f + 1, cz1, cx2, y_2f - 1, cz2, MAT['wall_white'])
    c.fill(cx1 + 1, y_1f + 1, cz1 + 1, cx2 - 1, y_2f - 1, cz2 - 1, 'minecraft:air')
    build_curtain_wall(c, cx2, y_1f + 1, cz1 + 2, cx2, y_2f - 1, cz2 - 2, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, cx1, y_1f + 1, cz1 + 2, cx1, y_2f - 1, cz2 - 2, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, cx1 + 2, y_1f + 1, cz1, cx2 - 2, y_2f - 1, cz1, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)
    build_curtain_wall(c, cx1 + 2, y_1f + 1, cz2, cx2 - 2, y_2f - 1, cz2, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=4)

    build_recessed_ceiling_grid(c, cx1 + 2, y_2f, cz1 + 2, cx2 - 2, cz2 - 2, step_x=4, step_z=4, light_mat=MAT['light_ochre'])
    build_illuminated_carpet_rug(c, 36, y_1f, -568, 48, -556, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_bar(c, 38, y_1f, -570, length=8)
    build_outdoor_sofa(c, 39, y_1f, -560, length=6, facing='north')

    c.fill(cx1, y_2f, cz1, cx2, y_2f, cz2, MAT['wood_dark'])
    for x in range(cx1, cx2 + 1):
        for z in (cz1, cz2):
            c.set_block(x, y_2f, z, MAT['wall_quartz'])
            c.set_block(x, y_2f + 1, z, MAT['pane_cyan'])
    for z in range(cz1, cz2 + 1):
        for x in (cx1, cx2):
            c.set_block(x, y_2f, z, MAT['wall_quartz'])
            c.set_block(x, y_2f + 1, z, MAT['pane_cyan'])

    c.fill(33, y_2f + 1, -570, 47, y_roof - 1, -556, MAT['wall_white'])
    c.fill(34, y_2f + 1, -569, 46, y_roof - 1, -557, 'minecraft:air')
    build_curtain_wall(c, 47, y_2f + 1, -568, 47, y_roof - 1, -558, MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=3)
    build_curtain_wall(c, 33, y_2f + 1, -568, 33, y_roof - 1, -558, MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=3)
    place_double_door(c, 47, y_2f + 1, -563, 'dark_oak', 'west', 'true')
    place_double_door(c, 40, y_2f + 1, -556, 'dark_oak', 'north', 'true')
    build_flat_roof_and_eaves(c, 33, y_roof, -570, 47, -556, overhang=2, roof_mat='minecraft:orange_terracotta',
                              soffit_mat=MAT['wood_warm'], coping_slab=MAT['slab_quartz_b'], hidden_lights=True)

    build_spiral_staircase(c, 35, y_1f + 1, y_2f, -553, radius=2, start_sector=1, clockwise=True)
    for uz in (-570, -562):
        build_patio_umbrella(c, 50, y_2f, uz)

    place_double_door(c, cx1, y_1f + 1, -562, 'dark_oak', 'east', 'true')
    place_double_door(c, cx2, y_1f + 1, -562, 'dark_oak', 'west', 'true')
    place_double_door(c, 41, y_1f + 1, cz1, 'dark_oak', 'south', 'true')
    place_double_door(c, 41, y_1f + 1, cz2, 'dark_oak', 'north', 'true')

    for z in range(-648, -593):
        for x in range(28, 59):
            if x in (28, 58) or z in (-648, -594):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 16, z, 'minecraft:air')

    build_infinity_pool(c, 32, Y_BASE, -630, 54, -598)
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            if abs(dx) + abs(dz) <= 4:
                c.fill(43 + dx, Y_BASE - 2, -614 + dz, 43 + dx, Y_BASE, -614 + dz, MAT['wall_quartz'])
                if abs(dx) == 2 or abs(dz) == 2:
                    c.set_block(43 + dx, Y_BASE + 1, -614 + dz, MAT['slab_quartz_b'])
                elif dx == 0 and dz == 0:
                    c.fill(43, Y_BASE + 1, -614, 43, Y_BASE + 4, -614, MAT['beam_spruce_y'])
                    c.set_block(43, Y_BASE + 4, -614, MAT['light_ochre'])
                    for cdx in (-2, -1, 0, 1, 2):
                        for cdz in (-2, -1, 0, 1, 2):
                            if abs(cdx) + abs(cdz) <= 3:
                                c.set_block(43 + cdx, Y_BASE + 5, -614 + cdz, MAT['slab_spruce_b'])

    tx1, tx2, tz1, tz2 = 32, 42, -646, -636
    y_launch = Y_BASE + 11
    y_roof_t = Y_BASE + 15
    c.fill(tx1, Y_BASE, tz1, tx2, Y_BASE, tz2, MAT['wall_quartz'])
    for y in range(Y_BASE + 1, y_launch):
        for x in range(tx1, tx2 + 1):
            for z in range(tz1, tz2 + 1):
                cheb = max(abs(x - 37), abs(z - (-641)))
                if cheb == 3:
                    if (x == 37 or z == -641) and (y - Y_BASE) % 3 == 2:
                        c.set_block(x, y, z, MAT['glass_cyan'])
                    elif (x == 37 or z == -641) and (y - Y_BASE) % 4 == 0:
                        c.set_block(x, y, z, MAT['light_sea'])
                    else:
                        c.set_block(x, y, z, MAT['wall_white'])
                elif x in (tx1, tx2) and z in (tz1, tz2):
                    c.set_block(x, y, z, MAT['cyan_concrete'])

    c.fill(tx1, y_launch, tz1, 54, y_launch, tz2, MAT['wall_quartz'])
    for x in range(tx1, 55):
        for z in (tz1, tz2):
            c.set_block(x, y_launch + 1, z, MAT['pane_cyan'])
    for z in range(tz1, tz2 + 1):
        c.set_block(tx1, y_launch + 1, z, MAT['pane_cyan'])
        c.set_block(54, y_launch + 1, z, MAT['pane_cyan'])
    build_flat_roof_and_eaves(c, tx1, y_roof_t, tz1, 54, tz2, overhang=1,
                              roof_mat=MAT['cyan_concrete'], soffit_mat=MAT['wall_white'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)

    build_spiral_staircase(c, 37, Y_BASE + 1, y_launch, -641, radius=2, start_sector=4, clockwise=False)
    c.fill(32, Y_BASE + 1, -642, 34, Y_BASE + 3, -640, 'minecraft:air')

    for step_i in range(11):
        sz = -636 + step_i
        sy = y_launch - step_i
        for sx_c, wall_m in [(45, MAT['cyan_concrete']), (50, MAT['orange_concrete'])]:
            c.fill(sx_c - 1, sy + 1, sz, sx_c + 1, sy + 4, sz, 'minecraft:air')
            c.set_block(sx_c, sy - 1, sz, MAT['light_sea'] if step_i % 2 == 0 else MAT['wall_white'])
            c.set_block(sx_c, sy, sz, MAT['packed_ice'] if step_i < 10 else MAT['water'])
            c.set_block(sx_c, sy + 1, sz, MAT['carpet_cyan'] if sx_c == 45 else MAT['carpet_yellow'])
            c.set_block(sx_c - 1, sy, sz, wall_m)
            c.set_block(sx_c + 1, sy, sz, wall_m)
            c.set_block(sx_c - 1, sy + 1, sz, MAT['wall_white'])
            c.set_block(sx_c + 1, sy + 1, sz, MAT['wall_white'])
            if step_i % 3 == 0 and sz < -630:
                c.fill(sx_c, Y_BASE + 1, sz, sx_c, sy - 2, sz, MAT['frame_dark'])

def _build_north_santa_monica_volleyball_skatepark_and_surf_village(c: WorldCanvas):
    """
    Step 7: Populates the 160-block Northern Expansion of Santa Monica State Beach (`Z = -764..-612`):
      1. **4 Championship Santa Monica Beach Volleyball Courts & Covered Spectator Bleachers (`X = 72..102, Z = -684..-616`)**.
      2. **Oceanfront Skatepark Bowls, Half-Pipe & Street Plaza (`X = 28..56, Z = -712..-662, Y = 62..67`)**.
      3. **North Santa Monica Surf Village, Board Rental Shacks, Taco Cantina & Sunset Pergola (`X = 28..96, Z = -754..-720`)**.
      4. **Offshore Floating Water-Sports & Diving Island (`X = 152..176, Z = -682..-658, Y = 62..69`)**
         & **2-Masted Californian Coastal Schooner + 2 Racing Catamarans**.
      5. **4 Iconic Powder-Blue & Timber Santa Monica Lifeguard Towers (Towers 14, 15, 18, 20)**,
         12 Luxury Beach Cabanas & 36 Colorful Umbrella Sun-Lounger Bays!
    """

    for cz_min, cz_max in [(-682, -666), (-662, -646), (-642, -626), (-718, -702)]:
        cz_mid = (cz_min + cz_max) // 2
        for z in range(cz_min - 1, cz_max + 2):
            for x in range(75, 100):
                c.fill(x, 60, z, x, Y_BASE - 1, z, 'minecraft:smooth_sandstone')
                if (x in (76, 98) and cz_min <= z <= cz_max) or (z in (cz_min, cz_max) and 76 <= x <= 98):
                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                else:
                    c.set_block(x, Y_BASE, z, 'minecraft:sand')
                c.fill(x, Y_BASE + 1, z, x, Y_BASE + 5, z, 'minecraft:air')

        c.fill(76, Y_BASE + 1, cz_mid, 76, Y_BASE + 3, cz_mid, MAT['pillar_quartz'])
        c.fill(98, Y_BASE + 1, cz_mid, 98, Y_BASE + 3, cz_mid, MAT['pillar_quartz'])
        for x in range(77, 98):
            c.set_block(x, Y_BASE + 1, cz_mid, MAT['iron_bars'])
            c.set_block(x, Y_BASE + 2, cz_mid, 'minecraft:cobweb' if x % 2 == 0 else MAT['iron_bars'])
            c.set_block(x, Y_BASE + 3, cz_mid, MAT['carpet_white'])

        c.fill(75, Y_BASE + 1, cz_mid, 75, Y_BASE + 2, cz_mid, 'minecraft:oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        c.set_block(75, Y_BASE + 3, cz_mid, stair('smooth_quartz', 'west', 'bottom'))
        build_patio_umbrella(c, 100, Y_BASE, cz_mid - 4)
        build_patio_umbrella(c, 100, Y_BASE, cz_mid + 4)

    for z in range(-680, -627):
        if -665 <= z <= -663 or -645 <= z <= -643:
            continue
        for tier in range(3):
            bx = 73 - tier
            by = Y_BASE + 1 + tier
            c.fill(bx, Y_BASE + 1, z, bx, by - 1, z, MAT['stone_pol_and'])
            c.set_block(bx, by, z, stair('spruce' if tier % 2 == 0 else 'smooth_quartz', 'west', 'bottom'))

    for z in range(-708, -663):
        for x in range(28, 55):
            c.fill(x, 58, z, x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 6, z, 'minecraft:air')
            if x in (28, 54) or z in (-708, -664):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if (x + z) % 5 == 0 else MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 1, z, MAT['iron_bars'])

    for scz in (-696, -676):
        scx = 41
        for dx in range(-8, 9):
            for dz in range(-7, 8):
                d = math.hypot(dx / 8.0, dz / 7.0)
                x, z = scx + dx, scz + dz
                if d <= 0.65:
                    c.set_block(x, Y_BASE - 2, z, MAT['light_sea'] if (dx == 0 and dz == 0) else 'minecraft:cyan_terracotta')
                    c.fill(x, Y_BASE - 1, z, x, Y_BASE, z, 'minecraft:air')
                elif d <= 0.95:
                    c.set_block(x, Y_BASE - 1, z, MAT['wall_quartz'])
                    c.set_block(x, Y_BASE, z, 'minecraft:air')
                elif d <= 1.12:
                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'])

    for sx1, sx2, sz1, sz2, roof_m in [
        (32, 48, -744, -730, 'minecraft:orange_terracotta'),
        (74, 88, -742, -730, MAT['cyan_concrete']),
    ]:
        c.fill(sx1, Y_BASE - 2, sz1, sx2, Y_BASE, sz2, MAT['wood_dark'])
        for px in (sx1, sx2):
            for pz in (sz1, sz2):
                c.fill(px, Y_BASE + 1, pz, px, Y_BASE + 4, pz, MAT['beam_spruce_y'])
        build_flat_roof_and_eaves(c, sx1, Y_BASE + 5, sz1, sx2, sz2, overhang=1,
                                  roof_mat=roof_m, soffit_mat=MAT['wood_warm'],
                                  coping_slab=MAT['slab_spruce_b'], hidden_lights=True)
        build_outdoor_bar(c, sx1 + 2, Y_BASE, sz1 + 3, length=min(8, sx2 - sx1 - 3))

    surf_colors = [MAT['cyan_concrete'], MAT['yellow_concrete'], MAT['red_concrete'], MAT['lime_concrete'], MAT['orange_concrete']]
    for idx, sbx in enumerate(range(76, 87, 2)):
        c.fill(sbx, Y_BASE + 1, -740, sbx, Y_BASE + 3, -740, surf_colors[idx % len(surf_colors)])

    for lx_c, lz_c in [(116, -486), (112, -572), (110, -646), (114, -718)]:
        lx1, lx2, lz1, lz2 = lx_c - 3, lx_c + 3, lz_c - 3, lz_c + 3
        y_sand, y_deck, y_roof = 63, 67, 71
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
                    c.set_block(x, y_deck + 1, z, MAT['pool_shallow_2'] if (x + z) % 2 == 0 else MAT['wall_white'])
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

    umbrella_colors = [
        MAT['slab_quartz_b'],
        'minecraft:smooth_red_sandstone_slab[type=bottom,waterlogged=false]',
        MAT['slab_spruce_b'],
        MAT['slab_dio_b'],
    ]
    for idx, bz in enumerate(range(-742, -466, 10)):
        if -608 <= bz <= -522:
            continue
        bx = int(round(112 - 14.0 * _bay_curve_phase(bz))) + (2 if idx % 2 == 0 else -1)
        by = 63
        c.set_block(bx, by, bz, MAT['light_ochre'])
        build_patio_umbrella(c, bx, by, bz, canopy_mat=umbrella_colors[idx % len(umbrella_colors)])
        build_sun_lounger(c, bx, by, bz - 2, facing='east')
        build_sun_lounger(c, bx, by, bz + 2, facing='east')

    for cat_z, sail_col in [(-514, MAT['cyan_wool']), (-632, MAT['orange_wool'])]:
        cat_x = 168
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

    for z in range(-676, -653):
        for x in range(156, 179):
            is_ring = (x in (156, 157, 177, 178) or z in (-676, -675, -655, -654))
            is_cross = (166 <= x <= 168 or -666 <= z <= -664)
            if is_ring or is_cross:
                c.set_block(x, 62, z, MAT['yellow_concrete'] if (x + z) % 2 == 0 else MAT['orange_concrete'])
                c.set_block(x, 63, z, MAT['carpet_yellow'] if is_ring else MAT['carpet_cyan'])
                if (x in (156, 178) and z in (-676, -654)):
                    c.set_block(x, 62, z, MAT['light_sea'])
    c.fill(171, 63, -666, 173, 63, -664, MAT['wall_quartz'])
    c.fill(172, 64, -666, 172, 67, -666, MAT['pillar_quartz'])
    c.fill(172, 64, -664, 172, 67, -664, MAT['pillar_quartz'])
    c.fill(171, 67, -666, 176, 67, -664, MAT['slab_quartz_t'])
    c.set_block(176, 67, -665, MAT['light_sea'])

    ncx, ncz, ncy = 146, -772, Y_BASE + 2
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
    Master Builder Entry Point for V5.4 Santa Monica State Beach & Pacific Park Pier:
    50-Block Coastal & Parkland Transition Belt (`Z = -447..-397`) and
    352-Block Extended Santa Monica State Beach & Pier (`X = 24..255, Z = -800..-448`).
    """
    _bulldoze_and_generate_transition_and_beach_terrain(c)
    _build_transition_corridors_and_cliff_walk(c)
    _build_ocean_front_walk_and_marvin_braude_bike_trail(c)
    _build_original_muscle_beach_and_amphitheater(c)
    _build_santa_monica_pier_and_pacific_park(c)
    _build_perrys_beach_cafe_and_annenberg_aqua_club(c)
    _build_north_santa_monica_volleyball_skatepark_and_surf_village(c)

    palm_coords = [
        (46, -748, 10, 1, 0), (46, -722, 9, 1, 0), (48, -696, 10, 1, 0),
        (48, -672, 9, 1, 0), (48, -650, 10, 1, 0), (48, -618, 9, 1, 0),
        (48, -582, 10, 1, 0), (50, -520, 10, 1, 0),
        (52, -496, 9, 1, 0), (54, -476, 10, 1, 0), (56, -464, 9, 1, 0),
        (26, -736, 9, 0, 1), (26, -688, 10, 0, -1), (26, -622, 9, 1, 0),
        (26, -582, 10, 0, 1), (26, -516, 9, 1, 0), (26, -480, 10, 0, 1),
    ]
    for idx, (px, pz, ph, ldx, ldz) in enumerate(palm_coords):
        build_palm_tree(c, px, Y_BASE, pz, height=ph, lean_dx=ldx, lean_dz=ldz, seed=88000 + idx)
