from challenge import *
from Crypto.Util.number import *
from pwn import *

r = remote("crypto.chal.ctf.gdgalgiers.com", 1000)

r.sendlineafter(b"> ", b"1")
r.sendlineafter(b": ", b"hello")
data = eval(r.recvline().decode().strip())

s = data['S']
e = data['e']
a, R = s // e, s % e
assert Base.scalarmult(R).to_bytes() == data['R']

pk = bytes_to_long(Base.scalarmult(a).to_bytes())

r.sendlineafter(b"> ", b"3")
r.sendlineafter(b": ", f"{pk}".encode())
print(r.recvline())

# CyberErudites{ed25519_Uns4f3_L1b5}
# p.s. sk == sk[:32] duh!
