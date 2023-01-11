from sage.all import *
from pwn import *

def random_poly(N, d1, d2):
    coef_list = [1] * d1 + [-1] * d2 + [0] * (N - d1 - d2)
    shuffle(coef_list)
    return coef_list


N, p, q, d = 8, 2, 29, 2

F = ZZ['x']
mod = F([-1]+ [0] * (N - 1) + [1]) # x ^ 8 - 1
R  = F.quotient(mod, 'x')
Rp = F.change_ring(Integers(p)).quotient(mod, 'x')
Rq = F.change_ring(Integers(q)).quotient(mod, 'x')

# all polynomials generated by random_poly in quotient-ring Rq
polys = set()
for i in range(10000):
    polys.add(Rq(random_poly(N, d, d)))

assert len(polys) == 420
polys = list(polys)

r = remote("crypto.chal.ctf.gdgalgiers.com", 1001)

def recv(inx):
    r.sendlineafter(b"option \n", b"a")
    r.sendlineafter(b"index: ", f"{inx}".encode())
    ex = eval(r.recvline().decode().strip())
    hx = eval(r.recvline().decode().strip())
    ex, hx = Rq(ex), Rq(hx)
    return ex, hx

flag = bytearray()

for i in range(32):
    ex, hx = recv(i)
    found = false
    for rx in polys:
        for c in range(128):
            mx = Rq(Rp(list(f'{c:08b}')).lift())
            if Rq(2 * hx * rx + mx) == ex:
                flag.append(c)
                found = true
                log.info(f'flag[{i}] = {c}')
            if found:
                break
        if found:
            break
log.info(f"flag: {flag}")