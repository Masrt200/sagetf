import os
import sys
from Crypto.Util.number import *
from sage.all import QQ
from sage.all import ZZ
from sage.all import matrix
from sage.all import vector

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
if sys.path[1] != path:
    sys.path.insert(1, path)

from shared.lattice import shortest_vectors
from shared.partial_integer import *


def attack(a, b, m, X):
    """
    Solves the hidden number problem using an attack based on the shortest vector problem.
    The hidden number problem is defined as finding y such that {xi = {aij * yj} + bi mod m}.
    :param a: the aij values
    :param b: the bi values
    :param m: the modulus
    :param X: a bound on the xi values
    :return: a generator generating tuples containing a list of xi values and a list of yj values
    """
    assert len(a) == len(b), "a and b lists should be of equal length."

    n1 = len(a)
    n2 = len(a[0])
    B = matrix(QQ, n1 + n2 + 1, n1 + n2 + 1)
    for i in range(n1):
        for j in range(n2):
            B[n1 + j, i] = a[i][j]

        B[i, i] = m
        B[n1 + n2, i] = b[i] - X // 2

    for j in range(n2):
        B[n1 + j, n1 + j] = X / QQ(m)

    B[n1 + n2, n1 + n2] = X

    for v in shortest_vectors(B):
        xs = [int(v[i] + X // 2) for i in range(n1)]
        ys = [(int(v[n1 + j] * m) // X) % m for j in range(n2)]
        if all(y != 0 for y in ys) and v[n1 + n2] == X:
            yield xs, ys


def dsa_known_msb(n, h, r, s, k):
    """
    Recovers the (EC)DSA private key and nonces if the most significant nonce bits are known.
    :param n: the modulus
    :param h: a list containing the hashed messages
    :param r: a list containing the r values
    :param s: a list containing the s values
    :param k: a list containing the partial nonces (PartialIntegers)
    :return: a generator generating tuples containing the possible private key and a list of nonces
    """
    assert len(h) == len(r) == len(s) == len(k), "h, r, s, and k lists should be of equal length."
    a = []
    b = []
    X = 0
    for hi, ri, si, ki in zip(h, r, s, k):
        msb, msb_bit_length = ki.get_known_msb()
        shift = 2 ** ki.get_unknown_lsb()
        a.append([(inverse(si, n) * ri) % n])
        b.append((inverse(si, n) * hi - shift * msb) % n)
        X = max(X, shift)

    for k_, x in attack(a, b, n, X):
        print(x[0], [ki.sub([ki_]) for ki, ki_ in zip(k, k_)])


def dsa_known_lsb(n, h, r, s, k):
    """
    Recovers the (EC)DSA private key and nonces if the least significant nonce bits are known.
    :param n: the modulus
    :param h: a list containing the hashed messages
    :param r: a list containing the r values
    :param s: a list containing the s values
    :param k: a list containing the partial nonces (PartialIntegers)
    :return: a generator generating tuples containing the possible private key and a list of nonces
    """
    assert len(h) == len(r) == len(s) == len(k), "h, r, s, and k lists should be of equal length."
    a = []
    b = []
    X = 0
    for hi, ri, si, ki in zip(h, r, s, k):
        lsb, lsb_bit_length = ki.get_known_lsb()
        inv_shift = inverse(2 ** lsb_bit_length, n)
        a.append([(inv_shift * inverse(si, n) * ri) % n])
        b.append((inv_shift * inverse(si, n) * hi - inv_shift * lsb) % n)
        X = max(X, 2 ** ki.get_unknown_msb())

    for k_, x in attack(a, b, n, X):
        nonces = [ki.sub([ki_]) for ki, ki_ in zip(k, k_)]
        print(x[0], nonces)


def dsa_known_middle(n, h1, r1, s1, k1, h2, r2, s2, k2):
    """
    Recovers the (EC)DSA private key and nonces if the middle nonce bits are known.
    This is a heuristic extension which might perform worse than the methods to solve the Extended Hidden Number Problem.
    More information: De Micheli G., Heninger N., "Recovering cryptographic keys from partial information, by example" (Section 5.2.3)
    :param n: the modulus
    :param h1: the first hashed message
    :param r1: the first r value
    :param s1: the first s value
    :param k1: the first partial nonce (PartialInteger)
    :param h2: the second hashed message
    :param r2: the second r value
    :param s2: the second s value
    :param k2: the second partial nonce (PartialInteger)
    :return: a tuple containing the private key, the nonce of the first signature, and the nonce of the second signature
    """
    k_bit_length = k1.bit_length
    assert k_bit_length == k2.bit_length
    lsb_unknown = k1.get_unknown_lsb()
    assert lsb_unknown == k2.get_unknown_lsb()
    msb_unknown = k1.get_unknown_msb()
    assert msb_unknown == k2.get_unknown_msb()
    K = 2 ** max(lsb_unknown, msb_unknown)
    l = k_bit_length - msb_unknown

    a1 = k1.get_known_middle()[0] << lsb_unknown
    a2 = k2.get_known_middle()[0] << lsb_unknown
    t = -(inverse(s1, n) * s2 * r1 * inverse(r2, n))
    u = inverse(s1, n) * r1 * h2 * inverse(r2, n) - inverse(s1, n) * h1
    u_ = a1 + t * a2 + u

    B = matrix(ZZ, 5, 5)
    B[0] = vector(ZZ, [K, K * 2 ** l, K * t, K * t * 2 ** l, u_])
    B[1] = vector(ZZ, [0, K * n, 0, 0, 0])
    B[2] = vector(ZZ, [0, 0, K * n, 0, 0])
    B[3] = vector(ZZ, [0, 0, 0, K * n, 0])
    B[4] = vector(ZZ, [0, 0, 0, 0, n])

    A = matrix(ZZ, 4, 4)
    b = []
    for row, v in enumerate(shortest_vectors(B)):
        A[row] = v[:4].apply_map(lambda x: x // K)
        b.append(-v[4])
        if row == A.nrows() - 1:
            break

    assert len(b) == 4
    x1, y1, x2, y2 = A.solve_right(vector(ZZ, b))
    assert (x1 + 2 ** l * y1 + t * x2 + 2 ** l * t * y2 + u_) % n == 0

    k1 = k1.sub([int(x1), int(y1)])
    k2 = k2.sub([int(x2), int(y2)])
    private_key1 = (inverse_mod(r1, n) * (s1 * k1 - h1)) % n
    private_key2 = (inverse_mod(r2, n) * (s2 * k2 - h2)) % n
    assert private_key1 == private_key2
    return int(private_key1), int(k1), int(k2)

n=115792089210356248762697446949407573529996955224135760342422259061068512044369

h1=355501902541896437536654868453976450534148710694
r1=19848314572422587861231278589674139319431064295012233753400823137578615082891
s1=7683831275935456980967516653994731516750840327568323640860296759654718615168
#k1=PartialInteger.from_middle(76937036737828565805449787228884971896012,136,56,64)
k1=PartialInteger.from_msb(256,0x1f82366b41cecea9e218fe49e0693327,128)

h2=978484552188852248672151413110181573179931599902
r2=81554233513765324310299719860030406392025800735448792910371343626017562595809
s2=94956586053255086156817139385530245869782259380430445579147767765171283393737
#k2=PartialInteger.from_middle(15171036377530750968639382338770679521239,136,56,64)
k2=PartialInteger.from_msb(256,0x744e56998ea5bdfd2c956b531eb7889b,128)

# print(k1.bit_length())
# print(k2.bit_length())
#print(dsa_known_middle(n, h1, r1, s1, k1, h2, r2, s2, k2))
print(dsa_known_msb(n,[h1,h2],[r1,r2],[s1,s2],[k1,k2]))
