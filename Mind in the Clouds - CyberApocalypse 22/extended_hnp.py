import os
import sys

from sage.all import QQ
from sage.all import ZZ
from sage.all import block_matrix
from sage.all import identity_matrix
from sage.all import matrix
from sage.all import vector

from shared.lattice import closest_vectors
from shared.partial_integer import *

def attack(x_, N, pi, nu, a, p, u, b, delta=None):
    """
    Solves the extended hidden number problem (definition 6 in the source paper).
    More information: Hlavac M., Rosa T., "Extended Hidden Number Problem and Its Cryptanalytic Applications" (Section 4)
    :param x_: the known bits of x
    :param N: the modulus
    :param pi: the pi values
    :param nu: the nu values
    :param a: the alpha values
    :param p: the rho values
    :param u: the mu values
    :param b: the beta values
    :param delta: the delta value (default: automatically computed)
    :return: a generator generating possible values of x
    """
    assert len(pi) == len(nu), "pi and v lists should be of equal length."
    assert len(a) == len(p) == len(u) == len(b), "a, p, u, and b lists should be of equal length."

    m = len(pi)
    d = len(a)
    l = []
    for i in range(d):
        assert len(p[i]) == len(u[i]), "p[i] and u[i] lists should be of equal length."
        l.append(len(p[i]))

    L = sum(l)
    D = d + m + L
    KD = QQ(2 ** (D / 4) * (m + L) ** (1 / 2) + 1) / 2
    delta = QQ(1 / (2 * KD)) if delta is None else QQ(delta)
    assert 0 < KD * delta < 1

    Id = identity_matrix(ZZ, d)
    P = matrix(ZZ, L, d)
    row = 0
    for i in range(d):
        for j in range(l[i]):
            P[row, i] = p[i][j]
            row += 1

    A = matrix(ZZ, m, d)
    for i in range(d):
        for j in range(m):
            A[j, i] = a[i] * 2 ** pi[j]

    X = matrix(QQ, m, m)
    for j in range(m):
        X[j, j] = delta / (2 ** nu[j])

    K = matrix(QQ, L, L)
    pos = 0
    for i in range(d):
        for j in range(l[i]):
            K[pos, pos] = delta / (2 ** u[i][j])
            pos += 1

    B = block_matrix(QQ, [
        [N * Id, matrix(QQ, d, m), matrix(QQ, d, L)],
        [A, X, matrix(QQ, m, L)],
        [P, matrix(QQ, L, m), K]
    ])

    v = vector(QQ, [delta / 2] * D)
    for i in range(d):
        v[i] = (b[i] - a[i] * x_) % N

    for W in closest_vectors(B, v, algorithm="babai"):
        z = x_
        for j in range(m):
            z += 2 ** pi[j] * int((W[d + j] * 2 ** nu[j]) / delta)
            z %= N

        yield z


def dsa_known_bits(N, h, r, s, x, k):
    """
    Recovers the (EC)DSA private key if any nonce bits are known.
    :param N: the modulus
    :param h: a list containing the hashed messages
    :param r: a list containing the r values
    :param s: a list containing the s values
    :param x: the partial private key (PartialInteger, can be fully unknown)
    :param k: a list containing the partial nonces (PartialIntegers)
    :return: a generator generating possible private keys
    """
    assert len(h) == len(r) == len(s) == len(k), "h, r, s, and k lists should be of equal length."
    x_, pi, nu = x.get_known_and_unknowns()
    a = []
    p = []
    u = []
    b = []
    for hi, ri, si, ki in zip(h, r, s, k):
        a.append(ri)
        ki_, li, ui = ki.get_known_and_unknowns()
        p.append([(-si * 2 ** lij) % N for lij in li])
        u.append(ui)
        b.append((si * ki_ - hi) % N)

    yield from attack(x_, N, pi, nu, a, p, u, b)

# n = 115792089210356248762697446949407573529996955224135760342422259061068512044369

# h1=355501902541896437536654868453976450534148710694
# r1=60077222094867012740147295815401483764030761653188063322737839036039938472111
# s1=93193746802229777152979499699125504017598979395018191744602176241725402172640
# k1=PartialInteger.from_middle(0xf16ed1043b6bf274efaa1cd1215d014e37,136,56,64)

# h2=978484552188852248672151413110181573179931599902
# r2=32570848065333040088300161333227613687535483280464376592013867110973214506342
# s2=92863688242217366043485878042208217339931007951301448923337167748611461508499
# k2=PartialInteger.from_middle(56006252672673112537245705847722460947347,136,56,64)

# private=PartialInteger.unknown(256)

# for pk in dsa_known_bits(n, [h1,h2], [r1,r2], [s1,s2], private, [k1,k2]):
#     print(pk)