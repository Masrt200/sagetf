from random import seed, shuffle
from base64 import b64decode
from collections import defaultdict
from bitarray import bitarray

def xor(s1: bytes, s2: bytes) -> bytes:
    assert len(s1) == len(s2)
    return bytes(c1 ^ c2 for c1, c2 in zip(s1, s2))

with open("output", "r") as f:
    encs = f.read().split("\n")[:-1]

flagLength = 39
flagBits = [i for i in range(flagLength * 8)]
bitBias = defaultdict(lambda: defaultdict(int))

seed(2023)

# in extreme cases xD
prng_state = b64decode("a" * 52)

for enc in encs:
    shuffle(flagBits)
    enc = bytes.fromhex(enc)
    stream = f"{int.from_bytes(xor(prng_state, enc), 'big'):0b}"
    for i, bit in enumerate(stream):
        bitBias[flagBits[i]][bit] += 1
    flagBits.sort()

flag = bitarray(flagLength * 8)
flag.setall(0)

for pos in bitBias:
    flag[pos] = int(max(bitBias[pos], key=bitBias[pos].get))

flag = flag.tobytes().decode()
print(flag)
# TetCTF{fr0m_buggy_sw4p_t0_r4nd0m_b14s!}