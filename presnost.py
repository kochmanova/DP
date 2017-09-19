import numpy as np
import sympy as sp

from sympy.abc import beta,a,b,c,d,e,f,g,h,i,j,x

class presnost(object):
    """pro zadanou fci, levý kraj a sgn báze vypočte bázi, rozvoj levého a pravého kraje
    s možností spočítat mink, maxk a jejich vzdálenosti"""

    def __init__(self, fce='x**3-x**2-x-1', znamenko=1):
        """funkce, která se zavolá sama, jakmile vytvořím instanci třídy Soustava, v rámci dané instance si uloží
         znaménko, bázi, levý kraj, rozvoje"""
        # inicializace proměnných
        self.beta = None
        self.fce = fce
        if (znamenko != 1) and (znamenko != -1):
            raise ValueError("Báze může být kladná s hodnotou 1 nebo záporná s hodnotou -1.")
        self.znamenko = znamenko
        self.spocitej_bazi_beta()

    def spocitej_bazi_beta(self):
        """tato funkce je zavolaná v __init__, pro danou rovnici spočte bázi, se kterou budeme počítat a uloží si ji

        :raises: ValueError - v případě, že báze beta nesplňuje námi zadané požadavky
        """
        reseni = sp.solve(self.fce, x)
        polebazi = [i for i in reseni if np.isreal(np.complex(i))]
        if len(polebazi) < 1:
            raise ValueError("Špatně zvolená rovnice. Rovnice musí mít alespoň jeden reálný kořen.")
        baze = [i for i in polebazi if i > 1]
        if len(baze) != 1:
            # může mít báze více reálných kořenů > 1 ?
            raise ValueError(
                "Bázi je nutno volit tak, aby měla jeden reálný kořen větší jak 1. Špatně zvolená rovnice.")
        self.beta = baze[0]

    def kladna(self, pocet_cifer):
        zbytek = 1/self.beta**pocet_cifer* 1/(1-1/self.beta)
        print(sp.N(zbytek,n=100))

