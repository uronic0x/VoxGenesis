"""
zone_urban_district.py — V5.4 Santa Monica Palisades Bluff Park & California Incline
=====================================================================================
In V5.4, per user feedback:
  1. The rear Main Urban District is postponed ("后方大型主城区先延后") to focus 100% on
     polishing the Santa Monica Beach State Park & Pier complex.
  2. Matchbox-style buildings at `(-52, 90, -586)` ("坚决避免 -52 90 -586 这样的火柴盒建筑")
     are completely removed and replaced with authentic **Santa Monica Palisades Park**
     coastal bluffs, the **California Incline** curved hillside ramp, architectural pergola
     overlooks, rose gardens, and sculpted Mediterranean villas/pavilions.
  3. Natural terrain in the entire expanded zone (`Z = -800..-448`) is NOT reused
     ("自然地形不能复用，需要推倒自行生成") and raw cut stone cliffs ("大片裸露石壁") at the
     perimeter are completely eliminated via custom-sculpted coastal hills and vegetated
     terrace slopes that blend seamlessly into the outer terrain at `Z = -800` and `X = -320`.
"""

import math
from config import Y_BASE, MAT, SOFT_FLOWERS
from world_canvas import WorldCanvas
from arch_lib import (
    stair, trapdoor,
    place_double_door,
    build_lamppost, build_fountain, build_hedgerow_line,
    build_custom_tree, build_patio_umbrella,
    build_outdoor_sofa, build_outdoor_bar,
    build_vine_arch, build_pergola_colonnade,
)
from zone_beach_park import build_palm_tree

def _target_inland_bluff_elevation(c: WorldCanvas, x: int, z: int) -> int:
    """
    Computes the 100% custom-generated terrain elevation for `X in [c.x_min, 23], Z in [c.z_min, -448]`:
      - `X = 12..23`: Pacific Coast Highway (PCH, Highway 1) at `Y = 64` (except north edge transition `Z < -776`).
      - `X = -16..11`: Sculpted **California Coastal Bluff Slope** rising from `Y = 64` at `X = 11` up to
        `Y = 72` at `X = -16` (with the **California Incline** ramp cut smoothly through `Z = -542..-530`
        and a second north coastal ramp at `Z = -696..-686`).
      - `X = -76..-17`: **Santa Monica Palisades Park Bluff-Top Promenade & Rose Garden Terrace** at `Y = 72`,
        giving sweeping elevated ocean views over the beach, boardwalk, and Santa Monica Pier (`-52, 72..78, -586`
        is now an open-air Spanish-Revival Camera Obscura & Sunset Pergola Overlook—zero matchbox buildings!).
      - `X = -140..-77`: Gently rolling coastal foothills (`Y = 72 -> 66`).
      - `X = -320..-141`: Custom-generated coastal plain & western meadow (`Y = 64..66`), smoothly matching
        the outer seed_world elevation at `X = -320` and `Z = -800` so ZERO raw stone cliffs exist anywhere!
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
    elif x >= -76:

        if -543 <= z <= -529 and x >= -44:
            t_inc = max(0.0, min(1.0, (11 - x) / 55.0))
            base_y = Y_BASE + int(round(8.0 * t_inc))
        elif -696 <= z <= -686 and x >= -29:
            t_inc = max(0.0, min(1.0, (11 - x) / 40.0))
            base_y = Y_BASE + int(round(8.0 * t_inc))
        else:
            base_y = 72
    elif x >= -136:

        if -543 <= z <= -529:
            t_w = max(0.0, min(1.0, (x - (-136)) / 60.0))
            base_y = Y_BASE + int(round(8.0 * t_w))
        else:
            t_w = max(0.0, min(1.0, (x - (-136)) / 60.0))
            s_w = t_w * t_w * (3.0 - 2.0 * t_w)
            base_y = Y_BASE + int(round(8.0 * s_w))
    else:

        wave = int(round(1.5 * math.sin(x / 28.0) * math.cos(z / 32.0)))
        base_y = Y_BASE + max(0, wave)

    if z >= -468 and base_y > Y_BASE:
        t_south = max(0.0, min(1.0, (-448 - z) / 20.0))
        s_south = t_south * t_south * (3.0 - 2.0 * t_south)
        base_y = int(round(Y_BASE * (1.0 - s_south) + base_y * s_south))

    if z < -764:
        t_n = max(0.0, min(1.0, (-764 - z) / 36.0))
        s_n = t_n * t_n * (3.0 - 2.0 * t_n)

        if x >= -76:
            north_target = 72 + int(round(2.0 * math.sin((x - 24) / 20.0)))
        else:
            orig_w = min(74, max(62, c.orig_surface_y.get((x, z), Y_BASE)))
            t_xw = max(0.0, min(1.0, (x - (-160)) / 84.0))
            north_target = int(round(orig_w * (1.0 - t_xw) + 72 * t_xw))
        base_y = int(round(base_y * (1.0 - s_n) + north_target * s_n))

    d_west_edge = x - c.x_min
    if d_west_edge < 32:
        t_w_edge = max(0.0, min(1.0, d_west_edge / 32.0))
        s_w_edge = t_w_edge * t_w_edge * (3.0 - 2.0 * t_w_edge)
        clamped_west = min(74, max(62, c.orig_surface_y.get((x, z), Y_BASE)))
        base_y = int(round(clamped_west * (1.0 - s_w_edge) + base_y * s_w_edge))

    return base_y

def _bulldoze_and_sculpt_palisades_bluffs(c: WorldCanvas):
    """
    1. Demolishes 100% of the natural terrain in `X = -320..23, Z = -800..-448` (`Y = 46..175`)
       and generates the custom Santa Monica Palisades Park bluffs, terraced vegetated cliffside,
       California Incline ramp, and inland meadow—with zero raw cut stone walls!
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

            if -16 <= x <= 11 and ty > Y_BASE and not (-543 <= z <= -529 or -696 <= z <= -686):
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
    2. Builds:
       - **Pacific Coast Highway (PCH / State Route 1, `X = 12..23, Z = -768..-448, Y = 64`)**:
         12-block-wide iconic coastal boulevard at the base of the Palisades Bluffs with a palm-lined
         central median, dual asphalt lanes, coastal sidewalks, and pedestrian crosswalks at
         `Z = -460`, `-536` (Pier Bridge axis), `-614`, `-690`, and `-752`.
       - **The California Incline (`Z = -542..-530, X = -44..11, Y = 64 -> 72`)**:
         Santa Monica's famous sloped coastal roadway & pedestrian/bike promenade climbing from PCH
         up the Palisades Bluffs to the Bluff-Top Park, flanked by tiered white quartz & sandstone
         retaining walls and arched pedestrian overpass bridges!
    """
    crosswalk_zs = [(-464, -456), (-542, -530), (-618, -610), (-695, -687), (-756, -748)]

    def in_crosswalk_band(z):
        return any(z0 <= z <= z1 for z0, z1 in crosswalk_zs)

    for z in range(-768, -447):
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

    for x in range(-44, 12):
        ry = _target_inland_bluff_elevation(c, x, -536)
        next_ry = _target_inland_bluff_elevation(c, x - 1, -536)
        use_slab = (next_ry > ry)
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

    for x in range(-29, 12):
        ry = _target_inland_bluff_elevation(c, x, -691)
        next_ry = _target_inland_bluff_elevation(c, x - 1, -691)
        use_slab = (next_ry > ry)
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

    for av_cx, z_north_end in [(-91, -752), (-199, -614)]:
        for z in range(z_north_end, -447):
            ry = _target_inland_bluff_elevation(c, av_cx, z)
            for dx in range(-4, 5):
                x = av_cx + dx
                c.fill(x, ry - 2, z, x, ry - 1, z, MAT['stone_pol_and'])
                if abs(dx) == 4:
                    c.set_block(x, ry, z, MAT['stone_pol_and'])
                elif abs(dx) == 3:
                    c.set_block(x, ry, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_dio'])
                elif dx == 0:
                    c.set_block(x, ry, z, MAT['light_ochre'] if z % 6 == 0 else MAT['wall_quartz'])
                else:
                    c.set_block(x, ry, z, MAT['wall_gray'])
            if z % 20 == 0:
                build_lamppost(c, av_cx - 3, ry + 1, z, style='courtyard')
                build_lamppost(c, av_cx + 3, ry + 1, z, style='courtyard')

def _build_palisades_bluff_park_and_overlooks(c: WorldCanvas):
    """
    3. Builds the **Santa Monica Palisades Park** along the Bluff-Top Plateau (`X = -74..-16, Z = -748..-462, Y = 72`):
       - Cliffside Palm & Cypress Promenade (`X = -22..-16, Z = -744..-464, Y = 72`) with white sandstone
         balustrades and 3 cantilevered semi-circular panoramic ocean overlooks (`Z = -492, -586, -652`).
       - At `(-52, 72, -586)` (where the V5.3 matchbox hotel stood): builds the **Santa Monica Camera Obscura
         & Spanish-Revival Sunset Pergola Pavilion** (`X = -62..-34, Z = -602..-570, Y = 72..81`)—an open,
         articulated coastal arts & sunset viewpoint pavilion with arched colonnades, tiled terracotta pergola roofs,
         a domed astronomical Camera Obscura turret, and sunken reflection fountains (100% eliminating any boxy silhouette!).
       - At `(-52, 72, -490)` (South Bluff): builds the **Palisades Rose Garden, Totem Monument & Botanical Conservatory**.
       - At `(-52, 72, -652)` (North Bluff): builds the **Palisades Cliffside Amphitheater & Sunset Tea Pavilion**.
    """
    y_bluff = 72

    for z in range(-744, -463):
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

    for ov_z in (-490, -586, -652):
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

    bluff_trees = [
        (-32, -730, 'ornamental'), (-55, -725, 'birch_mix'), (-32, -708, 'oak_mix'),
        (-58, -680, 'ornamental'), (-32, -620, 'birch_mix'), (-58, -616, 'oak_mix'),
        (-32, -556, 'ornamental'), (-58, -554, 'birch_mix'), (-32, -520, 'oak_mix'),
        (-58, -464, 'ornamental'), (-110, -500, 'oak_mix'), (-110, -570, 'birch_mix'),
        (-110, -640, 'ornamental'), (-110, -710, 'oak_mix'), (-165, -500, 'birch_mix'),
        (-165, -580, 'ornamental'), (-165, -660, 'oak_mix'), (-230, -520, 'birch_mix'),
        (-230, -620, 'oak_mix'),
    ]
    for idx, (tx, tz, tst) in enumerate(bluff_trees):
        ty = _target_inland_bluff_elevation(c, tx, tz)
        build_custom_tree(c, tx, ty, tz, height=9, style=tst, seed=94000 + idx, max_radius=3)

def step17_main_urban_district_prototype(c: WorldCanvas):
    """
    Master Builder Entry Point for V5.4 Coastal Inland Zone (`X in [-320, 23], Z in [-800, -448]`):
    Replaces the postponed urban district & matchbox buildings with the custom-sculpted
    **Santa Monica Palisades Bluff Park**, **Pacific Coast Highway (PCH)**, **California Incline**,
    and **Camera Obscura & Rose Garden Overlooks**, while feathering terrain smoothly into the outer boundaries.
    """
    _bulldoze_and_sculpt_palisades_bluffs(c)
    _build_pch_and_california_incline(c)
    _build_palisades_bluff_park_and_overlooks(c)
