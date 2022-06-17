from collections import Counter,defaultdict
from Crypto.Cipher import ARC4
import json
from pwn import *

# key=b'hello'
# def encrypt(iv, pt):
#     return ARC4.new(iv + key).encrypt(pt)

def possible_key_bit(key, c):
    s = [i for i in range(256)]
    j = 0
    for i in range(len(key)):
        j = (j + s[i] + key[i]) % 256
        tmp = s[i]
        s[i] = s[j]
        s[j] = tmp

    return (c[0] - j - s[len(key)]) % 256


def attack(encrypt_oracle, key_len):
    """
    Recovers the hidden part of an RC4 key using the Fluhrer-Mantin-Shamir attack.
    :param encrypt_oracle: the padding oracle, returns the encryption of a plaintext under a hidden key concatenated with the iv
    :param key_len: the length of the hidden part of the key
    :return: the hidden part of the key
    """
    key = bytearray([3, 255, 0])
    for a in range(key_len):
        key[0] = a + 3
        possible = Counter()
        for x in range(256):
            print(f"\r{x}",end="")
            key[2] = x
            c = encrypt_oracle(key[:3], b"\x00")
            possible[possible_key_bit(key, c)] += 1
        key.append(possible.most_common(1)[0][0])
        print("\n",key,possible.most_common(3))

    return key[3:]

r=remote("188.166.172.138",32491)


def send_encrypt_request(iv,pt):
    request=defaultdict()
    request["option"]="encrypt"
    request["iv"]=iv.hex()
    request["pt"]=pt.hex()
    request = json.dumps(request)

    r.recvuntil(b"> ")
    r.sendline(request.encode())

    data = r.recvline().strip().decode()
    data = json.loads(data)
    return bytes.fromhex(data['ct'])

print(attack(send_encrypt_request,27))

# https://en.wikipedia.org/wiki/Fluhrer,_Mantin_and_Shamir_attack
# https://github.com/jvdsn/crypto-attacks/blob/master/attacks/rc4/fms.py
'''
masrt@bitc-box:~/tmp$ nc 188.166.172.138 32491
Connected to the cyborg's debugging interface

Options:
1. Encrypt your text.
2. Claim the key.
> {"option":"claim","key":"1fec0787bd1a52ade63a379a203c2be92b981eb117dac4034ecce0"}
{"response": "success", "flag": "HTB{f1uhr3r_m4n71n_p1u5_5h4m1r_15_4_cl4ss1c_0n3!!!}"}
'''
