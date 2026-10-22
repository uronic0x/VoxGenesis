import math
"""
world_canvas.py — Full-Height 3D Voxel Canvas (Y=16..175) & Deterministic .mca Writer
=====================================================================================
Includes automatic Minecraft 1.21.10 (DataVersion = 4556) BlockState canonicalization,
idempotent base-terrain snapshot loading, horizontal pane/fence/bar auto-connection,
and automatic double-door outer-hinge verification & repair.
"""

import os, struct, zlib
from array import array
from config import CANVAS_BOUNDS, FIXED_TIMESTAMP
from nbt_mca import (
    NBTReader, NBTWriter, TAG_COMPOUND, TAG_LIST, TAG_STRING, TAG_INT, TAG_BYTE,
    unpack_section_blocks, pack_section_blocks, pack_heightmap, unpack_heightmap
)

NON_MOTION_BLOCKS = {
    'minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:light',
    'minecraft:water', 'minecraft:lava',
    'minecraft:short_grass', 'minecraft:tall_grass', 'minecraft:seagrass', 'minecraft:tall_seagrass',
    'minecraft:leaf_litter', 'minecraft:bush', 'minecraft:fern', 'minecraft:large_fern',
    'minecraft:dandelion', 'minecraft:poppy', 'minecraft:blue_orchid', 'minecraft:allium',
    'minecraft:azure_bluet', 'minecraft:red_tulip', 'minecraft:orange_tulip', 'minecraft:white_tulip',
    'minecraft:pink_tulip', 'minecraft:oxeye_daisy', 'minecraft:cornflower', 'minecraft:lily_of_the_valley',
    'minecraft:pink_petals', 'minecraft:peony', 'minecraft:rose_bush', 'minecraft:lilac', 'minecraft:sunflower',
    'minecraft:vine', 'minecraft:glow_lichen', 'minecraft:spore_blossom', 'minecraft:cave_vines',
    'minecraft:cave_vines_plant', 'minecraft:hanging_roots', 'minecraft:torch', 'minecraft:wall_torch',
    'minecraft:soul_torch', 'minecraft:soul_wall_torch', 'minecraft:redstone_torch', 'minecraft:sugar_cane',
    'minecraft:kelp', 'minecraft:kelp_plant', 'minecraft:fire',
    'minecraft:wheat', 'minecraft:carrots', 'minecraft:potatoes', 'minecraft:beetroots',
    'minecraft:melon_stem', 'minecraft:attached_melon_stem', 'minecraft:pumpkin_stem', 'minecraft:attached_pumpkin_stem',
    'minecraft:sweet_berry_bush', 'minecraft:tripwire_hook', 'minecraft:lever',
}

NATURAL_TERRAIN_BLOCKS = {
    'minecraft:grass_block', 'minecraft:dirt', 'minecraft:coarse_dirt', 'minecraft:podzol',
    'minecraft:rooted_dirt', 'minecraft:mud', 'minecraft:clay', 'minecraft:gravel',
    'minecraft:sand', 'minecraft:sandstone', 'minecraft:red_sand', 'minecraft:red_sandstone',
    'minecraft:stone', 'minecraft:andesite', 'minecraft:diorite', 'minecraft:granite',
    'minecraft:tuff', 'minecraft:calcite', 'minecraft:deepslate', 'minecraft:water',
    'minecraft:coal_ore', 'minecraft:iron_ore', 'minecraft:copper_ore', 'minecraft:gold_ore',
    'minecraft:emerald_ore', 'minecraft:lapis_ore', 'minecraft:redstone_ore',
    'minecraft:deepslate_coal_ore', 'minecraft:deepslate_iron_ore',
}

NATURAL_VEGETATION_CLEAN_SET = {
    'minecraft:jungle_leaves', 'minecraft:oak_leaves', 'minecraft:birch_leaves',
    'minecraft:spruce_leaves', 'minecraft:dark_oak_leaves', 'minecraft:acacia_leaves',
    'minecraft:mangrove_leaves', 'minecraft:azalea_leaves', 'minecraft:flowering_azalea_leaves',
    'minecraft:cherry_leaves', 'minecraft:jungle_log', 'minecraft:oak_log',
    'minecraft:birch_log', 'minecraft:spruce_log', 'minecraft:dark_oak_log',
    'minecraft:acacia_log', 'minecraft:mangrove_log', 'minecraft:cherry_log',
    'minecraft:vine', 'minecraft:bamboo', 'minecraft:cocoa', 'minecraft:melon',
    'minecraft:pumpkin', 'minecraft:short_grass', 'minecraft:tall_grass',
    'minecraft:fern', 'minecraft:large_fern', 'minecraft:leaf_litter', 'minecraft:bush',
}

DEFAULT_1_21_10_PROPS = {
    'minecraft:iron_chain': {'axis': 'y', 'waterlogged': 'false'},
    'minecraft:oxidized_copper_grate': {'waterlogged': 'false'},
    'minecraft:waxed_oxidized_copper_grate': {'waterlogged': 'false'},
    'minecraft:copper_grate': {'waterlogged': 'false'},
    'minecraft:waxed_copper_grate': {'waterlogged': 'false'},
    'minecraft:grass_block': {'snowy': 'false'},
    'minecraft:podzol': {'snowy': 'false'},
    'minecraft:water': {'level': '0'},
    'minecraft:lava': {'level': '0'},
    'minecraft:sugar_cane': {'age': '0'},
    'minecraft:kelp': {'age': '20'},
    'minecraft:note_block': {'instrument': 'harp', 'note': '0', 'powered': 'false'},
    'minecraft:jukebox': {'has_record': 'false'},
}

def parse_block_spec(spec):
    if not spec.startswith('minecraft:'):
        spec = 'minecraft:' + spec
    if '[' not in spec:
        name = spec
        props = {}
    else:
        name, rest = spec.split('[', 1)
        rest = rest.rstrip(']')
        props = {}
        if rest:
            for pair in rest.split(','):
                k, v = pair.split('=', 1)
                props[k.strip()] = v.strip()

    if name == 'minecraft:chain':
        name = 'minecraft:iron_chain'

    if name in DEFAULT_1_21_10_PROPS:
        for dk, dv in DEFAULT_1_21_10_PROPS[name].items():
            props.setdefault(dk, dv)

    return name, props

def format_block_spec(name, props):
    if not props:
        return name
    items = ','.join(f"{k}={props[k]}" for k in sorted(props.keys()))
    return f"{name}[{items}]"

def spec_to_nbt(spec):
    name, props = parse_block_spec(spec)
    d = {'Name': ('string', name)}
    if props:
        d['Properties'] = ('compound', {k: ('string', v) for k, v in sorted(props.items())})
    return ('compound', d)

def nbt_to_spec(nbt_entry):
    d = nbt_entry[1]
    name = d['Name'][1]
    if 'Properties' not in d or not d['Properties'][1]:
        return format_block_spec(*parse_block_spec(name))
    props = {k: v[1] for k, v in d['Properties'][1].items()}
    raw = format_block_spec(name, props)
    return format_block_spec(*parse_block_spec(raw))

class WorldCanvas:
    def __init__(self, x_min=None, x_max=None, z_min=None, z_max=None, y_min=None, y_max=None):
        self.x_min = CANVAS_BOUNDS['x_min'] if x_min is None else x_min
        self.x_max = CANVAS_BOUNDS['x_max'] if x_max is None else x_max
        self.z_min = CANVAS_BOUNDS['z_min'] if z_min is None else z_min
        self.z_max = CANVAS_BOUNDS['z_max'] if z_max is None else z_max
        self.y_min = CANVAS_BOUNDS['y_min'] if y_min is None else y_min
        self.y_max = CANVAS_BOUNDS['y_max'] if y_max is None else y_max
        self.wx = self.x_max - self.x_min + 1
        self.wz = self.z_max - self.z_min + 1
        self.wy = self.y_max - self.y_min + 1

        self.spec_to_id = {}
        self.id_to_spec = []
        self.id_to_nbt = []
        self.id_to_name = []
        self.id_to_props = []

        self.air_id = self.get_or_register('minecraft:air')
        self.grid = array('H', [self.air_id]) * (self.wx * self.wz * self.wy)
        self.orig_surface_y = {}
        self.orig_top_block = {}
        self.block_entities = {}

    def get_or_register(self, spec):
        name, props = parse_block_spec(spec)
        canon = format_block_spec(name, props)
        if canon in self.spec_to_id:
            return self.spec_to_id[canon]
        idx = len(self.id_to_spec)
        self.spec_to_id[canon] = idx
        self.id_to_spec.append(canon)
        self.id_to_nbt.append(spec_to_nbt(canon))
        self.id_to_name.append(name)
        self.id_to_props.append(props)
        return idx

    def in_bounds(self, x, y, z):
        return (self.x_min <= x <= self.x_max and
                self.y_min <= y <= self.y_max and
                self.z_min <= z <= self.z_max)

    def _idx(self, x, y, z):
        return ((y - self.y_min) * self.wz + (z - self.z_min)) * self.wx + (x - self.x_min)

    def set_block(self, x, y, z, spec, be_data=None):
        if not (self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max and self.z_min <= z <= self.z_max):
            return
        bid = self.spec_to_id.get(spec)
        if bid is None:
            bid = self.get_or_register(spec)
        self.grid[self._idx(x, y, z)] = bid
        bname = self.id_to_name[bid]
        if be_data is None and bname == 'minecraft:jukebox':
            be_data = {
                'id': ('string', 'minecraft:jukebox'),
                'x': ('int', x), 'y': ('int', y), 'z': ('int', z),
                'keepPacked': ('byte', 0),
            }
        if be_data is not None:
            self.block_entities[(x, y, z)] = be_data
        elif (x, y, z) in self.block_entities:
            del self.block_entities[(x, y, z)]

    def set_block_id(self, x, y, z, bid):
        if not (self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max and self.z_min <= z <= self.z_max):
            return
        self.grid[self._idx(x, y, z)] = bid
        if (x, y, z) in self.block_entities:
            del self.block_entities[(x, y, z)]

    def get_block(self, x, y, z):
        if not (self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max and self.z_min <= z <= self.z_max):
            return 'minecraft:air'
        return self.id_to_spec[self.grid[self._idx(x, y, z)]]

    def get_block_name(self, x, y, z):
        if not (self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max and self.z_min <= z <= self.z_max):
            return 'minecraft:air'
        return self.id_to_name[self.grid[self._idx(x, y, z)]]

    def fill(self, x1, y1, z1, x2, y2, z2, spec):
        bid = self.get_or_register(spec)
        xa, xb = max(self.x_min, min(x1, x2)), min(self.x_max, max(x1, x2))
        ya, yb = max(self.y_min, min(y1, y2)), min(self.y_max, max(y1, y2))
        za, zb = max(self.z_min, min(z1, z2)), min(self.z_max, max(z1, z2))
        if xa > xb or ya > yb or za > zb:
            return
        span_x = xb - xa + 1
        row_vals = array('H', [bid]) * span_x
        wx, wz, y_min, z_min, x_min = self.wx, self.wz, self.y_min, self.z_min, self.x_min
        grid = self.grid
        for y in range(ya, yb + 1):
            y_off = (y - y_min) * wz
            for z in range(za, zb + 1):
                start = (y_off + (z - z_min)) * wx + (xa - x_min)
                grid[start:start + span_x] = row_vals
        if self.block_entities:
            to_del = [pos for pos in self.block_entities if xa <= pos[0] <= xb and ya <= pos[1] <= yb and za <= pos[2] <= zb]
            for pos in to_del:
                del self.block_entities[pos]

    def load_from_regions(self, region_dir):
        cx_min, cx_max = self.x_min >> 4, self.x_max >> 4
        cz_min, cz_max = self.z_min >> 4, self.z_max >> 4
        sy_min, sy_max = self.y_min >> 4, self.y_max >> 4

        snapshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base_terrain_snapshot.bin')
        has_snapshot = os.path.isfile(snapshot_path)
        if has_snapshot:
            raw_snap = zlib.decompress(open(snapshot_path, 'rb').read())
            p = 0
            for z in range(self.z_min, self.z_max + 1):
                for x in range(self.x_min, self.x_max + 1):
                    self.orig_surface_y[(x, z)] = raw_snap[p]
                    self.orig_top_block[(x, z)] = 'minecraft:water' if raw_snap[p + 1] == 1 else 'minecraft:grass_block'
                    p += 2

        for rx in range(self.x_min >> 9, (self.x_max >> 9) + 1):
            for rz in range(self.z_min >> 9, (self.z_max >> 9) + 1):
                fn = os.path.join(region_dir, f"r.{rx}.{rz}.mca")
                with open(fn, 'rb') as f:
                    raw = f.read()
                locs = struct.unpack('>1024I', raw[:4096])
                for idx, loc in enumerate(locs):
                    if loc == 0:
                        continue
                    lx, lz = idx % 32, idx // 32
                    cx, cz = rx * 32 + lx, rz * 32 + lz
                    if not (cx_min <= cx <= cx_max and cz_min <= cz <= cz_max):
                        continue
                    offset = (loc >> 8) * 4096
                    length, comp = struct.unpack('>IB', raw[offset:offset+5])
                    cdata = zlib.decompress(raw[offset+5:offset+4+length])
                    croot = NBTReader(cdata).read_root()[1][1]
                    if croot['Status'][1] != 'minecraft:full':
                        continue

                    for s in croot['sections'][2]:
                        sc = s[1]
                        sy = sc['Y'][1]
                        if not (sy_min <= sy <= sy_max) or 'block_states' not in sc:
                            continue
                        pal_list, indices = unpack_section_blocks(sc['block_states'][1])
                        local_map = [self.get_or_register(nbt_to_spec(p)) for p in pal_list]
                        base_x, base_y, base_z = cx * 16, sy * 16, cz * 16
                        for ly in range(16):
                            wy = base_y + ly
                            y_off = (wy - self.y_min) * self.wz
                            ly_off = ly * 256
                            for lz_i in range(16):
                                wz_i = base_z + lz_i
                                row_start = (y_off + (wz_i - self.z_min)) * self.wx + (base_x - self.x_min)
                                idx_off = ly_off + lz_i * 16
                                for lx_i in range(16):
                                    self.grid[row_start + lx_i] = local_map[indices[idx_off + lx_i]]

                    if not has_snapshot:
                        base_x, base_z = cx * 16, cz * 16
                        for lz_i in range(16):
                            wz_i = base_z + lz_i
                            for lx_i in range(16):
                                wx_i = base_x + lx_i
                                if -114 <= wx_i <= 106 and -114 <= wz_i <= 116:
                                    self.orig_surface_y[(wx_i, wz_i)] = 64
                                    self.orig_top_block[(wx_i, wz_i)] = 'minecraft:grass_block'
                                    continue
                                surf_y = 63
                                top_b = 'minecraft:grass_block'
                                for wy in range(self.y_max, self.y_min - 1, -1):
                                    bname = self.get_block_name(wx_i, wy, wz_i)
                                    if bname in NATURAL_TERRAIN_BLOCKS:
                                        if bname == 'minecraft:water' and wy > 63:
                                            continue
                                        if bname == 'minecraft:calcite' and wy > 65:
                                            continue
                                        surf_y = wy
                                        top_b = bname
                                        break
                                self.orig_surface_y[(wx_i, wz_i)] = surf_y
                                self.orig_top_block[(wx_i, wz_i)] = top_b

    def auto_connect_panes_fences_walls(self):
        connectable_suffixes = ('_glass_pane', '_fence', 'iron_bars')
        solid_disconnect = {
            'minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:light',
            'minecraft:water', 'minecraft:lava', 'minecraft:short_grass',
            'minecraft:tall_grass', 'minecraft:pink_petals', 'minecraft:vine',
            'minecraft:lantern', 'minecraft:soul_lantern', 'minecraft:end_rod',
            'minecraft:chain', 'minecraft:iron_chain', 'minecraft:spore_blossom', 'minecraft:torch',
            'minecraft:sea_pickle', 'minecraft:lily_pad', 'minecraft:campfire',
            'minecraft:wheat', 'minecraft:carrots', 'minecraft:potatoes', 'minecraft:beetroots',
            'minecraft:sweet_berry_bush', 'minecraft:cave_vines', 'minecraft:cave_vines_plant',
            'minecraft:melon_stem', 'minecraft:pumpkin_stem', 'minecraft:attached_melon_stem',
            'minecraft:attached_pumpkin_stem', 'minecraft:sugar_cane', 'minecraft:bamboo',
            'minecraft:tripwire_hook', 'minecraft:lever', 'minecraft:brewing_stand',
            'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:kelp', 'minecraft:kelp_plant',
        }
        target_ids = set()
        for bid, name in enumerate(self.id_to_name):
            if name.endswith(connectable_suffixes):
                target_ids.add(bid)
        if not target_ids:
            return

        def can_connect(my_name, nb_name):
            if nb_name in solid_disconnect:
                return False
            if nb_name.endswith(('_carpet', '_sapling', '_tulip', '_orchid', '_bluet', '_daisy', '_lily', '_allium', '_peony', '_lilac', '_bush', '_fern', '_candle', '_sign', '_Sign', '_banner', '_button', '_pressure_plate', '_trapdoor', '_door', '_slab', '_stairs', '_bed', '_wall')):
                return False
            if my_name.endswith('_fence'):
                if nb_name.endswith('_glass_pane') or nb_name == 'minecraft:iron_bars':
                    return False
            return True

        for y in range(max(self.y_min, 50), min(self.y_max, 118) + 1):
            y_off = (y - self.y_min) * self.wz
            for z in range(self.z_min + 1, self.z_max):
                row_off = (y_off + (z - self.z_min)) * self.wx
                for x in range(self.x_min + 1, self.x_max):
                    idx = row_off + (x - self.x_min)
                    bid = self.grid[idx]
                    if bid not in target_ids:
                        continue
                    my_name = self.id_to_name[bid]
                    n_nb = self.id_to_name[self.grid[idx - self.wx]]
                    s_nb = self.id_to_name[self.grid[idx + self.wx]]
                    w_nb = self.id_to_name[self.grid[idx - 1]]
                    e_nb = self.id_to_name[self.grid[idx + 1]]
                    props = {
                        'north': 'true' if can_connect(my_name, n_nb) else 'false',
                        'south': 'true' if can_connect(my_name, s_nb) else 'false',
                        'west':  'true' if can_connect(my_name, w_nb) else 'false',
                        'east':  'true' if can_connect(my_name, e_nb) else 'false',
                        'waterlogged': 'false',
                    }
                    new_bid = self.get_or_register(format_block_spec(my_name, props))
                    self.grid[idx] = new_bid

    def auto_fix_double_door_hinges(self):
        """
        Ensures every adjacent pair of double doors across the entire world has its hinges
        attached to the outer walls rather than the center seam:
          - facing='north': lower-X door -> hinge='left',  higher-X door -> hinge='right'
          - facing='south': lower-X door -> hinge='right', higher-X door -> hinge='left'
          - facing='east':  lower-Z door -> hinge='left',  higher-Z door -> hinge='right'
          - facing='west':  lower-Z door -> hinge='right', higher-Z door -> hinge='left'
        """
        door_bids = {bid for bid, name in enumerate(self.id_to_name) if name.endswith('_door')}
        if not door_bids:
            return 0

        pairs_verified = 0
        for y in range(max(self.y_min, 50), min(self.y_max, 105)):
            for z in range(self.z_min + 1, self.z_max - 1):
                for x in range(self.x_min + 1, self.x_max - 1):
                    bid = self.grid[self._idx(x, y, z)]
                    if bid not in door_bids:
                        continue
                    props = dict(self.id_to_props[bid])
                    if props.get('half') != 'lower':
                        continue
                    bname = self.id_to_name[bid]
                    facing = props.get('facing', 'north')

                    if facing in ('north', 'south'):
                        bid_next = self.grid[self._idx(x + 1, y, z)]
                        if bid_next in door_bids and self.id_to_name[bid_next] == bname:
                            props_next = dict(self.id_to_props[bid_next])
                            if props_next.get('half') == 'lower' and props_next.get('facing') == facing:
                                h1 = 'left' if facing == 'north' else 'right'
                                h2 = 'right' if facing == 'north' else 'left'
                                for dy, half_str in [(0, 'lower'), (1, 'upper')]:
                                    p1 = dict(props, half=half_str, hinge=h1)
                                    p2 = dict(props_next, half=half_str, hinge=h2)
                                    self.set_block(x, y + dy, z, format_block_spec(bname, p1))
                                    self.set_block(x + 1, y + dy, z, format_block_spec(bname, p2))
                                pairs_verified += 1

                    elif facing in ('east', 'west'):
                        bid_next = self.grid[self._idx(x, y, z + 1)]
                        if bid_next in door_bids and self.id_to_name[bid_next] == bname:
                            props_next = dict(self.id_to_props[bid_next])
                            if props_next.get('half') == 'lower' and props_next.get('facing') == facing:
                                h1 = 'left' if facing == 'east' else 'right'
                                h2 = 'right' if facing == 'east' else 'left'
                                for dy, half_str in [(0, 'lower'), (1, 'upper')]:
                                    p1 = dict(props, half=half_str, hinge=h1)
                                    p2 = dict(props_next, half=half_str, hinge=h2)
                                    self.set_block(x, y + dy, z, format_block_spec(bname, p1))
                                    self.set_block(x, y + dy, z + 1, format_block_spec(bname, p2))
                                pairs_verified += 1
        return pairs_verified

    def apply_ambient_light_augmentation(self):
        light_air_id = self.get_or_register('minecraft:light[level=15,waterlogged=false]')
        air_id = self.air_id
        non_luminous_targets = {
            'minecraft:smooth_quartz_stairs', 'minecraft:dark_oak_stairs', 'minecraft:spruce_stairs',
            'minecraft:deepslate_tile_stairs', 'minecraft:smooth_quartz_slab', 'minecraft:dark_oak_slab',
            'minecraft:spruce_slab', 'minecraft:deepslate_tile_slab', 'minecraft:deepslate_tiles',
            'minecraft:oxidized_copper_grate', 'minecraft:white_carpet', 'minecraft:light_gray_carpet',
            'minecraft:cyan_carpet', 'minecraft:red_carpet', 'minecraft:green_carpet',
            'minecraft:yellow_carpet', 'minecraft:brown_carpet', 'minecraft:black_carpet',
            'minecraft:orange_wool', 'minecraft:red_wool', 'minecraft:yellow_wool', 'minecraft:cyan_wool',
            'minecraft:blue_wool', 'minecraft:pink_wool', 'minecraft:white_wool',
            'minecraft:crafting_table', 'minecraft:smithing_table', 'minecraft:note_block', 'minecraft:jukebox',
            'minecraft:tube_coral_block', 'minecraft:brain_coral_block', 'minecraft:bubble_coral_block',
            'minecraft:fire_coral_block', 'minecraft:horn_coral_block',
        }
        target_bids = {bid for bid, name in enumerate(self.id_to_name) if name in non_luminous_targets}
        if not target_bids:
            return 0

        placed = 0
        for y in range(52, 96, 2):
            y_off = (y - self.y_min) * self.wz
            y_above_off = (y + 1 - self.y_min) * self.wz
            for z in range(self.z_min + 2, self.z_max - 1, 3):
                row_off = (y_off + (z - self.z_min)) * self.wx
                row_above_off = (y_above_off + (z - self.z_min)) * self.wx
                for x in range(self.x_min + 2, self.x_max - 1, 3):
                    idx = row_off + (x - self.x_min)
                    if self.grid[idx] in target_bids:
                        idx_up = row_above_off + (x - self.x_min)
                        if self.grid[idx_up] == air_id:
                            self.grid[idx_up] = light_air_id
                            placed += 1
        return placed

    def clean_any_floating_natural_blocks(self):
        air_id = self.air_id
        removed = 0
        nat_check_bids = {
            bid for bid, name in enumerate(self.id_to_name)
            if name in ('minecraft:vine', 'minecraft:jungle_leaves', 'minecraft:jungle_log',
                        'minecraft:oak_log', 'minecraft:bamboo', 'minecraft:cocoa', 'minecraft:leaf_litter')
            or (name.endswith('_leaves') and self.id_to_props[bid].get('persistent') == 'false')
        }
        if nat_check_bids:
            for i in range(len(self.grid)):
                if self.grid[i] in nat_check_bids:
                    self.grid[i] = air_id
                    removed += 1
        return removed

    def save_to_regions(self, region_dir):
        cx_min, cx_max = self.x_min >> 4, self.x_max >> 4
        cz_min, cz_max = self.z_min >> 4, self.z_max >> 4
        sy_min, sy_max = self.y_min >> 4, self.y_max >> 4

        be_by_chunk = {}
        for (bx, by, bz) in sorted(self.block_entities.keys()):
            be_comp = self.block_entities[(bx, by, bz)]
            cc = (bx >> 4, bz >> 4)
            be_by_chunk.setdefault(cc, []).append(('compound', be_comp))

        modified_chunks = 0
        air_nbt = spec_to_nbt('minecraft:air')

        for rx in range(self.x_min >> 9, (self.x_max >> 9) + 1):
            for rz in range(self.z_min >> 9, (self.z_max >> 9) + 1):
                fn = os.path.join(region_dir, f"r.{rx}.{rz}.mca")
                with open(fn, 'rb') as f:
                    raw = f.read()
                locs = list(struct.unpack('>1024I', raw[:4096]))
                timestamps = list(struct.unpack('>1024I', raw[4096:8192]))

                chunk_blobs = {}
                for idx, loc in enumerate(locs):
                    if loc == 0:
                        continue
                    offset = (loc >> 8) * 4096
                    length, comp = struct.unpack('>IB', raw[offset:offset+5])
                    chunk_blobs[idx] = (comp, raw[offset+5:offset+4+length])

                for idx in sorted(chunk_blobs.keys()):
                    lx, lz = idx % 32, idx // 32
                    cx, cz = rx * 32 + lx, rz * 32 + lz

                    comp, cdata_compressed = chunk_blobs[idx]
                    cdata = zlib.decompress(cdata_compressed)
                    root_name, root_val = NBTReader(cdata).read_root()
                    croot = root_val[1]

                    if not (cx_min <= cx <= cx_max and cz_min <= cz <= cz_max) or croot['Status'][1] != 'minecraft:full':
                        changed_border = False
                        if 'entities' in croot and len(croot['entities'][2]) > 0:
                            croot['entities'] = ('list', 0, [])
                            changed_border = True

                        in_cliff_apron = (
                            croot['Status'][1] == 'minecraft:full' and (
                                (-65 <= cz < cz_min and cx_min - 4 <= cx <= 31) or
                                (cx_max < cx <= 31 and -65 <= cz <= -12)
                            )
                        )
                        if in_cliff_apron and 'sections' in croot:
                            base_x_b, base_z_b = cx * 16, cz * 16
                            grass_nbt = spec_to_nbt('minecraft:grass_block[snowy=false]')
                            moss_nbt = spec_to_nbt('minecraft:moss_block')
                            dirt_nbt = spec_to_nbt('minecraft:dirt')
                            sand_nbt = spec_to_nbt('minecraft:sand')
                            sandstone_nbt = spec_to_nbt('minecraft:smooth_sandstone')
                            water_nbt = spec_to_nbt('minecraft:water[level=0]')
                            azalea_nbt = spec_to_nbt('minecraft:azalea_leaves[distance=1,persistent=true,waterlogged=false]')
                            fl_azalea_nbt = spec_to_nbt('minecraft:flowering_azalea_leaves[distance=1,persistent=true,waterlogged=false]')

                            col_cap_y = [80] * 256
                            col_is_sea = [False] * 256
                            for lz_i in range(16):
                                wz_i = base_z_b + lz_i
                                cz_clamp = max(self.z_min, min(self.z_max, wz_i))
                                dz_out = max(0, self.z_min - wz_i, wz_i - self.z_max)
                                for lx_i in range(16):
                                    wx_i = base_x_b + lx_i
                                    cx_clamp = max(self.x_min, min(self.x_max, wx_i))
                                    dx_out = max(0, self.x_min - wx_i, wx_i - self.x_max)
                                    d_out = math.hypot(dx_out, dz_out)

                                    edge_y = 62
                                    edge_is_water = False
                                    for wy_scan in range(110, 48, -1):
                                        b_ed = self.get_block_name(cx_clamp, wy_scan, cz_clamp)
                                        if b_ed not in ('minecraft:air', 'minecraft:light') and not b_ed.endswith('_leaves'):
                                            edge_y = wy_scan
                                            edge_is_water = (b_ed == 'minecraft:water')
                                            break
                                    wave_h = int(round(2.0 * math.sin(wx_i / 24.0) * math.cos(wz_i / 28.0)))
                                    if edge_is_water and dx_out > 0 and wz_i >= self.z_min:
                                        if d_out <= 20.0:
                                            col_cap_y[lz_i * 16 + lx_i] = 56
                                            col_is_sea[lz_i * 16 + lx_i] = True
                                        else:
                                            col_cap_y[lz_i * 16 + lx_i] = min(82 + wave_h, 62 + int((d_out - 20.0) * 0.22) + wave_h)
                                    else:

                                        col_cap_y[lz_i * 16 + lx_i] = min(84 + wave_h, edge_y + int(d_out * 0.18) + max(0, wave_h))

                        if 'sections' in croot:
                            apron_secs = {}
                            for s in croot['sections'][2]:
                                sc = s[1]
                                sy = sc['Y'][1]
                                if sy >= 3 and 'block_states' in sc:
                                    pal_list, indices = unpack_section_blocks(sc['block_states'][1])
                                    if in_cliff_apron:
                                        base_y_b = sy * 16
                                    has_nat = (sy >= 5 and any(p[1]['Name'][1] in NATURAL_VEGETATION_CLEAN_SET for p in pal_list))
                                    if in_cliff_apron and base_y_b + 15 >= min(col_cap_y) - 4:
                                        new_pal = list(pal_list)
                                        spec_idx_map = {nbt_to_spec(p): i for i, p in enumerate(new_pal)}
                                        def _get_pidx(nbt_item):
                                            sp = nbt_to_spec(nbt_item)
                                            if sp not in spec_idx_map:
                                                spec_idx_map[sp] = len(new_pal)
                                                new_pal.append(nbt_item)
                                            return spec_idx_map[sp]
                                        air_pi = _get_pidx(air_nbt)
                                        grass_pi = _get_pidx(grass_nbt)
                                        moss_pi = _get_pidx(moss_nbt)
                                        dirt_pi = _get_pidx(dirt_nbt)
                                        sand_pi = _get_pidx(sand_nbt)
                                        sstone_pi = _get_pidx(sandstone_nbt)
                                        water_pi = _get_pidx(water_nbt)
                                        az_pi = _get_pidx(azalea_nbt)
                                        fl_az_pi = _get_pidx(fl_azalea_nbt)
                                        new_indices = list(indices)
                                        sec_modified = False
                                        for ly_i in range(16):
                                            wy_i = base_y_b + ly_i
                                            ly_off = ly_i * 256
                                            for col_i in range(256):
                                                cur_pi = new_indices[ly_off + col_i]
                                                cur_name = new_pal[cur_pi][1]['Name'][1]
                                                if sy >= 5 and cur_name in NATURAL_VEGETATION_CLEAN_SET:
                                                    new_indices[ly_off + col_i] = air_pi
                                                    sec_modified = True
                                                    cur_name = 'minecraft:air'
                                                cap_y = col_cap_y[col_i]
                                                is_sea_col = col_is_sea[col_i]
                                                lx_c, lz_c = col_i & 15, col_i >> 4
                                                wx_c, wz_c = base_x_b + lx_c, base_z_b + lz_c
                                                if is_sea_col:
                                                    if wy_i > 62 and cur_name != 'minecraft:air':
                                                        new_indices[ly_off + col_i] = air_pi
                                                        sec_modified = True
                                                    elif cap_y < wy_i <= 62 and cur_name != 'minecraft:water':
                                                        new_indices[ly_off + col_i] = water_pi
                                                        sec_modified = True
                                                    elif wy_i == cap_y and cur_name != 'minecraft:sand':
                                                        new_indices[ly_off + col_i] = sand_pi
                                                        sec_modified = True
                                                else:
                                                    if wy_i == cap_y + 1:

                                                        if cap_y >= 66 and ((wx_c * 7 + wz_c * 13) % 23 == 0):
                                                            new_indices[ly_off + col_i] = az_pi if (wx_c + wz_c) % 2 == 0 else fl_az_pi
                                                            sec_modified = True
                                                        elif cur_name != 'minecraft:air':
                                                            new_indices[ly_off + col_i] = air_pi
                                                            sec_modified = True
                                                    elif wy_i > cap_y + 1 and cur_name != 'minecraft:air':
                                                        new_indices[ly_off + col_i] = air_pi
                                                        sec_modified = True
                                                    elif wy_i == cap_y and cur_name not in ('minecraft:air', 'minecraft:water'):
                                                        surf_pi = (moss_pi if (wx_c + wz_c) % 4 == 0 else grass_pi) if wy_i >= 64 else sand_pi
                                                        if new_indices[ly_off + col_i] != surf_pi:
                                                            new_indices[ly_off + col_i] = surf_pi
                                                            sec_modified = True
                                                    elif cap_y - 3 <= wy_i < cap_y and cur_name not in ('minecraft:air', 'minecraft:water'):
                                                        sub_pi = (sstone_pi if (wy_i == cap_y - 3 or cap_y < 65) else dirt_pi)
                                                        if new_indices[ly_off + col_i] != sub_pi:
                                                            new_indices[ly_off + col_i] = sub_pi
                                                            sec_modified = True
                                        if sec_modified:
                                            used_pis = sorted(set(new_indices))
                                            compact_pal = [new_pal[u] for u in used_pis]
                                            remap = {u: ni for ni, u in enumerate(used_pis)}
                                            compact_indices = [remap[ix] for ix in new_indices]
                                            sc['block_states'] = ('compound', pack_section_blocks(compact_pal, compact_indices))
                                            if 'SkyLight' in sc: del sc['SkyLight']
                                            if 'BlockLight' in sc: del sc['BlockLight']
                                            changed_border = True
                                            pal_list, indices = compact_pal, compact_indices
                                    apron_secs[sy] = (pal_list, indices)
                            if in_cliff_apron and changed_border and 'Heightmaps' in croot:

                                b_ws, b_of, b_mb, b_mbnl = [63] * 256, [63] * 256, [63] * 256, [63] * 256
                                for col_i in range(256):
                                    f_ws = f_of = f_mb = f_mbnl = False
                                    for sy_h in sorted(apron_secs.keys(), reverse=True):
                                        pal_h, idx_h = apron_secs[sy_h]
                                        for ly_h in range(15, -1, -1):
                                            b_nm = pal_h[idx_h[ly_h * 256 + col_i]][1]['Name'][1]
                                            if b_nm in ('minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:light'):
                                                continue
                                            wy_h = sy_h * 16 + ly_h
                                            val_h = wy_h + 65
                                            is_w = (b_nm == 'minecraft:water')
                                            is_lv = b_nm.endswith('_leaves')
                                            if not f_ws: b_ws[col_i] = val_h; f_ws = True
                                            if not f_of and not is_w: b_of[col_i] = val_h; f_of = True
                                            if not f_mb: b_mb[col_i] = val_h; f_mb = True
                                            if not f_mbnl and not is_lv: b_mbnl[col_i] = val_h; f_mbnl = True
                                            if f_ws and f_of and f_mb and f_mbnl:
                                                break
                                        if f_ws and f_of and f_mb and f_mbnl:
                                            break
                                croot['Heightmaps'][1]['WORLD_SURFACE'] = ('long_array', pack_heightmap(b_ws))
                                croot['Heightmaps'][1]['OCEAN_FLOOR'] = ('long_array', pack_heightmap(b_of))
                                croot['Heightmaps'][1]['MOTION_BLOCKING'] = ('long_array', pack_heightmap(b_mb))
                                croot['Heightmaps'][1]['MOTION_BLOCKING_NO_LEAVES'] = ('long_array', pack_heightmap(b_mbnl))
                            for s in ([] if in_cliff_apron else croot['sections'][2]):
                                sc = s[1]
                                sy = sc['Y'][1]
                                if sy >= 3 and 'block_states' in sc:
                                    pal_list, indices = unpack_section_blocks(sc['block_states'][1])
                                    has_nat = (sy >= 6 and any(p[1]['Name'][1] in NATURAL_VEGETATION_CLEAN_SET for p in pal_list))
                                    if False:
                                        pass
                                    elif has_nat:
                                        new_pal = []
                                        old_to_new = {}
                                        air_p_idx = None
                                        for p_i, p in enumerate(pal_list):
                                            if p[1]['Name'][1] == 'minecraft:air':
                                                air_p_idx = len(new_pal)
                                                old_to_new[p_i] = air_p_idx
                                                new_pal.append(p)
                                        if air_p_idx is None:
                                            air_p_idx = 0
                                            new_pal.append(air_nbt)
                                        for p_i, p in enumerate(pal_list):
                                            if p_i in old_to_new:
                                                continue
                                            if p[1]['Name'][1] in NATURAL_VEGETATION_CLEAN_SET:
                                                old_to_new[p_i] = air_p_idx
                                            else:
                                                old_to_new[p_i] = len(new_pal)
                                                new_pal.append(p)
                                        new_indices = [old_to_new[ix] for ix in indices]
                                        sc['block_states'] = ('compound', pack_section_blocks(new_pal, new_indices))
                                        changed_border = True
                        if changed_border:
                            if in_cliff_apron:
                                croot['isLightOn'] = ('byte', 0)
                            new_nbt = NBTWriter().write_root(root_name, root_val)
                            chunk_blobs[idx] = (2, zlib.compress(new_nbt))
                        timestamps[idx] = FIXED_TIMESTAMP
                        continue

                    base_x, base_z = cx * 16, cz * 16

                    sec_lookup = {}
                    for s in croot['sections'][2]:
                        sc = s[1]
                        sy = sc['Y'][1]
                        sec_lookup[sy] = sc
                        if sy_min <= sy <= sy_max:
                            base_y = sy * 16
                            pal_map = {}
                            pal_list = []
                            indices = [0] * 4096
                            for ly in range(16):
                                wy = base_y + ly
                                y_off = (wy - self.y_min) * self.wz
                                ly_off = ly * 256
                                for lz_i in range(16):
                                    wz_i = base_z + lz_i
                                    row_start = (y_off + (wz_i - self.z_min)) * self.wx + (base_x - self.x_min)
                                    idx_off = ly_off + lz_i * 16
                                    for lx_i in range(16):
                                        bid = self.grid[row_start + lx_i]
                                        p_idx = pal_map.get(bid)
                                        if p_idx is None:
                                            p_idx = len(pal_list)
                                            pal_map[bid] = p_idx
                                            pal_list.append(self.id_to_nbt[bid])
                                        indices[idx_off + lx_i] = p_idx
                            sc['block_states'] = ('compound', pack_section_blocks(pal_list, indices))
                            if 'SkyLight' in sc:
                                del sc['SkyLight']
                            if 'BlockLight' in sc:
                                del sc['BlockLight']
                        elif sy > sy_max and 'block_states' in sc:
                            sc['block_states'] = ('compound', {'palette': ('list', TAG_COMPOUND, [air_nbt])})
                            if 'SkyLight' in sc:
                                del sc['SkyLight']
                            if 'BlockLight' in sc:
                                del sc['BlockLight']

                    croot['isLightOn'] = ('byte', 0)
                    if 'entities' in croot:
                        croot['entities'] = ('list', 0, [])
                    c_bes = be_by_chunk.get((cx, cz), [])
                    if c_bes:
                        croot['block_entities'] = ('list', TAG_COMPOUND, c_bes)
                    else:
                        croot['block_entities'] = ('list', 0, [])

                    hm_ws = [0] * 256
                    hm_of = [0] * 256
                    hm_mb = [0] * 256
                    hm_mbnl = [0] * 256

                    lower_secs = {}
                    for sy in range(sy_min - 1, -5, -1):
                        if sy in sec_lookup and 'block_states' in sec_lookup[sy]:
                            lower_secs[sy] = unpack_section_blocks(sec_lookup[sy]['block_states'][1])

                    for lz_i in range(16):
                        wz_i = base_z + lz_i
                        for lx_i in range(16):
                            wx_i = base_x + lx_i
                            col_idx = lz_i * 16 + lx_i
                            f_ws = f_of = f_mb = f_mbnl = False
                            for wy in range(self.y_max, self.y_min - 1, -1):
                                bid = self.grid[((wy - self.y_min) * self.wz + (wz_i - self.z_min)) * self.wx + (wx_i - self.x_min)]
                                b_name = self.id_to_name[bid]
                                props = self.id_to_props[bid]
                                if b_name in ('minecraft:air', 'minecraft:cave_air', 'minecraft:void_air'):
                                    continue
                                if b_name == 'minecraft:light' and props.get('waterlogged') != 'true':
                                    continue
                                is_fluid = b_name in ('minecraft:water', 'minecraft:lava', 'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:kelp', 'minecraft:kelp_plant') or (props.get('waterlogged') == 'true')
                                is_leaves = b_name.endswith('_leaves')
                                blocks_motion = (b_name not in NON_MOTION_BLOCKS) and not b_name.endswith(('_carpet', '_button', '_pressure_plate', '_sign', '_banner', '_candle'))
                                val = wy + 65
                                if not f_ws:
                                    hm_ws[col_idx] = val
                                    f_ws = True
                                if not f_of and blocks_motion:
                                    hm_of[col_idx] = val
                                    f_of = True
                                if not f_mb and (blocks_motion or is_fluid):
                                    hm_mb[col_idx] = val
                                    f_mb = True
                                if not f_mbnl and (blocks_motion or is_fluid) and not is_leaves:
                                    hm_mbnl[col_idx] = val
                                    f_mbnl = True
                                if f_ws and f_of and f_mb and f_mbnl:
                                    break

                            if not (f_ws and f_of and f_mb and f_mbnl):
                                for sy in range(sy_min - 1, -5, -1):
                                    if sy not in lower_secs:
                                        continue
                                    pal, indices = lower_secs[sy]
                                    for ly in range(15, -1, -1):
                                        p_entry = pal[indices[ly * 256 + lz_i * 16 + lx_i]][1]
                                        b_name = p_entry['Name'][1]
                                        if b_name in ('minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:light'):
                                            continue
                                        wy = sy * 16 + ly
                                        val = wy + 65
                                        if not f_ws: hm_ws[col_idx] = val; f_ws = True
                                        if not f_of: hm_of[col_idx] = val; f_of = True
                                        if not f_mb: hm_mb[col_idx] = val; f_mb = True
                                        if not f_mbnl: hm_mbnl[col_idx] = val; f_mbnl = True
                                        break
                                    if f_ws and f_of and f_mb and f_mbnl:
                                        break

                    croot['Heightmaps'][1]['WORLD_SURFACE'] = ('long_array', pack_heightmap(hm_ws))
                    croot['Heightmaps'][1]['OCEAN_FLOOR'] = ('long_array', pack_heightmap(hm_of))
                    croot['Heightmaps'][1]['MOTION_BLOCKING'] = ('long_array', pack_heightmap(hm_mb))
                    croot['Heightmaps'][1]['MOTION_BLOCKING_NO_LEAVES'] = ('long_array', pack_heightmap(hm_mbnl))

                    new_nbt = NBTWriter().write_root(root_name, root_val)
                    chunk_blobs[idx] = (2, zlib.compress(new_nbt))
                    timestamps[idx] = FIXED_TIMESTAMP
                    modified_chunks += 1

                out_sectors = bytearray(8192)
                new_locs = [0] * 1024
                cur_sector = 2
                for idx in range(1024):
                    if idx not in chunk_blobs:
                        continue
                    comp, cbytes = chunk_blobs[idx]
                    length = len(cbytes) + 1
                    header_and_body = struct.pack('>IB', length, comp) + cbytes
                    padded_len = ((len(header_and_body) + 4095) // 4096) * 4096
                    sector_count = padded_len // 4096
                    new_locs[idx] = ((cur_sector & 0xFFFFFF) << 8) | (sector_count & 0xFF)
                    out_sectors.extend(header_and_body)
                    out_sectors.extend(b'\x00' * (padded_len - len(header_and_body)))
                    cur_sector += sector_count

                out_sectors[0:4096] = struct.pack('>1024I', *new_locs)
                out_sectors[4096:8192] = struct.pack('>1024I', *timestamps)
                with open(fn, 'wb') as f:
                    f.write(out_sectors)

        return modified_chunks
