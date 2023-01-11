import re
from z3 import *
from pwn import *
from tqdm import trange

def rotl(n, k):
    return ((n << k) | LShR(n, (64-k))) & 0xffffffffffffffff

s = [BitVec(f's{i}', 64) for i in range(2)]

def next(s):
    res = rotl(s[0] + s[1], 17) + s[0]
    s[1]= s[1] ^ s[0]
    s[0] = rotl(s[0], 49) ^ s[1] ^ (s[1] << 21)
    s[1] = rotl(s[1], 28)
    return res


def get_last_state(nums):
    t = [BitVec(f's{i}', 64) for i in range(2)]
    s = t.copy()
    
    S = Solver()
    r1 = next(s)
    r2 = next(s)
    S.add(r1 == nums[0])
    S.add(r2 & ((1<<32) - 1) == nums[1])
    if S.check():
        M = S.model()
        p = [M[x].as_long() for x in t]
    return p

def get_first_state(p):
    
    for i in trange(10000):
        t = [BitVec(f's{i}', 64) for i in range(2)]
        s = t.copy()
        next(s)
        
        S = Solver()
        S.add(s[0] == p[0])
        S.add(s[1] == p[1])
        
        if S.check():
            M = S.model()
            p = [M[x].as_long() for x in t]
        #print(p)
    return p
        

r = process(["python","dist.py"])

nums = re.findall(r'[0-9]+', r.recvline().decode())
nums = list(map(int, nums))

print(nums)
ls = get_last_state(nums)
print(ls)
fs = get_first_state(ls)
print(fs)

r.interactive()