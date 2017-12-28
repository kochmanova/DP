import sympy as sp
from sympy import latex
from time import time
from numpy import isreal, complex
from sympy.abc import x

EPS = 9e-17
presnost = 1000#684  # max 684, 700 nejde zatím
MALO = 2e-8


class Soustava(object):
    """
    Pro zadanou fci, levý kraj a znaménko báze vypočte bázi a zda námi zvolený levý kraj splňuje základní požadavky.
    Dále může spočítat rozvoj levého a pravého kraje s možností spočítat mink, maxk a jejich vzdálenosti.
    """

    def __init__(self, fce='x**3-x**2-x-1', znamenko=1, symbol_levy_kraj='-x/3'):
        """
        Funkce, která se zavolá sama, jakmile vytvořím instanci třídy Soustava, v rámci dané instance si uloží
        rovnici (proměnná fce), znaménko, bázi a symbolický levý kraj
        """

        self.baze = None
        self.levy_kraj = None
        self.fce = fce
        if (znamenko != 1) and (znamenko != -1):
            raise ValueError("Báze může být kladná s hodnotou 1 nebo záporná s hodnotou -1.")
        self.znamenko = znamenko
        self.symbol_levy_kraj = symbol_levy_kraj

        self.rozvoj_leveho_kraje = None
        self.perioda_leveho_kraje = None
        self.rozvoj_praveho_kraje = None
        self.perioda_praveho_kraje = None

        self.mink = None
        self.maxk = None
        self.vzdalenosti = None
        self.vzdalenosti_symbolicky = None

        self.spocitej_hodnotu_baze()
        if symbol_levy_kraj is not None:
            self.spocitej_hodnotu_leveho_kraje(symbol_levy_kraj)

    def spocitej_hodnotu_baze(self):
        """
        Tato funkce se zavolá sama, jakmile vytvoříme instanci třídy Soustava. Pro danou rovnici spočte bázi,
        se kterou budeme počítat a ověří, že splňuje základní požadavky, tedy beta in R a |beta|>1.
        """

        # TODO existuje funkce, která se jmenuje podobně a možná dělá jen tu konkrétní věc a to chci -> podívat
        reseni_rovnice = sp.solve(self.fce, x)
        #realne_koreny = [koren for koren in reseni_rovnice if isreal(complex(koren))] -> dělá to to samé?? :D SNAD ANO, zjistit
        realne_koreny = [koren for koren in reseni_rovnice if sp.sympify(koren).is_real]
        if len(realne_koreny) < 1:
            raise ValueError("Špatně zvolená rovnice. Rovnice musí mít alespoň jeden reálný kořen.")
        baze = [i for i in realne_koreny if i > 1]
        if len(baze) == 0:
            raise ValueError(
                "Bázi je nutno volit tak, aby měla alespoň jeden reálný kořen větší jak 1. Špatně zvolená rovnice.")
        self.baze = baze[0]

    def spocitej_hodnotu_leveho_kraje(self, symbol_levy_kraj: str):
        """
        Tato funkce se zavolá sama, jakmile vytvoříme instanci třídy Soustava. Funkce, která pro levý kraj,
        jak symbolický vyjádřený pomocí bety(=x), tak hodnotu, zjistí, zda splňuje námi požadované podmínky.
        :param symbol_levy_kraj:
        """
        # TODO ohledně té podmínky a její správnosti

        symbolicky_levy_kraj = sp.sympify(symbol_levy_kraj)
        symbolicky_levy_kraj = symbolicky_levy_kraj.subs({x: self.baze})
        priblizny_kraj = sp.N(symbolicky_levy_kraj, n=presnost)
        # print(priblizny_kraj) # výpis hodnoty levého kraje
        if (priblizny_kraj > 0) or (priblizny_kraj < -1):
            raise ValueError("Nejsou splněny základní požadavky, nula neleží v zadaném intervalu.")
        if (self.znamenko == -1) and ((-priblizny_kraj / self.baze - EPS > (priblizny_kraj + 1)) or -(
                    priblizny_kraj + 1) / self.baze + EPS < priblizny_kraj):
            # Je tahle podmínka správně nepsaná?
            raise ValueError("Nejsou splněny základní požadavky, interval není invariantní vůči posunutí.")
        self.levy_kraj = symbolicky_levy_kraj

    def nalezeni_presneho_rozvoje(self, bod, pocet_cifer=30):
        """
        Funkce, která pro zadaný bod spočte rozvoj_bodu v dané bázi na pocet_cifer míst a vrátí je.

        :param bod (float, nebo přesný výraz, který leží v intervalu <l,l+1)) , tomuto bodu nalezne rozvoj
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat rozvoj daného bodu
        :returns rozvoj (list) bodu
        :returns perioda (int/None)
        """
        # TODO podmínka pro bod - ValueError, bod je sympy/ int?

        periodicke = False
        perioda = None
        transformace = list()
        rozvoj = list()
        transformace.append(bod)
        i = 1
        while (not periodicke) and (i <= pocet_cifer):
            #start = time()
            print("Počítáme {0:.0f}. cifru".format(i))
            cifra = self.znamenko * self.baze * transformace[i - 1] - self.levy_kraj
            # rozvoj.append(sp.simplify(sp.floor(cifra))) -> zjevně to dávám s cancel
            #mez = time()
            #print("Nalezli jsme cifru čas {0:.2f}".format(mez-start))
            rozvoj.append(int(sp.N(sp.cancel(sp.floor(cifra)),n=1,chop=True)))
            #mm = time()
            #print("Pripojili jsme cifru trvalo to {0:.2f}".format(mm-mez))
            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            #tr = time()
            #print("nova transformace s časem {0:.2f}".format(tr-mm))
            transformace.append(nova_transformace)
            #kk = time()
            #print("Pripojeni s časem {0:.2f}".format(kk-tr))
            for j in range(len(transformace)):
                if (abs(transformace[j] - transformace[i]) < MALO) and (j != i):
                    periodicke = True
                    perioda = i - j
            i += 1
            #tada = time()
            #print("Proběhl forcyklus s časem {0:.2f}".format(tada-kk))
            # cyklus = time() - start
            # print("Cyklus trval {0:.2f} s".format(cyklus))
        return tuple(rozvoj), perioda

    def nalezeni_priblizneho_rozvoje(self, bod, pocet_cifer=30):
        """
        Funkce, která pro zadaný bod spočte rozvoj_bodu v dané bázi na pocet_cifer. Tato funkce nepracuje
        s přesnými hodnotami (ukládá hodnoty vyjádřené na max. 684 desetinných míst), dochází zde k zaokrouhlování,
        což může vést k chybám, avšak oproti přesnému rozvoji je výpočet výrazně rychlejší.

        :param bod (float, nebo přesný výraz, který leží v intervalu <l,l+1)) , tomuto bodu nalezne rozvoj
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat rozvoj daného bodu
        :returns rozvoj (list) bodu
        :returns perioda (int/None)
        """
        # TODO podmínka pro bod - ValueError

        periodicke = False
        perioda = None
        transformace = list()
        rozvoj = list()
        transformace.append(sp.N(bod, n=presnost, chop=True))
        i = 1
        while (not periodicke) and (i <= pocet_cifer):
            # start = time()
            print("Počítáme {0:.0f}. cifru".format(i))
            cifra = sp.floor(self.znamenko * self.baze * transformace[i - 1] - self.levy_kraj)
            #rozvoj.append(int(sp.N(sp.cancel(cifra),n=1, chop=True)))
            rozvoj.append(int(sp.N(cifra,n=1,chop=True)))
            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append(sp.N(nova_transformace, n=presnost, chop=True))
            for j in range(len(transformace)):
                if (abs(transformace[j] - transformace[i]) < MALO) and (j != i):
                    periodicke = True
                    perioda = i - j
            i += 1
            # cyklus = time() - start
            # print("Cyklus trval {0:.2f} s".format(cyklus))
        return tuple(rozvoj), perioda

    def nalezeni_limitniho_rozvoje(self, pocet_cifer=30):
        """
        Funkce, která pro pravý kraj spočte limitní rozvoj v dané bázi na pocet_cifer.
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat rozvoj daného bodu
        :returns rozvoj (list)
        :returns perioda (int/None)
        """

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
            # zjednoduseni = sp.simplify(cifra_dosazena) # tu je to zlý -> opraveno ?
            zjednoduseni = sp.cancel(cifra_dosazena)

            if sp.sympify(zjednoduseni).is_Integer:
                if (self.znamenko < 0) and (i % 2 == 1):
                    rozvoj.append(zjednoduseni)
                else:
                    rozvoj.append(zjednoduseni - 1)
            else:
                if (self.znamenko < 0) and (i % 2 == 0):
                    rozvoj.append(sp.limit(dolni_cifra, x, transformace[i - 1], dir='+'))
                else:
                    rozvoj.append(sp.limit(dolni_cifra, x, transformace[i - 1], dir='-'))

            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append(nova_transformace)
            for j in range(len(transformace)):
                if (abs(sp.N((transformace[j] - transformace[i]).subs({x: self.levy_kraj + 1}))) < MALO) and (j != i):
                    periodicke = True
                    perioda = i - j
            i += 1
            # cyklus = time() - start
            # print("Cyklus trval {0:.2f} s".format(cyklus))
        return tuple(rozvoj), perioda

    def nalezeni_limitniho_rozvoj_bez_limit(self, pocet_cifer=30):
        """
        Funkce, která pro pravý kraj spočte limitní rozvoj pravého kraje bez použití limit v dané bázi
        na pocet_cifer.
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat rozvoj daného bodu
        :returns rozvoj (list)
        :returns perioda (int/None)
        """
        # TODO zjistit, zda je časově rychlejší oproti pravému kraji

        #print("Jsem tu")
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
            # zjednoduseni = sp.simplify(cifra_dosazena) # Tu je to zlý
            zjednoduseni = sp.cancel(cifra_dosazena)
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
                rozvoj.append(sp.cancel(dolni_cifra.subs(x, transformace[i - 1])))
            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append(nova_transformace)
            for j in range(len(transformace)):
                if (abs(sp.N((transformace[j] - transformace[i]).subs({x: self.levy_kraj + 1}))) < MALO) and (
                            j != i):
                    periodicke = True
                    perioda = i - j
            i += 1
            # cyklus = time()-start
            # print("Cyklus trval {0:.2f} s".format(cyklus))
        return tuple(rozvoj), perioda

    def spocitej_rozvoj_leveho_kraje(self, presne=True, pocet_cifer=30):
        """
        Funkce, která zavolá funkci pro nalezení rozvoje levého kraje přesně, resp. nepřesně podle parametru presne,
        na pocet_cifer. Danou hodnotu spolu s hodnotou periody si uloží a vypíše. V případě, že perioda nebyla nalezena,
        bude tato proměnná obsahovat hodnotu None.
        :param presne:
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat rozvoj daného bodu
        """

        if presne:
            self.rozvoj_leveho_kraje, self.perioda_leveho_kraje = self.nalezeni_presneho_rozvoje(self.levy_kraj,
                                                                                                 pocet_cifer)
        else:
            self.rozvoj_leveho_kraje, self.perioda_leveho_kraje = self.nalezeni_priblizneho_rozvoje(self.levy_kraj,
                                                                                                    pocet_cifer)
        print("Nalezli jsme rozvoj levého kraje: [%s]" % ",".join(map(str, self.rozvoj_leveho_kraje)))
        print("S periodou délky {}".format(self.perioda_leveho_kraje))

    def spocitej_rozvoj_praveho_kraje(self, presne=True, pocet_cifer=30):
        """
        Funkce, která zavolá funkci pro nalezení limitního rozvoje pravého kraje pomocí limity, resp. bez limity
        podle parametru presne, na pocet_cifer. Danou hodnotu spolu s hodnotou periody si uloží a vypíše. V případě, že
        perioda nebyla nalezena, bude tato proměnná obsahovat hodnotu None.
        :param presne:
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat rozvoj daného bodu
        """

        if presne:
            self.rozvoj_praveho_kraje, self.perioda_praveho_kraje = self.nalezeni_limitniho_rozvoje(pocet_cifer)
        else:
            self.rozvoj_praveho_kraje, self.perioda_praveho_kraje = self.nalezeni_limitniho_rozvoj_bez_limit(
                pocet_cifer)
        print("Nalezli jsme rozvoj pravého kraje: [%s]" % ",".join(map(str, self.rozvoj_praveho_kraje)))
        print("S periodou délky {}".format(self.perioda_praveho_kraje))

    def prilep_periodu(self, retezec: list, perioda: int, delka_retezce: int):
        """
        Pomocná funkce, která zřetězí retezec, v případě periody o periodu tolikrát, aby délka výsledného řetězce byla
        rovna delka_retezce; v případě, že retezec není periodický, se zřetězí na požadovanou délku pomocí nul.
        V případě, že původní retezec je delší než delka_retezce, je retezec zkrácen na požadovanou délku.

        :param retezec: počáteční řetězec, který chceme prodloužit
        :param perioda: délka periody řetězce (int), pokud nemá periodu, hodnota je None a řetezec se doplní nulami
        :param delka_retezce: požadovaná délka prodlouženého řetězce
        :returns list: prodloužený nebo zkrácený řetězec na požadovanou délku
        """
        pom = retezec # jak je to s retezec.copy()?
        delka = len(pom)
        if perioda is None:
            pridam_nuly = [0] * (delka_retezce - delka)
            pom.extend(pridam_nuly)
        else:
            perioda_retezce = pom[-perioda:]
            pridam_periodu = (delka_retezce - delka) // perioda + 1
            prodlouzeni = perioda_retezce * pridam_periodu
            pom.extend(prodlouzeni)
        useknu = len(pom) - delka_retezce
        pom = pom[:-useknu]
        return pom

    def porovnej_retezce(self, prvni_retezec: list, druhy_retezec: list, perioda_prvniho: int, perioda_druheho: int):
        """
        Funkce, která porovná dva řetězce i různé délky.

        :param prvni_retezec: první řetezec, který porovnáváme
        :param druhy_retezec: řetězec, se kterým porovnáváme prvni_retezec
        :param perioda_prvniho: délka periody prvního řetězce (int), pokud nemá periodu, hodnota je None
        :param perioda_druheho: délka periody druhého řetězce (int), pokud nemá periodu, hodnota je None

        :returns: -1: prvni_retezec < druhy_retezec
        :returns: 1: prvni_retezec > druhy_retezec
        :returns: 0: prvni_retezec = druhy_retezec
        """

        #if (perioda_prvniho is not None) and (perioda_druheho is not None):
        #    raise ValueError("V současnosti neumíme a neporovnáváme dva řetězce s periodou!")

        # TODO Budeme umět

        pracovni_retezec_1 = prvni_retezec.copy()
        pracovni_retezec_2 = druhy_retezec.copy()
        if perioda_prvniho is None and perioda_druheho is None:
            delka_retezce = max(len(pracovni_retezec_1), len(pracovni_retezec_2))
        elif perioda_prvniho is not None:
            delka_retezce = max(len(pracovni_retezec_1),len(pracovni_retezec_2))+perioda_prvniho
        elif perioda_druheho is not None:
            delka_retezce = max(len(pracovni_retezec_1),len(pracovni_retezec_2))+perioda_druheho
        else:
            delka_retezce = max(len(pracovni_retezec_1),len(pracovni_retezec_2))+max(perioda_prvniho,perioda_druheho)
        #if perioda_prvniho is not None:
        #    pridam_nuly = [0] * perioda_prvniho
        #    pracovni_retezec_2.extend(pridam_nuly)
        #if perioda_druheho is not None:
        #    pridam_nuly = [0] * perioda_druheho
        #    pracovni_retezec_1.extend(pridam_nuly)
        #if len(pracovni_retezec_1) > len(pracovni_retezec_2):
        #    pracovni_retezec_2 = self.prilep_periodu(pracovni_retezec_2, perioda_druheho, len(pracovni_retezec_1))
        #elif len(pracovni_retezec_2) > len(pracovni_retezec_1):
        #    pracovni_retezec_1 = self.prilep_periodu(pracovni_retezec_1, perioda_prvniho, len(pracovni_retezec_2))
        pracovni_retezec_1 = self.prilep_periodu(pracovni_retezec_1,perioda_prvniho,delka_retezce)
        pracovni_retezec_2 = self.prilep_periodu(pracovni_retezec_2,perioda_druheho,delka_retezce)
        for i in range(len(pracovni_retezec_1)):
            if self.znamenko ** (i + 1) * pracovni_retezec_1[i] < self.znamenko ** (i + 1) * pracovni_retezec_2[i]:
                return -1  # prvni retezec je MENSI jak druhy retezec
            elif self.znamenko ** (i + 1) * pracovni_retezec_1[i] \
                    > self.znamenko ** (i + 1) * pracovni_retezec_2[i]:
                return 1  # prvni retezec je VETSI jak druhy retezec
        return 0  # retezce se rovnaji

    def je_retezec_zleva_pripustny(self, retezec: list, perioda_retezce: int):
        """
        Funkce, která zjistí, zda je retezec a libovolný jeho sufix >=lex/alt rozvoj_leveho_kraje.rozvoj_bodu
        :param retezec:
        :param perioda_retezce: délka periody řetězce (int), pokud nemá periodu, hodnota je None
        :returns: bool
        """

        pracovni_retezec = retezec.copy()
        while len(pracovni_retezec) > 0:
            if self.porovnej_retezce(list(self.rozvoj_leveho_kraje), pracovni_retezec,
                                     self.perioda_leveho_kraje, perioda_retezce) > 0:
                return False
            pracovni_retezec.pop(0)
        return True

    def je_retezec_zprava_pripustny(self, retezec: list, perioda_retezce: int):
        """
        Funkce, která zjistí, zda je retezec a libovolný jeho sufix <lex/alt rozvoj_praveho_kraje.rozvoj_bodu
        :param retezec:
        :param perioda_retezce: délka periody řetězce (int), pokud nemá periodu, hodnota je None
        :returns: bool
        """

        pracovni_retezec = retezec.copy()
        while len(pracovni_retezec) > 0:
            if self.porovnej_retezce(pracovni_retezec, list(self.rozvoj_praveho_kraje), perioda_retezce,
                                     self.perioda_praveho_kraje) >= 0:
                return False
            pracovni_retezec.pop(0)
        return True

    def je_retezec_pripustny(self, retezec: list, perioda_retezce: int):
        """
        Funkce, která zjistí, zda je retezec připustný.

        :param retezec:
        :param perioda_retezce: délka periody řetězce, pokud nemá periodu, hodnota je None
        :returns: bool
        """

        if self.je_retezec_zprava_pripustny(retezec, perioda_retezce) \
                and self.je_retezec_zleva_pripustny(retezec, perioda_retezce):
            return True
        else:
            return False

    def spocitej_mink_maxk(self, k: int):
        """
        Funkce pro zadané k nalézne řetězce mink a maxk až do délky řetězce k.

        :param k: maximální délka řetězců mink a maxk, kterou chceme vytvořit
        """

        rozvoj_levy = list(self.rozvoj_leveho_kraje)
        rozvoj_pravy = list(self.rozvoj_praveho_kraje)
        mink = list()
        maxk = list()
        min0 = []
        max0 = []
        mink.append(min0)
        maxk.append(max0)
        for i in range(1, k):
            mini = self.prilep_periodu(rozvoj_levy, self.perioda_leveho_kraje,
                                       i)
            maxi = self.prilep_periodu(rozvoj_pravy,
                                       self.perioda_praveho_kraje, i)
            print(mini)
            print(maxi)
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
        self.spocitej_vzdalenosti(k)
        self.spocitej_vzdalenosti_symbolicky(k)

    def gamma_funkce(self, retezec: list):
        """
        Tato funkce zadaný konečný řetězec převede do desítkové soustavy

        :param retezec: řetězec, který chceme převést
        """

        gamma = 0
        obraceny_retezec = retezec[::-1]  # přetočíme pro jednodušší počty
        for i in range(len(retezec)):
            gamma += (self.znamenko * self.baze) ** i * obraceny_retezec[i]
        return sp.N(gamma, n=20)

    def spocitej_vzdalenosti(self, k: int):
        """
        Tato funkce pro zadaná mink a maxk spočte jednotlivé vzdálenosti podle vzorce TODO č.vzorce

        :param k:  maximální délka řetězců mink a maxk, pro kterou chceme spočítat vzdálenosti
        """

        delta = list()
        for i in range(k):
            vzdalenost = sp.N(abs(
                (self.znamenko * self.baze) ** i + self.gamma_funkce(self.mink[i]) - self.gamma_funkce(self.maxk[i])),
                n=20)
            delta.append(vzdalenost)
        self.vzdalenosti = delta

    def gamma_funkce_symbolicky(self, retezec: list):
        """
        Tato funkce zadaný konečný řetězec převede do desítkové soustavy

        :param retezec: řetězec, který chceme převést
        """

        gamma = 0
        obraceny_retezec = retezec[::-1]  # přetočíme pro jednodušší počty
        for i in range(len(retezec)):
            gamma += (self.znamenko * x) ** i * obraceny_retezec[i]
        return sp.N(gamma, n=20)

    def spocitej_vzdalenosti_symbolicky(self, k: int):
        """
        Tato funkce pro zadaná mink a maxk spočte jednotlivé vzdálenosti podle vzorce TODO č.vzorce

        :param k:  maximální délka řetězců mink a maxk, pro kterou chceme spočítat vzdálenosti
        """

        delta = list()
        for i in range(k):
            vzdalenost = abs(
                (self.znamenko * x) ** i + self.gamma_funkce_symbolicky(self.mink[i]) - self.gamma_funkce_symbolicky(self.maxk[i]))
            delta.append(vzdalenost)
        self.vzdalenosti_symbolicky = delta

    def lezi_retezec_mezi(self, retezec: tuple, perioda_retezce: int, levy:tuple, levy_perioda: int, pravy:tuple, pravy_perioda: int):
        pom_retezec = list(retezec)
        while len(pom_retezec)>0:
            if self.porovnej_retezce(pom_retezec, list(levy), perioda_retezce, levy_perioda) <= 0:
                return False
            if self.porovnej_retezce(pom_retezec, list(pravy), perioda_retezce, pravy_perioda) >= 0:
                return False
            pom_retezec.pop(0)
        return True
