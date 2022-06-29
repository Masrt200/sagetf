import re
from pwn import *

r = remote("high-expectations.ctf.bsidestlv.com", 8643)

def magic(games):
    peeps = re.findall(r'(\x1b\[95m\d+\x1b\[0m)', r.recvuntil(b'>> ').decode())[0]
    log.info(f'peeps -> {peeps} games -> {games}')
    r.sendline(b'1')
    r.sendlineafter(b'>> ',b'11')

# you will surely win
for _ in range(3000):
    magic(_)

# BSidesTLV2022{i_think_i7s_a_co0l_cHall3nge_bu7_1m_bi4s3d}
