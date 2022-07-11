from PIL import Image
import random
from base64 import b64decode
from mt19937predictor import MT19937Predictor
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

boring = Image.open('Art_Final_2022.png', 'r').convert('RGBA')
boring_pix = boring.load()

spicy = Image.open('ENHANCED_Final_2022.png', 'r').convert('RGBA')
spicy_pix = spicy.load()

rands = []

for i in range(boring.size[0] * boring.size[1]):
    x = i % boring.size[0]
    y = i // boring.size[0]
    rand32 = bytes([i^j for i,j in zip(boring_pix[x, y], spicy_pix[x, y])])
    rand32 = int.from_bytes(rand32, 'little')
    rands.append(rand32)
    
predictor = MT19937Predictor()
for state in rands[-625: - 1]:
    predictor.setrandbits(state, 32)

# setting state for our own random
random.setstate((3, tuple(predictor._mt) + (624,),None)) 
assert predictor.getrandbits(32) == random.getrandbits(32)

key = bytes(random.sample(b''.join([random.getrandbits(32).to_bytes(4, 'little') for _ in range(4)]), 16))
enc = b64decode('Tl5nK8L2KYZRCJCqLF7TbgKLgy1vIkH+KIAJv5/ILFoC+llemcmoLmCQYkiOrJ/orOOV+lwX+cVh+pwE5mtx6w==')
iv, ct = enc[:16], enc[16:]

cipher = AES.new(key, AES.MODE_CBC, iv)
print(unpad(cipher.decrypt(ct), 16))