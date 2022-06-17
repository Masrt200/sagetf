import re

from sage.all import *
from pwn import *

r = process("./main.py")
r.recvuntil(b'(0-9): ')

payload = b"0\n" * 4900
r.sendline(payload[:-1])

data = r.clean().decode()
leaks = re.findall(r'(?<=it was )\d',data)

k = '0.' + ''.join(leaks)

# finding minimum polynomial for K, till the fourth degree
f = algdep(Reals((10**4900).bit_length())(k), 4)
f = f.change_ring(Reals((10**5002).bit_length()))
k = f.roots()[1][0]

ans = '\n'.join(list(str(k)[4902:5002]))
r.sendline(ans.encode())
r.interactive()