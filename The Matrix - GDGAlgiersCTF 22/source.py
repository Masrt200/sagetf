from os import urandom
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from sage.all import *
from Crypto.Util.number import getPrime
from random import randint

p = getPrime(64)

def read_matrix(file_name):
    data = open(file_name, 'r').read().strip()
    rows = [list(eval(row)) for row in data.splitlines()]
    return Matrix(GF(p), rows)

def encrypt(plaintext,key):
    iv = urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext,16))
    return iv,ciphertext

G = read_matrix('matrix.txt')
priv = randint(1,p-1)

pub = G**priv
key = SHA256.new(data=str(priv).encode()).digest()[:2**8]

flag = b'CyberErudites{???????????????????????????????}'
iv,encrypted_flag = encrypt(flag,key)
with open('public_key.txt', 'wb') as f:
    for i in range(N):
           f.write((str(list(pub[i])).encode())+b'\n')


# iv = c534df3e87713beace67144f85aca107
# ciphertext = c843230a54cc51d7b7ce2b47b0da5f8b98a04c3baad4bdae20f3fdcb5747f81c34a6962aef330f0d244116650c4305fd
# p = 12143520799543738643
