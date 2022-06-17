'''
references:

https://github.com/jvdsn/crypto-attacks#hidden-number-problem
https://github.com/bitlogik/lattice-attack

https://eprint.iacr.org/2013/346.pdf
https://tches.iacr.org/index.php/TCHES/article/download/7337/6509/2461
https://hal.archives-ouvertes.fr/hal-02393302/file/a_tale_of_three_sig_eprint.pdf
https://hal.archives-ouvertes.fr/hal-03045663/document
https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/
https://crypto.hyperlink.cz/files/SAC06-rosa-hlavac.pdf
https://www.researchgate.net/publication/346593589_LadderLeak_Breaking_ECDSA_with_Less_than_One_Bit_of_Nonce_Leakage

https://jsur.in/posts/2020-09-20-downunderctf-2020-writeups   # Impeccable Challenge
https://jsur.in/posts/2021-07-25-ijctf-2021-ecsign-writeup    # ECsign Challenge
'''

from pwn import *
from sage.all import EllipticCurve,GF,inverse_mod
from shared.partial_integer import PartialInteger
from extended_hnp import dsa_known_bits
from hashlib import sha1
from Crypto.Util.number import bytes_to_long,inverse
from collections import defaultdict
import json

## Curve secp256r1
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369 # order
a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
E=EllipticCurve(GF(p),[a,b])
G=E((gx,gy))

def sign(fname,pk):
    h = bytes_to_long(sha1(fname).digest())
    k = randint(1, n - 1)
    K = k * G
    r = int(K.xy()[0])
    s = (inverse_mod(k,n)*(h + r*pk))%n
    return r,int(s)

fnames = [b'subject_kolhen', b'subject_stommb', b'subject_danbeer']
H = [bytes_to_long(sha1(fname).digest()) for fname in fnames[:-1]]
R,S,kP = [],[],[]
private=PartialInteger.unknown(256)

p = remote("64.227.37.154",31689)

request = defaultdict()
request["option"]="list"

p.recvuntil(b"file\n")
p.sendline(json.dumps(request).encode())
response=json.loads(p.recvline())["files"]

for file in response:
    _,__,r,s,kp=file.split('_')
    if len(kp)==36:
        kp=kp[2:]
    r,s,kp=map(lambda x:int(x,16),[r,s,kp])
    R.append(r)
    S.append(s)
    # partial nonce kp obtained has 144 for the signature, 136 for the second.
    # we trim the first to 136 as well~
    kP.append(PartialInteger.from_middle(kp,136,56,64)) # 56 unknown lsb, 64 unknown msb
    #actually extended HNP totally ignores this, so we are good with different lengths as well
    
for pk in dsa_known_bits(n,H,R,S,private,kP):
    log.info(f'Found Private Key : {pk}')
    r,s = sign(fnames[-1],pk)
    request["option"]="access"
    request["fname"]=fnames[-1].decode()
    request["r"]=hex(r)[2:]
    request["s"]=hex(s)[2:]
    
    p.recvuntil(b"file\n")
    p.sendline(json.dumps(request).encode())
    response=json.loads(p.recvline())
    if "data" in response:
        print(bytes.fromhex(response["data"]).decode())
        break
# p.s too tired to read other messages, flag matters after all!
# learnt a lot and got confused a lot! Came to know about a lot of attacks!
# need to learn about Lattice Cryptography and LLL