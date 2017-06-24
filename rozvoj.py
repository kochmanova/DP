import numpy as np
import sympy as sp
import time

from sympy.abc import x

EPS = 9e-17
MALO = 2e-8


class Soustava(object):
    """pro zadanou fci, levý kraj a sgn báze vypočte bázi, rozvoj levého a pravého kraje
    s možností spočítat mink, maxk a jejich vzdálenosti"""

    def __init__(self, fce='x**3-x**2-x-1', znamenko=1, levy_kraj='-x/3'):
        """funkce, která se zavolá sama, jakmile vytvořím instanci třídy Soustava, v rámci dané instance si uloží
         znaménko, bázi, levý kraj, rozvoje"""
        # inicializace proměnných
        self.beta = None
        self.levy_kraj = None
        self.delta = None
        self.maxk = None
        self.mink = None
        self.pravy_kraj = None
        self.fce = fce
        if (znamenko != 1) and (znamenko != -1):
            raise ValueError("Báze může být kladná s hodnotou 1 nebo záporná s hodnotou -1.")
        self.znamenko = znamenko
        self.spocitej_bazi_beta()
        self.vycisleni_leveho_kraje(levy_kraj)
        self.nalezeni_rozvoje_leveho_kraje()
        self.nalezeni_rozvoje_praveho_kraje()

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

    def vycisleni_leveho_kraje(self, levy_kraj):
        """funkce, která pro levý kraj, jak symbolický vyjádřený pomocí bety(x), tak hodnotu, zjistí, zda
        splňuje námi požadované podmínky a přiřadí ho do proměnné

        :param levy_kraj: levý kraj intervalu <l, l+1), může být zadán pomocí báze beta, kterou ve vzorci reprezentuje
               x, například chceme-li, aby hodnota levého kraje byla beta/(beta+1), pak do proměnné levy_kraj='x/(x+1)'
        :type levy_kraj: str
        """
        symbolicky_levy_kraj = sp.sympify(levy_kraj)
        kraj = sp.N(symbolicky_levy_kraj.subs({x: self.beta}))
        symbolicky_levy_kraj = symbolicky_levy_kraj.subs({x: self.beta})
        print(kraj)
        if (kraj > 0) or (kraj < -1):
            raise ValueError("Nejsou splněny základní požadavky, nula neleží v zadaném intervalu.")
        if (self.znamenko == -1) and ((-kraj / self.beta - EPS > (kraj + 1)) or -(kraj + 1) / self.beta + EPS < kraj):
            raise ValueError("Nejsou splněny základní požadavky, interval není invariantní vůči posunutí.")
        self.levy_kraj = symbolicky_levy_kraj
        self.pravy_kraj = symbolicky_levy_kraj + 1 - EPS

    def nalezeni_rozvoje_leveho_kraje(self, pocet_cifer=30):
        """tato funkce vytvoří instanci třídy Rozvoj, v rámci níž spočte rozvoj levého kraje a jeho periodu
        tyto hodnoty lze pak nalézt v self.rozvoj_leveho_kraje.rozvoj_bodu a self.rozvoj_leveho_kraje.perioda

        :param pocet_cifer: počet míst, na který chceme vyčíslit rozvoj levého kraje, defaultně nastaven na 30
        """
        self.rozvoj_leveho_kraje = Rozvoj(self.beta, self.levy_kraj, self.levy_kraj, self.znamenko, False, pocet_cifer)
        self.rozvoj_leveho_kraje.nalezeni_rozvoje(pocet_cifer)

    def nalezeni_rozvoje_praveho_kraje(self, pocet_cifer=30):
        """tato funkce vytvoří instanci třídy Rozvoj, v rámci níž spočte rozvoj pravého kraje a jeho periodu
        tyto hodnoty lze pak nalézt v self.rozvoj_leveho_kraje.rozvoj_bodu a self.rozvoj_leveho_kraje.perioda

         :param pocet_cifer: počet míst, na který chceme vyčíslit rozvoj pravého kraje, defaultně nastaven na 30
        """
        self.rozvoj_praveho_kraje = Rozvoj(self.beta, self.pravy_kraj, self.levy_kraj, self.znamenko, False,
                                           pocet_cifer)
        self.rozvoj_praveho_kraje.limitni_rozvoj(pocet_cifer)

    def prilep_periodu(self, retezec, perioda, delka_retezce):
        """pomocná funkce, která k retezci v případě periody přilepí periodu tolikrát, aby délka řetězce byla rovna
        delka_retezce v případě, že rětezec nemá periodu, mu přilepí tolik 0, aby jeho délka byla rovna delka_retezce

        :param retezec: počáteční řetězec, který chceme prodloužit
        :type retezec: list
        :param perioda: délka periody řetězce (int), pokud nemá periodu, hodnota je None a řetezec se doplní nulami
        :param delka_retezce: požadovaná délka prodlouženého řetězce
        :returns: list - prodloužený nebo zkrácený řetězec na požadovanou délku
        """
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
        """Funkce, která dokáže porovnat dva řetězce i různé délky

        :param prvni_retezec: první řetezec (list), který porovnáváme
        :type prvni_retezec: list
        :param druhy_retezec: řetězec, se kterým porovnáváme prvni_retezec
        :type druhy_retezec: list
        :param perioda_prvniho: délka periody prvního řetězce (int), pokud nemá periodu, hodnota je None
        :param perioda_druheho: délka periody druhého řetězce (int), pokud nemá periodu, hodnota je None

        :returns: -1: prvni_retezec < druhy_retezec
        :returns: 1: prvni_retezec > druhy_retezec
        :returns: 0: prvni_retezec = druhy_retezec"""

        if (perioda_prvniho is not None) and (perioda_druheho is not None):
            raise ValueError("V současnosti neumíme a neporovnáváme dva řetězce s periodou!")
        # Nyní zjistíme, který z řetězců je periodický
        pracovni_retezec_1 = prvni_retezec.copy()
        pracovni_retezec_2 = druhy_retezec.copy()
        if perioda_prvniho is not None:
            pridam_nuly = [0] * perioda_prvniho
            pracovni_retezec_2.extend(pridam_nuly)
        if perioda_druheho is not None:
            pridam_nuly = [0] * perioda_druheho
            pracovni_retezec_1.extend(pridam_nuly)
        if len(pracovni_retezec_1) > len(pracovni_retezec_2):
            pracovni_retezec_2 = self.prilep_periodu(pracovni_retezec_2, perioda_druheho, len(pracovni_retezec_1))
        elif len(pracovni_retezec_2) > len(pracovni_retezec_1):
            pracovni_retezec_1 = self.prilep_periodu(pracovni_retezec_1, perioda_prvniho, len(pracovni_retezec_2))
        for i in range(len(pracovni_retezec_1)):
            if (self.znamenko) ** (i + 1) * pracovni_retezec_1[i] < (self.znamenko) ** (i + 1) * pracovni_retezec_2[i]:
                return -1  # prvni retezec je MENSI jak druhy retezec
            elif (self.znamenko) ** (i + 1) * pracovni_retezec_1[i] \
                    > (self.znamenko) ** (i + 1) * pracovni_retezec_2[i]:
                return 1  # prvni retezec je VETSI jak druhy retezec
        return 0  # retezce se rovnaji

    def je_retezec_zleva_pripustny(self, retezec, perioda_retezce):
        """funkce, která zjistí, zda je retezec a libovolný jeho sufix >= rozvoj_leveho_kraje.rozvoj_bodu

        :type retezec: list
        :param perioda_retezce: délka periody řetězce (int), pokud nemá periodu, hodnota je None
        :returns: bool
        """
        pracovni_retezec = retezec.copy()
        while len(pracovni_retezec) > 0:
            if self.porovnej_retezce(self.rozvoj_leveho_kraje.rozvoj_bodu, pracovni_retezec,
                                     self.rozvoj_leveho_kraje.perioda, perioda_retezce) > 0:
                return False
            pracovni_retezec.pop(0)
        return True

    def je_retezec_zprava_pripustny(self, retezec, perioda_retezce):
        """funkce, která zjistí, zda je retezec a libovolný jeho sufix < rozvoj_praveho_kraje.rozvoj_bodu

        :type retezec: list
        :param perioda_retezce: délka periody řetězce (int), pokud nemá periodu, hodnota je None
        :returns: bool
        """
        pracovni_retezec = retezec.copy()
        while len(pracovni_retezec) > 0:
            if self.porovnej_retezce(pracovni_retezec, self.rozvoj_praveho_kraje.rozvoj_bodu, perioda_retezce,
                                     self.rozvoj_praveho_kraje.perioda) >= 0:
                return False
            pracovni_retezec.pop(0)
        return True

    def je_retezec_pripustny(self, retezec, perioda_retezce):
        """funkce, která spojuje fce je_retezec_zleva_pripustny a fci je_retezec_zprava_pripustny a určuje,
        zda je retezec připustný

        :type retezec: list
        :param perioda_retezce: délka periody řetězce (int), pokud nemá periodu, hodnota je None
        :returns: bool
        """
        if self.je_retezec_zprava_pripustny(retezec, perioda_retezce) \
                and self.je_retezec_zleva_pripustny(retezec, perioda_retezce):
            return True
        else:
            return False

    def vytvoreni_mink_maxk(self, k):
        """tato funkce pro dané k nalézne řetězce mink a maxk až do délky řetězce k

        :param k: maximální délka řetězců mink a maxk, kterou chceme vytvořit
        """
        mink = list()
        maxk = list()
        min0 = []
        max0 = []
        mink.append(min0)
        maxk.append(max0)
        for i in range(1, k):
            mini = self.prilep_periodu(self.rozvoj_leveho_kraje.rozvoj_bodu, self.rozvoj_leveho_kraje.perioda, i)
            maxi = self.prilep_periodu(self.rozvoj_praveho_kraje.rozvoj_bodu, self.rozvoj_praveho_kraje.perioda, i)
            mk = 0
            while mk <= i - 1:
                min_prefix = mini[:i - mk - 1]  # neměnný prefix
                max_prefix = maxi[:i - mk - 1]
                min_cifra = mini[i - mk - 1]  # měnící se cifra
                max_cifra = maxi[i - mk - 1]
                mozne_min1 = list()
                mozne_max1 = list()
                mozne_min1.extend(min_prefix)
                mozne_max1.extend(max_prefix)
                if (i - mk) % 2 == 0 or self.znamenko == 1:  # sude
                    mozne_min1.append(min_cifra + 1)
                    mozne_min1.extend(mink[mk])
                    mozne_max1.append(max_cifra - 1)
                    mozne_max1.extend(maxk[mk])
                else:
                    mozne_min1.append(min_cifra - 1)
                    mozne_min1.extend(maxk[mk])
                    mozne_max1.append(max_cifra + 1)
                    mozne_max1.extend(mink[mk])
                if self.je_retezec_pripustny(mozne_min1, None):
                    if self.porovnej_retezce(mini, mozne_min1, None, None) == 1:
                        mini = mozne_min1
                    if not self.je_retezec_pripustny(mini, None):
                        mini = mozne_min1
                if self.je_retezec_pripustny(mozne_max1, None):
                    if self.porovnej_retezce(maxi, mozne_max1, None, None) == -1:
                        maxi = mozne_max1
                    if not self.je_retezec_pripustny(maxi, None):
                        maxi = mozne_max1
                mk += 1
            mink.append(mini)  # do mink, resp. maxk se na pozici k připojuje řetezec mink pro konkrétní k
            maxk.append(maxi)
        self.mink = mink
        self.maxk = maxk

    def gamma_funkce(self, retezec):
        """Tato funkce zadaný konečný řetězec převede do desítkové soustavy

        :param retezec: řetězec, který chceme převést
        :type retezec: list
        """
        gamma = 0
        obraceny_retezec = retezec[::-1]  # přetočíme pro jednodušší počty
        for i in range(len(retezec)):
            gamma += (self.znamenko * self.beta) ** i * obraceny_retezec[i]
        return sp.N(gamma, n=20)

    def spocteni_vzdalenosti(self, k):
        """Tato funkce pro zadaná mink a maxk spočte jednotlivé vzdálenosti podle vzorce vzdálenost = abs()

        :param k:  maximální délka řetězců mink a maxk, pro kterou chceme spočítat vzdálenosti
        """
        delta = list()
        for i in range(k):
            vzdalenost = sp.N(abs(
                (self.znamenko * self.beta) ** i + self.gamma_funkce(self.mink[i]) - self.gamma_funkce(self.maxk[i])),
                n=20)
            delta.append(vzdalenost)
        self.delta = delta


class Rozvoj(object):
    """Třída pro rozvoj libovolného čísla v intervalu <l,l+1), nutno znát kladnou/zápornou (znaménko)
     bázi beta, bod, l, a počet cifer"""

    def __init__(self, baze, bod, levy_kraj, znamenko=1, symbolicke=False, pocet_cifer=30):
        """funkce, která se spustí automaticky s vytvořením instance Rozvoj, uloží si jednotlivé hodnoty a spočte
        rozvoj bodu s jeho periodou"""
        self.baze = baze
        self.znamenko = znamenko
        self.levy_kraj = levy_kraj
        if symbolicke:
            symbolicky_bod = sp.sympify(bod)
            self.bod = sp.N(symbolicky_bod.subs({x: self.baze}), n=40)  # přesnost
        else:
            self.bod = bod
        self.perioda = None
        self.rozvoj_bodu = None
        # self.nalezeni_rozvoje(pocet_cifer)

    def nalezeni_rozvoje(self, pocet_cifer=30):
        """pomocná funkce, která pro zadaný bod spočte rozvoj_bodu v dané bázi na pocet_cifer

        :param pocet_cifer: počet míst, na který chceme vyčíslit rozvoj pravého kraje, defaultně nastaven na 30
        """
        perioda = False
        transformace = list()
        rozvoj = list()
        transformace.append(self.bod)
        i = 1
        #start = time.time()
        while (not perioda) and (i < pocet_cifer):
            start = time.time()
            print(i)
            cifra = self.znamenko * self.baze * transformace[i - 1] - self.levy_kraj
            rozvoj.append(sp.floor(cifra))
            # rozvoj.append(sp.floor(sp.N(cifra.subs({x: self.baze}), n=30)))
            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            # transformace.append(sp.N(nova_transformace.subs({x: self.baze}), n=40))
            transformace.append(nova_transformace)

            print(cifra)
            print(rozvoj[i - 1])
            print(nova_transformace)

            for j in range(len(transformace)):
                if (abs(transformace[j] - transformace[i]) < MALO) and (j != i):
                    perioda = True
                    self.perioda = i - j
            i += 1
            cyklus= time.time() - start
            print("Cyklus trval {0:.2f} s".format(cyklus))
        self.rozvoj_bodu = rozvoj

    def limitni_rozvoj(self, pocet_cifer=10):
        """pomocná limitní funkce, která by pro pravý kraj měla spočítat rozvoj v dané bázi na pocet_cifer

        :param pocet_cifer: počet míst, na který chceme vyčíslit rozvoj pravého kraje, defaultně nastaven na 30
        """
        perioda = False
        transformace = list()
        rozvoj = list()
        transformace.append(self.bod)
        # y=sp.Symbol('y')
        # prvni = sp.limit(sp.floor(self.znamenko*self.baze*(self.levy_kraj+y)-self.levy_kraj),y,1,dir="-")
        # print(prvni)
        # print(self.levy_kraj)
        # kraj = sp.N(self.levy_kraj.subs({x: self.baze}))
        print(self.levy_kraj)
        print(self.baze)
        print("Následuje while cyklus")
        i = 1
        while (not perioda) and (i < pocet_cifer):
            print(i)
            cifra = self.znamenko * self.baze * transformace[i - 1] - self.levy_kraj
            print(cifra)
            pomocne = sp.floor(cifra)
            print(pomocne)
            rozvoj.append(sp.limit(pomocne, x, self.baze, dir="-"))
            # rozvoj.append(sp.floor(sp.N(cifra.subs({x: self.baze}), n=30)))
            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append((nova_transformace))
            for j in range(len(transformace)):
                if (abs(transformace[j] - transformace[i]) < MALO) and (j != i):
                    perioda = True
                    self.perioda = i - j
            i += 1
        self.rozvoj_bodu = rozvoj
