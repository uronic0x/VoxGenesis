import math, random

from config import MAT as _CFG_MAT, SOFT_FLOWERS as _CFG_FLOWERS, CORAL_BLOCKS
MAT = {**_CFG_MAT}
SOFT_FLOWERS = list(_CFG_FLOWERS)

def stair(mat_prefix, facing='north', half='bottom', shape='straight'):
    return f"minecraft:{mat_prefix}_stairs[facing={facing},half={half},shape={shape},waterlogged=false]"

def trapdoor(mat_prefix, facing='north', half='bottom', open_state='false'):
    return f"minecraft:{mat_prefix}_trapdoor[facing={facing},half={half},open={open_state},powered=false,waterlogged=false]"

def place_bed(c, x_foot, y, z_foot, facing='north', color='white'):
    dx, dz = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}[facing]
    xh, zh = x_foot + dx, z_foot + dz
    c.set_block(x_foot, y, z_foot, f"minecraft:{color}_bed[facing={facing},occupied=false,part=foot]",
                {'id': ('string', 'minecraft:bed'), 'x': ('int', x_foot), 'y': ('int', y), 'z': ('int', z_foot), 'keepPacked': ('byte', 0)})
    c.set_block(xh, y, zh, f"minecraft:{color}_bed[facing={facing},occupied=false,part=head]",
                {'id': ('string', 'minecraft:bed'), 'x': ('int', xh), 'y': ('int', y), 'z': ('int', zh), 'keepPacked': ('byte', 0)})

def place_barrel(c, x, y, z, facing='up'):
    c.set_block(x, y, z, f"minecraft:barrel[facing={facing},open=false]",
                {'id': ('string', 'minecraft:barrel'), 'x': ('int', x), 'y': ('int', y), 'z': ('int', z), 'keepPacked': ('byte', 0)})

def place_brewing_stand(c, x, y, z):
    c.set_block(x, y, z, "minecraft:brewing_stand[has_bottle_0=true,has_bottle_1=false,has_bottle_2=true]",
                {'id': ('string', 'minecraft:brewing_stand'), 'x': ('int', x), 'y': ('int', y), 'z': ('int', z), 'keepPacked': ('byte', 0)})

def place_smoker(c, x, y, z, facing='south', lit='true'):
    c.set_block(x, y, z, f"minecraft:smoker[facing={facing},lit={lit}]",
                {'id': ('string', 'minecraft:smoker'), 'x': ('int', x), 'y': ('int', y), 'z': ('int', z), 'keepPacked': ('byte', 0)})

def place_blast_furnace(c, x, y, z, facing='south', lit='false'):
    c.set_block(x, y, z, f"minecraft:blast_furnace[facing={facing},lit={lit}]",
                {'id': ('string', 'minecraft:blast_furnace'), 'x': ('int', x), 'y': ('int', y), 'z': ('int', z), 'keepPacked': ('byte', 0)})

def place_beehive(c, x, y, z, facing='west', honey_level=5):
    c.set_block(x, y, z, f"minecraft:beehive[facing={facing},honey_level={honey_level}]",
                {'id': ('string', 'minecraft:beehive'), 'x': ('int', x), 'y': ('int', y), 'z': ('int', z), 'keepPacked': ('byte', 0), 'Bees': ('list', 0, [])})

def place_lectern(c, x, y, z, facing='south'):
    c.set_block(x, y, z, f"minecraft:lectern[facing={facing},has_book=false,powered=false]",
                {'id': ('string', 'minecraft:lectern'), 'x': ('int', x), 'y': ('int', y), 'z': ('int', z), 'keepPacked': ('byte', 0)})

def place_tall_flower(c, x, y, z, flower_name='minecraft:peony'):
    if not flower_name.startswith('minecraft:'):
        flower_name = 'minecraft:' + flower_name
    c.set_block(x, y, z, f"{flower_name}[half=lower]")
    c.set_block(x, y + 1, z, f"{flower_name}[half=upper]")

def place_door(c, x, y, z, mat_prefix='dark_oak', facing='north', hinge='left', open_state='false'):
    c.set_block(x, y, z, f"minecraft:{mat_prefix}_door[facing={facing},half=lower,hinge={hinge},open={open_state},powered=false]")
    c.set_block(x, y + 1, z, f"minecraft:{mat_prefix}_door[facing={facing},half=upper,hinge={hinge},open={open_state},powered=false]")

def place_double_door(c, x1, y, z1, arg4='dark_oak', arg5='north', arg6='true', arg7=None, arg8=None):
    """
    Places a 2-block-wide architectural double door with hinges guaranteed to attach
    to the outer doorframes/walls rather than the center seam:
      - facing == 'north': lower X -> hinge='left',  higher X -> hinge='right'
      - facing == 'south': lower X -> hinge='right', higher X -> hinge='left'
      - facing == 'east':  lower Z -> hinge='left',  higher Z -> hinge='right'
      - facing == 'west':  lower Z -> hinge='right', higher Z -> hinge='left'
    Supports both:
      - place_double_door(c, x, y, z, mat_prefix='dark_oak', facing='north', open_state='true')
      - place_double_door(c, x1, y, z1, x2, z2, mat_prefix='dark_oak', facing='north', open_state='true')
    """
    if isinstance(arg4, int):
        x2, z2 = arg4, arg5
        mat_prefix = arg6 if isinstance(arg6, str) else 'dark_oak'
        facing = arg7 if arg7 is not None else 'north'
        open_state = arg8 if arg8 is not None else 'true'
        xa, xb = min(x1, x2), max(x1, x2)
        za, zb = min(z1, z2), max(z1, z2)
    else:
        mat_prefix = arg4
        facing = arg5
        open_state = arg6
        if facing in ('north', 'south'):
            xa, xb = x1, x1 + 1
            za, zb = z1, z1
        else:
            xa, xb = x1, x1
            za, zb = z1, z1 + 1
    if facing in ('north', 'south'):
        h_low = 'left' if facing == 'north' else 'right'
        h_high = 'right' if facing == 'north' else 'left'
        place_door(c, xa, y, za, mat_prefix, facing, h_low, open_state)
        place_door(c, xb, y, za, mat_prefix, facing, h_high, open_state)
    else:
        h_low = 'left' if facing == 'east' else 'right'
        h_high = 'right' if facing == 'east' else 'left'
        place_door(c, xa, y, za, mat_prefix, facing, h_low, open_state)
        place_door(c, xa, y, zb, mat_prefix, facing, h_high, open_state)

def build_recessed_ceiling_grid(c, x1, y_ceil, z1, x2, z2, step_x=4, step_z=4, light_mat=None, add_diffuser=False):
    light_mat = light_mat or MAT['light_ochre']
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    for x in range(xa, xb + 1, step_x):
        for z in range(za, zb + 1, step_z):
            c.set_block(x, y_ceil, z, light_mat)
            if add_diffuser:
                c.set_block(x, y_ceil - 1, z, trapdoor('dark_oak', 'north', 'top', 'false'))

def build_crystal_chandelier(c, cx, y_ceil, cz, drop=2, style='grand'):
    for dy in range(1, drop):
        c.set_block(cx, y_ceil - dy, cz, MAT['chain_y'])
    y_core = y_ceil - drop
    c.set_block(cx, y_core, cz, MAT['light_ochre'] if style == 'grand' else MAT['light_pearl'])
    c.set_block(cx, y_core - 1, cz, MAT['end_rod_down'])
    if style == 'grand':
        c.set_block(cx, y_core + 1, cz, MAT['chain_y'])
        c.set_block(cx - 1, y_core, cz, MAT['end_rod_w'])
        c.set_block(cx + 1, y_core, cz, MAT['end_rod_e'])
        c.set_block(cx, y_core, cz - 1, MAT['end_rod_n'])
        c.set_block(cx, y_core, cz + 1, MAT['end_rod_s'])

def build_illuminated_carpet_rug(c, x1, y_floor, z1, x2, z2, border_carpet=None, center_carpet=None, light_mat=None):
    border_carpet = border_carpet or MAT['carpet_white']
    center_carpet = center_carpet or MAT['carpet_lgray']
    light_mat = light_mat or MAT['light_ochre']
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    for x in range(xa, xb + 1):
        for z in range(za, zb + 1):
            if c.get_block_name(x, y_floor, z) in ('minecraft:air', 'minecraft:cave_air', 'minecraft:void_air'):
                continue
            is_border = (x in (xa, xb) or z in (za, zb))
            if (x - xa) % 2 == 0 and (z - za) % 2 == 0:
                c.set_block(x, y_floor, z, light_mat)
            c.set_block(x, y_floor + 1, z, border_carpet if is_border else center_carpet)

def build_floor_lamp(c, x, y_floor, z, style='modern'):
    c.set_block(x, y_floor + 1, z, MAT['wall_deep_post'] if style == 'modern' else 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
    c.set_block(x, y_floor + 2, z, MAT['end_rod_up'])
    c.set_block(x, y_floor + 3, z, MAT['light_ochre'] if style == 'modern' else MAT['light_pearl'])
    c.set_block(x, y_floor + 4, z, MAT['slab_quartz_b'])

def build_indoor_planter(c, x, y_floor, z, tall=False):
    c.set_block(x, y_floor, z, MAT['light_ochre'])
    c.set_block(x, y_floor + 1, z, MAT['moss_block'])
    for side, dx, dz in [('north', 0, -1), ('south', 0, 1), ('west', -1, 0), ('east', 1, 0)]:
        if c.get_block_name(x + dx, y_floor + 1, z + dz) == 'minecraft:air':
            c.set_block(x + dx, y_floor + 1, z + dz, trapdoor('dark_oak', side, 'bottom', 'true'))
    c.set_block(x, y_floor + 2, z, MAT['leaf_fl_azalea'])
    if tall:
        c.set_block(x, y_floor + 3, z, MAT['leaf_azalea'])

def build_billiards_table(c, x1, y_floor, z1, y_ceil=None):
    for x in range(x1, x1 + 4):
        for z in range(z1, z1 + 6):
            c.set_block(x, y_floor, z, MAT['light_ochre'])
            is_corner = (x in (x1, x1 + 3) and z in (z1, z1 + 5))
            if is_corner:
                c.set_block(x, y_floor + 1, z, MAT['frame_dark'])
            else:
                c.set_block(x, y_floor + 1, z, MAT['wood_dark'])
            c.set_block(x, y_floor + 2, z, MAT['carpet_green'] if not is_corner else MAT['carpet_black'])

    if y_ceil:
        for z in (z1 + 1, z1 + 3, z1 + 4):
            c.set_block(x1 + 1, y_ceil - 1, z, MAT['chain_y'])
            c.set_block(x1 + 2, y_ceil - 1, z, MAT['chain_y'])
            c.set_block(x1 + 1, y_ceil - 2, z, MAT['light_ochre'] if z in (z1 + 1, z1 + 4) else MAT['slab_dark_t'])
            c.set_block(x1 + 2, y_ceil - 2, z, MAT['light_ochre'] if z in (z1 + 1, z1 + 4) else MAT['slab_dark_t'])

def build_home_theater_wall(c, x1, y_floor, z_wall, width=7, facing='south'):
    dz_front = 1 if facing == 'south' else -1
    for x in range(x1, x1 + width):
        c.set_block(x, y_floor + 1, z_wall, MAT['wood_dark'])
        c.set_block(x, y_floor + 4, z_wall, MAT['light_ochre'])
        c.set_block(x, y_floor + 4, z_wall + dz_front, trapdoor('dark_oak', facing, 'top', 'false'))
        if x in (x1, x1 + width - 1):
            c.fill(x, y_floor + 1, z_wall, x, y_floor + 3, z_wall, MAT['beam_dark_y'])
            c.set_block(x, y_floor + 1, z_wall + dz_front, MAT['note_block'])
            c.set_block(x, y_floor + 2, z_wall + dz_front, MAT['jukebox'])
            c.set_block(x, y_floor + 3, z_wall + dz_front, MAT['end_rod_up'])
        else:
            c.fill(x, y_floor + 2, z_wall, x, y_floor + 3, z_wall, MAT['wall_black'])
            c.set_block(x, y_floor + 1, z_wall + dz_front, MAT['slab_dark_t'])
            c.set_block(x, y_floor, z_wall + dz_front, MAT['light_ochre'])
    c.set_block(x1 + width // 2, y_floor + 2, z_wall + dz_front, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')

def build_ensuite_bathroom(c, x1, y_floor, z1, x2, z2, door_side='south'):
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    for x in range(xa, xb + 1):
        for z in range(za, zb + 1):
            if (x + z) % 3 == 0:
                c.set_block(x, y_floor, z, MAT['light_sea'])
            else:
                c.set_block(x, y_floor, z, MAT['wall_quartz'] if (x + z) % 2 == 0 else MAT['wall_calcite'])

    for x in range(xa, xb + 1):
        for y in range(y_floor + 1, y_floor + 5):
            if door_side == 'south' and abs(x - (xa + xb) // 2) <= 1 and y <= y_floor + 3:
                continue
            c.set_block(x, y, zb, MAT['wall_white'] if y in (y_floor + 1, y_floor + 4) else MAT['glass_tinted'])

    tx1, tx2 = xa + 1, min(xa + 4, xb - 1)
    for x in range(tx1, tx2 + 1):
        for z in range(za + 1, za + 4):
            if x in (tx1, tx2) or z in (za + 1, za + 3):
                c.set_block(x, y_floor + 1, z, stair('smooth_quartz', 'north' if z == za + 1 else 'south', 'bottom'))
            else:
                c.set_block(x, y_floor, z, MAT['light_sea'])
                c.set_block(x, y_floor + 1, z, MAT['water'])
    c.set_block(tx2, y_floor + 2, za + 1, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')

    for z in range(za + 2, zb - 1):
        c.set_block(xb - 1, y_floor + 1, z, 'minecraft:water_cauldron[level=3]' if z % 2 == 0 else MAT['wall_quartz'])
        c.set_block(xb, y_floor + 2, z, MAT['light_sea'])
        c.set_block(xb, y_floor + 3, z, MAT['light_sea'])
        c.set_block(xb - 1, y_floor + 2, z, MAT['pane_white'])
        c.set_block(xb - 1, y_floor + 3, z, MAT['pane_white'])

    c.set_block(xa + 1, y_floor, zb - 1, MAT['light_sea'])
    c.set_block(xa + 1, y_floor + 4, zb - 1, MAT['light_sea'])
    c.set_block(xa + 1, y_floor + 3, zb - 1, MAT['end_rod_down'])
    c.set_block(xa + 2, y_floor + 1, zb - 2, MAT['pane_clear'])
    c.set_block(xa + 2, y_floor + 2, zb - 2, MAT['pane_clear'])
    c.set_block(xa + 2, y_floor + 3, zb - 2, MAT['pane_clear'])

def build_wall(c, x1, y1, z1, x2, y2, z2, mat=None, trim_bottom=None, trim_top=None):
    mat = mat or MAT['wall_white']
    c.fill(x1, y1, z1, x2, y2, z2, mat)
    if trim_bottom:
        c.fill(x1, y1, z1, x2, y1, z2, trim_bottom)
    if trim_top:
        c.fill(x1, y2, z1, x2, y2, z2, trim_top)

def build_slatted_feature_wall(c, x1, y1, z1, x2, y2, z2, wall_mat=None, glass_mat=None):
    wall_mat = wall_mat or MAT['wall_white']
    glass_mat = glass_mat or MAT['glass_black']
    c.fill(x1, y1, z1, x2, y2, z2, wall_mat)
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    if xb - xa >= zb - za:
        for x in range(xa + 2, xb - 1, 2):
            c.fill(x, y1 + 1, za, x, y2 - 1, zb, glass_mat)
    else:
        for z in range(za + 2, zb - 1, 2):
            c.fill(xa, y1 + 1, z, xb, y2 - 1, z, glass_mat)

def build_curtain_wall(c, x1, y1, z1, x2, y2, z2, glass_primary=None, glass_accent=None, frame_mat=None, bay_width=4):
    glass_primary = glass_primary or MAT['glass_black']
    glass_accent = glass_accent or MAT['glass_gray']
    frame_mat = frame_mat or MAT['frame_dark']
    xa, xb = min(x1, x2), max(x1, x2)
    ya, yb = min(y1, y2), max(y1, y2)
    za, zb = min(z1, z2), max(z1, z2)

    if xb - xa >= zb - za:
        for x in range(xa, xb + 1):
            is_mullion = (x == xa or x == xb or (x - xa) % bay_width == 0)
            for y in range(ya, yb + 1):
                if is_mullion:
                    b = frame_mat
                elif y == yb:
                    b = glass_accent
                else:
                    b = glass_primary if ((x - xa) // bay_width) % 2 == 0 else glass_accent
                for z in range(za, zb + 1):
                    c.set_block(x, y, z, b)
    else:
        for z in range(za, zb + 1):
            is_mullion = (z == za or z == zb or (z - za) % bay_width == 0)
            for y in range(ya, yb + 1):
                if is_mullion:
                    b = frame_mat
                elif y == yb:
                    b = glass_accent
                else:
                    b = glass_primary if ((z - za) // bay_width) % 2 == 0 else glass_accent
                for x in range(xa, xb + 1):
                    c.set_block(x, y, z, b)

def build_flat_roof_and_eaves(c, x1, y_roof, z1, x2, z2, overhang=2, roof_mat=None, soffit_mat=None, coping_slab=None, hidden_lights=True):
    roof_mat = roof_mat or MAT['wall_white']
    soffit_mat = soffit_mat or MAT['wood_dark']
    coping_slab = coping_slab or MAT['slab_quartz_b']
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    ox1, ox2 = xa - overhang, xb + overhang
    oz1, oz2 = za - overhang, zb + overhang

    c.fill(ox1, y_roof, oz1, ox2, y_roof, oz2, soffit_mat)
    c.fill(ox1, y_roof + 1, oz1, ox2, y_roof + 1, oz2, roof_mat)

    if xb - xa >= 5 and zb - za >= 5:
        for x in range(xa + 2, xb - 1, 4):
            for z in range(za + 2, zb - 1, 4):
                c.set_block(x, y_roof, z, MAT['light_ochre'] if (x + z) % 8 == 0 else MAT['light_pearl'])

    for x in range(ox1, ox2 + 1):
        c.set_block(x, y_roof + 2, oz1, coping_slab)
        c.set_block(x, y_roof + 2, oz2, coping_slab)
    for z in range(oz1, oz2 + 1):
        c.set_block(ox1, y_roof + 2, z, coping_slab)
        c.set_block(ox2, y_roof + 2, z, coping_slab)

    if hidden_lights and overhang >= 1:
        lx1, lx2 = xa - 1, xb + 1
        lz1, lz2 = za - 1, zb + 1
        for x in range(lx1, lx2 + 1, 2):
            c.set_block(x, y_roof, lz1, MAT['light_ochre'])
            c.set_block(x, y_roof - 1, lz1, trapdoor('dark_oak', 'north', 'top', 'false'))
            c.set_block(x, y_roof, lz2, MAT['light_ochre'])
            c.set_block(x, y_roof - 1, lz2, trapdoor('dark_oak', 'south', 'top', 'false'))
        for z in range(lz1, lz2 + 1, 2):
            c.set_block(lx1, y_roof, z, MAT['light_ochre'])
            c.set_block(lx1, y_roof - 1, z, trapdoor('dark_oak', 'west', 'top', 'false'))
            c.set_block(lx2, y_roof, z, MAT['light_ochre'])
            c.set_block(lx2, y_roof - 1, z, trapdoor('dark_oak', 'east', 'top', 'false'))

def build_support_beams_under_cantilever(c, x1, y_soffit, z1, x2, z2, axis='z', step=4):
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    if axis == 'z':
        for x in range(xa, xb + 1, step):
            c.fill(x, y_soffit, za, x, y_soffit, zb, MAT['beam_dark_z'])
            if x + step // 2 <= xb:
                c.set_block(x + step // 2, y_soffit + 1, (za + zb) // 2, MAT['light_ochre'])
        c.fill(xa, y_soffit, za, xb, y_soffit, za, MAT['beam_dark_x'])
        c.fill(xa, y_soffit, zb, xb, y_soffit, zb, MAT['beam_dark_x'])
    else:
        for z in range(za, zb + 1, step):
            c.fill(xa, y_soffit, z, xb, y_soffit, z, MAT['beam_dark_x'])
            if z + step // 2 <= zb:
                c.set_block((xa + xb) // 2, y_soffit + 1, z + step // 2, MAT['light_ochre'])
        c.fill(xa, y_soffit, za, xa, y_soffit, zb, MAT['beam_dark_z'])
        c.fill(xb, y_soffit, za, xb, y_soffit, zb, MAT['beam_dark_z'])

def build_pitched_modern_roof(c, x1, y_base, z1, x2, z2, ridge_offset=9):
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    x_ridge = xa + ridge_offset
    max_rise = 4

    for x in range(xa - 1, xb + 2):
        if x <= x_ridge:
            span = max(1, x_ridge - (xa - 1))
            t = (x - (xa - 1)) / span
        else:
            span = max(1, (xb + 1) - x_ridge)
            t = ((xb + 1) - x) / span
        half_steps = int(round(t * max_rise * 2))
        dy = half_steps // 2
        is_top_half = (half_steps % 2 == 1)
        ry = y_base + dy

        for gx in [x]:
            if xa <= gx <= xb and ry > y_base:
                c.fill(gx, y_base, za, gx, ry - 1, za, MAT['wall_white'])
                c.fill(gx, y_base, zb, gx, ry - 1, zb, MAT['wall_white'])
                c.fill(gx, ry - 1, za + 1, gx, ry - 1, zb - 1, MAT['wood_dark'])
                if (gx - xa) % 4 == 2 and xa + 2 <= gx <= xb - 2:
                    for lz in range(za + 2, zb - 1, 3):
                        c.set_block(gx, ry - 1, lz, MAT['light_ochre'])

        for z in range(za - 2, zb + 3):
            if is_top_half:
                c.set_block(x, ry, z, MAT['wall_white'])
                c.set_block(x, ry + 1, z, MAT['slab_quartz_b'])
            else:
                c.set_block(x, ry, z, MAT['wall_white'])
                c.set_block(x, ry - 1, z, MAT['slab_quartz_t'])

SPIRAL_8_SECTORS = [
    [(0, 1), (0, 2), (1, 2)],
    [(1, 1), (2, 2), (2, 1)],
    [(1, 0), (2, 0), (2, -1)],
    [(1, -1), (2, -2), (1, -2)],
    [(0, -1), (0, -2), (-1, -2)],
    [(-1, -1), (-2, -2), (-2, -1)],
    [(-1, 0), (-2, 0), (-2, 1)],
    [(-1, 1), (-2, 2), (-1, 2)],
]

def build_spiral_staircase(c, cx, y_bottom, y_top, cz, radius=2, start_sector=5, clockwise=True, intermediate_floors=None):
    """
    V4 Ergonomic 8-Sector 3-Block-Wide Fan Spiral Staircase:
    - Each 45-degree sector places a 3-block fan (1 inner block at r=1 + 2 outer blocks at r=2)
      at the exact same slab elevation (+0.5 Y per sector = 4.0 blocks rise per full 360-degree turn).
    - Zero duplicate inner-ring coordinates (every single inner block in the 3x3 ring belongs to
      a distinct sector), and zero `iron_bars` or `end_rod` posts placed on the walkable steps!
    - Illumination is embedded directly into the central column (`stripped_dark_oak_wood` + `ochre_froglight`).
    - Provides 3.0 to 3.5 blocks of vertical headroom at every step and automatic top/bottom landing bridges.
    """
    intermediate_floors = set(intermediate_floors or [])

    for dx in range(-2, 3):
        for dz in range(-2, 3):
            b_base = c.get_block_name(cx + dx, y_bottom - 1, cz + dz)
            if b_base in ('minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:water', 'minecraft:light'):
                c.set_block(cx + dx, y_bottom - 1, cz + dz, MAT['wall_quartz'])

    for y in range(y_bottom, y_top + 4):
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                c.set_block(cx + dx, y, cz + dz, 'minecraft:air')

    for y in range(y_bottom - 1, y_top + 2):
        mat_col = MAT['light_ochre'] if (y - y_bottom) % 3 == 1 else MAT['beam_dark_y']
        c.set_block(cx, y, cz, mat_col)
    c.set_block(cx, y_top + 2, cz, MAT['lantern_stand'])

    total_half_steps = (y_top - y_bottom) * 2 + 1
    step_sign = 1 if clockwise else -1

    for hs in range(total_half_steps + 1):
        y = y_bottom + (hs // 2)
        is_top = (hs % 2 == 1)
        sec_idx = (start_sector + step_sign * hs) % 8
        slab_mat = MAT['slab_quartz_t'] if is_top else MAT['slab_quartz_b']

        for dx, dz in SPIRAL_8_SECTORS[sec_idx]:
            for hy in range(y + 1, y + 4):
                c.set_block(cx + dx, hy, cz + dz, 'minecraft:air')
            c.set_block(cx + dx, y, cz + dz, slab_mat)

        if is_top and y in intermediate_floors:
            for dx, dz in SPIRAL_8_SECTORS[sec_idx]:
                c.set_block(cx + dx, y, cz + dz, MAT['slab_quartz_t'])

    for extra in (1, 2):
        land_sec = (start_sector + step_sign * (total_half_steps + extra)) % 8
        for dx, dz in SPIRAL_8_SECTORS[land_sec]:
            for hy in range(y_top + 1, y_top + 4):
                c.set_block(cx + dx, hy, cz + dz, 'minecraft:air')
            c.set_block(cx + dx, y_top, cz + dz, MAT['slab_quartz_t'])

def build_straight_stairs(c, x1, y_bottom, z1, width, height, direction='north', stair_prefix='smooth_quartz', hidden_lights=True):
    """
    V4 Straight Architectural Staircase:
    - Connects a lower floor at `y_bottom - 1` (walking surface `y_bottom`) to an upper floor
      at `y_top = y_bottom + height - 1` (walking surface `y_top + 1`).
    - Places `height` stair blocks from `step = 0` (`y = y_bottom`) to `step = height - 1` (`y = y_top`).
    - Guarantees a solid lower-floor entry platform (`step = -1` and `step = 0` at `y_bottom - 1`),
      continuous sloped underside stringers (`stair(..., opp_dir, 'top')` + `light_ochre`),
      a solid flush upper-floor landing at `step = height` (`y = y_top`), and 4 blocks of clear headroom!
    """
    opp_dir = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}[direction]
    y_top = y_bottom + height - 1

    def step_coords(step_idx, w_idx):
        if direction == 'north':
            return x1 + w_idx, z1 - step_idx
        elif direction == 'south':
            return x1 + w_idx, z1 + step_idx
        elif direction == 'east':
            return x1 + step_idx, z1 + w_idx
        else:
            return x1 - step_idx, z1 + w_idx

    for w in range(width):
        bx, bz = step_coords(-1, w)
        b_floor = c.get_block_name(bx, y_bottom - 1, bz)
        if b_floor in ('minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:water', 'minecraft:light'):
            c.set_block(bx, y_bottom - 1, bz, MAT['wall_quartz'])
        for hy in range(y_bottom, y_bottom + 4):
            if not c.get_block_name(bx, hy, bz).endswith('_carpet'):
                c.set_block(bx, hy, bz, 'minecraft:air')

    for step in range(height):
        y = y_bottom + step
        for w in range(width):
            sx, sz = step_coords(step, w)
            for hy in range(y + 1, max(y + 5, y_top + 4)):
                c.set_block(sx, hy, sz, 'minecraft:air')

            c.set_block(sx, y, sz, stair(stair_prefix, direction, 'bottom'))

            if step == 0:
                c.set_block(sx, y - 1, sz, MAT['light_ochre'] if hidden_lights and w == width // 2 else MAT['wall_quartz'])
            else:
                if hidden_lights and (w == width // 2 and step % 2 == 1):
                    c.set_block(sx, y - 1, sz, MAT['light_ochre'])
                else:
                    c.set_block(sx, y - 1, sz, stair(stair_prefix, opp_dir, 'top'))

    for land_step in (height, height + 1):
        for w in range(width):
            lx, lz = step_coords(land_step, w)
            b_land = c.get_block_name(lx, y_top, lz)
            if b_land in ('minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:water', 'minecraft:light') or b_land.endswith('_stairs'):
                c.set_block(lx, y_top, lz, MAT['wood_dark'])
            for hy in range(y_top + 1, y_top + 4):
                b_up = c.get_block_name(lx, hy, lz)
                if not (hy == y_top + 1 and b_up.endswith('_carpet')):
                    c.set_block(lx, hy, lz, 'minecraft:air')

def build_tower(c, x1, y_base, z1, size=8, height=22):
    """
    V4 Modernist Architectural Belvedere & Lantern Tower (X=28..35, Z=-41..-34):
    - Aligns tower landings with the exact Main Villa floor elevations:
        * 1F: y_base      (Y = 64)
        * 2F: y_base + 6  (Y = 70)
        * 3F: y_base + 13 (Y = 77)
        * 4F: y_base + 19 (Y = 83, Rooftop Belvedere Observation Deck)
    - Opens wide 3-block archways on BOTH the South wall (`Z = z2 = -34`) and West wall (`X = x1 = 28`)
      on 1F, 2F, and 3F so the tower is 100% connected to the Main Villa on every single floor!
    """
    x2, z2 = x1 + size - 1, z1 + size - 1
    y_top = y_base + height
    floor_levels = [y_base + 6, y_base + 13, y_base + 19]

    c.fill(x1, y_base, z1, x2, y_base + 1, z2, MAT['stone_pol_and'])

    for y in range(y_base + 1, y_top - 2):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                on_x = (x in (x1, x2))
                on_z = (z in (z1, z2))
                if on_x and on_z:
                    c.set_block(x, y, z, MAT['wall_white'])
                elif on_x or on_z:
                    if y in floor_levels:
                        c.set_block(x, y, z, MAT['wall_white'])
                    elif x in (x1 + 1, x2 - 1) and on_z:
                        c.set_block(x, y, z, MAT['wall_white'])
                    elif z in (z1 + 1, z2 - 1) and on_x:
                        c.set_block(x, y, z, MAT['wall_white'])
                    else:
                        c.set_block(x, y, z, MAT['glass_black'])
                else:
                    c.set_block(x, y, z, 'minecraft:air')

    for fy in floor_levels:
        c.fill(x1 - 2, fy, z1 - 2, x2 + 2, fy, z2 + 2, MAT['slab_dark_t'])
        c.fill(x1 + 1, fy, z1 + 1, x2 - 1, fy, z2 - 1, MAT['wood_dark'])
        for lx in (x1 + 1, x2 - 1):
            for lz in (z1 + 1, z2 - 1):
                c.set_block(lx, fy, lz, MAT['light_ochre'])
        for x in range(x1 - 2, x2 + 3):
            c.set_block(x, fy, z1 - 2, MAT['wall_quartz'])
            c.set_block(x, fy, z2 + 2, MAT['wall_quartz'])
            c.set_block(x, fy + 1, z1 - 2, MAT['pane_black'])
            c.set_block(x, fy + 1, z2 + 2, MAT['pane_black'])
        for z in range(z1 - 2, z2 + 3):
            c.set_block(x1 - 2, fy, z, MAT['wall_quartz'])
            c.set_block(x2 + 2, fy, z, MAT['wall_quartz'])
            c.set_block(x1 - 2, fy + 1, z, MAT['pane_black'])
            c.set_block(x2 + 2, fy + 1, z, MAT['pane_black'])
        c.fill(x1 + 1, fy + 1, z1 + 1, x2 - 1, fy + 1, z2 - 1, 'minecraft:air')

    for lx in (x1 + 1, x2 - 1):
        for lz in (z1 + 1, z2 - 1):
            c.set_block(lx, y_base, lz, MAT['light_ochre'])

    c.fill(x1 - 2, y_base + 20, z1 - 2, x2 + 3, y_top - 1, z2 + 2, 'minecraft:air')
    for x in range(x1 - 2, x2 + 3):
        c.set_block(x, y_base + 20, z1 - 2, MAT['pane_black'])
        c.set_block(x, y_base + 20, z2 + 2, MAT['pane_black'])
    for z in range(z1 - 2, z2 + 3):
        c.set_block(x1 - 2, y_base + 20, z, MAT['pane_black'])
        c.set_block(x2 + 2, y_base + 20, z, MAT['pane_black'])

    cx, cz = (x1 + x2) // 2, (z1 + z2) // 2
    build_spiral_staircase(c, cx, y_base + 1, y_base + 19, cz, radius=2, start_sector=5, clockwise=True, intermediate_floors=[y_base + 6, y_base + 13])

    for fy_open in [y_base, y_base + 6, y_base + 13, y_base + 19]:
        h_open = 3 if fy_open < y_base + 19 else 2

        c.fill(x1 + 2, fy_open, z2 - 1, x1 + 4, fy_open, z2 + 2, MAT['wood_dark'] if fy_open > y_base else MAT['wall_quartz'])
        c.fill(x1 + 2, fy_open + 1, z2, x1 + 4, fy_open + h_open, z2 + 2, 'minecraft:air')

        c.fill(x1 - 2, fy_open, z1 + 2, x1, fy_open, z2 - 2, MAT['wood_dark'] if fy_open > y_base else MAT['wall_quartz'])
        c.fill(x1 - 2, fy_open + 1, z1 + 2, x1, fy_open + h_open, z2 - 2, 'minecraft:air')

        if fy_open in (y_base + 6, y_base + 13) and c.get_block_name(x1 + 1, fy_open, z2 - 2) == 'minecraft:air':
            c.set_block(x1 + 1, fy_open, z2 - 2, MAT['slab_quartz_t'])

        if fy_open == y_base + 19:
            c.fill(x2, fy_open + 1, z1 + 2, x2, fy_open + 2, z2 - 2, 'minecraft:air')
            c.fill(x1 + 2, fy_open + 1, z1, x2 - 2, fy_open + 2, z1, 'minecraft:air')

    for y in (y_top - 2, y_top - 1):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if x in (x1, x2) and z in (z1, z2):
                    c.set_block(x, y, z, MAT['wall_white'])
                elif x in (x1, x2) or z in (z1, z2):
                    if not (y <= y_base + 21 and ((z == z2 and x1 + 2 <= x <= x1 + 4) or (x == x1 and z1 + 2 <= z <= z2 - 2) or (x == x2 and z1 + 2 <= z <= z2 - 2) or (z == z1 and x1 + 2 <= x <= x2 - 2))):
                        c.set_block(x, y, z, MAT['glass_clear'])
                elif (x, z) != (cx, cz):
                    c.set_block(x, y, z, 'minecraft:air')
    build_flat_roof_and_eaves(c, x1, y_top, z1, x2, z2, overhang=2, hidden_lights=True)

def build_pergola_colonnade(c, x1, y_ground, z1, x2, z2, axis='z', lamp_step=8):
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    y_top = y_ground + 5
    rng = random.Random(4242 ^ xa ^ za)

    for x in range(xa, xb + 1):
        for z in range(za, zb + 1):
            if (x == (xa + xb) // 2) and ((z if axis == 'z' else x) % 4 == 0):
                c.set_block(x, y_ground - 1, z, MAT['light_ochre'])
                c.set_block(x, y_ground, z, MAT['glass_gray'])
            elif (x + z) % 2 == 0:
                c.set_block(x, y_ground, z, MAT['stone_smooth'])
            else:
                c.set_block(x, y_ground, z, MAT['stone_pol_and'])

    if axis == 'z':
        for z in range(za, zb + 1):
            c.set_block(xa - 1, y_ground, z, MAT['grass_block'])
            c.set_block(xb + 1, y_ground, z, MAT['grass_block'])
            if (z - za) % lamp_step == 0:
                build_lamppost(c, xa - 1, y_ground + 1, z, style='garden')
                build_lamppost(c, xb + 1, y_ground + 1, z, style='garden')
            else:
                c.set_block(xa - 1, y_ground + 1, z, rng.choice(SOFT_FLOWERS))
                c.set_block(xb + 1, y_ground + 1, z, rng.choice(SOFT_FLOWERS))

            if (z - za) % 5 == 0 or z == zb:
                for px in (xa, xb):
                    c.set_block(px, y_ground + 1, z, MAT['stone_pol_and'])
                    c.fill(px, y_ground + 2, z, px, y_top, z, MAT['beam_dark_y'])
                    for py in range(y_ground + 2, y_top):
                        if rng.random() < 0.65:
                            side_x = px - 1 if px == xa else px + 1
                            c.set_block(side_x, py, z, rng.choice([MAT['leaf_fl_azalea'], MAT['leaf_cherry'], MAT['leaf_azalea']]))
                c.fill(xa, y_top, z, xb, y_top, z, MAT['beam_dark_x'])
                c.set_block((xa + xb) // 2, y_top - 1, z, MAT['lantern_hang'])

            for x in range(xa, xb + 1):
                if (x + z) % 2 == 0:
                    c.set_block(x, y_top, z, trapdoor('dark_oak', 'north', 'top', 'false'))
                if rng.random() < 0.72:
                    leaf = rng.choice([MAT['leaf_fl_azalea'], MAT['leaf_cherry'], MAT['leaf_azalea'], MAT['leaf_oak']])
                    c.set_block(x, y_top + 1, z, leaf)
                    if x in (xa, xb) and rng.random() < 0.55:
                        c.set_block(x, y_top - 1, z, leaf)
                if rng.random() < 0.18 and x not in (xa, xb):
                    c.set_block(x, y_top - 1, z, 'minecraft:spore_blossom')
    else:
        for x in range(xa, xb + 1):
            c.set_block(x, y_ground, za - 1, MAT['grass_block'])
            c.set_block(x, y_ground, zb + 1, MAT['grass_block'])
            if (x - xa) % lamp_step == 0:
                build_lamppost(c, x, y_ground + 1, za - 1, style='garden')
                build_lamppost(c, x, y_ground + 1, zb + 1, style='garden')
            else:
                c.set_block(x, y_ground + 1, za - 1, rng.choice(SOFT_FLOWERS))
                c.set_block(x, y_ground + 1, zb + 1, rng.choice(SOFT_FLOWERS))
            if (x - xa) % 5 == 0 or x == xb:
                for pz in (za, zb):
                    c.set_block(x, y_ground + 1, pz, MAT['stone_pol_and'])
                    c.fill(x, y_ground + 2, pz, x, y_top, pz, MAT['beam_dark_y'])
                c.fill(x, y_top, za, x, y_top, zb, MAT['beam_dark_z'])
                c.set_block(x, y_top - 1, (za + zb) // 2, MAT['lantern_hang'])
            for z in range(za, zb + 1):
                if (x + z) % 2 == 0:
                    c.set_block(x, y_top, z, trapdoor('dark_oak', 'east', 'top', 'false'))
                if rng.random() < 0.72:
                    leaf = rng.choice([MAT['leaf_fl_azalea'], MAT['leaf_cherry'], MAT['leaf_azalea']])
                    c.set_block(x, y_top + 1, z, leaf)

def build_vine_arch(c, cx, y_ground, cz, span=5, height=5, axis='x'):
    half = span // 2
    y_top = y_ground + height
    if axis == 'x':
        x1, x2 = cx - half, cx + half
        for px in (x1, x2):
            c.set_block(px, y_ground + 1, cz, MAT['stone_pol_and'])
            c.fill(px, y_ground + 2, cz, px, y_top, cz, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
            c.fill(px, y_ground + 2, cz - 1, px, y_top - 1, cz - 1, MAT['leaf_fl_azalea'])
            c.fill(px, y_ground + 2, cz + 1, px, y_top - 1, cz + 1, MAT['leaf_cherry'])
        c.fill(x1, y_top, cz, x2, y_top, cz, MAT['slab_dark_b'])
        c.fill(x1, y_top + 1, cz - 1, x2, y_top + 1, cz + 1, MAT['leaf_fl_azalea'])
        c.set_block(cx, y_top + 1, cz, MAT['leaf_cherry'])
        c.set_block(cx, y_top - 1, cz, MAT['lantern_hang'])
    else:
        z1, z2 = cz - half, cz + half
        for pz in (z1, z2):
            c.set_block(cx, y_ground + 1, pz, MAT['stone_pol_and'])
            c.fill(cx, y_ground + 2, pz, cx, y_top, pz, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
            c.fill(cx - 1, y_ground + 2, pz, cx - 1, y_top - 1, pz, MAT['leaf_fl_azalea'])
            c.fill(cx + 1, y_ground + 2, pz, cx + 1, y_top - 1, pz, MAT['leaf_cherry'])
        c.fill(cx, y_top, z1, cx, y_top, z2, MAT['slab_dark_b'])
        c.fill(cx - 1, y_top + 1, z1, cx + 1, y_top + 1, z2, MAT['leaf_fl_azalea'])
        c.set_block(cx, y_top + 1, cz, MAT['leaf_cherry'])
        c.set_block(cx, y_top - 1, cz, MAT['lantern_hang'])

def build_lamppost(c, x, y, z, style='courtyard'):
    if style == 'courtyard':
        c.set_block(x, y, z, MAT['stone_pol_and'])
        c.set_block(x, y + 1, z, MAT['wall_deep_post'])
        c.set_block(x, y + 2, z, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        c.set_block(x, y + 3, z, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        c.set_block(x, y + 4, z, MAT['light_ochre'])
        c.set_block(x, y + 5, z, MAT['slab_dark_b'])
    elif style == 'garden':
        c.set_block(x, y, z, MAT['wall_deep_post'])
        c.set_block(x, y + 1, z, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        c.set_block(x, y + 2, z, MAT['lantern_stand'])
    elif style == 'bollard':
        c.set_block(x, y, z, MAT['wall_deep_post'])
        c.set_block(x, y + 1, z, MAT['end_rod_up'])
        c.set_block(x, y + 2, z, MAT['slab_quartz_b'])
    elif style == 'avenue':
        c.set_block(x, y, z, MAT['stone_pol_and'])
        c.set_block(x, y + 1, z, MAT['wall_deep_post'])
        c.fill(x, y + 2, z, x, y + 4, z, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
        c.fill(x - 1, y + 5, z, x + 1, y + 5, z, MAT['slab_dark_t'])
        c.set_block(x - 1, y + 4, z, MAT['lantern_hang'])
        c.set_block(x + 1, y + 4, z, MAT['lantern_hang'])
        c.set_block(x, y + 5, z, MAT['light_ochre'])
        c.set_block(x, y + 6, z, MAT['slab_quartz_b'])

def build_infinity_pool(c, x1, y_ground, z1, x2, z2):
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)

    for x in range(xa, xb + 1):
        for z in range(za, zb + 1):
            is_outer = (x in (xa, xb) or z in (za, zb))
            is_inner_wall = (x in (xa + 1, xb - 1) or z in (za + 1, zb - 1)) and not is_outer
            if is_outer:
                c.set_block(x, y_ground - 2, z, MAT['pool_deep_1'])
                c.set_block(x, y_ground - 1, z, MAT['pool_shallow_1'])
                if z == za:
                    c.set_block(x, y_ground, z, MAT['slab_quartz_t'])
                    c.set_block(x, y_ground - 1, za - 1, MAT['light_sea'] if x % 4 == 0 else MAT['pool_deep_1'])
                    c.set_block(x, y_ground, za - 1, MAT['water'])
                    c.set_block(x, y_ground, za - 2, MAT['slab_quartz_t'])
                else:
                    c.set_block(x, y_ground, z, MAT['wall_quartz'])
            elif is_inner_wall:
                c.set_block(x, y_ground - 3, z, MAT['pool_deep_2'])
                c.set_block(x, y_ground - 2, z, MAT['pool_deep_1'])
                c.set_block(x, y_ground - 1, z, MAT['pool_shallow_2'])
                c.set_block(x, y_ground, z, MAT['water'])
            else:
                if (x - xa) % 5 == 0 or (z - za) % 4 == 0:
                    c.set_block(x, y_ground - 3, z, MAT['light_sea'])
                elif (x + z) % 2 == 0:
                    c.set_block(x, y_ground - 3, z, MAT['pool_deep_1'])
                else:
                    c.set_block(x, y_ground - 3, z, MAT['pool_deep_2'])
                if z >= zb - 3:
                    c.set_block(x, y_ground - 2, z, MAT['pool_shallow_1'])
                    c.set_block(x, y_ground - 1, z, MAT['water'])
                    c.set_block(x, y_ground, z, MAT['water'])
                else:
                    c.set_block(x, y_ground - 2, z, MAT['water'])
                    c.set_block(x, y_ground - 1, z, MAT['water'])
                    c.set_block(x, y_ground, z, MAT['water'])

def build_fountain(c, cx, y_ground, cz, radius=6):
    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            x, z = cx + dx, cz + dz
            dist = max(abs(dx), abs(dz))
            if dist == radius:
                c.set_block(x, y_ground - 1, z, MAT['stone_pol_and'])
                c.set_block(x, y_ground, z, MAT['wall_quartz'])
                c.set_block(x, y_ground + 1, z, MAT['slab_quartz_b'])
            elif dist == radius - 1:
                c.set_block(x, y_ground - 2, z, MAT['pool_deep_1'])
                c.set_block(x, y_ground - 1, z, MAT['pool_shallow_2'])
                c.set_block(x, y_ground, z, MAT['water'])
            else:
                if (dx + dz) % 2 == 0 and dist in (2, 3):
                    c.set_block(x, y_ground - 2, z, MAT['light_sea'])
                else:
                    c.set_block(x, y_ground - 2, z, MAT['pool_deep_2'])
                c.set_block(x, y_ground - 1, z, MAT['water'])
                c.set_block(x, y_ground, z, MAT['water'])

    c.fill(cx - 1, y_ground - 1, cz - 1, cx + 1, y_ground, cz + 1, MAT['wall_quartz'])
    c.set_block(cx - 1, y_ground + 1, cz, MAT['slab_quartz_b'])
    c.set_block(cx + 1, y_ground + 1, cz, MAT['slab_quartz_b'])
    c.set_block(cx, y_ground + 1, cz - 1, MAT['slab_quartz_b'])
    c.set_block(cx, y_ground + 1, cz + 1, MAT['slab_quartz_b'])
    c.set_block(cx, y_ground + 1, cz, MAT['light_sea'])
    c.set_block(cx, y_ground + 2, cz, MAT['water'])
    c.set_block(cx, y_ground + 3, cz, MAT['end_rod_up'])

def build_topiary_sculpture(c, cx, y_ground, cz):
    rng = random.Random(202604 ^ (cx * 73856093) ^ (cz * 19349663))
    for dx in range(-5, 6):
        for dz in range(-5, 6):
            if abs(dx) == 5 or abs(dz) == 5:
                if abs(dx) <= 1 or abs(dz) <= 1:
                    continue
                c.set_block(cx + dx, y_ground + 1, cz + dz, MAT['leaf_azalea'])
                c.set_block(cx + dx, y_ground + 2, cz + dz, MAT['leaf_oak'])
            elif abs(dx) == 4 or abs(dz) == 4:
                c.set_block(cx + dx, y_ground, cz + dz, MAT['moss_block'])
                c.set_block(cx + dx, y_ground + 1, cz + dz, rng.choice(SOFT_FLOWERS))

    c.fill(cx - 2, y_ground + 1, cz - 2, cx + 2, y_ground + 1, cz + 2, MAT['slab_quartz_b'])
    c.fill(cx - 1, y_ground + 1, cz - 1, cx + 1, y_ground + 1, cz + 1, MAT['wall_quartz'])
    for bx in (cx - 2, cx + 2):
        for bz in (cz - 2, cz + 2):
            c.set_block(bx, y_ground, bz, MAT['light_ochre'])
            c.set_block(bx, y_ground + 1, bz, MAT['wall_quartz'])
            c.set_block(bx, y_ground + 2, bz, MAT['end_rod_up'])

    sculpt_coords = [
        (0, 2, 0), (-1, 2, 0), (1, 2, 0), (0, 2, -1), (0, 2, 1),
        (0, 3, 0), (-1, 3, 0), (1, 3, 0), (0, 3, -1), (0, 3, 1), (1, 3, 1),
        (0, 4, 0), (1, 4, 0), (1, 4, 1), (2, 4, 1), (-1, 4, -1),
        (1, 5, 0), (2, 5, 0), (2, 5, 1), (1, 5, 1),
        (2, 6, 0), (3, 5, 0), (3, 4, 0),
    ]
    for dx, dy, dz in sculpt_coords:
        leaf = MAT['leaf_oak'] if (dx + dy + dz) % 2 == 0 else MAT['leaf_azalea']
        c.set_block(cx + dx, y_ground + dy, cz + dz, leaf)

def build_zen_sand_garden(c, x1, y_ground, z1, x2, z2):
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)

    for x in range(xa, xb + 1):
        for z in range(za, zb + 1):
            if x in (xa, xb) or z in (za, zb):
                c.set_block(x, y_ground, z, MAT['wall_quartz'])
                c.set_block(x, y_ground + 1, z, MAT['slab_stone_b'])
            else:
                if (x + z) % 3 == 0:
                    c.set_block(x, y_ground, z, 'minecraft:smooth_sandstone')
                else:
                    c.set_block(x, y_ground, z, 'minecraft:sand')

    for lx in (xa + 2, xb - 2):
        for lz in (za + 2, zb - 2):
            c.set_block(lx, y_ground, lz, MAT['light_ochre'])
            c.set_block(lx, y_ground + 1, lz, MAT['slab_stone_b'])

    rx1, rz1 = xa + (xb - xa) // 3, za + (zb - za) // 2
    for dx, dy, dz, b in [
        (0, 1, 0, 'minecraft:tuff'), (-1, 1, 0, 'minecraft:andesite'), (1, 1, 0, 'minecraft:mossy_cobblestone'),
        (0, 1, 1, 'minecraft:tuff'), (0, 2, 0, 'minecraft:polished_tuff'), (-1, 1, 1, MAT['slab_and_b']),
    ]:
        c.set_block(rx1 + dx, y_ground + dy, rz1 + dz, b)

    rx2, rz2 = xb - 4, zb - 5
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            dist = abs(dx) + abs(dz)
            if dist <= 3:
                h = max(1, 4 - dist)
                for dy in range(1, h + 1):
                    c.set_block(rx2 + dx, y_ground + dy, rz2 + dz, 'minecraft:smooth_sandstone' if dy < h else 'minecraft:sandstone_slab[type=bottom,waterlogged=false]')

    bx, bz = xa + (xb - xa) // 2, za + 4
    c.set_block(bx, y_ground, bz, MAT['moss_block'])
    c.set_block(bx, y_ground + 1, bz, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
    c.set_block(bx, y_ground + 2, bz, MAT['leaf_azalea'])
    c.set_block(bx - 1, y_ground + 2, bz, MAT['leaf_oak'])
    c.set_block(bx + 1, y_ground + 2, bz, MAT['leaf_fl_azalea'])
    c.set_block(bx, y_ground + 2, bz + 1, MAT['leaf_azalea'])

def build_hedgerow_line(c, x1, y_ground, z1, x2, z2, height=2, gap_every=6):
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    if xb - xa >= zb - za:
        for i, x in enumerate(range(xa, xb + 1)):
            if gap_every and i > 0 and i < (xb - xa) and i % gap_every == 0:
                c.set_block(x, y_ground, za, MAT['stone_smooth'])
                continue
            c.set_block(x, y_ground, za, MAT['light_ochre'] if i % 4 == 2 else MAT['moss_block'])
            for hy in range(1, height + 1):
                leaf = MAT['leaf_azalea'] if (x + hy) % 2 == 0 else MAT['leaf_oak']
                c.set_block(x, y_ground + hy, za, leaf)
    else:
        for i, z in enumerate(range(za, zb + 1)):
            if gap_every and i > 0 and i < (zb - za) and i % gap_every == 0:
                c.set_block(xa, y_ground, z, MAT['stone_smooth'])
                continue
            c.set_block(xa, y_ground, z, MAT['light_ochre'] if i % 4 == 2 else MAT['moss_block'])
            for hy in range(1, height + 1):
                leaf = MAT['leaf_azalea'] if (z + hy) % 2 == 0 else MAT['leaf_oak']
                c.set_block(xa, y_ground + hy, z, leaf)

def build_spherical_shrub(c, cx, y_ground, cz, radius=1, tone='light'):
    leaf_main = MAT['leaf_azalea'] if tone == 'light' else MAT['leaf_dark_oak']
    leaf_sub = MAT['leaf_fl_azalea'] if tone == 'light' else MAT['leaf_spruce']
    c.set_block(cx, y_ground, cz, MAT['light_ochre'])
    c.set_block(cx, y_ground + 1, cz, 'minecraft:oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
    if radius == 1:
        for dx, dy, dz in [(0,1,0), (-1,1,0), (1,1,0), (0,1,-1), (0,1,1), (0,2,0)]:
            c.set_block(cx + dx, y_ground + dy, cz + dz, leaf_main if (dx+dz)%2==0 else leaf_sub)
    else:
        for dx in range(-2, 3):
            for dy in range(1, 4):
                for dz in range(-2, 3):
                    if dx*dx + (dy-2)*(dy-2) + dz*dz <= 4:
                        c.set_block(cx + dx, y_ground + dy, cz + dz, leaf_main if (dx+dy+dz)%2==0 else leaf_sub)

_TREE_BUILDING_GUARD = {
    'minecraft:white_concrete', 'minecraft:light_gray_concrete', 'minecraft:gray_concrete',
    'minecraft:black_concrete', 'minecraft:cyan_terracotta', 'minecraft:polished_deepslate',
    'minecraft:deepslate_tiles', 'minecraft:dark_oak_planks', 'minecraft:spruce_planks',
    'minecraft:birch_planks', 'minecraft:glass', 'minecraft:black_stained_glass',
    'minecraft:gray_stained_glass', 'minecraft:white_stained_glass', 'minecraft:cyan_stained_glass',
    'minecraft:light_blue_stained_glass', 'minecraft:glass_pane', 'minecraft:black_stained_glass_pane',
    'minecraft:gray_stained_glass_pane', 'minecraft:cyan_stained_glass_pane',
    'minecraft:dark_oak_door', 'minecraft:iron_door', 'minecraft:smooth_quartz',
    'minecraft:smooth_quartz_slab', 'minecraft:dark_oak_slab', 'minecraft:spruce_slab',
    'minecraft:smooth_quartz_stairs', 'minecraft:dark_oak_stairs', 'minecraft:spruce_stairs',
    'minecraft:stripped_dark_oak_wood', 'minecraft:stripped_spruce_wood',
    'minecraft:red_wool', 'minecraft:orange_wool', 'minecraft:yellow_wool', 'minecraft:cyan_wool',
    'minecraft:blue_wool', 'minecraft:pink_wool', 'minecraft:white_wool',
    'minecraft:red_concrete', 'minecraft:yellow_concrete', 'minecraft:blue_concrete',
}

def build_custom_tree(c, cx, y_ground, cz, height=10, style='oak_mix', seed=0, max_radius=4):

    for ty in range(y_ground + 1, y_ground + height + 1):
        for tdx in (-1, 0, 1):
            for tdz in (-1, 0, 1):
                if c.get_block_name(cx + tdx, ty, cz + tdz) in _TREE_BUILDING_GUARD:
                    return

    rng = random.Random(seed ^ (cx * 73856093) ^ (cz * 19349663))
    if style == 'oak_mix':
        trunk = 'minecraft:dark_oak_log[axis=y]'
        leaves = [MAT['leaf_oak'], MAT['leaf_azalea'], MAT['leaf_dark_oak']]
    elif style == 'ornamental':
        trunk = 'minecraft:cherry_log[axis=y]'
        leaves = [MAT['leaf_cherry'], MAT['leaf_fl_azalea'], MAT['leaf_azalea']]
    elif style == 'birch_mix':
        trunk = 'minecraft:birch_log[axis=y]'
        leaves = [MAT['leaf_birch'], MAT['leaf_oak'], MAT['leaf_azalea']]
    else:
        trunk = 'minecraft:spruce_log[axis=y]'
        leaves = [MAT['leaf_spruce'], MAT['leaf_dark_oak'], MAT['leaf_oak']]

    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if dx*dx + dz*dz <= 5:
                b_cur = c.get_block_name(cx + dx, y_ground, cz + dz)
                if b_cur in ('minecraft:grass_block', 'minecraft:dirt', 'minecraft:moss_block'):
                    c.set_block(cx + dx, y_ground, cz + dz, MAT['moss_block'] if rng.random() < 0.4 else MAT['grass_block'])
                    if (dx != 0 or dz != 0) and c.get_block_name(cx + dx, y_ground + 1, cz + dz) == 'minecraft:air':
                        if rng.random() < 0.45:
                            c.set_block(cx + dx, y_ground + 1, cz + dz, rng.choice([
                                'minecraft:pink_petals[facing=north,flower_amount=3]',
                                'minecraft:short_grass',
                                'minecraft:azure_bluet',
                            ]))

    trunk_top = y_ground + height - 2
    c.fill(cx, y_ground + 1, cz, cx, trunk_top, cz, trunk)

    canopy_base = y_ground + max(4, height // 2)
    for y in range(canopy_base, y_ground + height + 2):
        rel = (y - canopy_base) / max(1, (y_ground + height + 1 - canopy_base))
        rad = min(max_radius, int(round(3.4 * math.sin(rel * math.pi) + 1.2)))
        for dx in range(-rad, rad + 1):
            for dz in range(-rad, rad + 1):
                dist_sq = dx*dx + dz*dz
                if dist_sq <= rad*rad + (1 if rng.random() < 0.35 and rad < max_radius else 0):
                    if dx == 0 and dz == 0 and y <= trunk_top:
                        continue
                    lx, lz = cx + dx, cz + dz
                    if c.get_block_name(lx, y, lz) != 'minecraft:air':
                        continue

                    near_arch = False
                    for nx, ny, nz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                        if c.get_block_name(lx + nx, y + ny, lz + nz) in _TREE_BUILDING_GUARD:
                            near_arch = True
                            break
                    if not near_arch:
                        c.set_block(lx, y, lz, rng.choice(leaves))

def build_patio_umbrella(c, cx, y_ground, cz, canopy_mat=None):
    canopy_mat = canopy_mat or MAT['slab_quartz_b']
    c.fill(cx, y_ground + 1, cz, cx, y_ground + 3, cz, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
    c.set_block(cx, y_ground + 2, cz, 'minecraft:white_carpet')
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) == 2 and abs(dz) == 2:
                continue
            c.set_block(cx + dx, y_ground + 4, cz + dz, canopy_mat)
    c.set_block(cx, y_ground + 4, cz, MAT['wall_quartz'])
    c.set_block(cx, y_ground + 5, cz, MAT['slab_quartz_b'])
    c.set_block(cx, y_ground + 3, cz, MAT['light_ochre'])

def build_sun_lounger(c, x, y_ground, z, facing='north'):
    if facing == 'north':
        c.set_block(x, y_ground + 1, z, MAT['slab_quartz_b'])
        c.set_block(x, y_ground + 1, z + 1, stair('smooth_quartz', 'south', 'bottom'))
        c.set_block(x, y_ground + 1, z + 2, trapdoor('dark_oak', 'south', 'bottom', 'false'))
    elif facing == 'south':
        c.set_block(x, y_ground + 1, z, MAT['slab_quartz_b'])
        c.set_block(x, y_ground + 1, z - 1, stair('smooth_quartz', 'north', 'bottom'))
        c.set_block(x, y_ground + 1, z - 2, trapdoor('dark_oak', 'north', 'bottom', 'false'))
    elif facing == 'east':
        c.set_block(x, y_ground + 1, z, MAT['slab_quartz_b'])
        c.set_block(x - 1, y_ground + 1, z, stair('smooth_quartz', 'west', 'bottom'))
    else:
        c.set_block(x, y_ground + 1, z, MAT['slab_quartz_b'])
        c.set_block(x + 1, y_ground + 1, z, stair('smooth_quartz', 'east', 'bottom'))

def build_outdoor_sofa(c, x1, y_ground, z1, length=5, facing='north'):
    if facing in ('north', 'south'):
        seat_dir = 'south' if facing == 'north' else 'north'
        for i in range(length):
            if i % 2 == 1:
                c.set_block(x1 + i, y_ground, z1, MAT['light_ochre'])
            c.set_block(x1 + i, y_ground + 1, z1, stair('smooth_quartz', seat_dir, 'bottom'))
        c.set_block(x1 - 1, y_ground + 1, z1, trapdoor('dark_oak', 'west', 'bottom', 'true'))
        c.set_block(x1 + length, y_ground + 1, z1, trapdoor('dark_oak', 'east', 'bottom', 'true'))
        tz = z1 - 2 if facing == 'north' else z1 + 2
        for i in range(1, length - 1):
            c.set_block(x1 + i, y_ground, tz, MAT['light_ochre'] if i == length // 2 else MAT['wood_dark'])
            c.set_block(x1 + i, y_ground + 1, tz, MAT['slab_dark_b'])
        c.set_block(x1 + length // 2, y_ground + 2, tz, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    else:
        seat_dir = 'east' if facing == 'west' else 'west'
        for i in range(length):
            if i % 2 == 1:
                c.set_block(x1, y_ground, z1 + i, MAT['light_ochre'])
            c.set_block(x1, y_ground + 1, z1 + i, stair('smooth_quartz', seat_dir, 'bottom'))
        c.set_block(x1, y_ground + 1, z1 - 1, trapdoor('dark_oak', 'north', 'bottom', 'true'))
        c.set_block(x1, y_ground + 1, z1 + length, trapdoor('dark_oak', 'south', 'bottom', 'true'))

def build_outdoor_bar(c, x1, y_ground, z1, length=6):
    for i in range(length):
        bx = x1 + i
        c.set_block(bx, y_ground, z1, MAT['light_ochre'] if i % 2 == 0 else MAT['wood_dark'])
        c.set_block(bx, y_ground + 1, z1, MAT['wood_dark'])
        c.set_block(bx, y_ground + 2, z1, MAT['slab_quartz_b'])
        if i % 2 == 0:
            c.set_block(bx, y_ground, z1 - 2, MAT['light_ochre'])
            c.set_block(bx, y_ground + 1, z1 - 2, 'minecraft:dark_oak_fence[north=false,south=false,east=false,west=false,waterlogged=false]')
            c.set_block(bx, y_ground + 2, z1 - 2, 'minecraft:white_carpet')
    for i in range(length):
        bx = x1 + i
        if i in (1, 4):
            place_barrel(c, bx, y_ground + 1, z1 + 2, facing='north')
            c.set_block(bx, y_ground + 2, z1 + 2, MAT['light_ochre'])
        else:
            c.set_block(bx, y_ground + 1, z1 + 2, MAT['wall_quartz'])
            c.set_block(bx, y_ground + 2, z1 + 2, 'minecraft:bookshelf')
        c.set_block(bx, y_ground + 3, z1 + 2, MAT['slab_dark_b'])
    place_brewing_stand(c, x1 + 2, y_ground + 2, z1)
    c.set_block(x1 + 4, y_ground + 2, z1, 'minecraft:flower_pot')

def build_seed_variant_outbuilding(c, x1, y_ground, z1, w, d, h, seed, role='casita'):
    rng = random.Random(seed)
    x2, z2 = x1 + w - 1, z1 + d - 1
    y_top = y_ground + h

    roof_copings = [MAT['slab_quartz_b'], MAT['slab_stone_b'], MAT['slab_and_b'], MAT['slab_dark_b']]
    accent_walls = [MAT['wall_lgray'], MAT['stone_pol_and'], MAT['wall_quartz'], MAT['wood_dark']]
    glass_choices = [MAT['glass_black'], MAT['glass_gray'], MAT['glass_clear']]

    coping = rng.choice(roof_copings)
    accent = rng.choice(accent_walls)
    glass = rng.choice(glass_choices)
    win_style = seed % 3

    c.fill(x1, y_ground, z1, x2, y_ground, z2, MAT['wood_warm'])
    c.fill(x1, y_ground + 1, z1, x2, y_top - 1, z2, MAT['wall_white'])
    c.fill(x1 + 1, y_ground + 1, z1 + 1, x2 - 1, y_top - 1, z2 - 1, 'minecraft:air')

    for cx_p in (x1, x2):
        for cz_p in (z1, z2):
            c.fill(cx_p, y_ground + 1, cz_p, cx_p, y_top - 1, cz_p, accent)

    if win_style == 0:
        if x2 - x1 >= 5:
            build_curtain_wall(c, x1 + 2, y_ground + 1, z2, x2 - 2, y_top - 2, z2, glass, glass, accent, bay_width=3)
        if z2 - z1 >= 5:
            build_curtain_wall(c, x1, y_ground + 1, z1 + 2, x1, y_top - 2, z2 - 2, glass, glass, accent, bay_width=3)
            build_curtain_wall(c, x2, y_ground + 1, z1 + 2, x2, y_top - 2, z2 - 2, glass, glass, accent, bay_width=3)
    elif win_style == 1:
        c.fill(x1 + 1, y_ground + 2, z2, x2 - 1, y_ground + 3, z2, glass)
        c.fill(x1, y_ground + 2, z1 + 1, x1, y_ground + 3, z2 - 1, glass)
        c.fill(x2, y_ground + 2, z1 + 1, x2, y_ground + 3, z2 - 1, glass)
    else:
        build_slatted_feature_wall(c, x1 + 1, y_ground + 1, z2, x2 - 1, y_top - 1, z2, MAT['wall_white'], glass)
        build_slatted_feature_wall(c, x1, y_ground + 1, z1 + 1, x1, y_top - 1, z2 - 1, MAT['wall_white'], glass)
        build_slatted_feature_wall(c, x2, y_ground + 1, z1 + 1, x2, y_top - 1, z2 - 1, MAT['wall_white'], glass)

    mx, mz = (x1 + x2) // 2, (z1 + z2) // 2
    c.fill(x1 + 2, y_ground + 1, z1, x2 - 2, y_top - 2, z1, glass)
    place_door(c, mx, y_ground + 1, z1, 'dark_oak', 'south', 'right', 'false')
    c.set_block(mx, y_ground, z1 - 1, MAT['stone_smooth'])

    build_flat_roof_and_eaves(c, x1, y_top, z1, x2, z2, overhang=1, roof_mat=MAT['wall_white'],
                              soffit_mat=MAT['wood_dark'], coping_slab=coping, hidden_lights=True)
    build_recessed_ceiling_grid(c, x1 + 2, y_top, z1 + 2, x2 - 2, z2 - 2, step_x=3, step_z=3, light_mat=MAT['light_ochre'])

    if w >= 7 and d >= 7:
        build_illuminated_carpet_rug(c, x1 + 2, y_ground, z1 + 2, x2 - 2, z2 - 2, MAT['carpet_white'], MAT['carpet_lgray'])
    c.set_block(mx, y_top - 1, mz, MAT['lantern_hang'])

    if role == 'tool_house':
        place_barrel(c, x1 + 1, y_ground + 1, z2 - 1, 'north')
        place_barrel(c, x1 + 2, y_ground + 1, z2 - 1, 'north')
        c.set_block(x2 - 1, y_ground + 1, z2 - 1, 'minecraft:crafting_table')
        c.set_block(x2 - 1, y_ground + 1, z1 + 1, 'minecraft:smithing_table')
        c.set_block(x1 + 1, y_ground + 2, z2 - 1, MAT['lantern_stand'])
    elif role == 'art_pavilion':
        c.set_block(mx, y_ground + 1, mz, MAT['wall_quartz'])
        c.set_block(mx, y_ground + 2, mz, MAT['light_ochre'])
        c.set_block(mx, y_ground + 3, mz, MAT['slab_quartz_b'])
        c.fill(x1 + 1, y_ground + 1, z2 - 1, min(x1 + 4, x2 - 1), y_ground + 2, z2 - 1, 'minecraft:bookshelf')
        build_floor_lamp(c, x1 + 1, y_ground, z1 + 1, 'modern')
        build_floor_lamp(c, x2 - 1, y_ground, z2 - 1, 'modern')
    else:
        place_bed(c, x1 + 1, y_ground + 1, z2 - 2, facing='south', color='white')
        c.set_block(x2 - 1, y_ground + 1, z2 - 1, 'minecraft:bookshelf')
        c.set_block(x2 - 1, y_ground + 2, z2 - 1, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
        c.set_block(x2 - 2, y_ground + 1, z2 - 1, stair('smooth_quartz', 'north', 'bottom'))
        if w >= 12:
            build_floor_lamp(c, x2 - 1, y_ground, z1 + 1, 'modern')
            place_bed(c, x2 - 2, y_ground + 1, z2 - 2, facing='south', color='white')

def build_executive_helicopter(c, cx, y_pad, cz):
    for sz in (cz - 2, cz + 2):
        c.fill(cx - 3, y_pad + 1, sz, cx + 2, y_pad + 1, sz, MAT['slab_deep_b'])
        c.set_block(cx - 4, y_pad + 1, sz, trapdoor('dark_oak', 'west', 'bottom', 'false'))
        c.set_block(cx - 2, y_pad + 1, sz - (1 if sz > cz else -1), MAT['iron_bars'])
        c.set_block(cx + 1, y_pad + 1, sz - (1 if sz > cz else -1), MAT['iron_bars'])

    c.fill(cx - 4, y_pad + 2, cz - 1, cx + 2, y_pad + 2, cz + 1, MAT['wall_quartz'])
    c.set_block(cx - 5, y_pad + 2, cz, stair('smooth_quartz', 'east', 'top'))
    c.set_block(cx - 5, y_pad + 2, cz - 1, MAT['slab_quartz_t'])
    c.set_block(cx - 5, y_pad + 2, cz + 1, MAT['slab_quartz_t'])
    c.set_block(cx, y_pad + 2, cz, MAT['light_ochre'])

    c.fill(cx - 4, y_pad + 3, cz - 1, cx - 3, y_pad + 3, cz + 1, MAT['glass_black'])
    c.set_block(cx - 5, y_pad + 3, cz, MAT['glass_black'])
    c.set_block(cx - 3, y_pad + 3, cz, MAT['light_sea'])
    c.set_block(cx - 2, y_pad + 3, cz - 1, stair('smooth_quartz', 'west', 'bottom'))
    c.set_block(cx - 2, y_pad + 3, cz + 1, stair('smooth_quartz', 'west', 'bottom'))
    c.set_block(cx - 2, y_pad + 3, cz, MAT['light_ochre'])
    for x in range(cx - 1, cx + 3):
        c.set_block(x, y_pad + 3, cz - 1, MAT['glass_black'] if x <= cx + 1 else MAT['wall_white'])
        c.set_block(x, y_pad + 3, cz + 1, MAT['glass_black'] if x <= cx + 1 else MAT['wall_white'])
        c.set_block(x, y_pad + 4, cz - 1, MAT['wall_white'])
        c.set_block(x, y_pad + 4, cz + 1, MAT['wall_white'])
        c.set_block(x, y_pad + 4, cz, MAT['wall_white'])
    c.fill(cx - 3, y_pad + 4, cz - 1, cx - 2, y_pad + 4, cz + 1, MAT['slab_quartz_b'])

    c.fill(cx - 1, y_pad + 5, cz - 1, cx + 1, y_pad + 5, cz + 1, MAT['stone_pol_and'])
    c.set_block(cx + 2, y_pad + 5, cz - 1, MAT['light_ochre'])
    c.set_block(cx + 2, y_pad + 5, cz + 1, MAT['light_ochre'])
    c.set_block(cx + 2, y_pad + 5, cz, MAT['frame_dark'])

    c.fill(cx + 3, y_pad + 3, cz, cx + 6, y_pad + 3, cz, MAT['wall_white'])
    c.fill(cx + 3, y_pad + 4, cz, cx + 8, y_pad + 4, cz, MAT['wall_white'])
    c.set_block(cx + 7, y_pad + 4, cz - 1, MAT['slab_deep_b'])
    c.set_block(cx + 7, y_pad + 4, cz + 1, MAT['slab_deep_b'])
    c.set_block(cx + 7, y_pad + 4, cz - 2, MAT['end_rod_n'])
    c.set_block(cx + 7, y_pad + 4, cz + 2, MAT['end_rod_s'])
    c.set_block(cx + 8, y_pad + 5, cz, MAT['wall_white'])
    c.set_block(cx + 9, y_pad + 5, cz, stair('smooth_quartz', 'west', 'bottom'))
    c.set_block(cx + 9, y_pad + 6, cz, MAT['end_rod_up'])
    c.set_block(cx + 8, y_pad + 5, cz - 1, MAT['iron_bars'])
    c.set_block(cx + 7, y_pad + 5, cz - 1, MAT['iron_trap_b'])
    c.set_block(cx + 9, y_pad + 5, cz - 1, MAT['iron_trap_b'])

    c.set_block(cx, y_pad + 6, cz, MAT['frame_dark'])
    c.set_block(cx, y_pad + 7, cz, MAT['slab_quartz_b'])
    for r in range(1, 9):
        mat_blade = MAT['slab_deep_t'] if r % 2 == 1 else MAT['iron_trap_t']
        c.set_block(cx - r, y_pad + 6, cz, mat_blade)
        c.set_block(cx + r, y_pad + 6, cz, mat_blade)
        c.set_block(cx, y_pad + 6, cz - r, mat_blade)
        c.set_block(cx, y_pad + 6, cz + r, mat_blade)
    for tx, tz in [(cx - 8, cz), (cx + 8, cz), (cx, cz - 8), (cx, cz + 8)]:
        c.set_block(tx, y_pad + 6, tz, MAT['end_rod_up'])

def build_windsock_tower(c, x, y_ground, z):
    c.set_block(x, y_ground + 1, z, MAT['stone_pol_and'])
    c.set_block(x, y_ground + 2, z, MAT['wall_deep_post'])
    c.fill(x, y_ground + 3, z, x, y_ground + 8, z, MAT['iron_bars'])
    c.set_block(x, y_ground + 9, z, MAT['light_ochre'])
    c.set_block(x, y_ground + 10, z, MAT['end_rod_up'])
    c.set_block(x + 1, y_ground + 8, z, MAT['orange_wool'])
    c.set_block(x + 2, y_ground + 8, z, MAT['white_wool'])
    c.set_block(x + 3, y_ground + 8, z, MAT['light_shroom'])
    c.set_block(x + 4, y_ground + 7, z, MAT['orange_wool'])
    c.set_block(x + 5, y_ground + 7, z, MAT['white_wool'])

def build_golf_flag_and_cup(c, cx, y_green, cz, hole_num=1):
    c.set_block(cx, y_green - 1, cz, MAT['light_sea'])
    c.set_block(cx, y_green, cz, 'minecraft:cauldron')
    c.fill(cx, y_green + 1, cz, cx, y_green + 4, cz, MAT['end_rod_up'])
    flag_color = MAT['red_concrete'] if hole_num % 2 == 1 else MAT['yellow_concrete']
    c.set_block(cx + 1, y_green + 4, cz, flag_color)
    c.set_block(cx + 2, y_green + 4, cz, MAT['wall_white'])
    c.set_block(cx + 1, y_green + 5, cz, MAT['slab_quartz_b'])

def build_golf_cart(c, x, y_ground, z, facing='north'):
    if facing in ('north', 'south'):
        for wx in (x - 1, x + 1):
            for wz in (z - 1, z + 1):
                c.set_block(wx, y_ground + 1, wz, MAT['wall_black'])
        c.fill(x - 1, y_ground + 1, z, x + 1, y_ground + 1, z, MAT['slab_quartz_t'])
        c.set_block(x, y_ground + 1, z - 1, MAT['light_ochre'])
        c.set_block(x, y_ground + 1, z + 1, MAT['wall_quartz'])
        seat_dir = 'south' if facing == 'north' else 'north'
        c.set_block(x - 1, y_ground + 2, z, stair('smooth_quartz', seat_dir, 'bottom'))
        c.set_block(x + 1, y_ground + 2, z, stair('smooth_quartz', seat_dir, 'bottom'))
        c.set_block(x, y_ground + 2, z, MAT['slab_quartz_b'])
        for wx in (x - 1, x + 1):
            for wz in (z - 1, z + 1):
                c.set_block(wx, y_ground + 2, wz, MAT['iron_bars'])
                c.set_block(wx, y_ground + 3, wz, MAT['iron_bars'])
        c.fill(x - 1, y_ground + 4, z - 1, x + 1, y_ground + 4, z + 1, MAT['slab_quartz_b'])
    else:
        for wx in (x - 1, x + 1):
            for wz in (z - 1, z + 1):
                c.set_block(wx, y_ground + 1, wz, MAT['wall_black'])
        c.fill(x, y_ground + 1, z - 1, x, y_ground + 1, z + 1, MAT['slab_quartz_t'])
        c.set_block(x - 1, y_ground + 1, z, MAT['light_ochre'])
        c.set_block(x + 1, y_ground + 1, z, MAT['wall_quartz'])
        seat_dir = 'east' if facing == 'west' else 'west'
        c.set_block(x, y_ground + 2, z - 1, stair('smooth_quartz', seat_dir, 'bottom'))
        c.set_block(x, y_ground + 2, z + 1, stair('smooth_quartz', seat_dir, 'bottom'))
        c.set_block(x, y_ground + 2, z, MAT['slab_quartz_b'])
        for wx in (x - 1, x + 1):
            for wz in (z - 1, z + 1):
                c.set_block(wx, y_ground + 2, wz, MAT['iron_bars'])
                c.set_block(wx, y_ground + 3, wz, MAT['iron_bars'])
        c.fill(x - 1, y_ground + 4, z - 1, x + 1, y_ground + 4, z + 1, MAT['slab_quartz_b'])

def build_golf_gazebo(c, cx, y_ground, cz):
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            if abs(dx) + abs(dz) <= 6:
                c.set_block(cx + dx, y_ground, cz + dz, MAT['wall_quartz'] if (dx + dz) % 2 == 0 else MAT['stone_dio'])
                c.set_block(cx + dx, y_ground + 4, cz + dz, MAT['wood_dark'])
                c.set_block(cx + dx, y_ground + 5, cz + dz, MAT['slab_quartz_b'])
    for dx in (-3, 3):
        for dz in (-3, 3):
            c.set_block(cx + dx, y_ground + 1, cz + dz, MAT['stone_pol_and'])
            c.fill(cx + dx, y_ground + 2, cz + dz, cx + dx, y_ground + 4, cz + dz, MAT['beam_dark_y'])
            c.set_block(cx + dx, y_ground + 4, cz + dz, MAT['light_ochre'])
    c.fill(cx - 2, y_ground + 5, cz - 2, cx + 2, y_ground + 5, cz + 2, MAT['wall_white'])
    c.set_block(cx, y_ground + 4, cz, MAT['light_ochre'])
    c.set_block(cx, y_ground + 3, cz, MAT['lantern_hang'])
    c.set_block(cx, y_ground + 1, cz, MAT['wall_quartz'])
    c.set_block(cx, y_ground + 2, cz, 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]')
    c.set_block(cx - 2, y_ground + 1, cz, stair('smooth_quartz', 'west', 'bottom'))
    c.set_block(cx + 2, y_ground + 1, cz, stair('smooth_quartz', 'east', 'bottom'))

def build_arched_canal_bridge(c, cx, y_ground, cz, width=5, span=14, axis='z'):
    half_w = width // 2
    half_s = span // 2
    if axis == 'z':
        for dz in range(-half_s, half_s + 1):
            z = cz + dz
            t = 1.0 - (abs(dz) / max(1, half_s)) ** 2
            arch_h = int(round(t * 1.6))
            y_deck = y_ground + arch_h
            for dx in range(-half_w, half_w + 1):
                x = cx + dx
                c.fill(x, y_deck + 1, z, x, y_deck + 5, z, 'minecraft:air')
                if abs(dx) == half_w:
                    c.set_block(x, y_deck, z, MAT['wall_quartz'])
                    c.set_block(x, y_deck + 1, z, MAT['pane_black'])
                    if dz % 3 == 0:
                        c.set_block(x, y_deck + 1, z, MAT['wall_quartz'])
                        c.set_block(x, y_deck + 2, z, MAT['lantern_stand'])
                else:
                    if dx == 0 and dz % 3 == 0:
                        c.set_block(x, y_deck, z, MAT['light_ochre'])
                    else:
                        c.set_block(x, y_deck, z, MAT['slab_dark_t'] if arch_h > 0 else MAT['wood_dark'])
    else:
        for dx in range(-half_s, half_s + 1):
            x = cx + dx
            t = 1.0 - (abs(dx) / max(1, half_s)) ** 2
            arch_h = int(round(t * 1.6))
            y_deck = y_ground + arch_h
            for dz in range(-half_w, half_w + 1):
                z = cz + dz
                c.fill(x, y_deck + 1, z, x, y_deck + 5, z, 'minecraft:air')
                if abs(dz) == half_w:
                    c.set_block(x, y_deck, z, MAT['wall_quartz'])
                    c.set_block(x, y_deck + 1, z, MAT['pane_black'])
                    if dx % 3 == 0:
                        c.set_block(x, y_deck + 1, z, MAT['wall_quartz'])
                        c.set_block(x, y_deck + 2, z, MAT['lantern_stand'])
                else:
                    if dz == 0 and dx % 3 == 0:
                        c.set_block(x, y_deck, z, MAT['light_ochre'])
                    else:
                        c.set_block(x, y_deck, z, MAT['slab_dark_t'] if arch_h > 0 else MAT['wood_dark'])

def build_smart_greenhouse(c, x1, y_ground, z1, x2, z2, variant='hydro_veg'):
    xa, xb = min(x1, x2), max(x1, x2)
    za, zb = min(z1, z2), max(z1, z2)
    mx, mz = (xa + xb) // 2, (za + zb) // 2
    y_wall_top = y_ground + 4
    y_ridge = y_ground + 7

    for x in range(xa, xb + 1):
        for z in range(za, zb + 1):
            c.set_block(x, y_ground, z, MAT['stone_smooth'] if (x + z) % 2 == 0 else MAT['wall_quartz'])
            c.fill(x, y_ground + 1, z, x, y_ridge + 1, z, 'minecraft:air')

    for x in range(xa, xb + 1):
        is_rib = (x == xa or x == xb or (x - xa) % 4 == 0)
        for z in (za, zb):
            c.set_block(x, y_ground + 1, z, MAT['wall_quartz'])
            for y in range(y_ground + 2, y_wall_top + 1):
                c.set_block(x, y, z, MAT['frame_dark'] if is_rib else MAT['glass_clear'])

        for z in range(za, zb + 1):
            rel_z = abs(z - mz) / max(1.0, (zb - za) / 2.0)
            arch_dy = int(round((1.0 - rel_z * rel_z) * 3.0))
            ry = y_wall_top + arch_dy
            if is_rib:
                c.set_block(x, ry, z, MAT['frame_dark'])
                if abs(z - mz) <= 1:
                    c.set_block(x, ry + 1, z, MAT['slab_quartz_b'])
            else:
                if z == mz:
                    c.set_block(x, ry, z, MAT['light_ochre'] if x % 3 == 0 else MAT['wall_quartz'])
                else:
                    c.set_block(x, ry, z, MAT['glass_clear'] if (x + z) % 2 == 0 else MAT['glass_gray'])

    for gx in (xa, xb):
        for z in range(za, zb + 1):
            rel_z = abs(z - mz) / max(1.0, (zb - za) / 2.0)
            arch_dy = int(round((1.0 - rel_z * rel_z) * 3.0))
            ry = y_wall_top + arch_dy
            c.set_block(gx, y_ground + 1, z, MAT['wall_quartz'])
            for y in range(y_ground + 2, ry):
                if z in (za, zb, mz - 2, mz + 2):
                    c.set_block(gx, y, z, MAT['frame_dark'])
                else:
                    c.set_block(gx, y, z, MAT['glass_clear'])
        c.fill(gx, y_ground + 1, mz - 1, gx, y_ground + 3, mz + 1, 'minecraft:air')

    for x in range(xa + 3, xb - 2, 4):
        for z in (za + 3, mz, zb - 3):
            c.set_block(x, y_wall_top + 1, z, MAT['light_shroom'] if z != mz else MAT['light_ochre'])
            c.set_block(x - 1, y_wall_top + 1, z, MAT['end_rod_w'])
            c.set_block(x + 1, y_wall_top + 1, z, MAT['end_rod_e'])
        if variant == 'aeroponic_berry':
            c.set_block(x, y_wall_top + 1, mz - 2, 'minecraft:cave_vines_plant[berries=true]')
            c.set_block(x, y_wall_top, mz - 2, 'minecraft:cave_vines[age=22,berries=true]')
            c.set_block(x, y_wall_top + 1, mz + 2, 'minecraft:cave_vines_plant[berries=true]')
            c.set_block(x, y_wall_top, mz + 2, 'minecraft:cave_vines[age=22,berries=true]')

    crops = [MAT['wheat_full'], MAT['carrots_full'], MAT['potatoes_full'], MAT['beetroots_full']]
    for band_idx, (bz1, bz2) in enumerate([(za + 2, mz - 2), (mz + 2, zb - 2)]):
        if bz2 < bz1:
            continue
        b_mid = (bz1 + bz2) // 2
        for x in range(xa + 2, xb - 1):
            for z in range(bz1, bz2 + 1):
                if z == b_mid:
                    c.set_block(x, y_ground - 1, z, MAT['light_sea'])
                    c.set_block(x, y_ground, z, MAT['water'])
                    c.set_block(x, y_ground + 1, z, 'minecraft:lily_pad' if x % 5 == 0 else 'minecraft:air')
                else:
                    c.set_block(x, y_ground, z, MAT['farmland_wet'] if variant != 'orchid_nursery' else MAT['moss_block'])
                    if variant == 'hydro_veg':
                        crop = crops[(x + z + band_idx) % len(crops)]
                        c.set_block(x, y_ground + 1, z, crop)
                    elif variant == 'aeroponic_berry':
                        if (x - xa) % 5 == 0 and z in (bz1 + 1, bz2 - 1):
                            c.set_block(x, y_ground, z, MAT['light_sea'])
                            c.set_block(x, y_ground + 1, z, MAT['moss_block'])
                            c.set_block(x, y_ground + 2, z, MAT['leaf_fl_azalea'])
                            c.set_block(x, y_ground + 3, z, MAT['light_verdant'])
                            c.set_block(x, y_ground + 4, z, MAT['slab_quartz_b'])
                        else:
                            c.set_block(x, y_ground + 1, z, MAT['sweet_berry_full'] if (x + z) % 2 == 0 else MAT['carrots_full'])
                    else:
                        if x % 4 == 0 and z == bz1:
                            c.set_block(x, y_ground + 1, z, MAT['melon_block'] if (x // 4) % 2 == 0 else MAT['pumpkin_block'])
                        else:
                            c.set_block(x, y_ground + 1, z, SOFT_FLOWERS[(x * 3 + z) % len(SOFT_FLOWERS)])

    c.set_block(xa + 2, y_ground + 1, mz - 1, 'minecraft:water_cauldron[level=3]')
    place_lectern(c, xa + 2, y_ground + 1, mz + 1, 'east')
    c.set_block(xb - 2, y_ground + 1, mz - 1, 'minecraft:composter[level=6]')
    place_barrel(c, xb - 2, y_ground + 1, mz + 1, 'west')

def build_irrigation_boom(c, x1, y_ground, x2, z_pos):
    xa, xb = min(x1, x2), max(x1, x2)
    for tx in (xa, xb):
        c.set_block(tx, y_ground + 1, z_pos - 1, MAT['wall_black'])
        c.set_block(tx, y_ground + 1, z_pos + 1, MAT['wall_black'])
        c.fill(tx, y_ground + 1, z_pos, tx, y_ground + 4, z_pos, MAT['stone_pol_and'])
        c.set_block(tx, y_ground + 5, z_pos, MAT['light_ochre'])
        c.set_block(tx, y_ground + 6, z_pos, MAT['slab_quartz_b'])
    for x in range(xa + 1, xb):
        c.set_block(x, y_ground + 4, z_pos, MAT['slab_quartz_t'] if x % 2 == 0 else MAT['iron_bars'])
        if (x - xa) % 3 == 0:
            c.set_block(x, y_ground + 3, z_pos, MAT['end_rod_down'])
        if (x - xa) % 6 == 0:
            c.set_block(x, y_ground + 4, z_pos, MAT['light_ochre'])

def build_cylindrical_silo(c, cx, y_ground, cz, radius=4, height=18):
    y_top = y_ground + height
    for y in range(y_ground + 1, y_top):
        is_ring = ((y - y_ground) % 5 == 0)
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                d2 = dx*dx + dz*dz
                if (radius - 1)**2 < d2 <= radius**2 + 1:
                    if is_ring:
                        c.set_block(cx + dx, y, cz + dz, MAT['stone_pol_and'])
                    elif dx == 0 or dz == 0:
                        c.set_block(cx + dx, y, cz + dz, MAT['wall_white'])
                    else:
                        c.set_block(cx + dx, y, cz + dz, MAT['wall_lgray'] if (dx + dz + y) % 2 == 0 else MAT['wall_quartz'])
                elif d2 <= (radius - 1)**2:
                    if y <= y_ground + 4:
                        c.set_block(cx + dx, y, cz + dz, MAT['hay_y'])
                    elif y == y_top - 1:
                        c.set_block(cx + dx, y, cz + dz, MAT['light_ochre'])
                    else:
                        c.set_block(cx + dx, y, cz + dz, 'minecraft:air')

    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            d2 = dx*dx + dz*dz
            if d2 <= radius**2 + 1:
                c.set_block(cx + dx, y_top, cz + dz, MAT['slab_quartz_b'])
            if d2 <= (radius - 2)**2:
                c.set_block(cx + dx, y_top, cz + dz, MAT['wall_white'])
                c.set_block(cx + dx, y_top + 1, cz + dz, MAT['slab_quartz_b'])
    c.set_block(cx, y_top + 1, cz, MAT['light_ochre'])
    c.set_block(cx, y_top + 2, cz, MAT['end_rod_up'])

def build_modern_windmill_tower(c, cx, y_ground, cz, height=22):
    y_hub = y_ground + height - 3
    for y in range(y_ground + 1, y_hub + 2):
        rad = 3 if y < y_ground + 7 else (2 if y < y_ground + 14 else 1)
        for dx in range(-rad, rad + 1):
            for dz in range(-rad, rad + 1):
                if abs(dx) == rad or abs(dz) == rad:
                    if rad == 1 or abs(dx) + abs(dz) < 2 * rad:
                        mat = MAT['stone_pol_and'] if y < y_ground + 5 else (MAT['light_ochre'] if (y - y_ground) % 5 == 0 else MAT['wall_white'])
                        c.set_block(cx + dx, y, cz + dz, mat)

    c.fill(cx - 1, y_hub - 1, cz - 1, cx + 2, y_hub + 1, cz + 1, MAT['wall_white'])
    c.fill(cx - 1, y_hub + 2, cz - 1, cx + 2, y_hub + 2, cz + 1, MAT['slab_quartz_b'])
    c.set_block(cx + 3, y_hub, cz, MAT['frame_dark'])
    c.set_block(cx + 4, y_hub, cz, MAT['light_ochre'])

    for r in range(1, 9):
        c.set_block(cx + 3, y_hub + r, cz, MAT['beam_dark_y'])
        c.set_block(cx + 3, y_hub + r, cz + 1, MAT['wall_quartz'] if r % 2 == 0 else MAT['pane_white'])
        c.set_block(cx + 3, y_hub - r, cz, MAT['beam_dark_y'])
        c.set_block(cx + 3, y_hub - r, cz - 1, MAT['wall_quartz'] if r % 2 == 0 else MAT['pane_white'])
        c.set_block(cx + 3, y_hub, cz + r, MAT['beam_dark_z'])
        c.set_block(cx + 3, y_hub - 1, cz + r, MAT['wall_quartz'] if r % 2 == 0 else MAT['pane_white'])
        c.set_block(cx + 3, y_hub, cz - r, MAT['beam_dark_z'])
        c.set_block(cx + 3, y_hub + 1, cz - r, MAT['wall_quartz'] if r % 2 == 0 else MAT['pane_white'])

def build_farm_tractor(c, x, y_ground, z):
    for tz in (z - 2, z + 2):
        c.fill(x - 2, y_ground + 1, tz, x - 1, y_ground + 2, tz, MAT['wall_black'])
        c.set_block(x + 2, y_ground + 1, tz, MAT['wall_black'])
    c.fill(x - 2, y_ground + 1, z - 1, x + 2, y_ground + 1, z + 1, MAT['frame_dark'])
    c.fill(x, y_ground + 2, z - 1, x + 2, y_ground + 2, z + 1, MAT['green_concrete'])
    c.set_block(x + 3, y_ground + 2, z, MAT['light_ochre'])
    c.set_block(x + 1, y_ground + 3, z + 1, MAT['wall_deep_post'])
    c.set_block(x - 1, y_ground + 2, z, stair('smooth_quartz', 'west', 'bottom'))
    for cx_cab in (x - 2, x - 1):
        for cz_cab in (z - 1, z + 1):
            c.set_block(cx_cab, y_ground + 2, cz_cab, MAT['glass_black'])
            c.set_block(cx_cab, y_ground + 3, cz_cab, MAT['glass_black'])
    c.fill(x - 2, y_ground + 4, z - 1, x - 1, y_ground + 4, z + 1, MAT['slab_quartz_b'])
    c.set_block(x - 1, y_ground + 4, z, MAT['light_ochre'])
    c.fill(x + 4, y_ground + 1, z - 2, x + 4, y_ground + 1, z + 2, MAT['slab_deep_b'])
    c.set_block(x + 3, y_ground + 1, z - 1, MAT['iron_bars'])
    c.set_block(x + 3, y_ground + 1, z + 1, MAT['iron_bars'])
