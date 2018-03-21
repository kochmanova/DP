import sympy as sp
from sympy.abc import x
from itertools import product

EPS = 9e-17
presnost = 1000
MALO = 2e-8


class Soustava(object):
    """
    Pro zadanou fci, levý kraj a znaménko báze vypočte bázi a zda námi zvolený levý kraj splňuje základní požadavky.
    Dále může spočítat rozvoj levého a pravého kraje s možností spočítat mink, maxk a jejich vzdálenosti.
    """

    def __init__(self, fce='x**2-x-1', znamenko=1, symbol_levy_kraj='-1/x'):
        """
        Metoda je volána, jakmile vytvoříme instanci třídy Soustava.
        V rámci dané instance si uloží polynom (proměnná fce),
        znaménko a symbolický levý kraj. Poté zavolá metodu spocitej_hodnotu_baze
        pro výpočet báze beta a ověření beta in R, beta > 1, a
        spocitej_hodnotu_leveho_kraje pro ověření podmínek pro daný levý kraj ell.

        :param fce: polynom, jehož největším kořenem je báze beta
        :param znamenko: udává, zda se jedná o zápornou, resp. kladnou bázi
        :param symbol_levy_kraj: symbolické vyjádření levého kraje, kde symbolická proměnná
                                 x představuje zjednodušený zápis báze beta
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
        Pro daný polynom vypočítá bázi beta, se kterou budeme počítat a ověří,
        že splňuje základní požadavky z definice, tedy beta in R a |beta|>1.

        :raises ValueError v případě, že báze beta <= 1 nebo není reálná
        """
        reseni_rovnice = sp.solve(self.fce, x)
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
        Pro levý kraj, jak symbolicky vyjádřený pomocí beta = x, tak pro konkrétní hodnotu,
        zjistí, zda splňuje námi požadované podmínky. V případě nesplnění těchto podmínek vyvolá vyjímku

        :param symbol_levy_kraj: levý kraj intervalu <l, l+1), může být zadán pomocí báze beta,
                                 kterou ve vzorci reprezentuje symbol x (např. '-1/x'), nebo může být zadán
                                 jako číslo '0', popřípadě jako výraz (např. '1/2*(sqrt(5)-1)')

        :raises ValueError v případě, kdy nejsou splněny požadované podmínky pro výpočet
        """

        symbolicky_levy_kraj = sp.sympify(symbol_levy_kraj)
        symbolicky_levy_kraj = symbolicky_levy_kraj.subs({x: self.baze})
        priblizny_kraj = sp.N(symbolicky_levy_kraj, n=presnost)
        if (priblizny_kraj > 0) or (priblizny_kraj < -1):
            raise ValueError("Nejsou splněny základní požadavky, nula neleží v zadaném intervalu.")
        if (self.znamenko == -1) and ((-priblizny_kraj / self.baze - EPS > (priblizny_kraj + 1)) or -(
                    priblizny_kraj + 1) / self.baze + EPS < priblizny_kraj):
            raise ValueError("Nejsou splněny základní požadavky, interval není invariantní vůči posunutí.")
        self.levy_kraj = symbolicky_levy_kraj

    def nalezeni_presneho_rozvoje(self, bod, pocet_cifer=30):
        """
        Funkce, která pro zadaný bod spočte rozvoj_bodu v dané bázi na pocet_cifer míst a vrátí je.

        :param bod (float, nebo přesný výraz, který leží v intervalu <l,l+1)) , tomuto bodu nalezne rozvoj
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat rozvoj daného bodu
        :returns rozvoj (list) bodu
        :returns perioda (int/None): délka periody jestli, jestliže ji metoda nalezla
        """
        if bod >= self.levy_kraj + 1 or bod < self.levy_kraj:
            raise ValueError("Bod neleží v intervalu <l, l+1). V současnosti nelze vypočítat.")

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
            rozvoj.append(int(sp.N(sp.cancel(sp.floor(cifra)), n=1, chop=True)))
            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append(nova_transformace)
            for j in range(len(transformace)):
                if (abs(transformace[j] - transformace[i]) < MALO) and (j != i):
                    periodicke = True
                    perioda = i - j
            i += 1
            # cyklus = time() - start
            # print("Cyklus trval {0:.2f} s".format(cyklus))
        return tuple(rozvoj), perioda

    def nalezeni_priblizneho_rozvoje(self, bod, pocet_cifer=30):
        """
        Funkce, která pro zadaný bod spočte rozvoj_bodu v dané bázi na pocet_cifer. Tato funkce nepracuje
        s přesnými hodnotami, dochází zde k zaokrouhlování, což může vést k chybám, avšak oproti přesnému
        rozvoji je výpočet výrazně rychlejší.

        :param bod (float, nebo přesný výraz, který leží v intervalu <l,l+1)) , tomuto bodu nalezne rozvoj
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat rozvoj daného bodu
        :returns rozvoj (list) bodu
        :returns perioda (int/None): délka periody jestli, jestliže ji metoda nalezla
        """
        if bod >= self.levy_kraj + 1 or bod < self.levy_kraj:
            raise ValueError("Bod neleží v intervalu <l, l+1). V současnosti nelze vypočítat.")

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
            rozvoj.append(int(sp.N(cifra, n=1, chop=True)))
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
        Funkce, která pro pravý kraj spočte limitní rozvoj pravého kraje v dané bázi na pocet_cifer.
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
            # start = time()
            print("Počítáme {0:.0f}.cifru ".format(i))
            cifra_dosazena = cifra.subs(x, transformace[i - 1])
            zjednoduseni = sp.cancel(sp.expand(cifra_dosazena))
            if sp.sympify(zjednoduseni).is_Integer:
                if (self.znamenko < 0) and (i % 2 == 1):
                    rozvoj.append(zjednoduseni)
                else:
                    rozvoj.append(zjednoduseni - 1)
            else:
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
        :param presne: True/False
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

    def spocitej_rozvoj_praveho_kraje(self, pocet_cifer=30):
        """
        Funkce, která zavolá metodu nalezeni_limitniho_rozvoje pro nalezení limitního rozvoje pravého kraje
        na pocet_cifer. Danou hodnotu rozvoje spolu s hodnotou periody si uloží a vypíše. V případě, že
        perioda nebyla nalezena, bude tato proměnná obsahovat hodnotu None.
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat limitní rozvoj pravého kraje
        """

        self.rozvoj_praveho_kraje, self.perioda_praveho_kraje = self.nalezeni_limitniho_rozvoje(pocet_cifer)
        print("Nalezli jsme rozvoj pravého kraje: [%s]" % ",".join(map(str, self.rozvoj_praveho_kraje)))
        print("S periodou délky {}".format(self.perioda_praveho_kraje))

    def spocitej_rozvoj_bodu(self, bod, presne=True, pocet_cifer: int = 30):
        """
        Funkce, která zavolá metodu nalezeni_presneho_rozvoje pro nalezení rozvoje bodu přesně, resp. nepřesně podle
        parametru presne, na pocet_cifer. Rozvoj spolu s periodou vypíše.
        :param bod: z intervalu <l,l+1)
        :param presne:
        :param pocet_cifer: volitelný parametr, na kolik cifer chceme získat rozvoj daného bodu
        :return: rozvoj_bodu
        :return: perioda_bodu
        """

        bod = sp.sympify(bod)
        if (bod < self.levy_kraj+1) and (self.levy_kraj >= bod):
            print("skočila jsem sem")
            if presne:
                rozvoj_bodu, perioda_bodu = self.nalezeni_presneho_rozvoje(bod, pocet_cifer)
            else:
                rozvoj_bodu, perioda_bodu = self.nalezeni_priblizneho_rozvoje(bod, pocet_cifer)
            print("Nalezli jsme rozvoj bodu: [%s]" % ",".join(map(str, rozvoj_bodu)))
            print("S periodou délky {}".format(perioda_bodu))
            tecka = None
            return rozvoj_bodu, perioda_bodu, tecka
        else:
            bod_k = bod
            bod_k1 = bod/ (self.znamenko*self.baze)
            k=0
            #print(sp.N(self.levy_kraj))
            while (bod_k >= self.levy_kraj+1 or bod_k < self.levy_kraj):
                #TODO nevím, jestli tuhle část u while mám správně - je to špatně, vlastně pokud bod_k1 tam neleží tak
                # to přejde, prostě to řeší jen to, aby bod_k tam ležel - nutno pořešit
                if (bod_k1 < self.levy_kraj+1 and bod_k1 >= self.levy_kraj):
                    pass
                k= k+1
                bod_k = bod_k1
                bod_k1 = bod_k/ (self.znamenko*self.baze)
                #print(sp.N(bod_k))
            if presne:
                rozvoj_bodu, perioda_bodu = self.nalezeni_presneho_rozvoje(bod_k, pocet_cifer)
            else:
                rozvoj_bodu, perioda_bodu = self.nalezeni_priblizneho_rozvoje(bod_k, pocet_cifer)
            print("Nalezli jsme rozvoj bodu: [%s]" % ",".join(map(str, rozvoj_bodu)))
            print("S periodou délky {}".format(perioda_bodu))
            print("Tecka je za {}. pozici".format(k))
            tecka = k
            return rozvoj_bodu, perioda_bodu, tecka

    def porovnej_retezce(self, prvni_retezec: list, druhy_retezec: list, perioda_prvniho: list,
                         perioda_druheho: list):
        """
        Funkce, která porovná dva řetězce v závislosti na znaménku báze lexikografickým,
        resp. alternujícím uspořádáním.

        :param prvni_retezec: první řetezec, který porovnáváme
        :param druhy_retezec: řetězec, se kterým porovnáváme prvni_retezec
        :param perioda_prvniho: řetězec reprezentující periodickou část prvního řetězce
        :param perioda_druheho: řetězec reprezentující periodickou část druhého řetězce

        :returns: -1: prvni_retezec < druhy_retezec
        :returns: 1: prvni_retezec > druhy_retezec
        :returns: 0: prvni_retezec = druhy_retezec
        """

        pracovni_retezec_1 = prvni_retezec.copy()
        pracovni_retezec_2 = druhy_retezec.copy()
        if perioda_prvniho == [0] and perioda_druheho == [0]:
            delka_retezce = max(len(pracovni_retezec_1), len(pracovni_retezec_2))
        elif perioda_prvniho != [0]:
            delka_retezce = max(len(pracovni_retezec_1), len(pracovni_retezec_2)) + len(perioda_prvniho)
        elif perioda_druheho != [0]:
            delka_retezce = max(len(pracovni_retezec_1), len(pracovni_retezec_2)) + len(perioda_druheho)
        else:
            delka_retezce = max(len(pracovni_retezec_1), len(pracovni_retezec_2)) + sp.lcm(len(perioda_prvniho),
                                                                                           len(perioda_druheho), 2)
        pracovni_retezec_1 = self.prilep_periodu(pracovni_retezec_1, perioda_prvniho, delka_retezce)
        pracovni_retezec_2 = self.prilep_periodu(pracovni_retezec_2, perioda_druheho, delka_retezce)
        for i in range(len(pracovni_retezec_1)):
            if self.znamenko ** (i + 1) * pracovni_retezec_1[i] < self.znamenko ** (i + 1) * pracovni_retezec_2[i]:
                return -1  # prvni retezec je MENSI jak druhy retezec
            elif self.znamenko ** (i + 1) * pracovni_retezec_1[i] \
                    > self.znamenko ** (i + 1) * pracovni_retezec_2[i]:
                return 1  # prvni retezec je VETSI jak druhy retezec
        return 0  # retezce se rovnaji

    def prilep_periodu(self, retezec: list, perioda: list, delka_retezce: int):
        """
        Pomocná metoda, která retezec, v případě jeho periodičnosti, prodlouží o periodu tolikrát,
        aby délka výsledného řetězce byla rovna delka_retezce. Jestliže retezec není periodický,
        na požadovanou délku se doplní nulami. Pokud je původní retezec delší než delka_retezce,
        je tento retezec zkrácen na požadovanou délku.

        :param retezec: řetězec, který chceme prodloužit, popř. zkrátit
        :param perioda: řetězec reprezentující periodickou část, pokud retezec nemá periodu, hodnota je [0]
        :param delka_retezce: požadovaná délka prodlouženého, popř. zkráceného řetězce
        :returns list: prodloužený nebo zkrácený řetězec na požadovanou délku
        """
        pom = list(retezec)
        delka = len(pom)
        pridam_periodu = (delka_retezce - delka) // len(perioda) + 1
        prodlouzeni = perioda * pridam_periodu
        pom.extend(prodlouzeni)
        useknu = len(pom) - delka_retezce
        pom = pom[:-useknu]
        return pom

    def je_retezec_zleva_pripustny(self, retezec: list, perioda_retezce: list):
        """
        Funkce, která zjistí, zda je retezec a libovolný jeho sufix >=lex/alt rozvoj_leveho_kraje.rozvoj_bodu
        :param retezec: řetězec, který chceme porovnávat
        :param perioda_retezce: řetězec reprezentující periodickou část, pokud retezec nemá periodu, hodnota je [0]
        :returns: bool, hodnota je True v případě přípustnosti zleva
        """

        pracovni_retezec = list(retezec)
        leva_perioda = self.dej_periodu_kraje(list(self.rozvoj_leveho_kraje), self.perioda_leveho_kraje)
        while len(pracovni_retezec) > 0:
            if self.porovnej_retezce(list(self.rozvoj_leveho_kraje), pracovni_retezec,
                                     leva_perioda, perioda_retezce) > 0:
                return False
            pracovni_retezec.pop(0)
        return True

    def je_retezec_zprava_pripustny(self, retezec: list, perioda_retezce: list):
        """
        Funkce, která zjistí, zda je retezec a libovolný jeho sufix <lex/alt rozvoj_praveho_kraje.rozvoj_bodu
        :param retezec: řetězec, který chceme porovnávat
        :param perioda_retezce: řetězec reprezentující periodickou část, pokud retezec nemá periodu, hodnota je [0]
        :returns: bool, hodnota je True v případě přípustnosti zprava
        """

        pracovni_retezec = list(retezec)
        prava_perioda = self.dej_periodu_kraje(list(self.rozvoj_praveho_kraje), self.perioda_praveho_kraje)
        while len(pracovni_retezec) > 0:
            if self.porovnej_retezce(pracovni_retezec, list(self.rozvoj_praveho_kraje), perioda_retezce,
                                     prava_perioda) >= 0:
                return False
            pracovni_retezec.pop(0)
        return True

    def je_retezec_pripustny(self, retezec: list, perioda_retezce: int):
        """
        Funkce, která zjistí, zda je retezec připustný.

        :param retezec: řetězec, který chceme otestovat
        :param perioda_retezce: řetězec reprezentující periodickou část, pokud retezec nemá periodu, hodnota je [0]
        :returns: bool, hodnota je True v případě, že je řetězec přípustný
        """

        perioda = self.dej_periodu_kraje(retezec, perioda_retezce)
        if self.je_retezec_zprava_pripustny(retezec, perioda) \
                and self.je_retezec_zleva_pripustny(retezec, perioda):
            return True
        else:
            return False

    def spocitej_mink_maxk(self, k: int):
        """
        Funkce pro zadané k nalézne řetězce mink a maxk až do délky řetězce k.
        Řetězce mink, resp. maxk uloží do mink, resp. maxk.
        Po nalezení jednotlivých řetězců mink a maxk zavolá tato metoda metodu spocitej_vzdalenosti,
        poté spocitej_vzdalenosti_symbolicky pro výpočet jedlotlivých vzdáleností mezi sousedními
        pm,beta,l-celými čísly.

        :param k: maximální délka řetězců mink a maxk, kterou chceme nalézt
        """

        rozvoj_levy = list(self.rozvoj_leveho_kraje)
        rozvoj_pravy = list(self.rozvoj_praveho_kraje)
        leva_perioda = self.dej_periodu_kraje(rozvoj_levy, self.perioda_leveho_kraje)
        prava_perioda = self.dej_periodu_kraje(rozvoj_pravy, self.perioda_praveho_kraje)
        mink = list()
        maxk = list()
        min0 = []
        max0 = []
        mink.append(min0)
        maxk.append(max0)
        for i in range(1, k + 1):
            mini = self.prilep_periodu(rozvoj_levy, leva_perioda, i)
            maxi = self.prilep_periodu(rozvoj_pravy, prava_perioda, i)
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
                    if self.porovnej_retezce(mini, mozne_min1, [0], [0]) == 1:
                        mini = mozne_min1
                    if not self.je_retezec_pripustny(mini, None):
                        mini = mozne_min1
                if self.je_retezec_pripustny(mozne_max1, None):
                    if self.porovnej_retezce(maxi, mozne_max1, [0], [0]) == -1:
                        maxi = mozne_max1
                    if not self.je_retezec_pripustny(maxi, None):
                        maxi = mozne_max1
                mk += 1
            mink.append(mini)  # do mink, resp. maxk se na pozici k připojuje řetezec mink pro konkrétní k
            maxk.append(maxi)
        self.mink = mink
        self.maxk = maxk
        self.spocitej_vzdalenosti(k + 1)
        self.spocitej_vzdalenosti_symbolicky(k + 1)

    def gamma_funkce(self, retezec: list):
        """
        Metoda převede zadaný konečný řetězec na pm,beta,l-celé číslo

        :param retezec: řetězec, který chceme převést
        """

        gamma = 0
        obraceny_retezec = retezec[::-1]  # přetočíme pro jednodušší počty
        for i in range(len(retezec)):
            gamma += (self.znamenko * self.baze) ** i * obraceny_retezec[i]
        return sp.N(gamma, n=20)

    def spocitej_vzdalenosti(self, k: int):
        """
        Tato metoda pro zadaná mink a maxk vypočte jednotlivé vzdálenosti.

        :param k: maximální délka řetězců mink a maxk, pro kterou chceme vypočítat vzdálenosti
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
        Metoda převede zadaný konečný řetězec na pm,beta,l-celé číslo, ovšem bázi beta ponechá symbolicky.

        :param retezec: řetězec, který chceme převést
        """

        gamma = 0
        obraceny_retezec = retezec[::-1]  # přetočíme pro jednodušší počty
        for i in range(len(retezec)):
            gamma += (self.znamenko * x) ** i * obraceny_retezec[i]
        return sp.N(gamma, n=20)

    def spocitej_vzdalenosti_symbolicky(self, k: int):
        """
        Tato metoda pro zadaná mink a maxk vypočte jednotlivé vzdálenosti, ale bázi beta ponechá symbolicky.

        :param k:  maximální délka řetězců mink a maxk, pro kterou chceme spočítat vzdálenosti
        """

        delta = list()
        for i in range(k):
            if self.znamenko < 0:
                vzdalenost = abs(
                    (self.znamenko * x) ** i + self.gamma_funkce_symbolicky(
                        self.mink[i]) - self.gamma_funkce_symbolicky(
                        self.maxk[i]))
            else:
                vzdalenost = (self.znamenko * x) ** i + self.gamma_funkce_symbolicky(
                    self.mink[i]) - self.gamma_funkce_symbolicky(
                    self.maxk[i])
            delta.append(vzdalenost)
        self.vzdalenosti_symbolicky = delta

    def lezi_retezec_mezi(self, retezec: tuple, perioda_retezce: int, levy: tuple, levy_perioda: int, pravy: tuple,
                          pravy_perioda: int):
        """
        Tato metoda zčásti vychází z metody je_retezec_pripustny, ale namísto poronávání, zda libovolný sufix řetězce
        leží mezi rozvoji krajů, porovnáváme, zda libovolný sufix řetězce leží mezi dvěma rozvoji (levy s periodou
        levy_perioda, a pravy s pravy_perioda).

        :param retezec: který chceme porovnávat
        :param perioda_retezce: délka periodické části řetězce, pokud retezec nemá periodu, je tato hodnota None
        :param levy: řetězec reprezentující minimální rozvoj levého kraje
        :param levy_perioda: délka periodické části řetězce levy
        :param pravy: řetězec reprezentující maximální limitní rozvoj pravého kraje
        :param pravy_perioda: délka periodické části řetězce pravy
        :return: bool, hodnota je True v případě, že retezec a jeho libovolný sufix leží mezi řetězci levy a pravy
        """
        pom_retezec = list(retezec)
        periodicka_cast = pom_retezec[-perioda_retezce:]
        while len(pom_retezec) > 0:
            leva_periodicka_cast = self.dej_periodu_kraje(list(levy), levy_perioda)
            prava_periodicka_cast = self.dej_periodu_kraje(list(pravy), pravy_perioda)
            if self.porovnej_retezce(pom_retezec, list(levy), periodicka_cast, leva_periodicka_cast) <= 0:
                return False
            if self.porovnej_retezce(pom_retezec, list(pravy), periodicka_cast, prava_periodicka_cast) >= 0:
                return False
            pom_retezec.pop(0)
        return True

    def dej_periodu_kraje(self, retezec: list, perioda: int):
        """
        Pomocná metoda, která pro zadaný retezec a jeho periodu vrátí řetězec reprezentující
        periodickou část tohoto řetězce.
        :param retezec: řetězec, jehož periodickou část chceme vyjádřit
        :param perioda: délka periodické části řetězce, pokud retezec nemá periodu, je tato hodnota None
        :return:
        """
        if perioda is None:
            return [0]
        else:
            return retezec[-perioda:]

    def vytvor_Zb(self, delka: int):
        """

        :param delka:
        :return:
        """
        znaky = self.rozvoj_praveho_kraje + self.rozvoj_leveho_kraje
        abeceda = set(znaky)
        #print(abeceda)
        mozne_retezce = list(product(abeceda, repeat=delka))
        print(len(mozne_retezce))

        vyhodit = set()

        for retezec in mozne_retezce:
            if not self.je_retezec_pripustny(retezec, None):
                vyhodit.add(retezec)

        Zb = [x for x in mozne_retezce if x not in vyhodit]
        print(len(Zb))
        return Zb

