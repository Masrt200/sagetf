from pwn import *
from Crypto.Util.number import *
import re

r=remote('tjc.tf',31996)

data=r.recvuntil(b':\n').decode()
N,L,C=map(int,re.findall(r'\d+',data))

msg=bytes_to_long(b'Please give me the flag')
reply=pow(C,inverse(L,N*N)*msg,N*N)
log.info(f'msg  -> {msg}')
log.info(f'reply -> {reply}')

r.sendline(str(reply).encode())
r.interactive()

# https://github.com/xfinest/ctf-Hacker-Resources/blob/master/CTFs_and_WarGames/2014/ASIS-final/crypto_paillier/paillier.md
