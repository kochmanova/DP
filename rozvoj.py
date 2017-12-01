import sympy as sp

from sympy.abc import x, a, b, c, d, e, f, g, h, k, l, m, n, o, p, q, r, s, t, u, v, w, beta
from sympy import latex
from time import time
from numpy import isreal, complex
from itertools import product

EPS = 9e-17
presnost = 684  # max 684, 700 nejde zatím
MALO = 2e-8


class Soustava(object):
    """ pro zadanou fci, levý kraj a znaménko báze vypočte bázi a zda námi zvolený levý kraj splňuje základní požadavky.
    Dále může spočítat rozvoj levého a pravého kraje s možností spočítat mink, maxk a jejich vzdálenosti"""

    def __init__(self, fce='x**3-x**2-x-1', znamenko=1, symbol_levy_kraj='-x/3'):
        """ funkce, která se zavolá sama, jakmile vytvořím instanci třídy Soustava, v rámci dané instance si uloží
         rovnici (proměnná fce), znaménko, bázi a symbolický levý kraj """
        self.baze = None
        self.levy_kraj = None
        self.fce = fce
        if (znamenko != 1) and (znamenko != -1):
            raise ValueError("Báze může být kladná s hodnotou 1 nebo záporná s hodnotou -1.")
        self.znamenko = znamenko

        self.rozvoj_leveho_kraje = None
        self.perioda_leveho_kraje = None
        self.rozvoj_praveho_kraje = None
        self.perioda_praveho_kraje = None

        self.mink = None
        self.maxk = None
        self.vzdalenosti = None

        self.spocitej_hodnotu_baze()
        self.spocitej_hodnotu_leveho_kraje(symbol_levy_kraj)

    def spocitej_hodnotu_baze(self):
        """ Tato funkce se zavolá sama, jakmile vytvoříme instanci třídy Soustava. Pro danou rovnici spočte bázi,
        se kterou budeme počítat a ověří, že splňuje základní požadavky, tedy beta in R a |beta|>1. """

        reseni_rovnice = sp.solve(self.fce, x)
        realne_koreny = [koren for koren in reseni_rovnice if isreal(complex(koren))]
        if len(realne_koreny) < 1:
            raise ValueError("Špatně zvolená rovnice. Rovnice musí mít alespoň jeden reálný kořen.")
        baze = [i for i in realne_koreny if i > 1]
        if len(baze) == 0:
            raise ValueError(
                "Bázi je nutno volit tak, aby měla alespoň jeden reálný kořen větší jak 1. Špatně zvolená rovnice.")
        self.baze = baze[0]

    def spocitej_hodnotu_leveho_kraje(self, symbol_levy_kraj):
        """ Tato funkce se zavolá sama, jakmile vytvoříme instanci třídy Soustava. Funkce, která pro levý kraj,
        jak symbolický vyjádřený pomocí bety(=x), tak hodnotu, zjistí, zda splňuje námi požadované podmínky."""

        symbolicky_levy_kraj = sp.sympify(symbol_levy_kraj)
        symbolicky_levy_kraj = symbolicky_levy_kraj.subs({x: self.baze})
        priblizny_kraj = sp.N(symbolicky_levy_kraj, n=presnost)
        print(priblizny_kraj)
        if (priblizny_kraj > 0) or (priblizny_kraj < -1):
            raise ValueError("Nejsou splněny základní požadavky, nula neleží v zadaném intervalu.")
        if (self.znamenko == -1) and ((-priblizny_kraj / self.baze - EPS > (priblizny_kraj + 1)) or -(
                    priblizny_kraj + 1) / self.baze + EPS < priblizny_kraj):
            # Je tahle podmínka správně nepsaná?
            raise ValueError("Nejsou splněny základní požadavky, interval není invariantní vůči posunutí.")
        self.levy_kraj = symbolicky_levy_kraj

    def nalezeni_presneho_rozvoje(self, bod, pocet_cifer=30):
        """ Funkce, která pro zadaný bod spočte rozvoj_bodu v dané bázi na pocet_cifer míst."""

        periodicke = False
        perioda = None
        transformace = list()
        rozvoj = list()
        transformace.append(bod)
        i = 1
        while (not periodicke) and (i <= pocet_cifer):
            # start = time()
            print("Počítáme {0:.0f}. cifru".format(i))
            cifra = self.znamenko * self.baze * transformace[i - 1] - self.levy_kraj
            rozvoj.append(sp.simplify(sp.floor(cifra)))
            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append(nova_transformace)
            for j in range(len(transformace)):
                if (abs(transformace[j] - transformace[i]) < MALO) and (j != i):
                    periodicke = True
                    perioda = i - j
            i += 1
            # cyklus = time() - start
            # print("Cyklus trval {0:.2f} s".format(cyklus))
        return rozvoj, perioda

    def nalezeni_priblizneho_rozvoje(self, bod, pocet_cifer=30):
        """ Funkce, která pro zadaný bod spočte rozvoj_bodu v dané bázi na pocet_cifer. Tato funkce nepracuje
        s přesnými hodnotami (ukládá hodnoty vyjádřené na max. 684 desetinných míst), dochází zde k zaokrouhlování,
        což může vést k chybám, avšak oproti přesnému rozvoji je výpočet výrazně rychlejší."""

        periodicke = False
        # print("Pocitame LEVY: {}".format(self.levy_kraj))
        perioda = None
        transformace = list()
        rozvoj = list()
        transformace.append(sp.N(bod, n=presnost))
        i = 1
        while (not periodicke) and (i <= pocet_cifer):
            # start = time()
            print("Počítáme {0:.0f}. cifru".format(i))
            cifra = sp.floor(self.znamenko * self.baze * transformace[i - 1] - self.levy_kraj)
            pom = sp.simplify(cifra)
            rozvoj.append(pom)
            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append(sp.N(nova_transformace, n=presnost))
            for j in range(len(transformace)):
                if (abs(transformace[j] - transformace[i]) < MALO) and (j != i):
                    periodicke = True
                    perioda = i - j
            i += 1
            # cyklus = time() - start
            # print("Cyklus trval {0:.2f} s".format(cyklus))
        return rozvoj, perioda

    def nalezeni_limitniho_rozvoje(self, pocet_cifer=30):
        """ Funkce, která pro pravý kraj spočte limitní rozvoj v dané bázi na pocet_cifer."""

        periodicke = False
        perioda = None
        transformace = list()
        rozvoj = list()
        transformace.append(self.levy_kraj + 1)
        i = 1
        dolni_cifra = sp.floor(self.znamenko * self.baze * x - self.levy_kraj)
        cifra = self.znamenko * self.baze * x - self.levy_kraj
        while (not periodicke) and (i <= pocet_cifer):
            # start = time.time()
            print("Počítáme {0:.0f}.cifru ".format(i))
            cifra_dosazena = cifra.subs(x, transformace[i - 1])
            zjednoduseni = sp.simplify(cifra_dosazena)

            if sp.sympify(zjednoduseni).is_Integer:
                if (self.znamenko < 0) and (i % 2 == 1):
                    rozvoj.append(zjednoduseni)
                else:
                    rozvoj.append(zjednoduseni - 1)
                    # print("Na {0:.0f}.pozici jsme nalezli integer, proto přičítáme -1".format(i))
            else:
                if (self.znamenko < 0) and (i % 2 == 0):
                    rozvoj.append(sp.limit(dolni_cifra, x, transformace[i - 1], dir='+'))
                else:
                    rozvoj.append(sp.limit(dolni_cifra, x, transformace[i - 1], dir='-'))

            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append((nova_transformace))
            for j in range(len(transformace)):
                if (abs(sp.N((transformace[j] - transformace[i]).subs({x: self.levy_kraj + 1}))) < MALO) and (j != i):
                    periodicke = True
                    perioda = i - j
            i += 1
            # cyklus = time() - start
            # print("Cyklus trval {0:.2f} s".format(cyklus))
        return rozvoj, perioda

    def nalezeni_limitniho_rozvoj_bez_limit(self, pocet_cifer=30):
        """ Funkce, která pro pravý kraj spočte limitní rozvoj pravého kraje bez použití limit v dané bázi
        na pocet_cifer. TODO zjistit, zda je časově rychlejší oproti pravému kraji"""

        periodicke = False
        perioda = None
        transformace = list()
        rozvoj = list()
        transformace.append(self.levy_kraj + 1)
        i = 1
        dolni_cifra = sp.floor(self.znamenko * self.baze * x - self.levy_kraj)
        cifra = self.znamenko * self.baze * x - self.levy_kraj
        while (not periodicke) and (i <= pocet_cifer):
            # start = time()
            print("Počítáme {0:.0f}.cifru ".format(i))
            cifra_dosazena = cifra.subs(x, transformace[i - 1])
            zjednoduseni = sp.simplify(cifra_dosazena)
            if sp.sympify(zjednoduseni).is_Integer:
                if (self.znamenko < 0) and (i % 2 == 1):
                    rozvoj.append(zjednoduseni)
                else:
                    rozvoj.append(zjednoduseni - 1)
                    # print("Na {0:.0f}.pozici jsme nalezli integer, proto přičítáme -1".format(i))
            else:

                #                 if (self.znamenko < 0) and (i % 2 == 0):
                #                     rozvoj.append(dolni_cifra.subs(x,transformace[i-1]))
                # #                     rozvoj.append(sp.limit(dolni_cifra, x, transformace[i - 1], dir='+'))
                #                 else:
                #                     cifra_upr = sp.floor(cifra-1)
                #                     rozvoj.append(cifra_upr.subs(x,transformace[i-1]))
                rozvoj.append(dolni_cifra.subs(x, transformace[i - 1]))
            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append((nova_transformace))
            for j in range(len(transformace)):
                if (abs(sp.N((transformace[j] - transformace[i]).subs({x: self.levy_kraj + 1}))) < MALO) and (
                            j != i):
                    periodicke = True
                    perioda = i - j
            i += 1
            # cyklus = time()-start
            # print("Cyklus trval {0:.2f} s".format(cyklus))
        return rozvoj, perioda

    def spocitej_rozvoj_leveho_kraje(self, presne=True, pocet_cifer=30):
        """ Funkce, která zavolá funkci pro nalezení rozvoje levého kraje přesně, resp. nepřesně podle parametru presne,
        na pocet_cifer. Danou hodnotu spolu s hodnotou periody si uloží. V případě, že perioda nebyla nalezena, bude
        tato proměnná obsahovat hodnotu None."""
        if presne:
            self.rozvoj_leveho_kraje, self.perioda_leveho_kraje = self.nalezeni_presneho_rozvoje(self.levy_kraj,
                                                                                                 pocet_cifer)
        else:
            self.rozvoj_leveho_kraje, self.perioda_leveho_kraje = self.nalezeni_priblizneho_rozvoje(self.levy_kraj,
                                                                                                    pocet_cifer)
        print("Nalezli jsme rozvoj levého kraje: [%s]" % ",".join(map(str, self.rozvoj_leveho_kraje)))
        print("S periodou délky {}".format(self.perioda_leveho_kraje))

    def spocitej_rozvoj_praveho_kraje(self, presne=True, pocet_cifer=30):
        """ Funkce, která zavolá funkci pro nalezení limitního rozvoje pravého kraje pomocí limity, resp. bez limity
        podle parametru presne, na pocet_cifer. Danou hodnotu spolu s hodnotou periody si uloží. V případě, že perioda
        nebyla nalezena, bude tato proměnná obsahovat hodnotu None."""
        if presne:
            self.rozvoj_praveho_kraje, self.perioda_praveho_kraje = self.nalezeni_limitniho_rozvoje(pocet_cifer)
        else:
            self.rozvoj_praveho_kraje, self.perioda_praveho_kraje = self.nalezeni_limitniho_rozvoj_bez_limit(
                pocet_cifer)
        print("Nalezli jsme rozvoj pravého kraje: [%s]" % ",".join(map(str, self.rozvoj_praveho_kraje)))
        print("S periodou délky {}".format(self.perioda_praveho_kraje))

    def prilep_periodu(self, retezec, perioda, delka_retezce):
        """ Pomocná funkce, která zřetězí retezec, v případě periody o periodu tolikrát, aby délka výsledného řetězce byla rovna
        delka_retezce v případě, že retezec nemá periodu, se zřetězí na požadovanou délku pomocí nul.
        V případě, že původní retezec je delší než delka_retezce, je retezec zkrácen na požadovanou délku.

        :param retezec (list): počáteční řetězec, který chceme prodloužit
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
        """Funkce, která porovná dva řetězce i různé délky.

        :param prvni_retezec (list): první řetezec, který porovnáváme
        :param druhy_retezec (list): řetězec, se kterým porovnáváme prvni_retezec
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
        """ Funkce, která zjistí, zda je retezec a libovolný jeho sufix >= rozvoj_leveho_kraje.rozvoj_bodu

        :type retezec: list
        :param perioda_retezce: délka periody řetězce (int), pokud nemá periodu, hodnota je None
        :returns: bool
        """
        pracovni_retezec = retezec.copy()
        while len(pracovni_retezec) > 0:
            if self.porovnej_retezce(self.rozvoj_leveho_kraje, pracovni_retezec,
                                     self.perioda_leveho_kraje, perioda_retezce) > 0:
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
            if self.porovnej_retezce(pracovni_retezec, self.rozvoj_praveho_kraje, perioda_retezce,
                                     self.perioda_praveho_kraje) >= 0:
                return False
            pracovni_retezec.pop(0)
        return True

    def je_retezec_pripustny(self, retezec, perioda_retezce):
        """funkce, která zjistí, zda je retezec připustný

        :type retezec: list
        :param perioda_retezce: délka periody řetězce (int), pokud nemá periodu, hodnota je None
        :returns: bool
        """
        if self.je_retezec_zprava_pripustny(retezec, perioda_retezce) \
                and self.je_retezec_zleva_pripustny(retezec, perioda_retezce):
            return True
        else:
            return False

    def spocitej_mink_maxk(self, k):
        """tato funkce pro zadané k nalézne řetězce mink a maxk až do délky řetězce k

        :param k: maximální délka řetězců mink a maxk, kterou chceme vytvořit
        """
        mink = list()
        maxk = list()
        min0 = []
        max0 = []
        mink.append(min0)
        maxk.append(max0)
        for i in range(1, k):
            mini = self.prilep_periodu(self.rozvoj_leveho_kraje.rozvoj_bodu, self.rozvoj_leveho_kraje.vyjadreni_periody,
                                       i)
            maxi = self.prilep_periodu(self.rozvoj_praveho_kraje.rozvoj_bodu,
                                       self.rozvoj_praveho_kraje.vyjadreni_periody, i)
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

    def spocitej_vzdalenosti(self, k):
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


class Perioda(object):
    def __init__(self, fce, baze, znamenko, k, p, presnost=True):
        """funkce, která se spustí automaticky s vytvořením instance Rozvoj, uloží si jednotlivé hodnoty a spočte
        rozvoj bodu s jeho periodou"""
        self.baze = baze
        self.fce = fce
        self.znamenko = znamenko
        self.k = k
        self.p = p
        self.symboly = [a, b, c, d, e, f, g, h, k, l, m, n, o, p, q, r, s, t, u, v, w]
        self.mocnina = 1
        self.hodnoty = list()
        self.leve_kraje = list()
        self.presne = presnost
        self.vycisleny_vyraz = None

        self.vyjadreni_celeho_vyrazu()
        self.vycisleni_vyrazu_beta()
        # self.dosazeni_vse()

    def vyjadreni_predperiody(self):
        vyraz = 0
        if self.k > 0:
            pomocna = self.k
            while pomocna > 0:
                vyraz = vyraz + self.symboly.pop(0) / beta ** self.mocnina
                self.mocnina = self.mocnina + 1
                pomocna = pomocna - 1
        self.vyraz_pred = vyraz

    def vyjadreni_periody(self):
        vyraz = 0
        pomocna = self.p
        while pomocna > 0:
            vyraz = vyraz + self.symboly.pop(0) / beta ** (self.mocnina - self.p) * 1 / (beta ** self.p - 1)
            self.mocnina = self.mocnina + 1
            pomocna -= 1
        self.vyraz_perioda = vyraz

    def vyjadreni_celeho_vyrazu(self):
        self.vyjadreni_predperiody()
        self.vyjadreni_periody()
        self.vyraz = self.vyraz_pred + self.vyraz_perioda
        print(self.vyraz)

    def vycisleni_vyrazu_beta(self):
        vycisleny = self.vyraz.subs(beta, self.baze)
        # print(vycisleny)
        self.vycisleny_vyraz = vycisleny

    # Bylo by hezké mít funkci, která dosadí všechny hodnoty krom bety abychom viděli, jak vypadá levý kraj vyjádřen s pomocí bety
    def vycisleni_vyrazu_abc(self, vyraz, hodnoty):
        pom_vyraz = vyraz
        symboly = [a, b, c, d, e, f, g, h, k, l, m, n, o, p, q, r, s, t, u, v, w]
        pom_hodnoty = list(hodnoty)
        while len(pom_hodnoty) > 0:
            pom_vyraz = pom_vyraz.subs(symboly.pop(0), pom_hodnoty.pop(0))
        return pom_vyraz

    def dosazeni_overeni_leveho_kraje(self, hodnoty):
        levy_kraj = self.vycisleni_vyrazu_abc(self.vycisleny_vyraz, hodnoty)
        # symboly=[a,b,c,d,e,f,g,h,i,j]
        # pomocne = self.k+self.p
        # vyraz=self.vycisleny_vyraz
        # pom_hodnoty = list(hodnoty)
        # while len(pom_hodnoty) > 0: #pomocne > 0:
        #    vyraz=vyraz.subs(symboly.pop(0),pom_hodnoty.pop(0))
        # print(vyraz)
        priblizny_levy_kraj = sp.N(levy_kraj, n=1000)
        if priblizny_levy_kraj <= 0 and priblizny_levy_kraj >= -1:
            rozvoj_leveho_kraje = list(hodnoty)
            # print(vyraz)
            self.zpetne_overeni(rozvoj_leveho_kraje, levy_kraj)
            # dodatečná podmínka pro tuto konkrétní bázi
            # if prosel and (levy_kraj > -1/self.baze and levy_kraj <= 1/self.baze-1):
            # TU PODMÍNKU JSEM POKANHALA
            #    print("Daný řetězec neleží v L_beta, tedy má Z_b jen s 0.")
            # self.hodnoty.append(list(hodnoty))
            # self.levy_kraj.append(vyraz)
            # levy_kraj = sp.N(vyraz,n=20)
            # print(hodnoty)
            # print(levy_kraj) # mít to ve formatu je problém s nulou...nevim proč

    def dosazeni_vse(self, abeceda=[-1, 0, 1]):
        # abeceda=[-1,0,1]
        delka = self.k + self.p
        hodnoty = list(product(abeceda, repeat=delka))
        # já to tak chci yeld!!!!
        # print(hodnoty)
        print("Celkem máme {0:.0f} řetezců".format(len(hodnoty)))
        # self.hodnoty=hodnoty
        i=0
        for retezec in hodnoty:
            print(i)
            self.dosazeni_overeni_leveho_kraje(retezec)
            i+=1

    def zpetne_overeni(self, hodnoty, levy):  # hodnoty jsou list!!
        hledany_rozvoj = Soustava(self.fce, self.znamenko, levy)
        # print(levy)
        # print(hodnoty)
        # print(hledany_rozvoj.rozvoj_leveho_kraje.rozvoj_bodu)
        print("Nyni delame rozvoj tohohle:  [%s]" % ",".join(map(str, hodnoty)))
        print(levy)
        # print(sp.simplify(levy))
        if hodnoty == [-1, -1, -1, 1, 0, 0]:
            print("ahoj")
        hledany_rozvoj.spocitej_rozvoj_leveho_kraje(self.presne, 2 * self.p + self.k)
        if hodnoty == hledany_rozvoj.rozvoj_leveho_kraje:
            if self.p == hledany_rozvoj.perioda_leveho_kraje:
                self.hodnoty.append(hodnoty)
                self.leve_kraje.append(levy)
                print("Retezec, ktery ma {} predperiodu a {} periodu je (retezec, levy kraj):".format(self.k, self.p))
                print(hodnoty)
                # print(self.p)
                print(levy)
                print(sp.simplify(levy))
                pomoc = Soustava(self.fce, self.znamenko, sp.simplify(levy))
                print("Tento retezec ma pak po ZJEDNODUSENI rozvoj praveho kraje:")
                pomoc.spocitej_rozvoj_praveho_kraje(False, 2 * self.p + self.k)
                print(pomoc.rozvoj_praveho_kraje)
                print(pomoc.perioda_praveho_kraje)
                print("Tento retezec ma pak rozvoj praveho kraje a periodu: ")
                hledany_rozvoj.spocitej_rozvoj_praveho_kraje(False, 2 * self.p + self.k)
                print(hledany_rozvoj.rozvoj_praveho_kraje)
                print(hledany_rozvoj.perioda_praveho_kraje)
                # return True
                # return False
