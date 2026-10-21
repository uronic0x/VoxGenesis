import struct, zlib, gzip, io, os

TAG_END = 0
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10
TAG_INT_ARRAY = 11
TAG_LONG_ARRAY = 12

TYPE_MAP = {
    'end': TAG_END,
    'byte': TAG_BYTE,
    'short': TAG_SHORT,
    'int': TAG_INT,
    'long': TAG_LONG,
    'float': TAG_FLOAT,
    'double': TAG_DOUBLE,
    'byte_array': TAG_BYTE_ARRAY,
    'string': TAG_STRING,
    'list': TAG_LIST,
    'compound': TAG_COMPOUND,
    'int_array': TAG_INT_ARRAY,
    'long_array': TAG_LONG_ARRAY,
}
INV_TYPE_MAP = {v: k for k, v in TYPE_MAP.items()}

class NBTReader:
    def __init__(self, data):
        self.stream = io.BytesIO(data)
    def read_byte(self):
        return struct.unpack('>b', self.stream.read(1))[0]
    def read_ubyte(self):
        return struct.unpack('>B', self.stream.read(1))[0]
    def read_short(self):
        return struct.unpack('>h', self.stream.read(2))[0]
    def read_ushort(self):
        return struct.unpack('>H', self.stream.read(2))[0]
    def read_int(self):
        return struct.unpack('>i', self.stream.read(4))[0]
    def read_long(self):
        return struct.unpack('>q', self.stream.read(8))[0]
    def read_float(self):
        return struct.unpack('>f', self.stream.read(4))[0]
    def read_double(self):
        return struct.unpack('>d', self.stream.read(8))[0]
    def read_string(self):
        length = self.read_ushort()
        return self.stream.read(length).decode('utf-8', errors='surrogateescape')
    def read_payload(self, tag_type):
        if tag_type == TAG_BYTE: return ('byte', self.read_byte())
        elif tag_type == TAG_SHORT: return ('short', self.read_short())
        elif tag_type == TAG_INT: return ('int', self.read_int())
        elif tag_type == TAG_LONG: return ('long', self.read_long())
        elif tag_type == TAG_FLOAT: return ('float', self.read_float())
        elif tag_type == TAG_DOUBLE: return ('double', self.read_double())
        elif tag_type == TAG_BYTE_ARRAY:
            n = self.read_int()
            return ('byte_array', list(struct.unpack(f'>{n}b', self.stream.read(n))))
        elif tag_type == TAG_STRING: return ('string', self.read_string())
        elif tag_type == TAG_LIST:
            item_type = self.read_ubyte()
            n = self.read_int()
            items = [self.read_payload(item_type) for _ in range(n)]
            return ('list', item_type, items)
        elif tag_type == TAG_COMPOUND:
            d = {}
            while True:
                t = self.read_ubyte()
                if t == TAG_END: break
                name = self.read_string()
                d[name] = self.read_payload(t)
            return ('compound', d)
        elif tag_type == TAG_INT_ARRAY:
            n = self.read_int()
            return ('int_array', list(struct.unpack(f'>{n}i', self.stream.read(4*n))))
        elif tag_type == TAG_LONG_ARRAY:
            n = self.read_int()
            return ('long_array', list(struct.unpack(f'>{n}q', self.stream.read(8*n))))
        else:
            raise ValueError(f"Unknown tag type {tag_type}")
    def read_root(self):
        t = self.read_ubyte()
        if t == TAG_END: return None
        name = self.read_string()
        return (name, self.read_payload(t))

class NBTWriter:
    def __init__(self):
        self.stream = io.BytesIO()
    def write_byte(self, v):
        self.stream.write(struct.pack('>b', v))
    def write_ubyte(self, v):
        self.stream.write(struct.pack('>B', v))
    def write_short(self, v):
        self.stream.write(struct.pack('>h', v))
    def write_ushort(self, v):
        self.stream.write(struct.pack('>H', v))
    def write_int(self, v):
        self.stream.write(struct.pack('>i', v))
    def write_long(self, v):
        self.stream.write(struct.pack('>q', v))
    def write_float(self, v):
        self.stream.write(struct.pack('>f', v))
    def write_double(self, v):
        self.stream.write(struct.pack('>d', v))
    def write_string(self, s):
        b = s.encode('utf-8', errors='surrogateescape')
        self.write_ushort(len(b))
        self.stream.write(b)
    def write_payload(self, val):
        tname = val[0]
        if tname == 'byte': self.write_byte(val[1])
        elif tname == 'short': self.write_short(val[1])
        elif tname == 'int': self.write_int(val[1])
        elif tname == 'long': self.write_long(val[1])
        elif tname == 'float': self.write_float(val[1])
        elif tname == 'double': self.write_double(val[1])
        elif tname == 'byte_array':
            arr = val[1]
            self.write_int(len(arr))
            if arr:
                self.stream.write(struct.pack(f'>{len(arr)}b', *arr))
        elif tname == 'string': self.write_string(val[1])
        elif tname == 'list':
            item_type, items = val[1], val[2]
            self.write_ubyte(item_type)
            self.write_int(len(items))
            for item in items:
                self.write_payload(item)
        elif tname == 'compound':
            for k, v in val[1].items():
                self.write_ubyte(TYPE_MAP[v[0]])
                self.write_string(k)
                self.write_payload(v)
            self.write_ubyte(TAG_END)
        elif tname == 'int_array':
            arr = val[1]
            self.write_int(len(arr))
            if arr:
                self.stream.write(struct.pack(f'>{len(arr)}i', *arr))
        elif tname == 'long_array':
            arr = val[1]
            self.write_int(len(arr))
            if arr:
                self.stream.write(struct.pack(f'>{len(arr)}q', *arr))
        else:
            raise ValueError(f"Unknown type {tname}")
    def write_root(self, root_name, root_val):
        self.write_ubyte(TYPE_MAP[root_val[0]])
        self.write_string(root_name)
        self.write_payload(root_val)
        return self.stream.getvalue()

def unpack_heightmap(longs):
    res = []
    for l in longs:
        ul = l & 0xFFFFFFFFFFFFFFFF
        for j in range(7):
            if len(res) < 256:
                res.append((ul >> (j * 9)) & 0x1FF)
    return res

def pack_heightmap(vals):
    longs = []
    for i in range(0, 256, 7):
        ul = 0
        for j in range(min(7, 256 - i)):
            ul |= (vals[i + j] & 0x1FF) << (j * 9)
        if ul >= (1 << 63):
            ul -= (1 << 64)
        longs.append(ul)
    return longs

def unpack_section_blocks(bs_compound):
    pal_list = bs_compound['palette'][2]
    if len(pal_list) == 1:
        return pal_list, [0] * 4096
    orig_longs = bs_compound['data'][1]
    bpe = max(4, (len(pal_list) - 1).bit_length())
    epw = 64 // bpe
    mask = (1 << bpe) - 1
    indices = []
    for l in orig_longs:
        ul = l & 0xFFFFFFFFFFFFFFFF
        for j in range(epw):
            if len(indices) < 4096:
                indices.append((ul >> (j * bpe)) & mask)
    return pal_list, indices

def pack_section_blocks(pal_list, indices):
    if len(pal_list) == 1:
        return {'palette': ('list', TAG_COMPOUND, pal_list)}
    bpe = max(4, (len(pal_list) - 1).bit_length())
    epw = 64 // bpe
    mask = (1 << bpe) - 1
    repacked = []
    for i in range(0, 4096, epw):
        ul = 0
        for j in range(min(epw, 4096 - i)):
            ul |= (indices[i + j] & mask) << (j * bpe)
        if ul >= (1 << 63):
            ul -= (1 << 64)
        repacked.append(ul)
    return {
        'palette': ('list', TAG_COMPOUND, pal_list),
        'data': ('long_array', repacked)
    }
