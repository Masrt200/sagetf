from pwn import *
from Crypto.Util.number import *
from sage.all import *
import re

r = remote("pwn.chall.pwnoh.io", 13382)

nums = re.findall(r'[0-9]{10,}', r.recvuntil(b">>> ").decode())
a, b, c = list(map(int, nums))

x = bytes_to_long(b"qxxxb, BuckeyeCTF admins, and NOT YOU")
y = bytes_to_long(b"qxxxb, BuckeyeCTF admins, and ME")

p = 3 * a - 3 * b + c
a_ = y + 3 * b - c 

if(p == x):
    print("fail")
    exit()

p = list(factor(p - x))[-1][0]
a_ = (a_ * inverse(3, p)) % p

r.sendline(f"(1, {a_})".encode())
r.interactive()

