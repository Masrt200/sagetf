from sage.all import *
from pwn import *
from secrets import token_urlsafe
from Crypto.Util.number import *
import re
import json

def gen_smooth_prime(v):
    while True:
        v = Integer(v).next_prime()
        if all(x<2**28 for x,y in list(factor(v - 1))):
            return v

def generate():
    r = remote('fun.chall.seetf.sg', 30002)
    token = re.findall(r'"(.*)"',r.recvuntil(b"128").decode())[0]
    log.info(f'token -> {token}')
    js = json.dumps({"token": token})
    fakejs = json.dumps({"token": token, "flag": int(2)})
    
    #remove unnecessary chars, since we can only have 65 bits of extra data
    fakejs = fakejs.replace(" ","")
    js, fakejs = bytes_to_long(js.encode()), bytes_to_long(fakejs.encode())
    assert fakejs.bit_length() < 256
    return js, fakejs, r


# taking discrete mod under both primes separately
def dlog(m2, m1, prime): 
    F = Zmod(prime)
    m1, m2 = F(m1), F(m2)
    return discrete_log(m2,m1)

# generating 128 bit smooth primes for faster discrete_log using Pohlig Hellman
p = 314159265358979300000000000000000020627#gen_smooth_prime(3141592653589793 * 10**23)
log.info(f'p -> {p}')
q = 271828182845904500000000000000000200637#gen_smooth_prime(2718281828459045 * 10**23)
log.info(f'q -> {q}')
n = p * q
e = 65537

while True:
    m1, m2, r = generate()
    m1 = pow(m1, e, n)
    try:
        pp, qq = ZZ(dlog(m2, m1, p)), ZZ(dlog(m2, m1, q))
        # while joining p-1, q-1 is used as moduli
        # because in RSA, dp = d mod p-1, dq = d mod q-1
        # basic RSA equations stuff
        d = crt([pp,qq],[p-1,q-1])
        break
    except:
        r.close()

assert pow(m1, d, n) == m2
log.info(f'd -> {d}')

r.sendlineafter(b'p=',f'{p}'.encode())
r.sendlineafter(b'q=',f'{q}'.encode())
r.sendlineafter(b'd=',f'{d}'.encode())
r.interactive()

# r.interactive()