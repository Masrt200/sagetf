import random
from Crypto.Util.number import long_to_bytes
from tqdm import tqdm

nbits = 328
enc = 444466166004822947723119817789495250410386698442581656332222628158680136313528100177866881816893557

ans = []
# using central limit theorem
for i in tqdm(range(24999000000,25001000000)):
    random.seed(i)
    k = random.getrandbits(nbits)
    ans.append(long_to_bytes(enc ^ k))
    
assert any(b'flag' in x for x in ans), 'Increase Bounds'

for x in ans:
    if b'flag' in x:
        print(x.decode())