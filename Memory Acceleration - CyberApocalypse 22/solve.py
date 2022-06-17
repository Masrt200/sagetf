from z3 import *
from pwn import *
from random import randint
from hashlib import md5
from Crypto.Util.number import long_to_bytes,bytes_to_long

'''
**SCREAMS** z3's `>>` means arithmetic right shift not logical!
To do logical right shit, using LShR(variable,shift), ex: LShR(h,4)
'''

m=0xffffffff

# why AES xD
sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

def sub(b):
    b = long_to_bytes(b)
    return bytes([sbox[i] for i in b])

def rotl(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

# simple shifts add over time
def ophash(h,key):
    
    key = sub(key)
    for i, d in enumerate(key):
        a = (h << 1) & m
        b = (h << 3) & m
        c = (h >> 4) & m
        h ^= (a + b + c - d)
        h += h
        h &= m
    
    return h

# I fucking hate you
def uchash(block, key1):
    
    block = md5(block.encode()).digest()
    block = 4 * block
    blocks = [bytes_to_long(block[i:i+4]) for i in range(0, len(block), 4)]

    m = 0xffffffff
    rv1, rv2 = 0x2423380b4d045, 0x3b30fa7ccaa83
    x, y, z, u = key1, 0x39ef52e9f30b3, 0x253ea615d0215, 0x2cd1372d21d77

    for i in range(13):
        x, y = blocks[i] ^ x, blocks[i+1] ^ y
        z, u = blocks[i+2] ^ z, blocks[i+3] ^ u
        x = (x & m) * (m + (y >> 16)) ^ rotl(z, 3)
        rv1 ^= x
        y = (y & m) * (m + (z >> 16)) ^ rotl(x, 3)
        rv2 ^= y
        rv1, rv2 = rv2, rv1
        rv1 = sub(rv1)
        rv1 = bytes_to_long(rv1)

    h = rv1 + 0x6276137d7 & m
    
    return h

# duplicate function for sat solver
def phash(h,key):
    
    for i, k in enumerate(key):
        h ^= ((h << 1) + (h << 3) + LShR(h,4) - (k & 0xff))
        h <<= 1
        
    return h

# typical sat solver :)
def sat_solver(H):
    
    h = BitVec('h',32)
    keysize = 6
    key = [BitVec(f'k{i}',32) for i in range(keysize)]
    
    # equations!!
    s = Solver()
    t = phash(h,key)
    s.add(h == H)
    s.add(t == 0)

    if s.check() == sat:
        M = s.model()
        crKey = [M[i].as_long() for i in key]
        crKey = bytearray([sbox.index(i) for i in crKey])
        crKey = bytes_to_long(crKey)
        assert ophash(H,crKey) == 0
        log.info(f'SAT solved! (hash: key) -> ({H}:{crKey})')
        return crKey
    
    return False

# returns keys for the given block that will turn the hash into 0!
def get_keys(block):
    
    while True:
        key1 = randint(0,2**32-1)
        key2 = sat_solver(uchash(block,key1))
        if key2: break
    
    log.info(f'key1 -> {key1:08x}')
    log.info(f'key2 -> {key2:08x}')
    
    return key1,key2

r = remote('138.68.183.64',32009)

for step in range(4):
    
    r.recvuntil(b'block: ')
    block = r.recvline().strip().decode()
    
    key1,key2 = get_keys(block)
    for key in [key1,key2]:
        r.recvuntil(b'key: ')
        r.sendline(f'{key}'.encode())
    
    r.recvuntil(b'sure!\n\n')

print(r.recv(4096).decode())