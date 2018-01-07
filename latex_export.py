from sympy import latex, sympify, N, cancel
from sympy.abc import x, beta
import Soustava
import Perioda

class Soubor(object):
    def __init__(self, nazev: str):
        """
        Metoda je spuštěna automaticky s vytvořením instance Soubor, uloží si název souboru, který vytvoří a vloží
        do něj hlavičku pro LaTeXový dokument.

        :param nazev: název souboru včetně cesty
        """
        self.f = None
        self.nazev = nazev
        self.otevri_soubor()
        self.napis_hlavicku()
        # self.ukonceni_souboru()

    def otevri_soubor(self):
        """
        Metoda pro otevření souboru.
        """
        f = open(self.nazev, "w")
        self.f = f

    def napis_hlavicku(self):
        """
        Metoda, která otevře soubor resources/hlavicka.tex a zkopíruje obsah souboru hlavicka.tex
        do vytvořeného souboru.
        """
        hl = open("resources/hlavicka.tex", "r")
        radky = hl.readlines()
        self.f.writelines(radky)
        hl.close()

    def ukonceni_souboru(self):
        """
        Jednoduchá metoda, která doplní do souboru, do kterého se v ostatních metodách zapisovalo, syntax pro ukončení
        LaTeXového dokumentu a bezpečně jej zavře.
        """
        self.f.write("\n \end{document}")
        self.f.close()

    def vypis_rozvoj_leveho(self, retezec: list, perioda: int):
        """
        Metoda, pro vypsání rozvoje levého kraje do souboru.

        :param retezec: rozvoj levého kraje
        :param perioda: délka periody
        """
        self.f.write("Rozvoj levého kraje: ")
        self.prevod_rozvoj_s_periodou(retezec, perioda)
        if perioda is None:
            self.f.write("\dots")
        self.f.write(" \n\n")

    def vypis_rozvoj_praveho(self, retezec: list, perioda: int):
        """
        Metoda, pro vypsání limitního rozvoje pravého kraje do souboru.

        :param retezec: rozvoj pravého kraje
        :param perioda: délka periody
        """
        self.f.write("Limitní rozvoj pravého kraje: ")
        self.prevod_rozvoj_s_periodou(retezec, perioda)
        if perioda is None:
            self.f.write("\dots")
        self.f.write(" \n\n")

    def vypis_minmax(self, mink: list, maxk: list, vzdalenosti: list, vzdalenosti_symbol: list):
        """
        Funkce pro vypsání řetězců mink, maxk, a jejich vzdáleností do souboru v podobě tabulky.
        Hlavička tabulky je zkopírována ze souboru resources/tabulka.tex.

        :param mink: seznam řetězců mink
        :param maxk: seznam řetězců maxk
        :param vzdalenosti: seznam vzdáleností
        :param vzdalenosti_symbol: seznam vzdáleností vyjádřených se symbolickou bází beta
        """
        hl = open("resources/tabulka.tex", "r")
        radky = hl.readlines()
        self.f.writelines(radky)

        for i in range(1, len(vzdalenosti)):
            self.f.write("{}".format(i))
            self.f.write(" & $")
            self.prevod_rozvoj_na_retezec(mink[i])
            self.f.write("$ & $")
            self.prevod_rozvoj_na_retezec(maxk[i])
            self.f.write("$ & $")
            self.prevod_x_na_beta(vzdalenosti_symbol[i])
            self.f.write("$ & {0:.5f} \\\\ ".format(vzdalenosti[i]))

        self.f.write(" \end{tabular}\end{center}\end{table} ")

    def prevod_rozvoj_s_periodou(self, retezec: list, perioda: int):
        """
        Metoda pro vypsání rozvoje bodu s periodou.

        :param retezec: rozvoj bodu
        :param perioda: délka periody
        """
        self.f.write("$")
        if perioda is None:
            self.prevod_rozvoj_na_retezec(retezec)
        elif len(retezec) == perioda:
            self.f.write("(")
            self.prevod_rozvoj_na_retezec(retezec)
            self.f.write(")^\omega")
        else:
            j = 0
            zav = len(retezec) - perioda
            for i in retezec:
                if j == zav:
                    self.f.write("(")
                if i < 0:
                    self.f.write("\overline{}".format(-i))
                else:
                    self.f.write("{}".format(i))
                j += 1
            self.f.write(")^\omega")

        self.f.write("$\n")

    def prevod_rozvoj_na_retezec(self, rozvoj: list):
        """
        Metoda pro vypsání rozvoje bodu bez periody.
        Pozor, při samostatném užití nevypíše rozvoj v matematickém prostředí.

        :param rozvoj: rozvoj bodu
        """
        for i in rozvoj:
            if i < 0:
                self.f.write("\overline{}".format(-i))
            else:
                self.f.write("{}".format(i))

    def prevod_vyrazu_na_latex(self, vyraz: str):
        """
        Metoda převede výraz do matematického prostředí v LaTeXu.
        Pozor, při samostatném užití nevypíše výraz v matematickém prostředí.

        :param vyraz: převáděný výraz
        """
        prevod = sympify(vyraz)
        self.f.write(latex(prevod))

    def prevod_x_na_beta(self, vyraz: str):
        """
        Metoda, která ve výrazu provede substituci x -> beta a výraz převede do matematického prostředí v LaTeXu.
        Pozor, při samostatném užití nevypíše výraz v matematickém prostředí.

        :param vyraz: převáděný výraz
        """
        prevod = sympify(vyraz)
        prevod = prevod.subs(x, beta)
        prevod = cancel(prevod)
        self.f.write(latex(prevod))

    def vypis_rovnice(self, rovnice: str, baze, znamenko: int):
        """
        Metoda, která vypíše základní informace o soustavě, tj. kladná nebo záporná báze, její hodnota a polynom,
        jehož je báze beta kořenem.

        :param rovnice: polynom
        :param baze: beta
        :param znamenko: hodnota +1 nebo -1, udává, zda se jedná o zápornou nebo kladnou bázi
        """
        self.f.write("Vytvořili jsme soustavu ")
        if znamenko < 0:
            self.f.write("se zápornou bází ")
        else:
            self.f.write("s kladnou bází ")
        self.f.write("z rovnice $")
        self.prevod_vyrazu_na_latex(rovnice)
        self.f.write("$. \\\\ Báze $\\beta = ")
        self.f.write(latex(baze))
        self.f.write("\doteq {}$. ".format(N(baze, n=3)))

    def vypis_levy(self, symbol_levy_kraj, levy_kraj):
        """
        Metoda, která vypíše informace o levém kraji, jeho vyjádření pomocí báze i jeho přibližnou hodnotu.

        :param symbol_levy_kraj:
        :param levy_kraj
        """
        # TODO popis parametru
        self.f.write("Levý kraj $\ell = ")
        self.prevod_x_na_beta(symbol_levy_kraj)
        self.f.write("\doteq {} $. \n\n".format(N(levy_kraj, n=3, chop=True)))
        # self.f.write("$.\n\n")

    def vypis_perioda(self, perioda: Perioda):
        """
        Metoda, která vypíše vše při výpočtu period; tj. rovnici, ze které vycházíme, bázi, znaménko, jednotlivé
        hodnoty levého kraje, které se pro danou periodu a předperiodu našly, jejich rozvoj, a následně i rozvoj
        pravého kraje. Tato metoda v rámci výpisu volá funkci nalezene_periody.

        :param perioda: instance třídy Perioda
        """
        self.vypis_rovnice(perioda.fce, perioda.baze, perioda.znamenko)
        self.f.write(
            "Počítáme rozvoje, které mají {} dlouhou předperiodu a {} délku periody. ".format(perioda.k, perioda.p))
        self.f.write("Levý kraj je pak ve tvaru $$\ell=")
        self.f.write(latex(perioda.vyraz))
        self.f.write("$$")
        moznosti = len(perioda.A) ** (perioda.k + perioda.p)
        if moznosti < 5:
            self.f.write("Celkem jsme prošli {} možnosti.\n\n".format(len(perioda.A) ** (perioda.k + perioda.p)))
        else:
            self.f.write("Celkem jsme prošli {} možností.\n\n".format(len(perioda.A) ** (perioda.k + perioda.p)))
        if len(perioda.hodnoty) > 0:
            self.nalezene_periody(perioda)
        else:
            self.f.write("Bohužel ani jedna z možností nebyla rozvojem levého kraje s danou předperiodou a periodou. ")
        if perioda.presne:
            self.f.write("Rozvoj levého kraje je spočten nepřesně (jednotlivé transformace zaokrouhlujeme na 1000 "
                         "desetinných míst. Limitní rozvoj pravého kraje je spočten přesně. ")
        else:
            self.f.write("Rozvoje krajů jsou spočteny nepřesně, resp. bez použití limity. ")
        print("Výsledky byly úspěšně zapsány do souboru ", self.nazev)

    def nalezene_periody(self, perioda: Perioda):
        """
        Funkce, která vypíše jednotlivé hodnoty levého kraje, vyjádřeného bází $\beta$ i přibližnou hodnotu, jejich
        periodický rozvoj s danou délkou předperiody a periody i limitní rozvoj pravého kraje pro dané l.

        :param perioda: instance třídy Perioda
        """
        # TODO popis parametru
        self.f.write("\\begin{itemize} ")
        for i in range(len(perioda.hodnoty)):
            self.f.write("\item $\ell = ")
            self.f.write(latex(perioda.leve_kraje_symbolicky[i]))
            self.f.write("\doteq {} $ \n\n".format(N(perioda.leve_kraje[i], n=3)))
            self.vypis_parametry_soustavy(perioda.fce, perioda.znamenko, perioda.leve_kraje[i])
            self.vypis_rozvoj_leveho(perioda.hodnoty[i], perioda.p)
            self.vypis_rozvoj_praveho(perioda.prave_kraje[i], perioda.prave_kraje_perioda[i])
        self.f.write("\end{itemize}")

    def vypis_parametry_soustavy(self, fce, znamenko, levy):
        """
        Metoda pro vypsání jednotlivých paramatrů soustavy (polynom, znaménko, levý kraj) jakožto komentář v LaTeXu.
        Pomůcka pro snadný výpočet konkrétního případu.

        :param fce: polynom
        :param znamenko: hodnota +1 nebo -1, udává, zda se jedná o zápornou nebo kladnou bázi
        :param levy: symbolické vyjádření levého kraje, kde symbolická proměnná x představuje zjednodušený zápis
                     báze beta
        """
        self.f.write("%% Soustava.Soustava(' ")
        self.f.write(fce)
        self.f.write(" ', {}, '{}') \n".format(znamenko, levy))

    def vypis_cas(self, cas: int):
        """
        Metoda pro výpis času v sekundách do LaTeX dokumentu.

        :param cas: počet sekund k vypsání
        """
        self.f.write("Celé to trvalo vypočítat {0:.2f} sekund. ".format(cas))

    def vypis_rozvoj_vse(self, soustava: Soustava):
        """
        Funkce, která vypíše vše při výpočtu rozvoje konkrétní soustavy; tj. polynom, ze kterého vycházíme,
        bázi beta, znaménko, hodnotu levého kraje ell, jeho rozvoj a následně i limitní rozvoj pravého kraje
        (pokud byly tyto hodnoty spočteny). Dále pak mink, maxk a vzdálenosti, pokud byly spočteny.

        :param soustava: instance třídy Soustava
        """
        self.vypis_rovnice(soustava.fce, soustava.baze, soustava.znamenko)
        self.vypis_levy(soustava.symbol_levy_kraj, soustava.levy_kraj)
        if not (soustava.rozvoj_leveho_kraje == None):
            self.vypis_rozvoj_leveho(soustava.rozvoj_leveho_kraje, soustava.perioda_leveho_kraje)
        if not (soustava.rozvoj_praveho_kraje == None):
            self.vypis_rozvoj_praveho(soustava.rozvoj_praveho_kraje, soustava.perioda_praveho_kraje)
        if not (soustava.mink == None):
            print(soustava.vzdalenosti)
            self.vypis_minmax(soustava.mink, soustava.maxk, soustava.vzdalenosti, soustava.vzdalenosti_symbolicky)
        if Soustava.presnost:
            self.f.write("Rozvoj levého kraje je spočten přesně, stejně tak limitní rozvoj pravého kraje. ")
        else:
            self.f.write("Rozvoj levého kraje je spočten nepřesně (jednotlivé transformace zaokrouhlujeme na 1000 "
                         "desetinných míst. Limitní rozvoj pravého kraje je spočten přesně. ")
