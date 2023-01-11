def rotl(n, k):
    return ((n << k) | (n >> (32-k))) & 0xffffffff

def next(s):
    res = (rotl((s[0] + s[3]) & 0xffffffff, 7) + s[0]) & 0xffffffff
    t = (s[1] << 9) & 0xffffffff
    s[2] = (s[2] ^ s[0]) & 0xffffffff
    s[3] = (s[3] ^ s[1]) & 0xffffffff
    s[1] = (s[1] ^ s[2]) & 0xffffffff
    s[0] = (s[0] ^ s[3]) & 0xffffffff
    s[2] = (s[2] ^ t) & 0xffffffff
    s[3] = rotl(s[3], 11)
    return res

def check(s):
    res = [next(s) for i in range(3)]
    return res

def check2(s):
    next(s)
    return s