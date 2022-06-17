from sage.all import *
from pwn import *
import re

def sage_fact(n):
    p,q=factor(n)
    return p[0],q[0]

def fermat_fact(n):
    a=isqrt(n)
    while True:
        b2=a**2-n
        if is_square(b2):
            b=sqrt(b2)
            return a-b,a+b
        a+=1

def pollard_pm1(N,B=0):
    if not B: B=ceil(sqrt(N))
    a = Integers(N).random_element()
    b = a
    for ell in primes(B):
        q = 1
        while q < N:
            q *= ell
        b = b**q
        if b == 1:
            return 0
        d = gcd(b.lift()-1,N)
        if d > 1: return sorted([d,N//d])
    return 0

funcs=[sage_fact,fermat_fact,pollard_pm1]

r=remote('tjc.tf',31782)

for i,dec in enumerate(funcs):
    data=r.recvuntil(b'? ').decode()
    n=int(re.findall(r'\d+',data)[1])

    log.info(f'n --> {n}')
    p,q=dec(n)
    log.info(f'p --> {p}')
    log.info(f'q --> {q}')
    r.sendline(f'{p} {q}'.encode())
r.interactive()