import requests
import re
from tqdm import trange
url = "https://hambone.chall.pwnoh.io/"


def sr():
    path = f"{int(''.join([str(i) for i in bits]), 2):096x}"
    r = requests.get(url + path)
    
    color = re.findall(r'background: #([0-9a-f]{6})', r.text)[0]
    color = sum(list(bytes.fromhex(color)))
    
    return color

bits = [0] * 48 * 8

cn = sr()

flag = ""
for i in trange(8 * 48):
    bits[i] = 1
    ncn = sr()
    
    if(ncn > cn):
        flag += "1"
    else:
        flag += "0"
    
    bits[i] = 0

flag = f"{int(flag, 2):096x}"
r = requests.get(url + flag)
print(r.text)
