from pwn import *
import numpy as np
from Crypto.Util.number import *

r=remote('ctf.b01lers.com',9003)

r.recv(4096)
r.sendline(b'2')
r.recv(4096)

init=np.zeros(256)

cases=[]
for j in range(10):
    flag=[]
    for i in range(256):
        s=init.copy()
        s[i]=(s[i]+1)%2
        s[j*8]=(s[j*8]+1)%2
        s=''.join(s.astype(int).astype(str))
        r.sendline(f'{s}'.encode())
        bit=r.recvline().strip().decode()
        log.info(f'at {i} --> {bit}')
        flag.append(bit)
    cases.append(flag)

FLAG=[]
for i in range(256):
    count=[0,0]
    for j in cases:
        if j[i]=='1': count[0]+=1
        else: count[1]+=1
    print(count)
    if(count[0]>=count[1]): FLAG.append('1')
    else: FLAG.append('0')

flag1=long_to_bytes(int(''.join(FLAG),2))
print(f'FLAG --> {flag1}')