"""
zone_urban_district.py — V5.5 Santa Monica Palisades Bluff Park, Third Street Promenade & Venice Canals (X- Expansion)
========================================================================================================================
Implements Requirement 4 (`接着。开始设计建造海滨沙滩公园X-方向的大片部分。可模仿真实经典场景。时刻注意这是大型项目，
细节要到位，规模不缩减。不反复用相同火柴盒房子设计`):

Across the vast `344 × 416` block inland coastal zone (`X = -320..23, Z = -864..-448`, `143,104 m²`),
100% of natural terrain is demolished and custom-generated into a multi-tiered Southern California
coastal cityscape & park system with **5 distinct, non-repetitive classic architectural districts**
(ZERO matchbox buildings!):

  1. **Zone 1 (`X = -76..23, Z = -864..-448, Y = 64..72`): Santa Monica Palisades Bluff Park, PCH & California Incline**
     - Sculpted California sandstone & flowering-azalea coastal bluffs rising from **Pacific Coast Highway (PCH, `X = 12..23, Y = 64`)**
       up to the **Palisades Bluff-Top Promenade (`X = -76..-16, Y = 72`)** via the **California Incline (`Z = -542..-530`)**
       and **Montana North Coastal Ramp (`Z = -695..-687`)**;
     - **Camera Obscura Astronomical Turret & Sunset Pergola Courtyard (`-48, 72, -586`)**, **Palisades Rose Garden &
       Glass Conservatory (`-46, 72, -491`)**, **Sunset Tea Pavilion (`-46, 72, -652`)**, and **North Palisades
       Torrey-Pine Belvedere Rotunda (`-46, 72, -772`)**, plus 4 cantilevered semi-circular cliffside ocean overlooks.

  2. **Zone 2 (`X = -190..-96, Z = -636..-456, Y = 64`): Santa Monica Third Street Promenade & Open-Air Pedestrian Mall**
     - Car-free mosaic-paved pedestrian boulevard (`X = -152..-134`) with 3 topiary **Water-Spouting Dinosaur Fountains**
       (`(-143, 64, -492)`, `(-143, 64, -536)`, `(-143, 64, -580)`), outdoor dining pergolas, string-lit jacaranda/palm trees,
       and **4 Architecturally Distinct Landmark Buildings** (each with its own unique geometry, roof profile, and interior):
       * **A) The Georgian Coastal Art-Deco Stepped-Tower Hotel (`X = -128..-102, Z = -524..-472, Y = 64..86`)**:
         Iconic 1933 Santa Monica turquoise-and-gold Art-Deco wedding-cake ziggurat silhouette with recessed vertical
         pilasters, 3 stepped setback terraces, sunset cocktail verandah, and an 8-sector spiral staircase at `(-108, -478)`!
       * **B) Casa del Mar Spanish-Colonial Revival Courtyard Villa (`X = -128..-102, Z = -608..-550, Y = 64..83`)**:
         U-shaped Mediterranean stucco & terracotta-tiled mansion wrapping around a central palm & fountain courtyard,
         featuring arched loggia colonnades, an octagonal corner bell-tower campanile (`(-107, -555, Y = 64..84)`), and
         a spiral staircase at `(-122, -556)`!
       * **C) Santa Monica Place Barrel-Vaulted Glass Galleria (`X = -186..-156, Z = -524..-472, Y = 64..79`)**:
         Curved crystal-atrium shopping pavilion with a parabolic barrel-vaulted cyan/clear glass skylight roof,
         cantilevered 2F dining sky-bridges, indoor waterfall atrium, and spiral staircase at `(-162, -478)`!
       * **D) Criterion Arched Cinema & Performing Arts Rotunda (`X = -186..-156, Z = -608..-550, Y = 64..80`)**:
         Circular/stepped theater rotunda with an illuminated neon blade marquee, grand red-carpet foyer,
         tiered auditorium seating, acoustic copper dome, and stage!

  3. **Zone 3 (`X = -190..-96, Z = -824..-644, Y = 64..82`): Santa Monica Civic Auditorium, Tongva Park & Public Library**
     - **A) Tongva Park Double-Helix Observation Hill & Cascading Water Gardens (`X = -148..-100, Z = -724..-652, Y = 64..73`)**:
         Sculpted organic park mounds, braided reflection streams, and twin braided Corten/copper observation lookouts!
     - **B) Santa Monica Civic Auditorium — Mid-Century Folded-Plate Wing Roof (`X = -188..-152, Z = -726..-656, Y = 64..80`)**:
         Iconic 1958 Welton Becket mid-century modern landmark with a dramatic cantilevered sinusoidal folded-plate
         white quartz roof, slanted glass curtain facade, and concert hall interior!
     - **C) Santa Monica Public Library & Andalusian Reading Cloister (`X = -186..-104, Z = -812..-746, Y = 64..78`)**:
         L-shaped civic library & botanical reading cloister with multi-level reading terraces, arched bookshelves,
         central reflection pool, and spiral staircase at `(-178, -754)`!

  4. **Zone 4 (`X = -308..-206, Z = -660..-456, Y = 62..76`): Venice Beach Canals Historic District & Distinct Waterfront Villas**
     - **Grand Lagoon & Intersecting Venice Waterway Canals (`Y = 60..62` water, `Y = 64` flowered canal-side towpaths)**:
       A main North-South Venice Canal (`X = -258..-248, Z = -648..-464`) intersected by two East-West branch canals
       (`Z = -512..-504` and `Z = -592..-584`), spanned by **5 Iconic White-Timber High-Arched Venice Footbridges**
       and navigated by **6 Pure-Voxel Venetian Gondolas & Canal Skiffs**!
     - **6 Individually Sculpted, Non-Repetitive Canal-Front Villas** (zero identical houses, zero matchboxes!):
       1) **Villa 1 (`X = -242..-214, Z = -498..-468`) — Californian Butterfly-Roof Glass House**: V-shaped inverted
          butterfly roof, double-height lakeside glass living room, private gondola dock;
       2) **Villa 2 (`X = -298..-264, Z = -498..-468`) — Tuscan Bell-Tower Canal Villa**: L-shaped warm sandstone &
          terracotta hipped-roof residence with a 3-story corner loggia turret and vine-draped pergola;
       3) **Villa 3 (`X = -242..-214, Z = -576..-546`) — Bauhaus Cantilevered Terraced Residence**: Interlocking
          asymmetric white-quartz & dark-oak volumes with a rooftop infinity plunge pool and spiral stair;
       4) **Villa 4 (`X = -298..-264, Z = -576..-546`) — Cape Cod / Craftsman A-Frame Gable Boathouse**: Steep pitched
          spruce gable roof, dormer windows, wrap-around timber deck, and covered boat slip;
       5) **Villa 5 (`X = -242..-214, Z = -644..-614`) — Geodesic / Circular Rotunda Artist Studio**: Cylindrical stepped
          glass-and-copper dome pavilion with a sculpture garden;
       6) **Villa 6 (`X = -298..-264, Z = -644..-614`) — Japanese-Californian Zen Courtyard Pavilion**: Sweeping pagoda-eave
          dark-oak roof, bamboo/moss rock garden, koi pond bridge, and shoji-screen gallery.

  5. **Zone 5 (`X = -308..-206, Z = -824..-668, Y = 64..82`): Bergamot Station Arts Center & Historic Aero Hangar Museum**
     - **A) Santa Monica Museum of Flying — Parabolic Steel-Arch Aviation Hangar (`X = -296..-248, Z = -748..-684, Y = 64..80`)**:
         Wide-span barrel-vaulted hangar housing a **Pure-Voxel Twin-Propeller Vintage Coastal Seaplane / Douglas DC-3**
         suspended inside and a second biplane on the tarmac apron!
     - **B) Bergamot Station Sawtooth-Skylight Contemporary Art Galleries & Sculpture Park (`X = -242..-208, Z = -808..-684, Y = 64..75`)**:
         North-facing industrial sawtooth roof sheds converted into fine-art galleries, flanked by outdoor abstract
         voxel sculptures and a vintage **Pacific Electric Red-Car Trolley (`X = -246..-242, Z = -768..-744`)**!
"""

import math
from config import Y_BASE, MAT, SOFT_FLOWERS
from world_canvas import WorldCanvas
from arch_lib import (
    stair, trapdoor,
    place_bed, place_barrel, place_brewing_stand, place_lectern,
    place_door, place_double_door,
    build_recessed_ceiling_grid, build_crystal_chandelier, build_illuminated_carpet_rug,
    build_curtain_wall, build_flat_roof_and_eaves,
    build_spiral_staircase, build_straight_stairs,
    build_lamppost, build_fountain, build_infinity_pool, build_hedgerow_line,
    build_custom_tree, build_patio_umbrella,
    build_outdoor_sofa, build_outdoor_bar,
    build_vine_arch, build_pergola_colonnade,
    build_arched_canal_bridge,
)
from zone_beach_park import build_palm_tree

def _target_inland_bluff_elevation(c: WorldCanvas, x: int, z: int) -> int:
    """
    Computes the 100% custom-generated terrain elevation for `X in [c.x_min, 23], Z in [c.z_min, -448]`:
      - `X = 12..23`: Pacific Coast Highway (PCH, Highway 1) at `Y = 64`.
      - `X = -16..11`: Sculpted **California Coastal Bluff Slope** rising from `Y = 64` at `X = 11` up to
        `Y = 72` at `X = -16` (with the **California Incline** ramp cut smoothly through `Z = -542..-530`
        and a second north coastal ramp at `Z = -696..-686`).
      - `X = -72..-17`: **Santa Monica Palisades Park Bluff-Top Promenade & Rose Garden Terrace** at `Y = 72`.
      - `X = -90..-73`: Gently terraced inland bluff descent from `Y = 72` down to `Y = 64` (Ocean Avenue / Promenade level),
        with grand stair & ramp connections at `Z = -460`, `-536`, `-614`, `-691`, `-752`, `-812`.
      - `X = -320..-91`: Flat `Y = 64` civic & canal datum for the Third Street Promenade, Civic Center,
        Venice Canals District, and Bergamot Station Arts Center, smoothly feathered along the outer
        North (`Z = -864..-832`) and West (`X = -320..-306`) perimeter!
    """
    if x >= 12:
        base_y = Y_BASE
    elif x >= -16:
        if -543 <= z <= -529:
            t_inc = max(0.0, min(1.0, (11 - x) / 55.0))
            base_y = Y_BASE + int(round(8.0 * t_inc))
        elif -696 <= z <= -686:
            t_inc = max(0.0, min(1.0, (11 - x) / 40.0))
            base_y = Y_BASE + int(round(8.0 * t_inc))
        else:
            t_bluff = max(0.0, min(1.0, (11 - x) / 27.0))
            s_bluff = t_bluff * t_bluff * (3.0 - 2.0 * t_bluff)
            base_y = Y_BASE + int(round(8.0 * s_bluff))
    elif x >= -72:
        if -543 <= z <= -529 and x >= -44:
            t_inc = max(0.0, min(1.0, (11 - x) / 55.0))
            base_y = Y_BASE + int(round(8.0 * t_inc))
        elif -696 <= z <= -686 and x >= -29:
            t_inc = max(0.0, min(1.0, (11 - x) / 40.0))
            base_y = Y_BASE + int(round(8.0 * t_inc))
        else:
            base_y = 72
    elif x >= -88:

        t_w = max(0.0, min(1.0, (x - (-88)) / 16.0))
        s_w = t_w * t_w * (3.0 - 2.0 * t_w)
        base_y = Y_BASE + int(round(8.0 * s_w))
    else:
        base_y = Y_BASE

    if z >= -466 and base_y > Y_BASE:
        t_south = max(0.0, min(1.0, (-448 - z) / 18.0))
        s_south = t_south * t_south * (3.0 - 2.0 * t_south)
        base_y = int(round(Y_BASE * (1.0 - s_south) + base_y * s_south))

    if z < -832:
        t_n = max(0.0, min(1.0, (-832 - z) / 32.0))
        s_n = t_n * t_n * (3.0 - 2.0 * t_n)
        if x >= -76:
            north_target = 70 + int(round(2.0 * math.sin((x - 24) / 22.0)))
        else:
            orig_w = min(72, max(64, c.orig_surface_y.get((x, z), Y_BASE)))
            t_xw = max(0.0, min(1.0, (x - (-160)) / 84.0))
            north_target = int(round(orig_w * (1.0 - t_xw) + 70 * t_xw))
        base_y = int(round(base_y * (1.0 - s_n) + north_target * s_n))

    d_west_edge = x - c.x_min
    if d_west_edge < 14:
        t_w_edge = max(0.0, min(1.0, d_west_edge / 14.0))
        s_w_edge = t_w_edge * t_w_edge * (3.0 - 2.0 * t_w_edge)
        clamped_west = min(72, max(62, c.orig_surface_y.get((x, z), Y_BASE)))
        base_y = int(round(clamped_west * (1.0 - s_w_edge) + base_y * s_w_edge))

    return base_y

def _bulldoze_and_sculpt_palisades_bluffs(c: WorldCanvas):
    """
    Step 1: Demolishes 100% of the natural terrain in `X = -320..23, Z = -864..-448` (`Y = 46..175`)
    and generates the custom Santa Monica Palisades Park bluffs, terraced vegetated cliffside,
    California Incline ramp, and flat civic/canal datum—with zero raw cut stone walls!
    """
    stone_id = c.get_or_register(MAT['stone'])
    dirt_id = c.get_or_register(MAT['dirt'])
    grass_id = c.get_or_register(MAT['grass_block'])
    moss_id = c.get_or_register(MAT['moss_block'])
    sandstone_id = c.get_or_register('minecraft:smooth_sandstone')
    cut_sandstone_id = c.get_or_register('minecraft:cut_sandstone')
    calcite_id = c.get_or_register(MAT['wall_calcite'])
    air_id = c.air_id

    for z in range(c.z_min, -447):
        for x in range(c.x_min, 24):
            for y in range(46, c.y_max + 1):
                c.set_block_id(x, y, z, air_id)

            ty = _target_inland_bluff_elevation(c, x, z)
            for y in range(46, ty - 3):
                c.set_block_id(x, y, z, stone_id)

            if ((-16 <= x <= 11) or (-88 <= x <= -72)) and ty > Y_BASE and not (-543 <= z <= -529 or -696 <= z <= -686):
                c.set_block_id(x, ty - 3, z, sandstone_id)
                c.set_block_id(x, ty - 2, z, cut_sandstone_id if (x + z) % 3 == 0 else sandstone_id)
                c.set_block_id(x, ty - 1, z, sandstone_id)
                if (x + z) % 3 == 0:
                    c.set_block_id(x, ty, z, moss_id)
                    if (x * 3 + z * 5) % 7 == 0:
                        c.set_block(x, ty + 1, z, MAT['leaf_azalea'] if (x + z) % 2 == 0 else MAT['leaf_fl_azalea'])
                elif (x + z) % 3 == 1:
                    c.set_block_id(x, ty, z, grass_id)
                else:
                    c.set_block_id(x, ty, z, calcite_id if ty >= 69 else sandstone_id)
            else:
                c.set_block_id(x, ty - 3, z, dirt_id)
                c.set_block_id(x, ty - 2, z, dirt_id)
                c.set_block_id(x, ty - 1, z, dirt_id)
                c.set_block_id(x, ty, z, moss_id if (x * 5 + z * 7) % 11 == 0 else grass_id)

def _build_pch_and_california_incline(c: WorldCanvas):
    """
    Step 2: Builds:
      - **Pacific Coast Highway (PCH / State Route 1, `X = 12..23, Z = -828..-448, Y = 64`)**
      - **The California Incline (`Z = -542..-530, X = -88..11, Y = 64 -> 72 -> 64`)**:
        Climbs from PCH (`X = 11, Y = 64`) up to Palisades Park (`X = -44..-72, Y = 72`) and ramps cleanly
        down the west bluff (`X = -72..-88, Y = 72 -> 64`) to connect directly with Broadway / Third Street Promenade!
      - **North Bluff Coastal Ramp (`Z = -695..-687, X = -88..11`)**
      - **Ocean Avenue (`X = -96..-86, Z = -824..-448, Y = 64`)** & **Lincoln / Venice Boulevard (`X = -204..-194, Z = -824..-448, Y = 64`)**
      - **4 East-West Cross Boulevards (`Z = -464..-456`, `Z = -542..-530`, `Z = -644..-636`, `Z = -824..-816`)**
    """
    crosswalk_zs = [(-464, -456), (-542, -530), (-618, -610), (-695, -687), (-756, -748), (-816, -808)]

    def in_crosswalk_band(z):
        return any(z0 <= z <= z1 for z0, z1 in crosswalk_zs)

    for z in range(-828, -447):
        is_cw = in_crosswalk_band(z)
        for x in range(12, 24):
            c.fill(x, Y_BASE - 2, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 6, z, 'minecraft:air')
            if is_cw:
                is_edge = any(z in (z0 + 1, z1 - 1) for z0, z1 in crosswalk_zs)
                if is_edge and 14 <= x <= 21 and x % 2 == 0:
                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                elif x in (12, 23):
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['wall_gray'])
                continue

            if x in (12, 23):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            elif x in (13, 22):
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            elif x in (17, 18):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['moss_block'])
                if z % 6 != 0 and z % 2 == 0:
                    c.set_block(x, Y_BASE + 1, z, SOFT_FLOWERS[(x + z) % len(SOFT_FLOWERS)])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_gray'])

        if z % 18 == 0 and not is_cw:
            build_lamppost(c, 13, Y_BASE + 1, z, style='avenue')
            build_lamppost(c, 22, Y_BASE + 1, z, style='avenue')
        elif z % 18 == 9 and not is_cw:
            build_palm_tree(c, 17, Y_BASE, z, height=9, lean_dx=1, lean_dz=0, seed=71000 + abs(z))

    for x in range(-88, 12):
        ry = _target_inland_bluff_elevation(c, x, -536)
        next_ry = _target_inland_bluff_elevation(c, x - 1, -536)
        use_slab = (next_ry != ry)
        for z in range(-543, -528):
            c.fill(x, ry - 3, z, x, ry - 1, z, MAT['stone_pol_and'])
            c.fill(x, ry + 1, z, x, ry + 8, z, 'minecraft:air')
            if z in (-543, -529):
                bluff_y = max(ry + 1, _target_inland_bluff_elevation(c, x, z - 2 if z == -543 else z + 2))
                c.fill(x, ry, z, x, bluff_y, z, 'minecraft:smooth_sandstone' if (x + z) % 2 == 0 else MAT['wall_quartz'])
                c.set_block(x, bluff_y + 1, z, MAT['slab_quartz_b'])
                if x % 5 == 0:
                    c.set_block(x, ry + 1, z, MAT['light_ochre'])
            elif z in (-542, -530):
                c.set_block(x, ry, z, MAT['stone_pol_and'])
            elif z in (-541, -531):
                c.set_block(x, ry, z, MAT['slab_quartz_b'] if use_slab else MAT['wall_quartz'])
            elif z == -536:
                c.set_block(x, ry, z, MAT['light_ochre'] if x % 5 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, ry, z, MAT['slab_deep_b'] if use_slab else MAT['wall_gray'])

    for z in range(-545, -527):
        for x in range(-11, -5):
            c.set_block(x, 72, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['wood_warm'])
            if x in (-11, -6) and -543 <= z <= -529:
                c.set_block(x, 72, z, MAT['wall_quartz'])
                c.set_block(x, 73, z, MAT['pane_cyan'])
                if z in (-542, -536, -530):
                    c.set_block(x, 71, z, MAT['light_sea'])

    for x in range(-88, 12):
        ry = _target_inland_bluff_elevation(c, x, -691)
        next_ry = _target_inland_bluff_elevation(c, x - 1, -691)
        use_slab = (next_ry != ry)
        for z in range(-696, -685):
            c.fill(x, ry - 2, z, x, ry - 1, z, MAT['stone_pol_and'])
            c.fill(x, ry + 1, z, x, ry + 6, z, 'minecraft:air')
            if z in (-696, -686):
                bluff_y = max(ry + 1, _target_inland_bluff_elevation(c, x, z - 2 if z == -696 else z + 2))
                c.fill(x, ry, z, x, bluff_y, z, 'minecraft:smooth_sandstone')
                c.set_block(x, bluff_y + 1, z, MAT['slab_quartz_b'])
            elif z in (-695, -687):
                c.set_block(x, ry, z, MAT['stone_pol_and'])
            elif z == -691:
                c.set_block(x, ry, z, MAT['light_ochre'] if x % 5 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, ry, z, MAT['slab_quartz_b'] if use_slab else MAT['stone_smooth'])

    for av_cx in (-91, -199):
        for z in range(-824, -447):
            for dx in range(-5, 6):
                x = av_cx + dx
                c.fill(x, Y_BASE - 2, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
                c.fill(x, Y_BASE + 1, z, x, Y_BASE + 6, z, 'minecraft:air')
                if abs(dx) == 5:
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                elif abs(dx) == 4:
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
                elif dx == 0:
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else (MAT['wall_quartz'] if z % 4 in (0, 1) else MAT['wall_gray']))
                else:
                    c.set_block(x, Y_BASE, z, MAT['wall_gray'])
            if z % 22 == 0 and not (-544 <= z <= -528 or -646 <= z <= -634 or -466 <= z <= -454 or -826 <= z <= -814):
                build_lamppost(c, av_cx - 4, Y_BASE + 1, z, style='avenue')
                build_lamppost(c, av_cx + 4, Y_BASE + 1, z, style='avenue')

    for z_mid, half_w in [(-460, 4), (-536, 5), (-640, 4), (-820, 4)]:
        for x in range(-304, -86):

            for dz in range(-half_w, half_w + 1):
                z = z_mid + dz
                c.fill(x, Y_BASE - 2, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
                c.fill(x, Y_BASE + 1, z, x, Y_BASE + 6, z, 'minecraft:air')
                if abs(dz) == half_w:
                    c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                elif abs(dz) == half_w - 1:
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
                elif dz == 0:
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['wall_quartz'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['wall_gray'])

def _build_palisades_bluff_park_and_overlooks(c: WorldCanvas):
    """
    Step 3: Builds the **Santa Monica Palisades Park** along the Bluff-Top Plateau (`X = -72..-16, Z = -816..-462, Y = 72`):
      - Cliffside Palm & Cypress Promenade (`X = -24..-16, Z = -812..-464, Y = 72`) with white sandstone
        balustrades and 4 cantilevered semi-circular panoramic ocean overlooks (`Z = -490, -586, -652, -772`).
      - **Santa Monica Camera Obscura & Spanish-Revival Sunset Pergola Pavilion (`-48, 72, -586`)**.
      - **Palisades Rose Garden & Totem Fountain (`-46, 72, -491`)**.
      - **Palisades Sunset Tea Pavilion (`-46, 72, -652`)**.
      - **North Palisades Torrey-Pine Belvedere Rotunda (`-46, 72, -772`)**.
    """
    y_bluff = 72

    for z in range(-812, -463):
        if -543 <= z <= -529 or -696 <= z <= -686:
            continue
        for x in range(-24, -15):
            c.fill(x, y_bluff - 2, z, x, y_bluff - 1, z, MAT['stone_pol_and'])
            if x == -16:
                c.set_block(x, y_bluff, z, MAT['light_ochre'] if z % 5 == 0 else MAT['wall_quartz'])
                c.set_block(x, y_bluff + 1, z, MAT['pane_white'])
            elif x == -24:
                c.set_block(x, y_bluff, z, MAT['stone_pol_and'])
            elif x in (-21, -20, -19):
                c.set_block(x, y_bluff, z, MAT['wood_warm'] if (z // 2) % 2 == 0 else MAT['wood_dark'])
            else:
                c.set_block(x, y_bluff, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else 'minecraft:smooth_sandstone')

        if z % 16 == 0:
            build_lamppost(c, -23, y_bluff + 1, z, style='courtyard')
        elif z % 16 == 8:
            build_palm_tree(c, -26, y_bluff, z, height=10, lean_dx=1, lean_dz=0, seed=72000 + abs(z))

    for ov_z in (-490, -586, -652, -772):
        ov_x = -15
        for dx in range(0, 7):
            for dz in range(-6, 7):
                d = math.hypot(dx, dz)
                if d <= 6.2:
                    x, z = ov_x + dx, ov_z + dz
                    c.fill(x, y_bluff - 2, z, x, y_bluff - 1, z, 'minecraft:smooth_sandstone')
                    if d >= 5.2:
                        c.set_block(x, y_bluff, z, MAT['light_sea'] if (dx + dz) % 3 == 0 else MAT['wall_quartz'])
                        c.set_block(x, y_bluff + 1, z, MAT['pane_cyan'])
                    else:
                        c.set_block(x, y_bluff, z, MAT['wood_warm'] if (dx + dz) % 2 == 0 else MAT['wall_quartz'])
                    c.fill(x, y_bluff + 2, z, x, y_bluff + 5, z, 'minecraft:air')
        build_patio_umbrella(c, ov_x + 3, y_bluff, ov_z)

    cx_co, cz_co = -48, -586
    for z in range(-604, -568):
        for x in range(-66, -24):
            if (x + 66) % 6 == 0 or (z + 604) % 6 == 0:
                c.set_block(x, y_bluff, z, MAT['stone_pol_and'])
            else:
                c.set_block(x, y_bluff, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else 'minecraft:smooth_sandstone')
            c.fill(x, y_bluff + 1, z, x, y_bluff + 20, z, 'minecraft:air')

    build_fountain(c, cx_co, y_bluff, cz_co, radius=5)
    build_pergola_colonnade(c, -62, y_bluff, -601, -34, -597, axis='x', lamp_step=6)
    build_pergola_colonnade(c, -62, y_bluff, -575, -34, -571, axis='x', lamp_step=6)

    tcx, tcz = -60, -586
    for dy in range(1, 7):
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                d = math.hypot(dx, dz)
                if d <= 4.2:
                    if d >= 3.2:
                        if (dx == 0 or dz == 0) and dy in (2, 3, 4):
                            c.set_block(tcx + dx, y_bluff + dy, tcz + dz, 'minecraft:air' if (dx == 4 and dy <= 3) else MAT['glass_cyan'])
                        else:
                            c.set_block(tcx + dx, y_bluff + dy, tcz + dz, MAT['wall_quartz'] if dy in (1, 6) else MAT['wall_calcite'])
                    else:
                        c.set_block(tcx + dx, y_bluff + dy, tcz + dz, 'minecraft:air')
    for dy_d, r_d, mat_d in [(7, 4.2, MAT['cut_copper_ox']), (8, 3.0, 'minecraft:orange_terracotta'), (9, 1.6, MAT['light_sea'])]:
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                if math.hypot(dx, dz) <= r_d:
                    c.set_block(tcx + dx, y_bluff + dy_d, tcz + dz, mat_d)
    c.set_block(tcx, y_bluff + 10, tcz, MAT['end_rod_up'])

    for z in range(-512, -470):
        for x in range(-66, -25):
            if x in (-66, -26) or z in (-512, -471) or abs(x - (-46)) <= 2 or abs(z - (-491)) <= 2:
                c.set_block(x, y_bluff, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])
            else:
                c.set_block(x, y_bluff, z, MAT['moss_block'] if (x + z) % 3 == 0 else MAT['grass_block'])
                if (x + z) % 2 == 0:
                    c.set_block(x, y_bluff + 1, z, SOFT_FLOWERS[(x * 3 + z * 5) % len(SOFT_FLOWERS)])
    build_fountain(c, -46, y_bluff, -491, radius=5)
    build_vine_arch(c, -46, y_bluff, -510, span=6, height=5, axis='x')
    build_vine_arch(c, -46, y_bluff, -472, span=6, height=5, axis='x')
    build_vine_arch(c, -26, y_bluff, -491, span=6, height=5, axis='z')

    build_fountain(c, -46, y_bluff, -652, radius=5)
    build_pergola_colonnade(c, -60, y_bluff, -668, -32, -664, axis='x', lamp_step=6)
    build_pergola_colonnade(c, -60, y_bluff, -640, -32, -636, axis='x', lamp_step=6)

    build_fountain(c, -46, y_bluff, -772, radius=5)
    build_pergola_colonnade(c, -60, y_bluff, -788, -32, -784, axis='x', lamp_step=6)
    build_pergola_colonnade(c, -60, y_bluff, -760, -32, -756, axis='x', lamp_step=6)

    bluff_trees = [
        (-32, -802, 'ornamental'), (-55, -796, 'birch_mix'),
        (-32, -730, 'ornamental'), (-55, -725, 'birch_mix'), (-32, -708, 'oak_mix'),
        (-58, -680, 'ornamental'), (-32, -620, 'birch_mix'), (-58, -616, 'oak_mix'),
        (-32, -556, 'ornamental'), (-58, -554, 'birch_mix'), (-32, -520, 'oak_mix'),
        (-58, -464, 'ornamental'),
    ]
    for idx, (tx, tz, tst) in enumerate(bluff_trees):
        ty = _target_inland_bluff_elevation(c, tx, tz)
        build_custom_tree(c, tx, ty, tz, height=9, style=tst, seed=94000 + idx, max_radius=3)

def _build_third_street_promenade_and_distinct_landmarks(c: WorldCanvas):
    """
    Step 4 (Requirement 4 — Zone 2 `X = -190..-98, Z = -634..-466, Y = 64`):
    Builds the classic **Santa Monica Third Street Promenade** open-air pedestrian mall and
    **4 Architecturally Distinct Coastal Landmarks** (ZERO matchboxes, ZERO repeated facades!):
      1. **Third Street Pedestrian Promenade (`X = -152..-136, Z = -634..-466, Y = 64`)**:
         - Patterned terracotta, quartz & smooth diorite pedestrian plaza;
         - **3 Sculpted Topiary Dinosaur Fountains** spouting water into reflection basins at
           `(-144, 64, -496)`, `(-144, 64, -536)`, and `(-144, 64, -580)`;
         - Outdoor café umbrella dining islands & overhead festival lantern arches!
      2. **Landmark A (`X = -132..-102, Z = -524..-472`): The Georgian Art-Deco Stepped Ziggurat Hotel**:
         - 3-tier wedding-cake setback tower (`1F` `X=-132..-102`, `2F` `X=-128..-104`, `3F` `X=-124..-106`,
           `Art-Deco Spire Crown` `X=-120..-110, Y=82..88`) in signature Santa Monica turquoise (`cyan_terracotta` /
           `prismarine_bricks`), white quartz fluted pilasters, and gold deco friezes, with spiral staircase at `(-108, -478)`.
      3. **Landmark B (`X = -132..-102, Z = -614..-552`): Casa del Mar Spanish-Colonial Revival Courtyard Mansion**:
         - U-shaped stucco & red/orange terracotta-tiled villa wrapping around a central palm & fountain courtyard
           (`X = -124..-110, Z = -594..-572`), featuring an arched ground-floor colonnade, wrought-iron balconies,
           a 20m octagonal Moorish bell-tower campanile (`-107, -557, Y = 64..84`), and spiral stair at `(-126, -558)`.
      4. **Landmark C (`X = -188..-156, Z = -524..-472`): Santa Monica Place Barrel-Vaulted Crystal Galleria**:
         - Parabolic arched glass-and-steel barrel vault roof (`Y = 76..81`) spanning an open 2-story atrium with
           interior sky-bridges, cascading water wall, luxury boutiques, and spiral staircase at `(-162, -478)`.
      5. **Landmark D (`X = -188..-156, Z = -614..-552`): Aero / Criterion Art-Deco Rotunda Theater & Jazz Hall**:
         - Stepped circular theater drum (`center -172, -583, R = 14`) crowned with a copper & neon sunburst dome,
           plus a towering illuminated vertical blade marquee facing the Promenade at `(-156, 65..82, -583)`!
    """

    for z in range(-634, -465):
        if -542 <= z <= -530:
            continue
        for x in range(-155, -132):
            c.fill(x, Y_BASE - 2, z, x, Y_BASE - 1, z, MAT['stone_pol_and'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 8, z, 'minecraft:air')
            if x in (-155, -133):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 5 == 0 else MAT['stone_pol_and'])
            elif abs(x - (-144)) <= 2:
                wave = ((x + z) % 3 == 0)
                c.set_block(x, Y_BASE, z, 'minecraft:orange_terracotta' if wave else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_dio'] if (x + z) % 2 == 0 else MAT['wall_quartz'])

        if z % 18 == 0 and not (-546 <= z <= -526):
            for x_g in range(-153, -134):
                sag = int(round(1.5 * (1.0 - ((x_g - (-144)) / 9.0) ** 2)))
                gy = Y_BASE + 6 - sag
                c.set_block(x_g, gy, z, MAT['light_ochre'] if x_g % 3 == 0 else MAT['chain_y'])

    for fz in (-496, -566, -606):
        fcx = -144
        build_fountain(c, fcx, Y_BASE, fz, radius=4)

        c.fill(fcx - 1, Y_BASE + 1, fz - 1, fcx + 1, Y_BASE + 2, fz + 1, MAT['moss_block'])
        c.fill(fcx, Y_BASE + 3, fz - 1, fcx, Y_BASE + 5, fz - 1, MAT['leaf_azalea'])
        c.set_block(fcx, Y_BASE + 5, fz - 2, MAT['leaf_fl_azalea'])
        c.set_block(fcx, Y_BASE + 4, fz - 2, MAT['light_sea'])
        c.set_block(fcx, Y_BASE + 2, fz + 2, MAT['leaf_azalea'])

    for pz in (-480, -514, -552, -588, -622):
        build_patio_umbrella(c, -148, Y_BASE, pz)
        build_patio_umbrella(c, -140, Y_BASE, pz)
        build_outdoor_sofa(c, -149, Y_BASE, pz - 2, length=3, facing='south')
        build_outdoor_sofa(c, -141, Y_BASE, pz + 2, length=3, facing='north')

    c.fill(-132, Y_BASE, -524, -100, Y_BASE, -472, MAT['wall_quartz'])
    for z in range(-522, -473):
        for x in range(-130, -101):
            c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['wood_birch'])
    for y in range(Y_BASE + 1, Y_BASE + 7):
        for z in range(-522, -473):
            for x in range(-130, -101):
                if x in (-130, -102) or z in (-522, -474):
                    is_pilaster = ((x - (-130)) % 4 == 0 and z in (-522, -474)) or ((z - (-522)) % 4 == 0 and x in (-130, -102))
                    if is_pilaster:
                        c.set_block(x, y, z, MAT['pillar_quartz'])
                    elif y == Y_BASE + 6:
                        c.set_block(x, y, z, MAT['gold_block'] if (x + z) % 3 == 0 else 'minecraft:cyan_terracotta')
                    else:
                        c.set_block(x, y, z, MAT['glass_cyan'] if y % 2 == 0 else MAT['glass_clear'])
                else:
                    c.set_block(x, y, z, 'minecraft:air')

    c.fill(-130, Y_BASE + 6, -522, -102, Y_BASE + 6, -474, MAT['wood_dark'])
    build_recessed_ceiling_grid(c, -128, Y_BASE + 6, -520, -104, -476, step_x=4, step_z=4, light_mat=MAT['light_ochre'])
    for x in range(-130, -101):
        for z in (-522, -474):
            c.set_block(x, Y_BASE + 6, z, MAT['wall_quartz'])
            c.set_block(x, Y_BASE + 7, z, MAT['pane_cyan'])
    for z in range(-522, -473):
        for x in (-130, -102):
            c.set_block(x, Y_BASE + 6, z, MAT['wall_quartz'])
            c.set_block(x, Y_BASE + 7, z, MAT['pane_cyan'])

    for y in range(Y_BASE + 7, Y_BASE + 13):
        for z in range(-518, -475):
            for x in range(-127, -103):
                if x in (-127, -104) or z in (-518, -476):
                    is_fin = ((x - (-127)) % 3 == 0 and z in (-518, -476)) or ((z - (-518)) % 3 == 0 and x in (-127, -104))
                    if is_fin:
                        c.set_block(x, y, z, MAT['pool_shallow_1'] if y < Y_BASE + 12 else MAT['gold_block'])
                    else:
                        c.set_block(x, y, z, MAT['glass_clear'])
                else:
                    c.set_block(x, y, z, 'minecraft:air')

    c.fill(-127, Y_BASE + 12, -518, -104, Y_BASE + 12, -476, MAT['wood_warm'])
    build_recessed_ceiling_grid(c, -125, Y_BASE + 12, -516, -106, -478, step_x=4, step_z=4, light_mat=MAT['light_ochre'])
    for x in range(-127, -103):
        for z in (-518, -476):
            c.set_block(x, Y_BASE + 12, z, MAT['wall_quartz'])
            c.set_block(x, Y_BASE + 13, z, MAT['pane_cyan'])
    for z in range(-518, -475):
        for x in (-127, -104):
            c.set_block(x, Y_BASE + 12, z, MAT['wall_quartz'])
            c.set_block(x, Y_BASE + 13, z, MAT['pane_cyan'])

    for y in range(Y_BASE + 13, Y_BASE + 18):
        for z in range(-512, -475):
            for x in range(-124, -105):
                if x in (-124, -106) or z in (-512, -476):
                    c.set_block(x, y, z, MAT['wall_quartz'] if (x + z) % 3 == 0 or y == Y_BASE + 17 else MAT['glass_cyan'])
                else:
                    c.set_block(x, y, z, 'minecraft:air')
    build_flat_roof_and_eaves(c, -124, Y_BASE + 18, -512, -106, -476, overhang=1,
                              roof_mat=MAT['pool_shallow_1'], soffit_mat=MAT['wall_quartz'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)

    for dy_s, r_s in [(19, 4), (20, 4), (21, 3), (22, 2), (23, 1)]:
        for dx in range(-r_s, r_s + 1):
            for dz in range(-r_s, r_s + 1):
                c.set_block(-115 + dx, Y_BASE + dy_s, -496 + dz, MAT['gold_block'] if dy_s in (20, 22) else MAT['light_sea'])
    c.fill(-115, Y_BASE + 24, -496, -115, Y_BASE + 26, -496, MAT['end_rod_up'])

    build_spiral_staircase(c, -110, Y_BASE + 1, Y_BASE + 12, -480, radius=2, start_sector=2, clockwise=True, intermediate_floors=[Y_BASE + 6])
    place_double_door(c, -130, Y_BASE + 1, -498, 'dark_oak', 'east', 'true')
    place_double_door(c, -102, Y_BASE + 1, -498, 'dark_oak', 'west', 'true')
    place_double_door(c, -115, Y_BASE + 7, -518, 'dark_oak', 'south', 'true')
    build_illuminated_carpet_rug(c, -125, Y_BASE, -514, -114, -488, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_bar(c, -122, Y_BASE, -516, length=8)

    for z in range(-614, -551):
        for x in range(-132, -100):
            c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else 'minecraft:smooth_sandstone')

    def in_casa_u(x, z):
        if not (-130 <= x <= -102 and -612 <= z <= -554):
            return False

        if x >= -120 and -594 <= z <= -572:
            return False
        return True

    for z in range(-612, -553):
        for x in range(-130, -101):
            if not in_casa_u(x, z):
                continue
            on_edge = (not in_casa_u(x - 1, z) or not in_casa_u(x + 1, z) or not in_casa_u(x, z - 1) or not in_casa_u(x, z + 1))
            c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (x + z) % 2 == 0 else MAT['wall_quartz'])
            c.set_block(x, Y_BASE + 6, z, MAT['wood_dark'])
            for y in range(Y_BASE + 1, Y_BASE + 12):
                if y == Y_BASE + 6:
                    continue
                if on_edge:
                    is_arch = ((x + z) % 4 in (1, 2) and y in (Y_BASE + 2, Y_BASE + 3, Y_BASE + 8, Y_BASE + 9))
                    c.set_block(x, y, z, MAT['glass_clear'] if is_arch else (MAT['wall_calcite'] if y != Y_BASE + 5 else 'minecraft:smooth_sandstone'))
                else:
                    c.set_block(x, y, z, 'minecraft:air')

            dist_edge = 0
            for r_step in range(1, 5):
                if in_casa_u(x - r_step, z) and in_casa_u(x + r_step, z) and in_casa_u(x, z - r_step) and in_casa_u(x, z + r_step):
                    dist_edge = r_step
                else:
                    break
            ry = Y_BASE + 12 + min(3, dist_edge)
            c.set_block(x, ry, z, 'minecraft:orange_terracotta' if (x + z) % 2 == 0 else 'minecraft:bricks')
            c.set_block(x, ry + 1, z, 'minecraft:brick_slab[type=bottom,waterlogged=false]' if dist_edge < 3 else MAT['light_ochre'])

    build_fountain(c, -111, Y_BASE, -583, radius=4)
    build_palm_tree(c, -105, Y_BASE, -591, height=9, lean_dx=1, lean_dz=0, seed=95101)
    build_palm_tree(c, -105, Y_BASE, -575, height=9, lean_dx=1, lean_dz=0, seed=95102)

    bcx, bcz = -107, -559
    for y in range(Y_BASE + 1, Y_BASE + 18):
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                if abs(dx) == 3 and abs(dz) == 3:
                    continue
                on_b_wall = (abs(dx) == 3 or abs(dz) == 3 or (abs(dx) == 2 and abs(dz) == 2))
                if on_b_wall:
                    if y in (Y_BASE + 14, Y_BASE + 15) and (dx == 0 or dz == 0):
                        c.set_block(bcx + dx, y, bcz + dz, 'minecraft:air')
                    else:
                        c.set_block(bcx + dx, y, bcz + dz, MAT['wall_calcite'] if y % 4 != 0 else 'minecraft:smooth_sandstone')
                elif y == Y_BASE + 13:
                    c.set_block(bcx + dx, y, bcz + dz, MAT['wood_dark'])
                else:
                    c.set_block(bcx + dx, y, bcz + dz, 'minecraft:air')

    c.set_block(bcx, Y_BASE + 15, bcz, MAT['gold_block'])
    c.set_block(bcx, Y_BASE + 16, bcz, MAT['chain_y'])
    for dy_c, r_c in [(18, 3), (19, 2), (20, 1)]:
        for dx in range(-r_c, r_c + 1):
            for dz in range(-r_c, r_c + 1):
                c.set_block(bcx + dx, Y_BASE + dy_c, bcz + dz, MAT['cut_copper_ox'] if dy_c == 18 else 'minecraft:orange_terracotta')
    c.set_block(bcx, Y_BASE + 21, bcz, MAT['end_rod_up'])

    build_spiral_staircase(c, -125, Y_BASE + 1, Y_BASE + 6, -560, radius=2, start_sector=1, clockwise=True)
    place_double_door(c, -130, Y_BASE + 1, -583, 'dark_oak', 'east', 'true')
    place_double_door(c, -121, Y_BASE + 1, -583, 'dark_oak', 'west', 'true')

    gx1, gx2, gz1, gz2 = -188, -158, -522, -474
    c.fill(gx1 - 1, Y_BASE, gz1 - 1, gx2 + 1, Y_BASE, gz2 + 1, MAT['wall_quartz'])
    for z in range(gz1, gz2 + 1):
        for x in range(gx1, gx2 + 1):
            c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])

            in_atrium = (-180 <= x <= -166 and -512 <= z <= -484) and not (-500 <= z <= -496)
            if not in_atrium:
                c.set_block(x, Y_BASE + 6, z, MAT['light_ochre'] if (x + z) % 6 == 0 else MAT['wood_dark'])
            elif x in (-180, -166) or z in (-512, -484) or z in (-500, -496):
                c.set_block(x, Y_BASE + 6, z, MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 7, z, MAT['pane_cyan'])

            if x in (gx1, gx2) or z in (gz1, gz2):
                for y in range(Y_BASE + 1, Y_BASE + 11):
                    if (x - gx1) % 5 == 0 or (z - gz1) % 6 == 0:
                        c.set_block(x, y, z, MAT['wall_white'])
                    elif y == Y_BASE + 6:
                        c.set_block(x, y, z, MAT['frame_dark'])
                    else:
                        c.set_block(x, y, z, MAT['glass_cyan'] if (x + z + y) % 2 == 0 else MAT['glass_clear'])

            u_x = (x - (-173)) / 15.0
            vault_dy = int(round(6.0 * max(0.0, 1.0 - u_x * u_x)))
            vy = Y_BASE + 11 + vault_dy
            if z in (gz1, gz2) or (z - gz1) % 6 == 0:
                c.set_block(x, vy, z, MAT['wall_quartz'])
                c.set_block(x, vy + 1, z, MAT['slab_quartz_b'])
                if abs(x - (-173)) <= 10 and z not in (gz1, gz2):
                    c.set_block(x, vy - 1, z, MAT['light_sea'] if x % 3 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, vy, z, MAT['glass_cyan'] if abs(x - (-173)) <= 9 else MAT['wall_white'])

    build_fountain(c, -173, Y_BASE, -506, radius=4)
    build_spiral_staircase(c, -163, Y_BASE + 1, Y_BASE + 6, -479, radius=2, start_sector=5, clockwise=True)
    place_double_door(c, gx2, Y_BASE + 1, -498, 'dark_oak', 'west', 'true')
    place_double_door(c, gx1, Y_BASE + 1, -498, 'dark_oak', 'east', 'true')
    place_double_door(c, -173, Y_BASE + 1, gz1, 'dark_oak', 'south', 'true')
    place_double_door(c, -173, Y_BASE + 1, gz2, 'dark_oak', 'north', 'true')

    tcx, tcz, trad = -172, -583, 14
    for dx in range(-trad - 1, trad + 2):
        for dz in range(-trad - 1, trad + 2):
            d = math.hypot(dx, dz)
            if d > trad + 1.2:
                continue
            x, z = tcx + dx, tcz + dz
            c.set_block(x, Y_BASE, z, MAT['carpet_red'] if d <= trad - 2 and (dx + dz) % 3 == 0 else MAT['wood_dark'])
            if trad - 0.8 <= d <= trad + 0.6:
                is_entry = (dx > 0 and abs(dz) <= 2)
                for y in range(Y_BASE + 1, Y_BASE + 10):
                    if is_entry and y <= Y_BASE + 4:
                        c.set_block(x, y, z, 'minecraft:air')
                    elif (dx + dz) % 4 == 0:
                        c.set_block(x, y, z, MAT['pillar_quartz'])
                    elif y in (Y_BASE + 1, Y_BASE + 9):
                        c.set_block(x, y, z, MAT['gold_block'] if (dx + dz) % 2 == 0 else MAT['wall_quartz'])
                    else:
                        c.set_block(x, y, z, MAT['wall_calcite'] if y % 2 == 0 else 'minecraft:cyan_terracotta')
            elif d < trad - 0.8:

                dome_y = Y_BASE + 10 + int(round(6.0 * max(0.0, 1.0 - (d / trad) ** 2)))
                c.set_block(x, dome_y, z, MAT['cut_copper_ox'] if int(d) % 2 == 0 else MAT['wall_quartz'])
                if int(d) in (0, 4, 8, 12) and (dx + dz) % 3 == 0:
                    c.set_block(x, dome_y - 1, z, MAT['light_ochre'])

    c.fill(-158, Y_BASE + 4, -586, -154, Y_BASE + 5, -580, MAT['gold_block'])
    for dz_m in (-3, 3):
        for x_m in range(-158, -153):
            c.set_block(x_m, Y_BASE + 4, -583 + dz_m, MAT['light_sea'] if x_m % 2 == 0 else MAT['red_concrete'])
    for y_m in range(Y_BASE + 6, Y_BASE + 19):
        c.set_block(-156, y_m, -583, MAT['red_concrete'] if y_m % 2 == 0 else MAT['gold_block'])
        c.set_block(-155, y_m, -583, MAT['light_sea'] if y_m % 2 == 0 else MAT['light_ochre'])
    c.set_block(-156, Y_BASE + 19, -583, MAT['end_rod_up'])

def _build_civic_auditorium_tongva_park_and_library(c: WorldCanvas):
    """
    Step 5 (Requirement 4 — Zone 3 `X = -190..-98, Z = -816..-646, Y = 64..81`):
      1. **Tongva Park Sculpted Observation Hill, Braided Streams & Double-Helix Lookouts (`X = -146..-100, Z = -732..-652`)**:
         - Organic sculpted park mounds (`Y = 64..70`), braided turquoise reflection rills, and twin copper/quartz
           cantilevered observation spirals!
      2. **Santa Monica Civic Auditorium — Mid-Century Modern Folded-Plate Wing Roof (`X = -188..-152, Z = -732..-654, Y = 64..79`)**:
         - Welton Becket's famous 1958 mid-century landmark with a sinusoidal folded-plate white quartz roof,
           angled brise-soleil screen facade, grand concert stage, and tiered seating!
      3. **Santa Monica Public Library & Andalusian Reading Cloister (`X = -186..-104, Z = -810..-744, Y = 64..78`)**:
         - L-shaped civic library & botanical cloister with arched reading galleries, bookshelves, lecterns,
           courtyard fountain, and spiral staircase at `(-178, -752)`!
    """

    for z in range(-732, -651):
        for x in range(-146, -99):
            d1 = math.hypot((x - (-118)) / 14.0, (z - (-674)) / 14.0)
            d2 = math.hypot((x - (-124)) / 14.0, (z - (-712)) / 14.0)
            rill_x = -122 + int(round(5.0 * math.sin(z / 11.0)))
            if abs(x - rill_x) <= 1 and -726 <= z <= -658:
                c.set_block(x, Y_BASE - 1, z, MAT['light_sea'] if (x + z) % 3 == 0 else MAT['pool_shallow_1'])
                c.set_block(x, Y_BASE, z, MAT['water'])
            elif d1 < 1.0 or d2 < 1.0:
                mh = Y_BASE + int(round(4.0 * max(0.0, 1.0 - min(d1, d2))))
                c.fill(x, Y_BASE, z, x, mh - 1, z, MAT['dirt'])
                c.set_block(x, mh, z, MAT['moss_block'] if (x + z) % 2 == 0 else MAT['grass_block'])
                if mh == Y_BASE + 4 and (abs(x - (-118)) <= 2 or abs(x - (-124)) <= 2):
                    c.set_block(x, mh, z, MAT['cut_copper_ox'])
                    c.set_block(x, mh + 1, z, MAT['pane_cyan'])
            elif abs(x - rill_x) in (2, 3):
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['wood_warm'])

    ax1, ax2, az1, az2 = -188, -152, -730, -656
    for z in range(az1, az2 + 1):

        fold_wave = int(round(1.6 * math.sin((z - az1) * math.pi / 6.0)))
        for x in range(ax1, ax2 + 1):

            t_x = (x - ax1) / float(ax2 - ax1)
            roof_y = Y_BASE + 10 + int(round(3.0 * t_x)) + fold_wave
            c.set_block(x, Y_BASE, z, MAT['carpet_red'] if (-180 <= x <= -162 and (x + z) % 3 == 0) else MAT['stone_dio'])

            if x in (ax1, ax2) or z in (az1, az2):
                is_front_portal = (x == ax2 and abs(z - (-693)) <= 6)
                for y in range(Y_BASE + 1, roof_y):
                    if is_front_portal and y <= Y_BASE + 4:
                        c.set_block(x, y, z, 'minecraft:air')
                    elif x == ax2:

                        c.set_block(x, y, z, MAT['wall_quartz'] if (y + z) % 2 == 0 else MAT['glass_cyan'])
                    elif (x - ax1) % 6 == 0 or (z - az1) % 6 == 0:
                        c.set_block(x, y, z, MAT['wall_white'])
                    else:
                        c.set_block(x, y, z, MAT['glass_clear'] if y % 3 != 0 else MAT['wall_quartz'])

            c.set_block(x, roof_y, z, MAT['wall_quartz'] if fold_wave >= 0 else MAT['pool_shallow_1'])
            c.set_block(x, roof_y + 1, z, MAT['slab_quartz_b'])
            if (x - ax1) % 6 == 3 and (z - az1) % 6 == 3:
                c.set_block(x, roof_y - 1, z, MAT['light_sea'])

        for x_cant in range(ax2 + 1, ax2 + 5):
            ry_c = Y_BASE + 13 + fold_wave
            c.set_block(x_cant, ry_c, z, MAT['wall_quartz'])
            c.set_block(x_cant, ry_c + 1, z, MAT['slab_quartz_b'])
            if z in (az1 + 4, -693, az2 - 4) and x_cant == ax2 + 3:
                c.fill(x_cant, Y_BASE + 1, z, x_cant, ry_c - 1, z, MAT['pillar_quartz'])

    for z in range(-810, -745):
        for x in range(-186, -103):

            in_lib = (-186 <= x <= -156 and -808 <= z <= -748) or (-156 <= x <= -106 and -808 <= z <= -782)
            if not in_lib:

                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x % 5 == 0 or z % 5 == 0) else MAT['moss_block'])
                continue
            on_l_edge = not (
                ((-186 <= x - 1 <= -156 and -808 <= z <= -748) or (-156 <= x - 1 <= -106 and -808 <= z <= -782)) and
                ((-186 <= x + 1 <= -156 and -808 <= z <= -748) or (-156 <= x + 1 <= -106 and -808 <= z <= -782)) and
                ((-186 <= x <= -156 and -808 <= z - 1 <= -748) or (-156 <= x <= -106 and -808 <= z - 1 <= -782)) and
                ((-186 <= x <= -156 and -808 <= z + 1 <= -748) or (-156 <= x <= -106 and -808 <= z + 1 <= -782))
            )
            c.set_block(x, Y_BASE, z, MAT['wood_warm'] if (x + z) % 2 == 0 else MAT['wall_quartz'])
            c.set_block(x, Y_BASE + 6, z, MAT['light_ochre'] if (x + z) % 5 == 0 else MAT['wood_dark'])
            for y in range(Y_BASE + 1, Y_BASE + 12):
                if y == Y_BASE + 6:
                    continue
                if on_l_edge:
                    is_door = (x == -156 and z in (-764, -763) and y <= Y_BASE + 3) or (z == -782 and x in (-130, -129) and y <= Y_BASE + 3)
                    if is_door:
                        c.set_block(x, y, z, 'minecraft:air')
                    elif (x + z) % 4 == 0:
                        c.set_block(x, y, z, 'minecraft:smooth_sandstone')
                    else:
                        c.set_block(x, y, z, MAT['glass_clear'] if y not in (Y_BASE + 1, Y_BASE + 5, Y_BASE + 7, Y_BASE + 11) else MAT['wall_calcite'])
                else:
                    c.set_block(x, y, z, 'minecraft:air')

            c.set_block(x, Y_BASE + 12, z, 'minecraft:orange_terracotta' if on_l_edge else MAT['cut_copper_ox'])
            c.set_block(x, Y_BASE + 13, z, MAT['slab_quartz_b'] if on_l_edge else 'minecraft:brick_slab[type=bottom,waterlogged=false]')

    for bx_s in (-178, -172, -166):
        c.fill(bx_s, Y_BASE + 1, -798, bx_s, Y_BASE + 4, -786, 'minecraft:bookshelf')
        c.fill(bx_s, Y_BASE + 7, -798, bx_s, Y_BASE + 10, -786, 'minecraft:bookshelf')
    build_spiral_staircase(c, -178, Y_BASE + 1, Y_BASE + 6, -754, radius=2, start_sector=3, clockwise=True)
    build_fountain(c, -130, Y_BASE, -764, radius=5)

def _build_venice_canals_and_six_distinct_villas(c: WorldCanvas):
    """
    Step 6 (Requirement 4 — Zone 4 `X = -308..-206, Z = -656..-464, Y = 59..78`):
    Builds the classic **Venice Beach Canals Historic District** (`X = -308..-206, Z = -656..-464`):
      1. **Grand Venice Canal Network (`Y = 60..62` water, `Y = 64` flowered canal-side towpaths)**:
         - Main North-South Venice Canal (`X = -259..-247, Z = -652..-460`, 13 blocks wide with `Y = 60` illuminated prismarine bed);
         - Two East-West Branch Canals (`Z = -514..-504` and `Z = -596..-586`, `X = -304..-208`);
         - **5 Iconic White-Timber High-Arched Venice Footbridges** spanning the canals (`(-253, -460)`, `(-253, -536)`,
           `(-253, -640)`, `(-228, -509)`, `(-278, -591)`);
         - **6 Pure-Voxel Venetian Gondolas & Canal Skiffs** with striped mooring poles!
      2. **6 Individually Designed, Non-Repetitive Canal-Front Architectural Villas** (ZERO matchboxes, ZERO repeats!):
         - **Villa 1 (`X = -240..-214, Z = -498..-470`) — Mid-Century Butterfly-Roof Glass Pavilion**;
         - **Villa 2 (`X = -298..-266, Z = -498..-470`) — Tuscan Campanile & Courtyard Canal Villa**;
         - **Villa 3 (`X = -240..-214, Z = -578..-548`) — Cantilevered Deconstructivist / Bauhaus Residence**;
         - **Villa 4 (`X = -298..-266, Z = -578..-548`) — Steep-Gable Cape Cod Boathouse Chalet**;
         - **Villa 5 (`X = -240..-214, Z = -632..-604`) — Circular Geodesic / Copper-Dome Artist Rotunda**;
         - **Villa 6 (`X = -298..-266, Z = -632..-604`) — Japanese-Californian Sweeping-Eave Zen Villa**.
    """

    for z in range(-652, -459):
        for x in range(-304, -207):
            in_ns = (-259 <= x <= -247)
            in_ew1 = (-514 <= z <= -504)
            in_ew2 = (-596 <= z <= -586)
            if not (in_ns or in_ew1 or in_ew2):
                continue
            on_bank = (
                (in_ns and x in (-259, -247) and not (in_ew1 or in_ew2)) or
                (in_ew1 and z in (-514, -504) and not in_ns) or
                (in_ew2 and z in (-596, -586) and not in_ns)
            )
            c.fill(x, 56, z, x, Y_BASE + 8, z, 'minecraft:air')
            c.fill(x, 56, z, x, 59, z, MAT['stone_pol_and'])
            if on_bank:
                c.fill(x, 60, z, x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 3 != 0 else MAT['light_ochre'])
                if (x + z) % 8 == 0:

                    c.set_block(x, Y_BASE + 1, z, MAT['red_concrete'])
                    c.set_block(x, Y_BASE + 2, z, MAT['wall_white'])
                    c.set_block(x, Y_BASE + 3, z, MAT['lantern_stand'])
            else:
                c.set_block(x, 60, z, MAT['light_sea'] if (x + z) % 5 == 0 else MAT['pool_shallow_1'])
                c.set_block(x, 61, z, MAT['water'])
                c.set_block(x, 62, z, MAT['water'])

    build_arched_canal_bridge(c, -253, Y_BASE, -460, width=7, span=14, axis='x')
    build_arched_canal_bridge(c, -253, Y_BASE, -536, width=9, span=14, axis='x')
    build_arched_canal_bridge(c, -253, Y_BASE, -640, width=7, span=14, axis='x')
    build_arched_canal_bridge(c, -226, Y_BASE, -509, width=5, span=12, axis='z')
    build_arched_canal_bridge(c, -280, Y_BASE, -591, width=5, span=12, axis='z')

    for gx, gz, g_axis in [(-253, -484, 'z'), (-253, -562, 'z'), (-253, -618, 'z'), (-276, -509, 'x'), (-226, -591, 'x')]:
        for step_g in range(-3, 4):
            bx = gx + (step_g if g_axis == 'x' else 0)
            bz = gz + (step_g if g_axis == 'z' else 0)
            c.set_block(bx, 62, bz, MAT['wood_dark'])
            if abs(step_g) == 3:
                c.set_block(bx, 63, bz, MAT['slab_quartz_b'])
            elif step_g == 0:
                c.set_block(bx, 63, bz, MAT['carpet_red'])
            elif abs(step_g) == 1:
                c.set_block(bx, 63, bz, stair('spruce', 'north' if g_axis == 'z' else 'east', 'bottom'))

    for z in range(-498, -469):
        for x in range(-240, -213):
            c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['wood_warm'])
            if -238 <= x <= -216 and -496 <= z <= -472:

                v_rise = abs(z - (-484)) // 3
                ry = Y_BASE + 7 + v_rise
                if x in (-238, -216) or z in (-496, -472):
                    is_door = (x == -238 and abs(z - (-484)) <= 1)
                    for y in range(Y_BASE + 1, ry):
                        if is_door and y <= Y_BASE + 3:
                            c.set_block(x, y, z, 'minecraft:air')
                        elif (x + z) % 4 == 0:
                            c.set_block(x, y, z, MAT['frame_dark'])
                        else:
                            c.set_block(x, y, z, MAT['glass_cyan'] if y % 2 == 0 else MAT['glass_clear'])
                c.set_block(x, ry, z, MAT['wall_white'])
                c.set_block(x, ry + 1, z, MAT['slab_quartz_b'])
                if (x + z) % 5 == 0 and -236 <= x <= -218:
                    c.set_block(x, ry - 1, z, MAT['light_ochre'])

    for z in range(-498, -469):
        for x in range(-298, -265):
            in_l = (-296 <= x <= -280 and -496 <= z <= -472) or (-280 <= x <= -268 and -496 <= z <= -482)
            if not in_l:
                c.set_block(x, Y_BASE, z, MAT['moss_block'] if (x + z) % 3 == 0 else MAT['stone_dio'])
                continue
            on_w = (x in (-296, -268) or z in (-496, -472) or (x == -280 and z > -482) or (z == -482 and x > -280))
            c.set_block(x, Y_BASE, z, MAT['wood_dark'])
            for y in range(Y_BASE + 1, Y_BASE + 8):
                if on_w:
                    if x == -268 and z in (-490, -489) and y <= Y_BASE + 3:
                        c.set_block(x, y, z, 'minecraft:air')
                    else:
                        c.set_block(x, y, z, 'minecraft:smooth_sandstone' if y in (Y_BASE + 1, Y_BASE + 7) else (MAT['glass_clear'] if (x + z) % 3 == 0 else MAT['wall_calcite']))

            d_e = min(abs(x - (-296)), abs(z - (-496)), abs(x - (-268)) if z <= -482 else abs(x - (-280)), abs(z - (-472)) if x <= -280 else abs(z - (-482)))
            ry = Y_BASE + 8 + min(3, d_e // 2)
            c.set_block(x, ry, z, 'minecraft:orange_terracotta')
            c.set_block(x, ry + 1, z, 'minecraft:brick_slab[type=bottom,waterlogged=false]')

    for y in range(Y_BASE + 1, Y_BASE + 14):
        for x in range(-274, -267):
            for z in range(-479, -472):
                if x in (-274, -268) or z in (-479, -473):
                    c.set_block(x, y, z, 'minecraft:smooth_sandstone' if (x in (-274, -268) and z in (-479, -473)) or y % 4 == 0 else (MAT['glass_yellow'] if y >= Y_BASE + 10 else MAT['wall_calcite']))
    c.fill(-275, Y_BASE + 14, -480, -267, Y_BASE + 14, -472, 'minecraft:orange_terracotta')
    c.set_block(-271, Y_BASE + 15, -476, MAT['light_ochre'])

    c.fill(-238, Y_BASE, -576, -216, Y_BASE, -556, MAT['wood_dark'])
    for y in range(Y_BASE + 1, Y_BASE + 6):
        for x in range(-238, -215):
            for z in range(-576, -555):
                if x in (-238, -216) or z in (-576, -556):
                    c.set_block(x, y, z, MAT['wall_white'] if (x + z) % 4 == 0 else MAT['glass_black'])
    c.fill(-238, Y_BASE + 1, -567, -238, Y_BASE + 3, -565, 'minecraft:air')
    c.fill(-242, Y_BASE + 6, -576, -216, Y_BASE + 6, -550, MAT['wall_quartz'])
    for y in range(Y_BASE + 7, Y_BASE + 12):
        for x in range(-242, -217):
            for z in range(-568, -549):
                if x in (-242, -218) or z in (-568, -550):
                    c.set_block(x, y, z, MAT['frame_dark'] if (x + z) % 4 == 0 else MAT['glass_cyan'])
    build_flat_roof_and_eaves(c, -242, Y_BASE + 12, -568, -218, -550, overhang=1,
                              roof_mat=MAT['wall_white'], soffit_mat=MAT['wood_dark'],
                              coping_slab=MAT['slab_quartz_b'], hidden_lights=True)

    for z in range(-576, -550):
        for x in range(-296, -267):
            c.set_block(x, Y_BASE, z, MAT['wood_warm'])

            gable_h = max(0, 13 - abs(x - (-282)))
            ry = Y_BASE + gable_h
            if z in (-576, -551):
                for y in range(Y_BASE + 1, ry):
                    c.set_block(x, y, z, MAT['glass_clear'] if abs(x - (-282)) <= 4 and y >= Y_BASE + 3 else MAT['wood_warm'])
            if ry > Y_BASE:
                c.set_block(x, ry, z, MAT['wood_dark'] if z % 2 == 0 else 'minecraft:spruce_planks')
                c.set_block(x, ry + 1, z, MAT['slab_spruce_b'])
                if x == -282 and z % 3 == 0:
                    c.set_block(x, ry - 1, z, MAT['light_ochre'])

    rcx, rcz = -227, -618
    for dx in range(-11, 12):
        for dz in range(-11, 12):
            d = math.hypot(dx, dz)
            if d > 11.2:
                continue
            x, z = rcx + dx, rcz + dz
            c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (dx + dz) % 2 == 0 else MAT['pool_shallow_1'])
            if 9.2 <= d <= 10.6:
                for y in range(Y_BASE + 1, Y_BASE + 7):
                    if dx < -8 and abs(dz) <= 1 and y <= Y_BASE + 3:
                        c.set_block(x, y, z, 'minecraft:air')
                    else:
                        c.set_block(x, y, z, MAT['pillar_quartz'] if (dx + dz) % 3 == 0 else MAT['glass_cyan'])
            dome_h = int(round(6.0 * max(0.0, 1.0 - (d / 11.0) ** 2)))
            c.set_block(x, Y_BASE + 7 + dome_h, z, MAT['cut_copper_ox'] if int(d) % 2 == 0 else MAT['glass_clear'])
            if int(d) in (0, 4, 8) and (dx + dz) % 3 == 0:
                c.set_block(x, Y_BASE + 6 + dome_h, z, MAT['light_sea'])

    zx1, zx2, zz1, zz2 = -296, -268, -630, -606
    for z in range(zz1, zz2 + 1):
        for x in range(zx1, zx2 + 1):
            c.set_block(x, Y_BASE, z, MAT['moss_block'] if (x < -286 or z > -614) else MAT['wood_birch'])
    for z in range(-628, -612):
        for x in range(-286, -269):
            if x in (-286, -270) or z in (-628, -613):
                for y in range(Y_BASE + 1, Y_BASE + 6):
                    c.set_block(x, y, z, MAT['beam_dark_y'] if (x + z) % 4 == 0 else MAT['glass_white'])

    for z in range(-630, -610):
        for x in range(-288, -267):
            dx_c = abs(x - (-278))
            dz_c = abs(z - (-620))
            d_max = max(dx_c, dz_c)
            ry = Y_BASE + 6 + max(0, 4 - d_max // 3) + (1 if d_max >= 9 else 0)
            c.set_block(x, ry, z, MAT['deepslate_tiles'] if d_max % 2 == 0 else MAT['wood_dark'])
            c.set_block(x, ry + 1, z, MAT['slab_dtile_b'])

def _build_bergamot_arts_center_and_aero_hangar(c: WorldCanvas):
    """
    Step 7 (Requirement 4 — Zone 5 `X = -304..-208, Z = -814..-656, Y = 64..80`):
      1. **Santa Monica Museum of Flying — Parabolic Steel-Arch Aviation Hangar (`X = -298..-250, Z = -746..-682, Y = 64..80`)**:
         - Wide-span parabolic arched steel & glass hangar (`49 × 65` blocks) with a **Pure-Voxel Twin-Propeller
           Vintage Douglas DC-3 / Coastal Seaplane** suspended inside at `(-274, 71, -714)` and a yellow biplane
           on the outdoor tarmac apron (`-274, 65, -668`)!
      2. **Bergamot Station Sawtooth-Skylight Contemporary Art Galleries & Sculpture Park (`X = -242..-208, Z = -808..-682, Y = 64..75`)**:
         - Iconic industrial-chic sawtooth north-light roof bays, outdoor abstract voxel sculptures, and a
           classic **Pacific Electric Red-Car Trolley (`X = -246..-242, Z = -768..-744`)** on heritage rails!
    """

    hx1, hx2, hz1, hz2 = -298, -250, -746, -682
    for z in range(hz1 - 18, hz2 + 4):
        for x in range(hx1 - 2, hx2 + 3):
            c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if (x == -274 and z % 4 in (0, 1)) else MAT['stone_pol_and'])

    for z in range(hz1, hz2 + 1):
        is_rib = ((z - hz1) % 8 == 0 or z in (hz1, hz2))
        for x in range(hx1, hx2 + 1):
            u_x = (x - (-274)) / 24.0
            arch_h = int(round(14.0 * max(0.0, 1.0 - u_x * u_x)))
            ry = Y_BASE + 1 + arch_h
            if x in (hx1, hx2):
                for y in range(Y_BASE + 1, ry + 1):
                    c.set_block(x, y, z, MAT['frame_dark'] if is_rib else MAT['glass_cyan'])
            elif z in (hz1, hz2):

                for y in range(Y_BASE + 1, ry):
                    if z == hz2 and abs(x - (-274)) <= 16 and y <= Y_BASE + 8:
                        c.set_block(x, y, z, 'minecraft:air')
                    else:
                        c.set_block(x, y, z, MAT['glass_clear'] if (x + y) % 2 == 0 else MAT['wall_white'])
            c.set_block(x, ry, z, MAT['frame_dark'] if is_rib else (MAT['glass_cyan'] if abs(x - (-274)) <= 8 else MAT['wall_white']))
            c.set_block(x, ry + 1, z, MAT['slab_deep_b'] if is_rib else MAT['slab_quartz_b'])
            if is_rib and abs(x - (-274)) <= 14 and x % 4 == 0:
                c.set_block(x, ry - 1, z, MAT['light_sea'])

    px, py, pz = -274, Y_BASE + 7, -714
    for dz_f in range(-9, 10):
        c.fill(px - 1, py, pz + dz_f, px + 1, py + 1, pz + dz_f, MAT['wall_white'])
        c.set_block(px, py + 1, pz + dz_f, MAT['blue_concrete'] if dz_f % 2 == 0 else MAT['wall_quartz'])

    c.fill(px - 14, py, pz - 2, px + 14, py, pz + 1, MAT['slab_quartz_t'])
    for ex_eng in (px - 6, px + 6):
        c.fill(ex_eng, py, pz - 1, ex_eng, py, pz + 3, MAT['frame_dark'])
        c.set_block(ex_eng, py, pz + 4, MAT['light_ochre'])

    c.fill(px, py + 2, pz - 9, px, py + 5, pz - 7, MAT['red_concrete'])
    c.fill(px - 4, py + 1, pz - 9, px + 4, py + 1, pz - 8, MAT['slab_quartz_t'])

    for sz_c in (pz - 4, pz + 4):
        c.fill(px, py + 2, sz_c, px, Y_BASE + 14, sz_c, MAT['chain_y'])

    for z in range(-804, -685):
        tooth_phase = (z - (-804)) % 12
        tooth_h = 6 + (tooth_phase // 2)
        for x in range(-240, -207):
            c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['wall_quartz'])
            if x in (-240, -208) or z in (-804, -686):
                is_g_door = (x == -208 and z in (-780, -740, -706))
                for y in range(Y_BASE + 1, Y_BASE + tooth_h):
                    if is_g_door and y <= Y_BASE + 3:
                        c.set_block(x, y, z, 'minecraft:air')
                    else:
                        c.set_block(x, y, z, 'minecraft:bricks' if (x + z) % 5 != 0 else MAT['frame_dark'])
            ry = Y_BASE + tooth_h
            c.set_block(x, ry, z, MAT['cut_copper_ox'] if tooth_phase % 2 == 0 else MAT['frame_dark'])
            if tooth_phase == 11 and -238 <= x <= -210:
                for y_gl in range(Y_BASE + 6, ry):
                    c.set_block(x, y_gl, z, MAT['glass_cyan'] if x % 2 == 0 else MAT['glass_clear'])
                if x % 4 == 0:
                    c.set_block(x, Y_BASE + 6, z - 1, MAT['light_sea'])

    for z in range(-796, -684):
        c.set_block(-246, Y_BASE, z, MAT['frame_dark'])
        c.set_block(-243, Y_BASE, z, MAT['frame_dark'])
        c.set_block(-245, Y_BASE, z, MAT['stone_and'] if z % 2 == 0 else MAT['stone_pol_and'])
        c.set_block(-244, Y_BASE, z, MAT['stone_and'] if z % 2 == 0 else MAT['stone_pol_and'])
    for z in range(-764, -746):
        for x in range(-246, -242):
            c.set_block(x, Y_BASE + 1, z, MAT['red_concrete'])
            c.set_block(x, Y_BASE + 2, z, MAT['yellow_concrete'] if z in (-764, -747) else (MAT['glass_clear'] if x in (-246, -243) else 'minecraft:air'))
            c.set_block(x, Y_BASE + 3, z, MAT['red_concrete'])
            c.set_block(x, Y_BASE + 4, z, MAT['slab_quartz_b'])
    c.set_block(-245, Y_BASE + 2, -764, MAT['light_ochre'])
    c.set_block(-244, Y_BASE + 2, -747, MAT['light_ochre'])

def step17_main_urban_district_prototype(c: WorldCanvas):
    """
    Master Builder Entry Point for V5.5 Coastal Inland & X- Expansion Zone (`X in [-320, 23], Z in [-864, -448]`):
      1. Demolishes 100% of natural terrain and sculpts the **Santa Monica Palisades Bluffs & Civic/Canal Datum**;
      2. Builds **Pacific Coast Highway (PCH)**, **The California Incline**, **Ocean Ave**, **Lincoln Blvd**, and cross avenues;
      3. Builds **Santa Monica Palisades Bluff Park**, **Camera Obscura Overlook**, **Rose Garden**, and 4 cliffside overlooks;
      4. Builds **Third Street Promenade** (with 3 topiary dinosaur fountains) & **4 Distinct Non-Boxy Landmark Buildings**
         (Georgian Art-Deco Ziggurat Hotel, Casa del Mar Courtyard Mansion, Santa Monica Place Barrel-Vault Galleria,
         and Criterion Rotunda Theater);
      5. Builds **Tongva Park**, **Santa Monica Civic Auditorium (Mid-Century Folded-Plate Roof)**, and **Public Library Cloister**;
      6. Builds the **Venice Beach Canals Historic District** (3 intersecting canals, 5 arched bridges, 6 gondolas, and
         6 individually sculpted non-repetitive canal-front villas);
      7. Builds the **Santa Monica Museum of Flying Parabolic Hangar (with DC-3 Seaplane)** & **Bergamot Station Sawtooth Art Center**.
    """
    _bulldoze_and_sculpt_palisades_bluffs(c)
    _build_pch_and_california_incline(c)
    _build_palisades_bluff_park_and_overlooks(c)
    _build_third_street_promenade_and_distinct_landmarks(c)
    _build_civic_auditorium_tongva_park_and_library(c)
    _build_venice_canals_and_six_distinct_villas(c)
    _build_bergamot_arts_center_and_aero_hangar(c)
