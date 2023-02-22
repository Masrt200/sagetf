from pwn import *
from tqdm import trange
import json

r = remote("socket.cryptohack.org", 13399)
def send(option, req = {}):
    req["option"] = option
    r.sendline(json.dumps(req).encode())
    resp = json.loads(r.recvline().decode())["msg"]
    return resp

r.recvline()
payload = b"A" * 28
for i in trange(1000):
    send("reset_password", {"token": payload.hex()})
    resp = send("authenticate", {"password": ""}) 
    if resp != "Wrong password.":
        log.info(resp)
        break
    send("reset_connection")
