from pwn import *
from z3 import *
from xoshiro128pp import check, check2
from tqdm import trange
import re

def rotl(n, k):
    return ((n << k) | LShR(n, (32-k))) & 0xffffffff

def next(s):
    res = (rotl((s[0] + s[3]) & 0xffffffff, 7) + s[0]) & 0xffffffff
    t = (s[1] << 9) & 0xffffffff
    s[2] = (s[2] ^ s[0]) & 0xffffffff
    s[3] = (s[3] ^ s[1]) & 0xffffffff
    s[1] = (s[1] ^ s[2]) & 0xffffffff
    s[0] = (s[0] ^ s[3]) & 0xffffffff
    s[2] = (s[2] ^ t) & 0xffffffff
    s[3] = rotl(s[3], 11)
    return res

r = remote("0.cloud.chals.io", 22743)
nums = re.findall(r'[0-9]+', r.recvline().decode())
nums = list(map(int, nums))

def recover_last_state(nums):
    t = [BitVec(f's{i}', 32) for i in range(4)]
    s = t.copy()
    res = [next(s) for i in range(3)]

    S = Solver()
    for i in range(3):
        S.add(res[i] == nums[i])

    if S.check() == sat:
        M = S.model()
        p = [M[x].as_long() for x in t]
    
    assert check(p.copy()) == nums
    return p

p = recover_last_state(nums)

for i in trange(10000):
    t = [BitVec(f's{i}', 32) for i in range(4)]
    s = t.copy()
    next(s)
    
    S = Solver()
    for i in range(4):
        S.add(s[i] == p[i])
    
    if S.check() == sat:
        M = S.model()
        P = [M[x].as_long() for x in t]

    assert check2(P.copy()) == p
    p = P

print(p)
    
