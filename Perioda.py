import sympy as sp
from itertools import product

from sympy.abc import a, b, c, d, e, f, g, h, l, m, n, o, q, r, s, t, u, v, w, beta
import Soustava

presnost = 1000 #684
EPS = 9e-17


class Perioda(object):
    def __init__(self, fce, baze, znamenko, k, p, presne=True, abeceda=(-1, 0, 1)):
        """
        Funkce, která se spustí automaticky s vytvořením instance Perioda, uloží si jednotlivé hodnoty a spočte
        vyjádření celého výrazu pro předperiodu délky k a periodu p.
        """

        self.baze = baze
        self.fce = fce
        self.znamenko = znamenko
        if k < 0:
            raise ValueError("Předperioda musí být větší nebo rovna nule. ")
        self.k = k
        if p < 1:
            raise ValueError(
                "Protože hledáme periodické rozvoje levého kraje, je potřeba nastavit hodnotu periody větší jak nula.")
        self.p = p
        self.symboly = [a, b, c, d, e, f, g, h, l, m, n, o, q, r, s, t, u, v, w]
        self.mocnina = 1
        self.hodnoty = list()
        self.leve_kraje = list()
        self.leve_kraje_symbolicky = list()
        self.prave_kraje = list()
        self.prave_kraje_perioda = list()
        self.presne = presne
        self.vycisleny_vyraz = None
        self.vyraz_pred = None
        self.vyraz_perioda = None
        self.vyraz = None
        self.A = abeceda

        self.vyjadreni_celeho_vyrazu()
        self.vycisleni_vyrazu_beta()

    def vyjadreni_predperiody(self):
        """
        Funkce, která podle hodnoty předperiody vyjádří 1. část vzorce pro výpočet hodnoty levého kraje.
        """

        vyraz = 0
        if self.k > 0:
            pomocna = self.k
            while pomocna > 0:
                vyraz = vyraz + self.symboly.pop(0) / (self.znamenko * beta) ** self.mocnina
                self.mocnina = self.mocnina + 1
                pomocna = pomocna - 1
        self.vyraz_pred = vyraz

    def vyjadreni_periody(self):
        """
        Funkce, která podle hodnoty periody vyjádří 2. část vzorce pro výpočet hodnoty levého kraje.
        """

        vyraz = 0
        pomocna = self.p
        while pomocna > 0:
            vyraz = vyraz + self.symboly.pop(0) / (self.znamenko * beta) ** (self.mocnina - self.p) * 1 / \
                            ((self.znamenko * beta) ** self.p - 1)
            self.mocnina = self.mocnina + 1
            pomocna -= 1
        self.vyraz_perioda = vyraz

    def vyjadreni_celeho_vyrazu(self):
        """
        Funkce, která dává dohromady celý vzorec pro výpočet hodnoty levého kraje. Volá funkce vyjadreni_predperiody
        a vyjadreni_periody a sečte je dohromady. Tuto novou hodnotu pak uloží do proměnné self.vyraz a vypíše ji.
        """

        self.vyjadreni_predperiody()
        self.vyjadreni_periody()
        self.vyraz = self.vyraz_pred + self.vyraz_perioda
        print(self.vyraz)

    def vycisleni_vyrazu_beta(self):
        """
        Funkce, která do proměnné vyraz dosadí za proměnnou beta reálnou hodnotu báze.
        """

        vycisleny = self.vyraz.subs(beta, self.baze)
        self.vycisleny_vyraz = vycisleny

    def vycisleni_vyrazu_abc(self, vyraz, hodnoty: tuple):
        """
        Funkce pro vyčíslení výrazu. Do proměnné vyraz dosadí za jednotlivé proměnné a, b, c, ... postupně jednotlivé
        cifry z listu hodnoty.

        :param vyraz: Symbolický výraz s proměnnými a, b, c, ...do kterého se dosadí jednotlivé hodnoty
        :param hodnoty: Pole dosazovaných hodnot.
        :return: pom_vyraz (): Vyčíslený výraz
        """

        pom_vyraz = vyraz
        symboly = [a, b, c, d, e, f, g, h, l, m, n, o, q, r, s, t, u, v, w]
        pom_hodnoty = list(hodnoty)
        while len(pom_hodnoty) > 0:
            pom_vyraz = pom_vyraz.subs(symboly.pop(0), pom_hodnoty.pop(0))
        return pom_vyraz

    def dosazeni_overeni_leveho_kraje(self, hodnoty: tuple):
        """
        Funkce pro ověření, zda vyčíslená hodnota levého kraje splňuje základní požadavky a ověření, že rozvoj tohoto
        kraje skutečně odpovídá námi odhadnutému rozvoji.
        :param hodnoty: Odhadnutý rozvoj levého kraje
        :return:
        """

        levy_kraj = self.vycisleni_vyrazu_abc(self.vycisleny_vyraz, hodnoty)
        priblizny_levy_kraj = sp.N(levy_kraj, n=presnost)
        if priblizny_levy_kraj < 0 and priblizny_levy_kraj > -1:
            if (self.znamenko == -1) and ((-priblizny_levy_kraj / self.baze - EPS > (priblizny_levy_kraj + 1)) or (
                        -(priblizny_levy_kraj + 1) / self.baze + EPS < priblizny_levy_kraj)):
                # print("Jsem tu")
                pass
            else:
                # rozvoj_leveho_kraje = list(hodnoty)
                self.zpetne_overeni(hodnoty, levy_kraj)

    def dosazeni_vse(self):
        """
        Funkce, která vygeneruje všechny možné kombinace konečných slov nad abecedou A s délkou k+p. Tyto slova pak
        ověří, po dosazení do vzorce pro levý kraj, spňují základní podmínky pro levý kraj. Pokud ano, je tato vzniklá
        hodnota levého kraje ověřena ve funkci zpetne_overeni.
        """

        delka = self.k + self.p
        hodnoty = list(product(self.A, repeat=delka))
        # upravit, abychom hodnoty dostávali po jednom, jednodušší pro paměť
        print("Celkem máme {0:.0f} řetezců".format(len(self.A) ** delka))
        procistene_retezce = self.odstraneni_retezcu(hodnoty)
        print("Celkem máme {0:.0f} řetezců".format(len(procistene_retezce)))
        i = 0
        for retezec in procistene_retezce:
            print("{}. případ dosazení, teď počítáme rozvoj: {}".format(i, list(retezec)))
            # print("{}. případ dosazení, nyní děláme rozvoj tohohle: [%s]" % ",".format(i) .join(map(str, retezec)))
            # print("Nyni delame rozvoj tohohle:  [%s]" % ",".join(map(str, hodnoty)))
            self.dosazeni_overeni_leveho_kraje(retezec)
            i += 1

    def odstraneni_retezcu(self, hodnoty:list):
        pomocny_rozvoj = Soustava.Soustava(self.fce, self.znamenko, symbol_levy_kraj='-1')
        pomocny_rozvoj.spocitej_rozvoj_leveho_kraje(self.presne)
        levy_rozvoj = pomocny_rozvoj.rozvoj_leveho_kraje
        leva_perioda = pomocny_rozvoj.perioda_leveho_kraje

        pomocny_rozvoj = Soustava.Soustava(self.fce, self.znamenko, symbol_levy_kraj='0')
        pomocny_rozvoj.spocitej_rozvoj_praveho_kraje(self.presne, 30)
        pravy_rozvoj = pomocny_rozvoj.rozvoj_praveho_kraje
        prava_perioda = pomocny_rozvoj.perioda_praveho_kraje

        vyhodit = set()

        for retezec in hodnoty:
            if not pomocny_rozvoj.lezi_retezec_mezi(retezec, self.p, levy_rozvoj, leva_perioda, pravy_rozvoj, prava_perioda):
                vyhodit.add(retezec)

        print("Vyhazujeme: ")
        print(vyhodit)

        procisteny_retezec = [x for x in hodnoty if not x in vyhodit]
        return procisteny_retezec

    def zpetne_overeni(self, hodnoty: tuple, levy):
        """
        Funkce, která zadané konečné slovo (resp. navrhovaný rozvoj levého kraje) a jeho spočtená hodnota levého kraje
        ověří, zda se skutečně jedná o rozvoj tohoto levého kraje.
        :param hodnoty: Navrhovaný rozvoj levého kraje nad danou abecenou
        :param levy: spočtená hodnota levého kraje
        """

        hledany_rozvoj = Soustava.Soustava(self.fce, self.znamenko, levy)
        #print(levy)
        hledany_rozvoj.spocitej_rozvoj_leveho_kraje(self.presne, 2 * self.p + self.k)
        if hodnoty == hledany_rozvoj.rozvoj_leveho_kraje:
            if self.p == hledany_rozvoj.perioda_leveho_kraje:
                self.hodnoty.append(hodnoty)
                self.leve_kraje.append(levy)
                symbolicke = self.vycisleni_vyrazu_abc(self.vyraz, tuple(hodnoty))
                self.leve_kraje_symbolicky.append(symbolicke)
                print("Retezec, ktery ma {} predperiodu a {} periodu je (retezec, levy kraj):".format(self.k, self.p))
                print(hodnoty)
                print(levy)
                hledany_rozvoj.spocitej_rozvoj_praveho_kraje(False, 8)
                self.prave_kraje.append(hledany_rozvoj.rozvoj_praveho_kraje)
                self.prave_kraje_perioda.append(hledany_rozvoj.perioda_praveho_kraje)
