import numpy as np
import sympy as sp


def hledam_min_eps():
    mocnina = -323
    eps = 9e-323
    vysledek = sp.floor(1 - eps)
    while vysledek == 1:
        eps = eps * 10
        mocnina += 1
        vysledek = sp.floor(1 - eps)
    return eps, mocnina

def forcyklus(k):
    for i in range(1,k):
        print(i)
