"""
generate_estate.py — Master Orchestrator for Modern Manor V5.3 World Generation
===============================================================================
"""

import os, sys, time, struct, zlib, gzip
from config import FIXED_TIMESTAMP, CANVAS_BOUNDS, EXPECTED_CANVAS_CHUNKS
from nbt_mca import NBTReader, NBTWriter, TAG_DOUBLE, TAG_FLOAT
from world_canvas import WorldCanvas
from zone_core_villa import (
    step1_flatten_and_grade_terrain,
    step2_paving_and_grounds,
    step3_landscaping_and_gardens,
    step4_gates_garage_and_outbuildings,
    step5_main_villa_complex,
    step6_backyard_pool_and_resort,
)
from zone_expansions import (
    step7_helipad_and_aviation_complex,
    step8_golf_course_and_clubhouse,
    step9_high_end_agri_farm,
)
from zone_seaside_park import step10_seaside_park_complex
from zone_cruise_ship import step11_luxury_cruise_ship
from zone_v5_expansions import (
    step12_supercar_showroom,
    step13_underwater_michelin_restaurant,
    step14_vaulted_cellar_cigar_and_art_vault,
)
from zone_sports_complex import step15_north_sports_complex
from zone_beach_park import step16_seaside_beach_park_and_transition
from zone_urban_district import step17_main_urban_district_prototype

def clean_entities_and_poi_and_update_level_dat(world_dir):
    ent_dir = os.path.join(world_dir, 'entities')
    if os.path.isdir(ent_dir):
        for fn in sorted(os.listdir(ent_dir)):
            if not fn.endswith('.mca'):
                continue
            fp = os.path.join(ent_dir, fn)
            with open(fp, 'rb') as f:
                raw = f.read()
            if len(raw) < 8192:
                continue
            locs = list(struct.unpack('>1024I', raw[:4096]))
            timestamps = [FIXED_TIMESTAMP if l != 0 else 0 for l in locs]
            chunk_blobs = {}
            for idx, loc in enumerate(locs):
                if loc == 0:
                    continue
                offset = (loc >> 8) * 4096
                length, comp = struct.unpack('>IB', raw[offset:offset+5])
                cdata = zlib.decompress(raw[offset+5:offset+4+length])
                rname, rval = NBTReader(cdata).read_root()
                rval[1]['Entities'] = ('list', 0, [])
                new_nbt = NBTWriter().write_root(rname, rval)
                chunk_blobs[idx] = (2, zlib.compress(new_nbt))

            out_sectors = bytearray(8192)
            new_locs = [0] * 1024
            cur_sector = 2
            for idx in range(1024):
                if idx not in chunk_blobs:
                    continue
                comp, cbytes = chunk_blobs[idx]
                header_and_body = struct.pack('>IB', len(cbytes) + 1, comp) + cbytes
                padded_len = ((len(header_and_body) + 4095) // 4096) * 4096
                sector_count = padded_len // 4096
                new_locs[idx] = ((cur_sector & 0xFFFFFF) << 8) | (sector_count & 0xFF)
                out_sectors.extend(header_and_body)
                out_sectors.extend(b'\x00' * (padded_len - len(header_and_body)))
                cur_sector += sector_count
            out_sectors[0:4096] = struct.pack('>1024I', *new_locs)
            out_sectors[4096:8192] = struct.pack('>1024I', *timestamps)
            with open(fp, 'wb') as f:
                f.write(out_sectors)

    player_pos = [('double', -9.5), ('double', 66.0), ('double', 38.5)]
    player_rot = [('float', -162.0), ('float', -4.0)]

    for lfn in ['level.dat', 'level.dat_old']:
        lpath = os.path.join(world_dir, lfn)
        if not os.path.isfile(lpath):
            continue
        with gzip.open(lpath, 'rb') as f:
            rname, rval = NBTReader(f.read()).read_root()
        data_d = rval[1]['Data'][1]
        data_d['DayTime'] = ('long', 12550)
        data_d['Time'] = ('long', 12550)
        data_d['SpawnX'] = ('int', -9)
        data_d['SpawnY'] = ('int', 66)
        data_d['SpawnZ'] = ('int', 38)
        data_d['rainTime'] = ('int', 100000)
        data_d['raining'] = ('byte', 0)
        data_d['thundering'] = ('byte', 0)
        if 'GameRules' in data_d:
            gr = data_d['GameRules'][1]
            gr['doMobSpawning'] = ('string', 'false')
            gr['doDaylightCycle'] = ('string', 'false')
            gr['doWeatherCycle'] = ('string', 'false')
            gr['doFireTick'] = ('string', 'false')
        if 'Player' in data_d:
            pl = data_d['Player'][1]
            pl['Pos'] = ('list', TAG_DOUBLE, player_pos)
            pl['Rotation'] = ('list', TAG_FLOAT, player_rot)
            pl['Dimension'] = ('string', 'minecraft:overworld')
        raw_nbt = NBTWriter().write_root(rname, rval)
        with open(lpath, 'wb') as raw_f:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw_f, mtime=0) as gz:
                gz.write(raw_nbt)

    pdir = os.path.join(world_dir, 'playerdata')
    if os.path.isdir(pdir):
        for fn in sorted(os.listdir(pdir)):
            if not (fn.endswith('.dat') or fn.endswith('.dat_old')):
                continue
            ppath = os.path.join(pdir, fn)
            with gzip.open(ppath, 'rb') as f:
                rname, rval = NBTReader(f.read()).read_root()
            pl = rval[1]
            pl['Pos'] = ('list', TAG_DOUBLE, player_pos)
            pl['Rotation'] = ('list', TAG_FLOAT, player_rot)
            raw_nbt = NBTWriter().write_root(rname, rval)
            with open(ppath, 'wb') as raw_f:
                with gzip.GzipFile(filename='', mode='wb', fileobj=raw_f, mtime=0) as gz:
                    gz.write(raw_nbt)

def main():
    t0 = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_world = os.path.abspath(os.path.join(base_dir, '..', 'TEST_BUILDINGS'))
    work_world = sys.argv[1] if len(sys.argv) > 1 else default_world
    region_dir = os.path.join(work_world, 'region')

    wx = CANVAS_BOUNDS['x_max'] - CANVAS_BOUNDS['x_min'] + 1
    wz = CANVAS_BOUNDS['z_max'] - CANVAS_BOUNDS['z_min'] + 1
    wy = CANVAS_BOUNDS['y_max'] - CANVAS_BOUNDS['y_min'] + 1
    print(f"=== MODERN MANOR V5.3 GENERATOR (Target: {work_world}) ===")
    print(f"1. Loading {wx}x{wz}x{wy} full-chunk canvas ({EXPECTED_CANVAS_CHUNKS} chunks: X in {CANVAS_BOUNDS['x_min']}..{CANVAS_BOUNDS['x_max']}, Z in {CANVAS_BOUNDS['z_min']}..{CANVAS_BOUNDS['z_max']})...")
    canvas = WorldCanvas()
    canvas.load_from_regions(region_dir)
    print(f"   Loaded in {time.time() - t0:.2f}s (registered {len(canvas.id_to_spec)} initial block states)")

    print("2. Flattening & grading terrain, dredging harbor & executing P0 full-sky cleanup (up to Y=175)...")
    step1_flatten_and_grade_terrain(canvas)

    print("3. Building Core Estate geometric paving, coastal boulevards & expansion avenues...")
    step2_paving_and_grounds(canvas)

    print("4. Building perimeter forests, 44-block West Woodland Brook Buffer & courtyard gardens...")
    step3_landscaping_and_gardens(canvas)

    print("5. Building Entrance Gate, 3-Bay Garage, Tool House, Recycling & Seed Outbuildings...")
    step4_gates_garage_and_outbuildings(canvas)

    print("6. Building Core 3-Story Modern Villa Complex with 4-Layer Interior Lighting...")
    step5_main_villa_complex(canvas)

    print("7. Building Backyard Infinity Pool, Outdoor Bar, Sun Loungers & Fire-Pit Lounge...")
    step6_backyard_pool_and_resort(canvas)

    print("8. Building Expansion 1: Southeast Waterfront Helipad, Helicopter, Radar Tower & VIP Lounge...")
    step7_helipad_and_aviation_complex(canvas)

    print("9. Building Expansion 2: North 3-Hole Championship Golf Course, Island Green & Clubhouse...")
    step8_golf_course_and_clubhouse(canvas)

    print("10. Building Expansion 3: Relocated West High-End Agri-Tech Farm (shifted farther West)...")
    step9_high_end_agri_farm(canvas)

    print("11. Building Expansion 4: Seaside Park (Relocated & Heightened Lighthouse at Z=-212, Pier, Boathouse, Lifeguard Tower, Seafood Restaurant, Market, Underwater Gallery, Pool+Bar, Musical Fountain, Boarding Hall)...")
    step10_seaside_park_complex(canvas)

    print("12. Building Expansion 5: Offshore 6-Deck Luxury Cruise Ship ('Serenity of the Seas')...")
    step11_luxury_cruise_ship(canvas)

    print("13. Building Expansion 6 (V5): Supercar Showroom with 6 Voxel Supercars (X=-48..-12, Z=62..98)...")
    step12_supercar_showroom(canvas)

    print("14. Building Expansion 7 (V5): Luxury Underwater Michelin 3-Star Restaurant ('L'Abysse d'Or', X=158..178, Z=-57..-28)...")
    step13_underwater_michelin_restaurant(canvas)

    print("15. Building Expansion 8 (V5): Barrel-Vaulted Wine Cellar, Cigar Lounge & Private Art Vault (X=44..94, Z=-41..-22)...")
    step14_vaulted_cellar_cigar_and_art_vault(canvas)

    print("15b. Building Expansion 9 (V5.3 Enlarged Sports Complex): 3-Block-Lane Track & Field Stadium, Non-Overlapping Grandstand & VIP Press Box, Crisp 5x7 Scoreboard, Basketball Park & Indoor Arena (X=-224..128, Z=-396..-252)...")
    step15_north_sports_complex(canvas)

    print("15c. Building Expansion 10 (V5.3): 50-Block Coastal Transition Belt & Custom-Terrain Large Seaside Beach Park (X=24..240, Z=-632..-448)...")
    step16_seaside_beach_park_and_transition(canvas)

    print("15d. Building Expansion 11 (V5.3): Main Urban District Prototype behind Beach Park (X=-304..23, Z=-632..-448)...")
    step17_main_urban_district_prototype(canvas)

    print("16. Running automatic double-door hinge symmetry & horizontal pane/fence connectivity passes...")
    doors_fixed = canvas.auto_fix_double_door_hinges()
    print(f"    Verified/normalized {doors_fixed} double-door leaf hinge states (wall-attached).")
    canvas.auto_connect_panes_fences_walls()

    cleaned_nat = canvas.clean_any_floating_natural_blocks()
    print(f"17. P0 Final Residual Safety Audit: removed {cleaned_nat} stray natural vegetation blocks.")

    light_added = canvas.apply_ambient_light_augmentation()
    print(f"18. Ambient Light Augmentation: placed {light_added:,d} invisible Level-15 `minecraft:light` blocks above non-luminous surfaces.")

    print(f"19. Saving modified chunks to .mca region files (total block states in palette registry: {len(canvas.id_to_spec)})...")
    mod_chunks = canvas.save_to_regions(region_dir)
    print(f"    Saved {mod_chunks} full chunks (+ cleaned border chunks) across 6 .mca files.")

    print("20. Cleaning entities/*.mca (zero mobs/armor stands) and updating level.dat to golden dusk...")
    clean_entities_and_poi_and_update_level_dat(work_world)
    print(f"=== GENERATION COMPLETE IN {time.time() - t0:.2f}s ===")

if __name__ == '__main__':
    main()
