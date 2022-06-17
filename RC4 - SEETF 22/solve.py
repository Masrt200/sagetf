import os
from collections import defaultdict
from tqdm import tqdm

def rc4(key:bytes, pt: bytes) -> bytes:
    s = [*range(0x100)]
    j = 0
    for i in range(len(key)):
        j = (j + s[i] + key[i]) & 0xff
        s[i], s[j] = s[j], s[i]

    i = 0
    j = 0
    ret = []
    for c in pt:
        i = (i + 1) & 0xff
        j = (j + s[i]) & 0xff
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) & 0xff]
        ret.append(k)

    return bytes(ret)

def gen_rand_key():
    return os.urandom(96).hex().encode()

secret = 44040192//0x100000

with open("ct","rb") as fp:
    ctFreq = list(defaultdict(int) for i in range(secret))
    for _ in tqdm(range(0x100000)):
        chunk = fp.read(42)
        if not chunk:
            fp.close()
            break
        for inx, key in enumerate(chunk):
            ctFreq[inx][key] += 1

best_of_ct = [max(pos.items(), key=lambda x: x[1])[0] for pos in ctFreq]
print(f'ct -> {best_of_ct}')

keyFreq = list(defaultdict(int) for i in range(secret))
for _ in tqdm(range(0x100000)):
    keystream = rc4(gen_rand_key(), b'\0' * secret)
    for inx, key in enumerate(keystream):
        keyFreq[inx][key] += 1

best_of_key = [max(pos.items(), key=lambda x: x[1])[0] for pos in keyFreq]

flag = bytearray()
for x,y in zip(best_of_key, best_of_ct):
    flag.append(x ^ y)
print(f'key -> {best_of_key}')
print(f'flag -> {flag}')

# flag -> bytearray(b'Lo0K_r`f"w4s_Writtmn_wh3n_n0body_k\xa33w_sh1t')
# best_key was [201,0] + list(range(2,42))
# SEE{Lo0K_rc4_w4s_Writt3n_wh3n_n0body_kn3w_sh1t}