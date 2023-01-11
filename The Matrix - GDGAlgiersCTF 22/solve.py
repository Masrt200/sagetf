from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from sage.all import *

def read_matrix(file_name):
    data = open(file_name, 'r').read().strip()
    rows = [list(eval(row)) for row in data.splitlines()]
    return Matrix(GF(p), rows)

p = 12143520799543738643
G = read_matrix("base.txt")
H = read_matrix("public_key.txt")

G_, P = G.jordan_form(transformation=true)
H_ = P.inverse() * H * P

priv = discrete_log(H_[0][0],G_[0][0])
assert G ** priv == H

key = SHA256.new(data=str(priv).encode()).digest()[:2**8]
iv = bytes.fromhex("c534df3e87713beace67144f85aca107")
ct = bytes.fromhex("c843230a54cc51d7b7ce2b47b0da5f8b98a04c3baad4bdae20f3fdcb5747f81c34a6962aef330f0d244116650c4305fd")

cipher = AES.new(key, AES.MODE_CBC, iv)
flag = cipher.decrypt(ct)
print(flag)

# CyberErudites{Y0u_kn0w_h0w_T0_XOR}
# CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}