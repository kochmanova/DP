import numpy as np
import sympy as sp

from sympy.abc import x

EPS = np.spacing(0)
MALO = 2e-8


class Soustava(object):
    """tak tam něco napišu"""

    def __init__(self, fce='x**3-x**2-x-1', znamenko=1, levy_kraj='-x/3'):
        self.fce = fce
        if (znamenko != 1) and (znamenko != -1):
            raise ValueError("Báze může být kladná s hodnotou 1 nebo záporná s hodnotou -1.")
        self.znamenko = znamenko
        self.spocitej_bazi_beta()
        self.vycisleni_leveho_kraje(levy_kraj)
        self.nalezeni_rozvoje_praveho_kraje()
        self.nalezeni_rozvoje_leveho_kraje()

    def spocitej_bazi_beta(self):
        reseni = sp.solve(self.fce, x)
        polebazi = [i for i in reseni if np.isreal(np.complex(i))]
        if len(polebazi) != 1:
            raise ValueError("Špatně zvolená rovnice. Rovnice musí mít právě jeden reálný kořen.")
        baze = polebazi[0]
        if baze <= 1:
            raise ValueError("Bázi je nutno volit tak, aby byla větší jak 1. Špatně zvolená rovnice.")
        self.beta = baze

    def vycisleni_leveho_kraje(self, levy_kraj):
        symbolicky_levy_kraj = sp.sympify(levy_kraj)
        kraj = sp.N(symbolicky_levy_kraj.subs({x: self.beta}))
        if (kraj > 0) or (kraj < -1):
            raise ValueError("Nejsou splněny základní požadavky, nula neleží v zadaném intervalu.")
        if (self.znamenko == -1) and ((-kraj / self.beta > (kraj + 1)) or -(kraj + 1) / self.beta < kraj):
            raise ValueError("Nejsou splněny základní požadavky, interval není invariantní vůči posunutí.")
        self.levy_kraj = symbolicky_levy_kraj
        self.pravy_kraj = symbolicky_levy_kraj + 1 - EPS

    def nalezeni_rozvoje_leveho_kraje(self, pocet_cifer=30):
        self.rozvoj_leveho_kraje = Rozvoj(self.beta, self.levy_kraj, self.levy_kraj, self.znamenko, True, pocet_cifer)

    def nalezeni_rozvoje_praveho_kraje(self, pocet_cifer=30):
        self.rozvoj_praveho_kraje = Rozvoj(self.beta, self.pravy_kraj, self.levy_kraj, self.znamenko, True, pocet_cifer)

    def prilep_periodu(self, retezec, perioda, delka_retezce):
        delka = len(retezec)
        if (perioda is None):
            pridam_nuly = [0] * (delka_retezce - delka)
            retezec.extend(pridam_nuly)
        else:
            perioda_retezce = retezec[-perioda:]
            pridam_periodu = (delka_retezce - delka) // perioda + 1
            prodlouzeni = perioda_retezce * pridam_periodu
            retezec.extend(prodlouzeni)
            useknu = len(retezec) - delka_retezce
            retezec = retezec[:-useknu]
        return retezec

    def porovnej_retezce(self, prvni_retezec, druhy_retezec, perioda_prvniho, perioda_druheho):
        if (perioda_prvniho is not None) and (perioda_druheho is not None):
            raise ValueError("V současnosti neumíme a neporovnáváme dva řetězce s periodou!")
        pracovni_retezec_1 = prvni_retezec.copy()
        pracovni_retezec_2 = druhy_retezec.copy()
        delka_prvniho = len(pracovni_retezec_1)
        delka_druheho = len(pracovni_retezec_2)
        if delka_prvniho > delka_druheho:
            pracovni_retezec_2 = self.prilep_periodu(pracovni_retezec_2, perioda_druheho, delka_prvniho)
        elif delka_druheho > delka_prvniho:
            pracovni_retezec_1 = self.prilep_periodu(pracovni_retezec_1, perioda_prvniho, delka_druheho)
        for i in range(len(pracovni_retezec_1)):
            if (self.znamenko) ** (i + 1) * pracovni_retezec_1[i] < (self.znamenko) ** (i + 1) * pracovni_retezec_2[i]:
                return -1  # prvni retezec je MENSI jak druhy retezec
            elif (self.znamenko) ** (i + 1) * pracovni_retezec_1[i] \
                    > (self.znamenko) ** (i + 1) * pracovni_retezec_2[i]:
                return 1  # prvni retezec je VETSI jak druhy retezec
        return 0  # retezce se rovnaji

    def je_retezec_zleva_pripustny(self, retezec, perioda_retezce):
        pracovni_retezec = retezec.copy()
        # if len(pracovni_retezec)> len(self.rozvoj_leveho_kraje.rozvoj_bodu):
        # delka_kraje = len(self.rozvoj_leveho_kraje)
        while len(pracovni_retezec) > 0:
            if self.porovnej_retezce(self.rozvoj_leveho_kraje.rozvoj_bodu, pracovni_retezec,
                                     self.rozvoj_leveho_kraje.perioda, perioda_retezce) > 0:
                return False
            pracovni_retezec.pop(0)
        return True

    def je_retezec_zprava_pripustny(self, retezec, perioda_retezce):
        pracovni_retezec = retezec.copy()
        while len(pracovni_retezec) > 0:
            if self.porovnej_retezce(pracovni_retezec, self.rozvoj_praveho_kraje.rozvoj_bodu, perioda_retezce,
                                     self.rozvoj_praveho_kraje.perioda) >= 0:
                return False
            pracovni_retezec.pop(0)
        return True

    def je_retezec_pripustny(self, retezec, perioda_retezce):
        if self.je_retezec_zprava_pripustny(retezec, perioda_retezce) \
                and self.je_retezec_zleva_pripustny(retezec, perioda_retezce):
            return True
        else:
            return False


class Rozvoj(object):
    '''Třída pro rozvoj libovolného čísla v intervalu <l,l+1), nutno znát kladnou/zápornou (znaménko) bázi beta, bod, l, a počet cifer'''

    def __init__(self, baze, bod, levy_kraj, znamenko=1, symbolicke=False, pocet_cifer=30):
        self.baze = baze
        self.znamenko = znamenko
        self.levy_kraj = levy_kraj
        if symbolicke:
            symbolicky_bod = sp.sympify(bod)
            self.bod = sp.N(symbolicky_bod.subs({x: self.baze}), n=15)  # přesnost
        else:
            self.bod = bod
        self.perioda = None
        self.rozvoj_bodu = None
        self.nalezeni_rozvoje(pocet_cifer)

    def nalezeni_rozvoje(self, pocet_cifer=30):
        perioda = False
        iterace = list()
        rozvoj = list()
        iterace.append(self.bod)
        i = 1
        while (not perioda) and (i < pocet_cifer):
            transformace = self.znamenko * self.baze * iterace[i - 1] - self.levy_kraj
            iterace.append(
                sp.N(self.znamenko * self.baze * iterace[i - 1] - sp.floor(transformace).subs({x: self.baze}),
                     n=40))  # n určuje přesnost vyčíslení
            rozvoj.append(sp.floor(sp.N(transformace.subs({x: self.baze}))))
            for j in range(len(iterace)):
                if (abs(iterace[j] - iterace[i]) < MALO) and (j != i):
                    perioda = True
                    self.perioda = i - j
            i += 1
        self.rozvoj_bodu = rozvoj
