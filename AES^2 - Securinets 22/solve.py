from pwn import *
import re
r=remote('20.233.7.174',4870)

data=r.recv()
messages=re.findall(r'[0-9a-f]{16,}',data.decode())

m1,m2=bytes.fromhex(messages[0][:32]),bytes.fromhex(messages[0][32:])
c1,c2=bytes.fromhex(messages[1][:32]),bytes.fromhex(messages[1][32:])

m3=xor(m2,c1,c2)
log.info(f"m3 --> {m3.hex()}")

r.sendline((m1+m2+m3).hex().encode())
messages=re.findall(r'[0-9a-f]{16,}',r.recv().decode())
c3=bytes.fromhex(messages[1][64:96])
log.info(f"c3 --> {c3.hex()}")

m4=xor(m2,c1,c3)
log.info(f"m4 --> {m4.hex()}")

r.sendline((m1+m2+m3+m4).hex().encode())
flag=re.findall(r'Securinets{.*}',r.recv().decode())[0]
log.info(flag)