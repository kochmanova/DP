from sympy import latex, sympify, N, cancel
from sympy.abc import x, beta
import Soustava
import Perioda

class Soubor(object):
    def __init__(self, nazev: str):
        """
        Funkce, která se spustí automaticky s vytvořením instance Soubor, uloží si název souboru, který vytvoří a vloží
        do něj hlavičku LaTeXu.
        :param nazev: název souboru
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
        Funkce, která si otevře hlavicka.tex, ze kterého si zkopíruje celý text a vloží jej do souboru, do kterého
        zapisuje.
        """
        hl = open("resources/hlavicka_dp.tex", "r")
        radky = hl.readlines()
        self.f.writelines(radky)
        hl.close()

    def ukonceni_souboru(self):
        """
        Jednoduchá funkce, která bezpečně zavře soubor, do kterého zapisovala a předtím jej doplní o syntax pro ukončení
        souboru v LaTeXu, aby šel tento soubor bez problémů zkonvertovat na pdf.
        """
        self.f.write("\n \end{document}")
        self.f.close()

    def vypis_rozvoj_leveho(self, retezec: list, perioda: int):
        """
        Funkce, pro vypsání rozvoje levého kraje do souboru.
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
        Funkce, pro vypsání rozvoje levého kraje do souboru.
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
        Funkce pro vypsání řetězců min(k), max(k), a jejich vzdáleností do souboru v podobě tabulky.
        :param mink:
        :param maxk:
        :param vzdalenosti:
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
        Funkce pro vypsání rozvoje bodu s periodou do souboru.
        :param retezec: rozvoj bodu
        :param perioda: délka periody
        """
        #self.f.write("$")
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

        self.f.write("$")

    def prevod_rozvoj_na_retezec(self, rozvoj: list):
        """
        Funkce pro vypsání rozvoje bodu bez periody do souboru. (Pozor: nevypíše rozvoj v matematickém modu)
        :param rozvoj: rozvoj bodu
        """
        for i in rozvoj:
            if i < 0:
                self.f.write("\overline{}".format(-i))
            else:
                self.f.write("{}".format(i))

    def prevod_vyrazu_na_latex(self, vyraz: str):
        """
        Metoda, která výraz převede do LaTeX formy. (Pozor: nevypíše výraz v matematickém modu)
        :param vyraz: převáděný výraz
        """
        prevod = sympify(vyraz)
        self.f.write(latex(prevod))

    def prevod_x_na_beta(self, vyraz: str):
        """
        Metoda, která ve výrazu zasubstitutuje proměnnou x za betu a výraz převede do LaTeX formy.
        Využíváno pro výpis hodnoty levého kraje vyjádřeného pomocí báze beta. (Pozor: nevypíše výraz v matematickém
        modu)
        :param vyraz: převáděný výraz
        """
        prevod = sympify(vyraz)
        prevod = prevod.subs(x, beta)
        prevod = cancel(prevod)
        self.f.write(latex(prevod))

    def vypis_rovnice(self, rovnice: str, baze, znamenko: int):
        """
        Metoda, která vypíše základní informace o soustavě, tj. kladná/záporná báze, její hodnota a rovnice.
        :param rovnice:
        :param baze:
        :param znamenko:
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
        Metoda, která vypíše informace o levém kraji, jeho vyjádření pomocí báze i jeho přibližnou hodnotu
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
        Funkce, která vypíše vše při výpočtu period; tj. rovnici, ze které vycházíme, bázi, znaménko, jednotlivé hodnoty
         levého kraje, které se pro danou periodu a předperiodu našli, jejich rozvoj, a následně i rozvoj pravého kraje.
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
                    #perioda.leve_kraje, perioda.leve_kraje_symbolicky, perioda.hodnoty, perioda.p,
                                  #perioda.prave_kraje, perioda.prave_kraje_perioda)
        else:
            self.f.write("Bohužel ani jedna z možností nebyla rozvojem levého kraje s danou předperiodou a periodou. ")
        if perioda.presne:
            self.f.write("Rozvoje krajů jsou spočteny přesně, resp. s použitím limity. ")
        else:
            self.f.write("Rozvoje krajů jsou spočteny nepřesně, resp. bez použití limity. ")
        print("Výsledky byly úspěšně zapsány do souboru ", self.nazev)

    def nalezene_periody(self, perioda: Perioda):
#                        self, leve_kraje, leve_kraje_symbolicke, hodnoty: list, p: int, prave_kraje: list,
  #                        perioda_praveho: list):
        """
        Funkce, která vypíše jednotlivé hodnoty levého kraje, vyjádřeného bází i přibližnou hodnotu, jejich periodický
        rozvoj s danou délkou předperiody a periody i hodnoty pravého kraje pro dané l.
        :param leve_kraje: hodnota levého kraje
        :param leve_kraje_symbolicke: hodnota levého kraje vyjádřena pomocí báze
        :param hodnoty: rozvoje levých krajů s periodou p
        :param p:
        :param prave_kraje: rozvoje pravých krajů s periodami perioda_praveho
        :param perioda_praveho:
        """
        # TODO popis parametru
        self.f.write("\\begin{itemize} ")
        for i in range(len(perioda.hodnoty)):
            self.f.write("\item $\ell = ")
            self.f.write(latex(perioda.leve_kraje_symbolicky[i]))
            self.f.write("\doteq {} $ \n".format(N(perioda.leve_kraje[i], n=3)))
            self.vypis_parametry_soustavy(perioda.fce, perioda.znamenko, perioda.leve_kraje[i])
            self.vypis_rozvoj_leveho(perioda.hodnoty[i], perioda.p)
            self.vypis_rozvoj_praveho(perioda.prave_kraje[i], perioda.prave_kraje_perioda[i])
        self.f.write("\end{itemize}")

    def vypis_parametry_soustavy(self, fce, znamenko, levy):
        self.f.write("%% Soustava.Soustava(' ")
        self.f.write(fce)
        self.f.write(" ', {}, ' {} ') \n".format(znamenko, levy))


    def vypis_cas(self, cas: int):
        """
        Metoda pro výpis času stráveného nad danným výpočtem.
        :param cas: čas strávený nad výpočtem
        """
        self.f.write("Celé to trvalo {0:.2f} sekund. ".format(cas))

    def vypis_rozvoj_vse(self, soustava: Soustava):
        """
        Funkce, která vypíše vše při výpočtu rozvoje konkrétní soustavy; tj. rovnici, ze které vycházíme, bázi,
        znaménko, hodnotu levého kraje, jeho rozvoj a následně i rozvoj pravého kraje. Pokud bylo spočteno mink, maxk,
        pak i jejich hodnoty.
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
            self.f.write("Rozvoje krajů jsou spočteny přesně, resp. s použitím limity. ")
        else:
            self.f.write("Rozvoje krajů jsou spočteny nepřesně, resp. bez použití limity. ")

    def vypis_perioda_DP(self, perioda: Perioda):
        self.f.write("\\begin{labeling}{k=9, } \n\n")
        self.f.write("   \item [$k= {} $,] \n".format(perioda.k))
        self.f.write("   \\begin{labeling}{$\circ$} \n")
        #self.f.write("\\begin{itemize} ")
        for i in range(len(perioda.hodnoty)):
            self.f.write("      \item [$\circ$] $\ell = ")
            self.f.write(latex(perioda.leve_kraje_symbolicky[i]))
            self.f.write("\doteq {} $ \\\\[5pt] \n".format(N(perioda.leve_kraje[i], n=3)))
            self.f.write("      $d(\ell) =  ")
            self.prevod_rozvoj_s_periodou(perioda.hodnoty[i],perioda.p)
            self.f.write("\\\\[5pt]\n $d^*(\ell+1) = ")
            self.prevod_rozvoj_s_periodou(perioda.prave_kraje[i], perioda.prave_kraje_perioda[i])
            self.f.write("\\\\[5pt]\n      $(\Delta_k)_{k \geq 1} = \{ \n")
            #print(perioda.leve_kraje_symbolicky[i])
            pomoc = Soustava.Soustava(perioda.fce, perioda.znamenko, perioda.leve_kraje[i])
            pomoc.spocitej_rozvoj_leveho_kraje(False)
            assert pomoc.rozvoj_leveho_kraje == tuple(perioda.hodnoty[i])
            pomoc.spocitej_rozvoj_praveho_kraje(False)
            assert pomoc.rozvoj_praveho_kraje == tuple(perioda.prave_kraje[i])
            pomoc.spocitej_mink_maxk(10)
            #self.prevod_vyrazu_na_latex(pomoc.vzdalenosti_symbolicky[0])
            for k in range (len(pomoc.vzdalenosti)):
                self.prevod_x_na_beta(pomoc.vzdalenosti_symbolicky[k])
                self.f.write(", \n ")
            self.f.write("\dots\}$ \n")
            #self.f.write(pomoc.vzdalenosti)
            vzdalenosti = [N(x,n=5,chop=True) for x in pomoc.vzdalenosti]
            #vzdalenosti = N(pomoc.vzdalenosti, n=5, chop=True)
            self.f.write("      %% Vzdalenosti: [%s]" % ",".join(map(str, vzdalenosti)))
            self.f.write("\n")
#            self.vypis_rozvoj_leveho(hodnoty[i], p)
#            self.vypis_rozvoj_praveho(prave_kraje[i], perioda_praveho[i])
        self.f.write("   \end{labeling}\n\n")
        self.f.write("\end{labeling}\n")