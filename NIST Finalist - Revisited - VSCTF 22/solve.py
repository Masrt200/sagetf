from ascon import ascon_xof

# reference https://eprint.iacr.org/2019/1115.pdf
# simple hash collider for 2 round ascon_xof
m = b"admin\0\0\0".hex()
for i in range(256):
    m1 = m2 = m + f'{i:02x}' + "000000"
    for j in range(0xe0):
        m1 = m1[:24] + f'{j:02x}'
        m2 = m2[:24] + f'{j+0x20:02x}'
        if ascon_xof(bytes.fromhex(m1)) == ascon_xof(bytes.fromhex(m2)):
            print(m1,m2)
            exit()
