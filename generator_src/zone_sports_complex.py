"""
zone_sports_complex.py — North Z- Expansion: Grand Estate Sports Complex (V5.3)
===============================================================================
Extends the estate northward (Z- direction, Z in [-396, -252], X in [-224, 128])
beyond the North Championship Golf Course, separated by a 26-to-32 block Scenic
Parkland & Boulevard Buffer (Z = -282..-252) with two 7-block-wide grand connecting
boulevards, a continuous East Coastal Boulevard link at X = 98..103, and an
Olympic Fountain Plaza.

V5.3 Upgrades & Fixes:
  1. Enlarged Stadium & Sports Complex toward Z- (`Z = -396..-252`):
     - Track & Field Stadium expanded to `X = -220..-46, Z = -396..-283` (175 x 114 blocks,
       centered at `tcx = -128, tcz = -336`, straightaway `X = -162..-94` = 68 blocks).
  2. True 3-Block-Wide Running Lanes (`对齐到跑道每道3格的宽度`):
     - 5 championship lanes from `r = 19` to `r = 39` with lane pitch = `4` blocks
       (`1` block `smooth_quartz` white divider line at `r = 19, 23, 27, 31, 35, 39` +
       `3` full blocks of `red_terracotta` / `red_concrete` running surface per lane:
       `|TTT|CCC|TTT|CCC|TTT|`).
  3. Non-Overlapping North Grandstand & Elevated VIP Press Box (`修复 (-125, 70, -367) 看台与座位重叠`):
     - Lower 4-tier grandstand seating bowl occupies `Z = -387..-380` (`Y = 65..68`) with
       full unobstructed vertical headroom up to the roof (`Y = 75`).
     - Elevated VIP Press Box & Broadcast Suite (`X = -150..-106, Z = -394..-388, Y = 69..75`)
       is positioned strictly BEHIND Tier 3 on a solid `Y = 69` structural floor with its
       panoramic glass wall at `Z = -388, Y = 70..73`—zero overlap with lower seats!
  4. Crisp 5x7 7-Segment LED Scoreboard at `X = -210` (`修复 (-210, 65, -237/-327) 计分板数字镜像问题`):
     - Enlarged scoreboard screen (`X = -210, Z = -348..-324, Y = 72..78`) displaying
       properly-oriented 5-wide x 7-tall 7-segment digits (`8 : 2` viewed from East looking West,
       where Left = `+Z` South and Right = `-Z` North).
  5. Enlarged Outdoor Basketball Park (`Z = -388..-284`) & Indoor Sports Arena (`Z = -386..-286`).
"""

import math
from config import Y_BASE, MAT
from world_canvas import WorldCanvas
from arch_lib import (
    stair,
    place_double_door,
    build_illuminated_carpet_rug,
    build_curtain_wall,
    build_spiral_staircase, build_straight_stairs,
    build_vine_arch, build_lamppost,
    build_fountain,
    build_custom_tree, build_patio_umbrella,
    build_outdoor_sofa, build_outdoor_bar,
)

def _build_basketball_hoop(c: WorldCanvas, x: int, y_floor: int, z: int, facing: str = 'south', indoor: bool = False):
    """
    Builds an architectural voxel basketball hoop with padded support stanchion,
    tempered glass backboard (width 5, height 3), orange/red target rim, and cobweb net.
    """
    dx_f, dz_f = {'south': (0, 1), 'north': (0, -1), 'east': (1, 0), 'west': (-1, 0)}[facing]
    dx_b, dz_b = -dx_f, -dz_f

    if not indoor:
        px, pz = x + dx_b, z + dz_b
        c.fill(px, y_floor + 1, pz, px, y_floor + 2, pz, MAT['red_concrete'])
        c.fill(px, y_floor + 3, pz, px, y_floor + 5, pz, MAT['frame_dark'])
        c.set_block(x, y_floor + 4, z, MAT['frame_dark'])

    for w in range(-2, 3):
        bx = x + (w if dx_f == 0 else 0)
        bz = z + (w if dz_f == 0 else 0)
        for by in range(y_floor + 4, y_floor + 7):
            if abs(w) == 2 or by == y_floor + 6:
                c.set_block(bx, by, bz, MAT['wall_white'])
            elif w == 0 and by == y_floor + 4:
                c.set_block(bx, by, bz, 'minecraft:target')
            else:
                c.set_block(bx, by, bz, MAT['glass_clear'])

    rx, rz = x + dx_f, z + dz_f
    c.set_block(rx, y_floor + 4, rz, 'minecraft:smooth_red_sandstone_slab[type=top,waterlogged=false]')
    c.set_block(rx, y_floor + 3, rz, 'minecraft:cobweb')
    c.set_block(rx, y_floor + 7, rz, MAT['light_air'])

def _build_stadium_floodlight_tower(c: WorldCanvas, cx: int, y_base: int, cz: int, aim_dx: int, aim_dz: int):
    """
    Builds a 22-block-tall architectural stadium floodlight mast with a steel truss column
    and an angled high-luminance LED array at Y = y_base + 18..22.
    """
    c.fill(cx - 1, y_base, cz - 1, cx + 1, y_base + 1, cz + 1, MAT['stone_pol_and'])
    c.set_block(cx, y_base + 2, cz, MAT['wall_chiseled'])
    for y in range(y_base + 2, y_base + 19):
        c.set_block(cx, y, cz, MAT['frame_dark'] if y % 3 != 0 else MAT['iron_block'])
        if y % 4 == 0:
            c.set_block(cx + aim_dx, y, cz, MAT['iron_bars'])
            c.set_block(cx, y, cz + aim_dz, MAT['iron_bars'])

    for dy in range(18, 22):
        y = y_base + dy
        for w in range(-2, 3):
            lx = cx + (w if aim_dx == 0 else 0)
            lz = cz + (w if aim_dz == 0 else 0)
            c.set_block(lx - aim_dx, y, lz - aim_dz, MAT['frame_dark'])
            if abs(w) == 2 or dy == 21:
                c.set_block(lx, y, lz, MAT['iron_block'])
            else:
                c.set_block(lx, y, lz, MAT['light_sea'] if (w + dy) % 2 == 0 else MAT['light_pearl'])

def _build_Connecting_Boulevards_And_Plaza(c: WorldCanvas):
    """
    1. Scenic Buffer Belt (Z = -282..-252), Twin Grand Connecting Boulevards,
       Continuous East Coastal Avenue (X = 98..103, Z = -276..-216),
       East-West Spine Boulevard (X = -218..124, Z = -282..-276), and Central Olympic Fountain Plaza.
    """

    for x in range(-218, 125):
        in_ns_junc = (-38 <= x <= -32) or (22 <= x <= 28) or (98 <= x <= 103) or (-45 <= x <= -24)
        for z in range(-282, -275):
            if z in (-282, -276) and not in_ns_junc:
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if x % 6 == 0 else MAT['wall_quartz'])
                if x % 16 == 0:
                    build_lamppost(c, x, Y_BASE + 1, z, style='avenue')
            elif z == -279 and not in_ns_junc:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if x % 4 in (0, 1) else MAT['stone_pol_and'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])

    for x_center, z_south in [(-35, -250), (25, -252)]:
        for z in range(-276, z_south + 1):
            for dx in range(-3, 4):
                x = x_center + dx
                if abs(dx) == 3 and z > -276:
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['wall_quartz'])
                elif dx == 0 and z > -276:
                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if z % 3 == 0 else MAT['stone_dio'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
            if z in (-272, -264, -256):
                build_lamppost(c, x_center - 3, Y_BASE + 1, z, style='courtyard')
                build_lamppost(c, x_center + 3, Y_BASE + 1, z, style='courtyard')
        build_vine_arch(c, x_center, Y_BASE, -274, span=6, height=5, axis='x')
        build_vine_arch(c, x_center, Y_BASE, -258, span=6, height=5, axis='x')

    for z in range(-276, -215):
        for x in range(98, 104):
            if x in (98, 103):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'] if z % 6 == 0 else MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
            for hy_clear in range(Y_BASE + 1, Y_BASE + 4):
                c.set_block(x, hy_clear, z, 'minecraft:air')
        if z % 12 == 0:
            build_lamppost(c, 97, Y_BASE + 1, z, style='avenue')

    for z in range(-390, -282):
        for x in range(-45, -23):
            if x in (-45, -24) or z in (-390, -283):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
            elif (x + z) % 6 == 0 and x in (-43, -26):
                c.set_block(x, Y_BASE, z, MAT['light_ochre'])
            else:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'] if ((x // 3 + z // 3) % 2 == 0) else MAT['stone_dio'])

    build_fountain(c, -35, Y_BASE, -312, radius=5)
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            d2 = dx * dx + dz * dz
            if d2 <= 16:
                c.set_block(-35 + dx, Y_BASE, -342 + dz, MAT['stone_pol_and'] if d2 > 9 else MAT['wall_quartz'])
                if d2 <= 9:
                    c.set_block(-35 + dx, Y_BASE + 1, -342 + dz, MAT['slab_quartz_b'] if d2 > 4 else MAT['wall_chiseled'])
    c.fill(-35, Y_BASE + 2, -342, -35, Y_BASE + 5, -342, MAT['pillar_quartz'])
    c.fill(-36, Y_BASE + 6, -343, -34, Y_BASE + 6, -341, MAT['gold_block'])
    c.set_block(-35, Y_BASE + 7, -342, 'minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]')
    for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        c.set_block(-35 + dx, Y_BASE + 7, -342 + dz, MAT['light_ochre'])

    c.fill(-39, Y_BASE + 1, -375, -31, Y_BASE + 1, -373, MAT['wall_quartz'])
    c.fill(-36, Y_BASE + 2, -375, -34, Y_BASE + 2, -373, MAT['gold_block'])
    c.fill(-39, Y_BASE + 1, -374, -37, Y_BASE + 1, -374, MAT['iron_block'])
    c.fill(-33, Y_BASE + 1, -374, -31, Y_BASE + 1, -374, MAT['copper_block'])

    ring_specs = [
        (-41, 71, MAT['blue_concrete']),
        (-35, 71, MAT['wall_black']),
        (-29, 71, MAT['red_concrete']),
        (-38, 69, MAT['yellow_concrete']),
        (-32, 69, MAT['green_concrete']),
    ]
    c.fill(-43, Y_BASE + 1, -292, -43, Y_BASE + 8, -292, MAT['frame_dark'])
    c.fill(-27, Y_BASE + 1, -292, -27, Y_BASE + 8, -292, MAT['frame_dark'])
    c.fill(-43, Y_BASE + 8, -292, -27, Y_BASE + 8, -292, MAT['frame_dark'])
    for rcx, rcy, rmat in ring_specs:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if abs(dx) == 2 or abs(dy) == 2:
                    if not (abs(dx) == 2 and abs(dy) == 2):
                        c.set_block(rcx + dx, rcy + dy, -292, rmat)
        c.set_block(rcx, rcy, -292, MAT['light_air'])

def _build_Athletics_Track_And_Stadium(c: WorldCanvas):
    """
    2. Enlarged East-West Championship Athletics Track & Field Stadium (X = -220..-46, Z = -396..-283, Y = 64..86)
       - Standard 400m-proportion stadium oval oriented East-West (centered at tcx = -128, tcz = -336):
         * Straightaways along X = -162..-94 (length = 68 blocks)
         * Semicircular West & East turns centered at (-162, -336) and (-94, -336)
         * True 3-Block-Wide Running Lanes (`对齐到跑道每道3格的宽度`):
           Inner kerb line at r_int = 19, outer kerb line at r_int = 39 (5 lanes with pitch = 4 blocks:
           1-block white `wall_quartz` divider lines at r_int in (19, 23, 27, 31, 35, 39) and
           3-block-wide `red_terracotta` / `red_concrete` running surfaces at r_int in
           20..22, 24..26, 28..30, 32..34, 36..38 -> `|TTT|CCC|TTT|CCC|TTT|`).
         * Outer track curb at r_int = 40 (X = -202..-54, Z = -376..-296).
       - Regulation-proportion 68 x 34 East-West Soccer Pitch infield (X = -162..-94, Z = -353..-319)
       - Long Jump sand pit & takeoff board in the West D-zone (X = -173..-168, Z = -346..-326)
       - Non-Overlapping North Grandstand (Z = -387..-380) & Elevated Rear VIP Press Box (Z = -394..-388)
       - Crisp 5x7 7-Segment West Scoreboard Tower at X = -212..-210, Z = -350..-322 (fixing Issue 3)
    """
    tcx, tcz = -128, -336
    straight_half_x = 34

    for z in range(-396, -282):
        for x in range(-220, -45):
            if x in (-220, -46) or z in (-396, -283):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                if (x + z) % 8 == 0:
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
            c.fill(x, Y_BASE + 1, z, x, Y_BASE + 16, z, 'minecraft:air')

    for z in range(-378, -294):
        dz = abs(z - tcz)
        for x in range(-204, -52):
            dx_seg = 0.0
            if x < tcx - straight_half_x:
                dx_seg = (tcx - straight_half_x) - x
            elif x > tcx + straight_half_x:
                dx_seg = x - (tcx + straight_half_x)
            r = math.hypot(dx_seg, dz)
            r_int = int(round(r))

            if r_int < 19:

                stripe = ((x - (-162)) // 5) % 2 == 0
                if (x % 8 == 0 and z % 8 == 0):
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'])
                    c.set_block(x, Y_BASE + 1, z, MAT['moss_carpet'] if stripe else MAT['carpet_green'])
                else:
                    c.set_block(x, Y_BASE, z, MAT['moss_block'] if stripe else MAT['grass_block'])
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
            elif 19 <= r_int <= 39:
                offset = r_int - 19
                if offset % 4 == 0:

                    c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
                else:

                    lane_idx = offset // 4
                    c.set_block(x, Y_BASE - 1, z, MAT['light_ochre'] if (x + z) % 8 == 0 else MAT['stone'])
                    c.set_block(x, Y_BASE, z, 'minecraft:red_terracotta' if lane_idx % 2 == 0 else MAT['red_concrete'])
                    c.set_block(x, Y_BASE + 1, z, 'minecraft:air')
            elif r_int == 40:

                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
                c.set_block(x, Y_BASE + 1, z, MAT['slab_quartz_b'])

    for lane in range(5):
        lz_start = -316 + lane * 4
        for w_l in range(3):
            c.set_block(-94, Y_BASE, lz_start + w_l, MAT['wall_white'])
        c.set_block(-163, Y_BASE + 1, lz_start + 1, stair('polished_blackstone_brick', 'east', 'bottom'))

    px1, px2, pz1, pz2 = -161, -95, -353, -319
    for x in range(px1, px2 + 1):
        c.set_block(x, Y_BASE, pz1, MAT['wall_white'])
        c.set_block(x, Y_BASE, pz2, MAT['wall_white'])
        c.set_block(x, Y_BASE + 1, pz1, 'minecraft:air')
        c.set_block(x, Y_BASE + 1, pz2, 'minecraft:air')
    for z in range(pz1, pz2 + 1):
        c.set_block(px1, Y_BASE, z, MAT['wall_white'])
        c.set_block(px2, Y_BASE, z, MAT['wall_white'])
        c.set_block(tcx, Y_BASE, z, MAT['wall_white'])
        c.set_block(px1, Y_BASE + 1, z, 'minecraft:air')
        c.set_block(px2, Y_BASE + 1, z, 'minecraft:air')
        c.set_block(tcx, Y_BASE + 1, z, 'minecraft:air')

    for dx in range(-6, 7):
        for dz in range(-6, 7):
            d = math.hypot(dx, dz)
            if 5.4 <= d <= 6.4 or d < 0.8:
                c.set_block(tcx + dx, Y_BASE, tcz + dz, MAT['wall_white'])
                c.set_block(tcx + dx, Y_BASE + 1, tcz + dz, 'minecraft:air')

    for z in range(-345, -326):
        c.set_block(-150, Y_BASE, z, MAT['wall_white'])
        c.set_block(-106, Y_BASE, z, MAT['wall_white'])
        c.set_block(-150, Y_BASE + 1, z, 'minecraft:air')
        c.set_block(-106, Y_BASE + 1, z, 'minecraft:air')
    for x in range(-161, -149):
        c.set_block(x, Y_BASE, -345, MAT['wall_white'])
        c.set_block(x, Y_BASE, -327, MAT['wall_white'])
        c.set_block(x, Y_BASE + 1, -345, 'minecraft:air')
        c.set_block(x, Y_BASE + 1, -327, 'minecraft:air')
    for x in range(-106, -94):
        c.set_block(x, Y_BASE, -345, MAT['wall_white'])
        c.set_block(x, Y_BASE, -327, MAT['wall_white'])
        c.set_block(x, Y_BASE + 1, -345, 'minecraft:air')
        c.set_block(x, Y_BASE + 1, -327, 'minecraft:air')

    c.set_block(-153, Y_BASE, tcz, MAT['wall_white'])
    c.set_block(-103, Y_BASE, tcz, MAT['wall_white'])

    for gx, net_x in [(-161, -162), (-95, -94)]:
        for y in range(Y_BASE + 1, Y_BASE + 4):
            c.set_block(gx, y, -340, MAT['pillar_quartz'])
            c.set_block(gx, y, -332, MAT['pillar_quartz'])
            c.set_block(net_x, y, -340, 'minecraft:cobweb')
            c.set_block(net_x, y, -332, 'minecraft:cobweb')
        for z in range(-340, -331):
            c.set_block(gx, Y_BASE + 3, z, MAT['pillar_quartz_z'])
            c.set_block(net_x, Y_BASE + 3, z, 'minecraft:cobweb')
            for y in range(Y_BASE + 1, Y_BASE + 3):
                c.set_block(net_x, y, z, 'minecraft:cobweb')

    for cx_f, cz_f in [(px1, pz1), (px2, pz1), (px1, pz2), (px2, pz2)]:
        c.set_block(cx_f, Y_BASE + 1, cz_f, 'minecraft:birch_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        c.set_block(cx_f, Y_BASE + 2, cz_f, MAT['yellow_wool'])

    for z in range(-346, -335):
        c.set_block(-168, Y_BASE, z, 'minecraft:red_terracotta')
        c.set_block(-167, Y_BASE, z, 'minecraft:red_terracotta')
    c.fill(-168, Y_BASE, -335, -167, Y_BASE, -335, MAT['wall_white'])
    for z in range(-334, -326):
        for x in range(-169, -165):
            if x in (-169, -166) or z == -327:
                c.set_block(x, Y_BASE, z, MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE, z, 'minecraft:sand')
                c.set_block(x, Y_BASE + 1, z, 'minecraft:air')

    for x in range(-170, -85):
        is_left_stair = (-170 <= x <= -165)
        is_right_stair = (-91 <= x <= -86)
        is_center_aisle = (-129 <= x <= -127)
        for tier in range(4):
            sz_seat = -380 - tier * 2
            sy_seat = Y_BASE + 1 + tier
            c.fill(x, Y_BASE + 1, sz_seat - 1, x, sy_seat - 1, sz_seat, MAT['stone_pol_and'])
            if is_left_stair or is_right_stair or is_center_aisle:
                c.set_block(x, sy_seat, sz_seat, stair('smooth_quartz', 'north', 'bottom'))
                c.set_block(x, sy_seat, sz_seat - 1, MAT['light_ochre'] if (tier % 2 == 1 and x in (-168, -128, -88)) else MAT['wall_quartz'])
            else:
                seat_mat = 'smooth_quartz' if (tier + x) % 3 == 0 else ('prismarine_brick' if tier % 2 == 0 else 'dark_prismarine')
                c.set_block(x, sy_seat, sz_seat, stair(seat_mat, 'south', 'bottom'))
                c.set_block(x, sy_seat, sz_seat - 1, MAT['wall_quartz'])

        if is_left_stair or is_right_stair:
            if x in (-170, -86):

                c.set_block(x, Y_BASE + 5, -387, MAT['wall_quartz'])
            else:
                c.set_block(x, Y_BASE + 5, -387, stair('smooth_quartz', 'north', 'bottom'))
                c.fill(x, Y_BASE + 6, -387, x, Y_BASE + 9, -387, 'minecraft:air')

        c.fill(x, Y_BASE + 1, -394, x, Y_BASE + 4, -388, MAT['stone_pol_and'])
        c.fill(x, Y_BASE + 5, -394, x, Y_BASE + 5, -388, MAT['wall_quartz'])
        if (is_left_stair or is_right_stair) and x in (-168, -88):
            c.set_block(x, Y_BASE + 5, -391, MAT['light_ochre'])

        c.fill(x, Y_BASE + 1, -395, x, Y_BASE + 10, -395, MAT['wall_white'])
        if x % 8 == 0 or x in (-170, -86):
            c.fill(x, Y_BASE + 1, -395, x, Y_BASE + 11, -395, MAT['frame_dark'])
            c.fill(x, Y_BASE + 11, -395, x, Y_BASE + 11, -379, MAT['frame_dark'])
        c.fill(x, Y_BASE + 10, -395, x, Y_BASE + 10, -379, MAT['slab_quartz_t'])
        c.fill(x, Y_BASE + 11, -395, x, Y_BASE + 11, -379, MAT['slab_deep_b'])
        if x % 4 == 0:
            c.set_block(x, Y_BASE + 10, -383, MAT['light_sea'])
            c.set_block(x, Y_BASE + 10, -391, MAT['light_ochre'])

    for z_side in range(-394, -387):
        c.set_block(-170, Y_BASE + 6, z_side, MAT['pane_cyan'])
        c.set_block(-86, Y_BASE + 6, z_side, MAT['pane_cyan'])

    for x in range(-150, -105):

        if x in (-150, -106):
            for z_pb in range(-394, -387):
                for y_pb in range(Y_BASE + 6, Y_BASE + 10):
                    if z_pb in (-392, -391, -390) and y_pb <= Y_BASE + 8:
                        c.set_block(x, y_pb, z_pb, 'minecraft:air')
                    else:
                        c.set_block(x, y_pb, z_pb, MAT['frame_dark'] if z_pb in (-394, -388) else MAT['glass_clear'])
            continue

        c.set_block(x, Y_BASE + 5, -388, MAT['wall_quartz'])
        c.set_block(x, Y_BASE + 6, -388, MAT['glass_cyan'])
        c.set_block(x, Y_BASE + 7, -388, MAT['glass_clear'])
        c.set_block(x, Y_BASE + 8, -388, MAT['glass_clear'])
        c.set_block(x, Y_BASE + 9, -388, MAT['frame_dark'])

        c.set_block(x, Y_BASE + 6, -389, MAT['slab_quartz_t'])
        if x % 3 == 0:
            c.set_block(x, Y_BASE + 6, -390, stair('dark_oak', 'north', 'bottom'))
            c.set_block(x, Y_BASE + 5, -390, MAT['light_ochre'])

    for x_wing in list(range(-164, -150)) + list(range(-105, -91)):
        c.set_block(x_wing, Y_BASE + 6, -388, MAT['pane_cyan'])

    for z_leg in (-346, -326):
        c.fill(-212, Y_BASE + 1, z_leg - 1, -211, Y_BASE + 6, z_leg + 1, MAT['frame_dark'])
    c.fill(-212, Y_BASE + 7, -350, -210, Y_BASE + 16, -322, MAT['wall_black'])
    c.fill(-210, Y_BASE + 8, -348, -210, Y_BASE + 14, -324, MAT['deepslate_tiles'])

    for z_sc in range(-350, -321, 2):
        c.set_block(-210, Y_BASE + 16, z_sc, MAT['slab_quartz_b'])

    for py in range(8, 15):
        for pz in range(-332, -327):
            if py in (8, 11, 14) or pz in (-332, -328):
                c.set_block(-210, Y_BASE + py, pz, MAT['light_sea'])

    c.set_block(-210, Y_BASE + 10, -336, MAT['light_pearl'])
    c.set_block(-210, Y_BASE + 12, -336, MAT['light_pearl'])

    for pz in range(-344, -339):
        c.set_block(-210, Y_BASE + 14, pz, MAT['light_ochre'])
        c.set_block(-210, Y_BASE + 11, pz, MAT['light_ochre'])
        c.set_block(-210, Y_BASE + 8, pz, MAT['light_ochre'])
    for py_ur in (12, 13):
        c.set_block(-210, Y_BASE + py_ur, -344, MAT['light_ochre'])
    for py_ll in (9, 10):
        c.set_block(-210, Y_BASE + py_ll, -340, MAT['light_ochre'])

    _build_stadium_floodlight_tower(c, -206, Y_BASE, -380, 1, 1)
    _build_stadium_floodlight_tower(c, -52, Y_BASE, -380, -1, 1)
    _build_stadium_floodlight_tower(c, -206, Y_BASE, -290, 1, -1)
    _build_stadium_floodlight_tower(c, -52, Y_BASE, -290, -1, -1)

def _build_Outdoor_Basketball_Park(c: WorldCanvas):
    """
    3. Enlarged Outdoor Basketball Park & Streetball Courts (X = -22..38, Z = -388..-284, Y = 64..76)
       - Court A (West Full Court): X = -17..3, Z = -352..-312 (center X = -7, Z = -332)
       - Court B (East Full Court): X = 13..33, Z = -352..-312 (center X = 23, Z = -332)
       - Enlarged North 3x3 Streetball & Dunk Contest Arena: X = -10..26, Z = -384..-358
       - South Lounge & Bleachers: X = -16..32, Z = -302..-288
    """
    for z in range(-388, -283):
        for x in range(-22, 39):
            if x in (-22, 38) or z in (-388, -284):
                c.set_block(x, Y_BASE, z, MAT['stone_pol_and'])
                if (x + z) % 4 == 0 and not (-338 <= z <= -326 or (z == -284 and -6 <= x <= 22)):
                    c.set_block(x, Y_BASE + 1, z, MAT['iron_bars'])
                    c.set_block(x, Y_BASE + 2, z, MAT['iron_bars'])
            else:
                c.set_block(x, Y_BASE, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['stone_pol_and'])
            c.fill(x, Y_BASE + 3, z, x, Y_BASE + 12, z, 'minecraft:air')

    def paint_full_court(ccx: int, primary_mat: str, key_mat: str):
        x1, x2 = ccx - 10, ccx + 10
        z1, z2 = -352, -312
        cz = -332
        for z in range(z1, z2 + 1):
            for x in range(x1, x2 + 1):
                is_border = (x in (x1, x2) or z in (z1, z2) or z == cz)
                d_center = math.hypot(x - ccx, z - cz)
                is_center_ring = (3.0 <= d_center <= 4.0)
                in_n_key = (abs(x - ccx) <= 3 and z1 <= z <= z1 + 7)
                in_s_key = (abs(x - ccx) <= 3 and z2 - 7 <= z <= z2)
                is_key_line = ((abs(x - ccx) == 3 and (z1 <= z <= z1 + 7 or z2 - 7 <= z <= z2)) or
                               (abs(x - ccx) <= 3 and z in (z1 + 7, z2 - 7)))
                d_n_hoop = math.hypot(x - ccx, z - (z1 + 2))
                d_s_hoop = math.hypot(x - ccx, z - (z2 - 2))
                is_3pt = ((8.0 <= d_n_hoop <= 9.0 and z >= z1 + 2) or
                          (8.0 <= d_s_hoop <= 9.0 and z <= z2 - 2))

                if is_border or is_center_ring or is_key_line or is_3pt:
                    c.set_block(x, Y_BASE, z, MAT['wall_white'])
                elif d_center < 3.0 or in_n_key or in_s_key:
                    c.set_block(x, Y_BASE, z, MAT['light_sea'] if (x + z) % 5 == 0 else key_mat)
                else:
                    c.set_block(x, Y_BASE, z, MAT['light_ochre'] if (x % 6 == 0 and z % 6 == 0) else primary_mat)
                c.set_block(x, Y_BASE + 1, z, 'minecraft:air')

        _build_basketball_hoop(c, ccx, Y_BASE, z1 - 1, facing='south', indoor=False)
        _build_basketball_hoop(c, ccx, Y_BASE, z2 + 1, facing='north', indoor=False)

    paint_full_court(-7, MAT['cyan_concrete'], MAT['orange_concrete'])
    paint_full_court(23, MAT['blue_concrete'], MAT['yellow_concrete'])

    for z in range(-349, -314):
        if z in (-345, -332, -319):
            build_lamppost(c, 8, Y_BASE + 1, z, style='avenue')
        elif -341 <= z <= -335 or -329 <= z <= -323:
            c.set_block(7, Y_BASE + 1, z, stair('smooth_quartz', 'west', 'bottom'))
            c.set_block(9, Y_BASE + 1, z, stair('smooth_quartz', 'east', 'bottom'))
        elif z in (-343, -321):
            c.set_block(8, Y_BASE + 1, z, 'minecraft:water_cauldron[level=3]')

    for z in range(-380, -359):
        for x in range(-4, 21):
            d_3pt = math.hypot(x - 8, z - (-378))
            if x in (-4, 20) or z in (-380, -360) or (8.5 <= d_3pt <= 9.5):
                c.set_block(x, Y_BASE, z, MAT['wall_white'])
            elif abs(x - 8) <= 3 and z <= -372:
                c.set_block(x, Y_BASE, z, MAT['red_concrete'])
            else:
                c.set_block(x, Y_BASE, z, MAT['deepslate_tiles'])
    _build_basketball_hoop(c, 8, Y_BASE, -381, facing='south', indoor=False)

    for x in range(-16, 33):
        if -4 <= x <= 20:
            for tier, tz in enumerate([-299, -297, -295]):
                sy = Y_BASE + 1 + tier
                c.fill(x, Y_BASE + 1, tz, x, sy - 1, tz, MAT['stone_pol_and'])
                c.set_block(x, sy, tz, stair('smooth_quartz' if x % 2 == 0 else 'dark_oak', 'north', 'bottom'))
            c.fill(x, Y_BASE + 6, -300, x, Y_BASE + 6, -294, MAT['slab_quartz_t'])
            if x in (-4, 8, 20):
                c.fill(x, Y_BASE + 1, -294, x, Y_BASE + 6, -294, MAT['frame_dark'])
                c.set_block(x, Y_BASE + 5, -297, MAT['light_ochre'])
    build_patio_umbrella(c, -12, Y_BASE, -296)
    build_patio_umbrella(c, 28, Y_BASE, -296)

def _build_Indoor_Sports_Arena_And_Natatorium(c: WorldCanvas):
    """
    4. Enlarged Multi-Story Indoor Sports Arena, Natatorium & Fitness Center (X = 42..124, Z = -386..-286, Y = 60..80)
    """
    ax1, ax2, az1, az2 = 42, 124, -386, -286
    y_1f = Y_BASE
    y_2f = Y_BASE + 7
    y_eave = Y_BASE + 13

    c.fill(ax1, y_1f - 3, az1, ax2, y_1f, az2, MAT['stone_pol_and'])
    c.fill(ax1 + 1, y_1f + 1, az1 + 1, ax2 - 1, y_eave + 3, az2 - 1, 'minecraft:air')

    for y in range(y_1f + 1, y_eave):
        for x in range(ax1, ax2 + 1):
            c.set_block(x, y, az1, MAT['wall_white'])
            c.set_block(x, y, az2, MAT['wall_white'])
        for z in range(az1, az2 + 1):
            c.set_block(ax1, y, z, MAT['wall_white'])
            c.set_block(ax2, y, z, MAT['wall_white'])

    for x in range(ax1, ax2 + 1, 8):
        c.fill(x, y_1f + 1, az1, x, y_eave, az1, MAT['frame_dark'])
        c.fill(x, y_1f + 1, az2, x, y_eave, az2, MAT['frame_dark'])
    for z in range(az1, az2 + 1, 8):
        c.fill(ax1, y_1f + 1, z, ax1, y_eave, z, MAT['frame_dark'])
        c.fill(ax2, y_1f + 1, z, ax2, y_eave, z, MAT['frame_dark'])

    build_curtain_wall(c, ax1 + 3, y_1f + 1, az2, ax2 - 3, y_2f - 1, az2,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=5)
    build_curtain_wall(c, ax1 + 3, y_2f + 1, az2, ax2 - 3, y_eave - 1, az2,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=5)
    build_curtain_wall(c, ax1 + 3, y_1f + 1, az1, ax2 - 3, y_eave - 1, az1,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=5)
    build_curtain_wall(c, ax1, y_1f + 1, az1 + 3, ax1, y_eave - 1, az2 - 3,
                       MAT['glass_clear'], MAT['glass_black'], MAT['frame_dark'], bay_width=5)
    build_curtain_wall(c, ax2, y_1f + 1, az1 + 3, ax2, y_eave - 1, az2 - 3,
                       MAT['glass_clear'], MAT['glass_cyan'], MAT['frame_dark'], bay_width=5)

    x_mid = (ax1 + ax2) / 2.0
    half_span = (ax2 - ax1) / 2.0
    for z in range(az1 - 1, az2 + 2):
        is_truss_z = ((z - az1) % 8 == 0)
        for x in range(ax1 - 1, ax2 + 2):
            u = abs(x - x_mid) / half_span
            arch_h = int(round(3.0 * max(0.0, 1.0 - u * u)))
            ry = y_eave + arch_h
            if x in (ax1 - 1, ax2 + 1) or z in (az1 - 1, az2 + 1):
                c.set_block(x, y_eave, z, MAT['slab_quartz_b'])
                continue
            in_skylight = ((64 <= x <= 74 or 94 <= x <= 104) and (az1 + 6 <= z <= az2 - 6) and not is_truss_z)
            if in_skylight:
                c.set_block(x, ry, z, MAT['glass_cyan'] if (x + z) % 2 == 0 else MAT['glass_clear'])
            elif is_truss_z:
                c.set_block(x, ry, z, MAT['frame_dark'])
                if x % 4 == 0 and ax1 + 2 <= x <= ax2 - 2:
                    c.set_block(x, ry - 1, z, MAT['light_sea'])
            else:
                c.set_block(x, ry, z, MAT['wall_white'] if (x // 4) % 2 == 0 else MAT['wall_quartz'])

    for z in range(az1 + 1, az2):
        for x in range(ax1 + 1, ax2):
            in_south_mezz = (z >= -302)
            in_north_mezz = (z <= -376)
            in_west_mezz = (x <= 50)
            in_east_mezz = (x >= 114)
            if in_south_mezz or in_north_mezz or in_west_mezz or in_east_mezz:
                c.set_block(x, y_2f, z, MAT['light_ochre'] if (x % 5 == 0 and z % 5 == 0) else MAT['wood_dark'])
                if ((z == -302 and 50 <= x <= 114) or
                    (z == -376 and 50 <= x <= 114) or
                    (x == 50 and -376 <= z <= -302) or
                    (x == 114 and -376 <= z <= -302)):
                    c.set_block(x, y_2f, z, MAT['wall_quartz'])
                    c.set_block(x, y_2f + 1, z, MAT['pane_cyan'])

    for z in range(-303, az2):
        for x in range(ax1 + 1, ax2):
            if (x + z) % 5 == 0:
                c.set_block(x, y_1f, z, MAT['light_ochre'])
            else:
                c.set_block(x, y_1f, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['stone_dio'])

    icx, icz = 70, -329
    ix1, ix2, iz1, iz2 = 58, 82, -350, -308
    for z in range(-375, -304):
        for x in range(51, 93):
            if z < -353:

                if x in (56, 84) or z in (-373, -356) or z == -364:
                    c.set_block(x, y_1f, z, MAT['wall_quartz'])
                else:
                    c.set_block(x, y_1f, z, MAT['light_sea'] if (x % 6 == 0 and z % 6 == 0) else MAT['wood_birch'])
                continue
            if x < ix1 or x > ix2 or z < iz1 or z > iz2:
                c.set_block(x, y_1f, z, MAT['light_ochre'] if (x % 6 == 0 and z % 6 == 0) else MAT['wood_dark'])
                continue
            is_line = (x in (ix1, ix2) or z in (iz1, iz2) or z == icz)
            d_c = math.hypot(x - icx, z - icz)
            in_key_n = (abs(x - icx) <= 3 and iz1 <= z <= iz1 + 7)
            in_key_s = (abs(x - icx) <= 3 and iz2 - 7 <= z <= iz2)
            is_key_edge = ((abs(x - icx) == 3 and (iz1 <= z <= iz1 + 7 or iz2 - 7 <= z <= iz2)) or
                           (abs(x - icx) <= 3 and z in (iz1 + 7, iz2 - 7)))
            d_3n = math.hypot(x - icx, z - (iz1 + 2))
            d_3s = math.hypot(x - icx, z - (iz2 - 2))
            is_3pt = ((8.5 <= d_3n <= 9.5 and z >= iz1 + 2) or (8.5 <= d_3s <= 9.5 and z <= iz2 - 2))

            if is_line or (3.2 <= d_c <= 4.2) or is_key_edge or is_3pt:
                c.set_block(x, y_1f, z, MAT['wall_quartz'])
            elif d_c < 3.2 or in_key_n or in_key_s:
                c.set_block(x, y_1f, z, MAT['light_sea'] if (x + z) % 4 == 0 else MAT['cyan_concrete'])
            else:
                c.set_block(x, y_1f, z, MAT['light_ochre'] if (x % 6 == 0 and z % 6 == 0) else (MAT['wood_birch'] if (x + z) % 2 == 0 else MAT['wood_warm']))

    for x_bm in range(58, 83):
        c.set_block(x_bm, y_1f + 1, -364, MAT['iron_bars'])
        c.set_block(x_bm, y_1f + 2, -364, MAT['carpet_white'])

    for z in range(-346, -311):
        if z in (-346, -329, -312):
            continue
        for t_idx in range(3):
            wx_b = 55 - t_idx
            wy_b = y_1f + 1 + t_idx
            c.fill(wx_b, y_1f + 1, z, wx_b, wy_b - 1, z, MAT['wood_dark'])
            c.set_block(wx_b, wy_b, z, stair('spruce' if t_idx % 2 == 0 else 'smooth_quartz', 'east', 'bottom'))
            ex_b = 85 + t_idx
            c.fill(ex_b, y_1f + 1, z, ex_b, wy_b - 1, z, MAT['wood_dark'])
            c.set_block(ex_b, wy_b, z, stair('spruce' if t_idx % 2 == 0 else 'smooth_quartz', 'west', 'bottom'))

    for z in range(-375, -304):
        for x in range(93, 114):
            if 95 <= x <= 110 and -370 <= z <= -310:
                is_lane_div = (x in (98, 102, 106))
                c.set_block(x, y_1f - 3, z, MAT['light_sea'] if (x + z) % 3 == 0 else (MAT['pool_deep_1'] if is_lane_div else MAT['pool_shallow_1']))
                c.set_block(x, y_1f - 2, z, MAT['water'])
                c.set_block(x, y_1f - 1, z, MAT['water'])
                if is_lane_div and -368 <= z <= -312:
                    c.set_block(x, y_1f, z, MAT['water'])
                    c.set_block(x, y_1f + 1, z, MAT['carpet_red'] if z % 2 == 0 else MAT['carpet_white'])
                else:
                    c.set_block(x, y_1f, z, MAT['water'])
            else:
                c.set_block(x, y_1f, z, MAT['light_sea'] if (x + z) % 5 == 0 else MAT['wall_quartz'])

    for sx_blk in (96, 100, 104, 108):
        c.set_block(sx_blk, y_1f + 1, -309, stair('smooth_quartz', 'north', 'top'))
        c.set_block(sx_blk, y_1f + 2, -309, MAT['carpet_cyan'])

    for z in range(-372, -307):
        if -331 <= z <= -327 or -362 <= z <= -358:
            continue
        c.set_block(91, y_1f + 1, z, MAT['wall_quartz'])
        c.set_block(91, y_1f + 2, z, MAT['pane_cyan'])

    build_spiral_staircase(c, 54, y_1f + 1, y_2f, -294, radius=2, start_sector=2, clockwise=True)
    for x_r in range(51, 58):
        c.set_block(x_r, y_2f + 1, -297, MAT['pane_cyan'])
    for z_r in range(-297, -293):
        c.set_block(51, y_2f + 1, z_r, MAT['pane_cyan'])
    for z_r in range(-297, -294):
        c.set_block(57, y_2f + 1, z_r, MAT['pane_cyan'])

    build_straight_stairs(c, 116, y_1f + 1, -294, width=3, height=y_2f - y_1f,
                          direction='north', stair_prefix='smooth_quartz', hidden_lights=True)

    _build_basketball_hoop(c, icx, y_1f, iz1, facing='south', indoor=True)
    _build_basketball_hoop(c, icx, y_1f, iz2, facing='north', indoor=True)

    for cx_j in (68, 72):
        for cz_j in (-331, -327):
            c.fill(cx_j, y_2f + 5, cz_j, cx_j, y_eave + 2, cz_j, MAT['chain_y'])
    for y_j in range(y_2f + 1, y_2f + 5):
        for x_j in range(67, 74):
            for z_j in range(-332, -325):
                if x_j in (67, 73) or z_j in (-332, -326):
                    if y_j in (y_2f + 1, y_2f + 4):
                        c.set_block(x_j, y_j, z_j, MAT['frame_dark'])
                    else:
                        c.set_block(x_j, y_j, z_j, MAT['light_sea'] if (x_j + z_j + y_j) % 2 == 0 else MAT['light_ochre'])
                elif y_j == y_2f + 1:
                    c.set_block(x_j, y_j, z_j, MAT['light_sea'])

    build_illuminated_carpet_rug(c, 66, y_1f, -299, 78, -290, MAT['carpet_cyan'], MAT['carpet_white'])
    build_outdoor_bar(c, 84, y_1f, -296, length=8)
    build_outdoor_sofa(c, 96, y_1f, -295, length=6, facing='north')
    for tx_p, t_mat in [(68, MAT['gold_block']), (72, MAT['diamond_block']), (76, MAT['emerald_block'])]:
        c.set_block(tx_p, y_1f + 1, -298, MAT['wall_chiseled'])
        c.set_block(tx_p, y_1f + 2, -298, t_mat)
        c.set_block(tx_p, y_1f + 3, -298, MAT['end_rod_up'])
        c.set_block(tx_p, y_1f + 4, -298, MAT['glass_clear'])

    for ttx in (66, 76):
        for dx in range(3):
            for dz in range(5):
                c.set_block(ttx + dx, y_2f + 1, -297 + dz, MAT['slab_quartz_t'])
                c.set_block(ttx + dx, y_2f + 2, -297 + dz, MAT['carpet_white'] if dz == 2 else MAT['carpet_blue'])
        c.set_block(ttx + 1, y_2f + 1, -295, MAT['light_ochre'])

    for tx_tm in range(60, 105, 6):
        c.set_block(tx_tm, y_2f + 1, -379, MAT['carpet_black'])
        c.set_block(tx_tm, y_2f + 1, -380, MAT['carpet_black'])
        c.set_block(tx_tm, y_2f + 1, -381, stair('polished_deepslate', 'south', 'bottom'))
        c.set_block(tx_tm, y_2f + 2, -381, MAT['pane_black'])

    build_illuminated_carpet_rug(c, 86, y_2f, -299, 106, -291, MAT['carpet_lgray'], MAT['carpet_white'])
    build_outdoor_sofa(c, 88, y_2f, -297, length=6, facing='north')
    build_outdoor_sofa(c, 98, y_2f, -297, length=6, facing='north')

    place_double_door(c, 71, y_1f + 1, az2, 'dark_oak', 'north', 'true')
    place_double_door(c, 101, y_1f + 1, az2, 'dark_oak', 'north', 'true')
    place_double_door(c, ax1, y_1f + 1, -332, 'dark_oak', 'east', 'true')
    place_double_door(c, ax2, y_1f + 1, -296, 'dark_oak', 'west', 'true')

    for dx_d in (71, 72, 101, 102):
        c.fill(dx_d, y_1f + 1, az2 - 2, dx_d, y_1f + 3, az2 - 1, 'minecraft:air')
        c.fill(dx_d, y_1f + 1, az2 + 1, dx_d, y_1f + 3, az2 + 3, 'minecraft:air')
    for dz_d in (-332, -331):
        c.fill(ax1 - 3, y_1f + 1, dz_d, ax1 - 1, y_1f + 3, dz_d, 'minecraft:air')
        c.fill(ax1 + 1, y_1f + 1, dz_d, ax1 + 3, y_1f + 3, dz_d, 'minecraft:air')
    for dz_e in (-296, -295):
        c.fill(ax2 - 3, y_1f + 1, dz_e, ax2 - 1, y_1f + 3, dz_e, 'minecraft:air')
        c.fill(ax2 + 1, y_1f + 1, dz_e, ax2 + 3, y_1f + 3, dz_e, 'minecraft:air')

def step15_north_sports_complex(c: WorldCanvas):
    """
    Master Builder Entry Point for Expansion 9 (V5.3):
    Enlarged North Sports Complex (East-West 400m-proportion Track & Field Stadium with 3-block lanes,
    Non-overlapping North Grandstand & VIP Press Box, Crisp 7-Segment Scoreboard, Outdoor Basketball Park,
    and Multi-Story Indoor Sports Arena & Natatorium) in Z in [-396, -252], X in [-224, 128].
    """
    _build_Connecting_Boulevards_And_Plaza(c)
    _build_Athletics_Track_And_Stadium(c)
    _build_Outdoor_Basketball_Park(c)
    _build_Indoor_Sports_Arena_And_Natatorium(c)

    sports_trees = [
        (-210, -272, 'ornamental'), (-175, -272, 'birch_mix'), (-140, -272, 'oak_mix'),
        (-105, -272, 'ornamental'), (-70, -272, 'birch_mix'), (-50, -272, 'ornamental'),
        (-12, -272, 'birch_mix'), (10, -272, 'ornamental'),
        (48, -272, 'oak_mix'), (85, -272, 'birch_mix'), (118, -272, 'ornamental'),
        (-216, -392, 'spruce_mix'), (-180, -394, 'ornamental'), (-76, -394, 'birch_mix'),
        (-35, -392, 'birch_mix'), (8, -392, 'ornamental'), (60, -392, 'oak_mix'), (105, -392, 'birch_mix'),
    ]
    for idx, (tx, tz, tst) in enumerate(sports_trees):
        build_custom_tree(c, tx, Y_BASE, tz, height=9, style=tst, seed=202650 + idx, max_radius=2)
