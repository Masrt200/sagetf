from random import seed, shuffle

with open("output", "r") as f:
    encs = f.read().split("\n")[:-1]

flagLength = 37
flagBits = [[i, 0] for i in range(flagLength * 8)]

seed(2023)

for enc in encs:
    enc = bytes.fromhex(enc)
    shuffle(flagBits)
    for j, byte in enumerate(enc):
        flagBits[8 * j][1] = (byte>>7) ^ 0 
    
    flagBits = sorted(flagBits, key = lambda x: x[0])
    
flagBits = sorted(flagBits, key = lambda x: x[0])
flag = ''.join([str(x[1]) for x in flagBits])
flag = bytes.fromhex(f"{int(flag, 2):0x}").decode()
print(flag)
# TetCTF{____1nsuff1c13nt_3ntr0py_____}