from message import *

def franklinReiter(n,e,r,c1,c2):
    R.<X> = Zmod(n)[]
    f1 = X^e - c1
    f2 = (X + r)^e - c2
    # coefficient 0 = -m, which is what we wanted!
    return Integer(n-(GCD(f1,f2)).coefficients()[0])

# GCD is not implemented for rings over composite modulus in Sage
# so we do our own implementation. Its the exact same as standard GCD, but with
# the polynomials monic representation
def GCD(a, b):
    if(b == 0):
        return a.monic()
    else:
        return GCD(b, a % b)
    
def CoppersmithShortPadAttack(e,n,C1,C2,eps=1/30):
    """
    Coppersmith's Shortpad attack!
    Reference: https://en.wikipedia.org/wiki/Coppersmith's_attack#Coppersmith.E2.80.99s_short-pad_attack
    """
    P.<x,y> = PolynomialRing(ZZ)
    ZmodN = Zmod(n)
    g1 = x^e - C1
    g2 = (x+y)^e - C2
    res = g1.resultant(g2)
    P.<z> = PolynomialRing(ZmodN)
    
    # Convert Multivariate Polynomial Ring to Univariate Polynomial Ring
    rres=res.univariate_polynomial()
    
    # change ring wrt to Zmod(n)
    rres=rres.change_ring(P).subs(y=z)
    
    diff = rres.small_roots(epsilon=eps)
    M1 = franklinReiter(n,e,diff[0],C1,C2)
    return M1

rand = CoppersmithShortPadAttack(e, N, ct[1], ct[2]) >> 24
assert pow(rand << 24, e, N) == ct[0]

M = {}

for i in range(128):
    M[pow(pow(i, e, N) + (rand << 24), e, N)] = i

for i in range(1, len(ct)):
    print(chr(M[ct[i]]), end='')
    
# CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}