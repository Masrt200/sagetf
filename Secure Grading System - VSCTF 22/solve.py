import string
import hashlib
import re
import base64

from sage.all import *
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
from pwn import *
from itertools import product

ALLOWED_CHARS = string.ascii_letters + string.digits

class ProofOfWorkSolver:
    def __init__(self, nonce, answer):
        self.nonce  = nonce
        self.answer = answer

    def generate(self):
        for choice in product(ALLOWED_CHARS, repeat = 4):
            prefix = ''.join(choice)
            if self.verify(prefix):
                return prefix

    def verify(self, prefix) -> bool:
        h = hashlib.sha256((prefix + self.nonce).encode('utf-8')).hexdigest()
        return h == self.answer

r = remote('104.197.118.147', 10140)

data = r.recvuntil(b'Your answer: ').decode()
nonce, answer = re.findall(r'[A-Za-z0-9]{16,}', data)
poow = ProofOfWorkSolver(nonce, answer)
prefix = poow.generate()
log.info(f'sha256({prefix} + {nonce}) == {answer}')

r.sendline(prefix.encode())
data = r.recvuntil(b'professor: ').decode()
r1, s1, r2, s2, N1, N2, N3 = map(int, re.findall(r'\d{16,}',data))
C1, C2, C3 = map(bytes_to_long, map(base64.b64decode, re.findall(r'Ciphertext = (.*)\n\n', data)))

M = crt([C1, C2, C3], [N1, N2, N3]).nth_root(3)
report = b"jayden_vs" + long_to_bytes(M)
z1 = int(hashlib.sha256(report[:len(report)//2]).hexdigest(), 16)
z2 = int(hashlib.sha256(report[len(report)//2:]).hexdigest(), 16)

order = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
k = (z1 - z2) * inverse(s1 - s2, order) % order
d = (s1 * k - z1) * inverse(r1, order) % order
log.info(f'k -> {k}')
log.info(f'd -> {d}')
r.sendline(f'{d}'.encode())
print(r.recv(4096).decode())