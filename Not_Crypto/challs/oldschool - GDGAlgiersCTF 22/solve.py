from z3 import *
from Crypto.Util.number import long_to_bytes

def rotl(n, b):
    return ((n << b) | (n >> (16 - b))) & 0xffff

A = BitVec('A', 16)
B = BitVec('B', 16)
C = BitVec('C', 16)
D = BitVec('D', 16)

s = Solver()

# cx = 0
ax = A
bx = B
dx = C
di = D

s.add(di & 0xff00 == ((bx ^ dx) ^ 0x0f00) & 0xff00)

# cx = 1
bx = A
ax = B
dx = C
di = D

s.add(di & 0xf0f0 == (rotl(bx ^ dx, 1) ^ 0x00f0) & 0xf0f0)

# cx = 2
bx = A
dx = B
ax = C
di = D

s.add(di == bx ^ dx ^ 0x3536)

# cx = 3
bx = A 
dx = B
di = C
ax = D

s.add(di & 0xf0f0 == (bx ^ dx) & 0xf0f0)

s.add(A & 0x0f0f == 0x0700)
s.add(B & 0x00ff == 0x0054)
s.add(C & 0x0f0f == 0x0d02)
s.add(D & 0x000f == 0x0002)

if s.check() == sat:
    M = s.model()
    print(M)
    flag = ''.join([f"{M[i].as_long():04x}" for i in (A, B, C, D)])
    print(f"ctf{{{bytes.fromhex(flag).decode()}}}") 