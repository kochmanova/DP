from sympy import latex, sympify, N, cancel
from sympy.abc import x, beta


class Soubor(object):
    def __init__(self, nazev):
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

    # TODO hlavičku a tabulku dát do RESOURCE
    # TODO PROFILY - zjistit, jak to udělat, aby se na dvou počítačích a ty adresáře...

    def napis_hlavicku(self):
        """
        Funkce, která si otevře hlavicka.tex, ze kterého si zkopíruje celý text a vloží jej do souboru, do kterého zapisuje.
        """
        hl = open("/home/mysska/Plocha/DP/vystup/hlavicka.tex", "r")
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

    def vypis_rozvoj_leveho(self, list, perioda):
        """
        Funkce, pro vypsání rozvoje levého kraje do souboru.
        :param list (list): rozvoj levého kraje
        :param perioda (int/None): délka periody
        """
        self.f.write("Rozvoj levého kraje: ")
        self.prevod_list_s_periodou(list, perioda)
        self.f.write(" \n\n")

    def vypis_rozvoj_praveho(self, list, perioda):
        """
        Funkce, pro vypsání rozvoje levého kraje do souboru.
        :param list (list): rozvoj levého kraje
        :param perioda (int/None): délka periody
        """
        self.f.write("Limitní rozvoj pravého kraje: ")
        self.prevod_list_s_periodou(list, perioda)
        self.f.write(" \n\n")

    def vypis_minmax(self, mink, maxk, gamma):
        """
        Funkce pro vypsání řetězců min(k), max(k), a jejich vzdáleností do souboru v podobě tabulky.
        :param mink, maxk (list listů): TODO..., gamma (list): spočtené vzdálenosti mezi řetězci min(k) a max(k)
        """
        hl = open("/home/mysska/Plocha/DP/vystup/tabulka.tex", "r")
        radky = hl.readlines()
        self.f.writelines(radky)

        for i in range(1, len(gamma)):
            self.f.write("{}".format(i))
            self.f.write(" & ")
            self.prevod_list_na_retezec(mink[i])
            self.f.write(" & ")
            self.prevod_list_na_retezec(maxk[i])
            self.f.write(" & {0:.5f} \\\\ ".format(gamma[i]))

        self.f.write(" \end{tabular}\end{center}\end{table} ")

    def prevod_list_s_periodou(self, list, perioda):
        """
        Funkce pro vypsání rozvoje bodu s periodou do souboru.
        :param list (list): rozvoj bodu
        :param perioda (int/None): délka periody
        """
        self.f.write("$")
        if perioda == None:
            self.prevod_list_na_retezec(list)
        elif len(list) == perioda:
            self.f.write("(")
            self.prevod_list_na_retezec(list)
            self.f.write(")^\omega")
        else:
            j = 0
            zav = len(list) - perioda
            for i in list:
                if j == zav:
                    self.f.write("(")
                if i < 0:
                    self.f.write("\overline {} ".format(-i))
                else:
                    self.f.write("{}".format(i))
                j += 1
            self.f.write(")^\omega")

        self.f.write("$\n")

    def prevod_list_na_retezec(self, list):
        """
        Funkce pro vypsání rozvoje bodu bez periody do souboru. (Pozor: nevypíše rozvoj v matematickém modu)
        :param list (list): rozvoj bodu
        """
        for i in list:
            if i < 0:
                self.f.write("\overline {} ".format(-i))
            else:
                self.f.write("{}".format(i))

    def prevod_vyrazu_na_latex(self, vyraz):
        """
        Metoda, která výraz převede do LaTeX formy. (Pozor: nevypíše výraz v matematickém modu)
        :param vyraz: převáděný výraz
        """
        prevod = sympify(vyraz)
        self.f.write(latex(prevod))

    def prevod_x_na_beta(self, vyraz):
        """
        Metoda, která ve výrazu zasubstitutuje proměnnou x za betu a výraz převede do LaTeX formy.
        Využíváno pro výpis hodnoty levého kraje vyjádřeného pomocí báze beta. (Pozor: nevypíše výraz v matematickém modu)
        :param vyraz: převáděný výraz
        """
        prevod = sympify(vyraz)
        prevod = prevod.subs(x, beta)
        prevod = cancel(prevod)
        self.f.write(latex(prevod))

    def vypis_rovnice(self, rovnice, baze, zn):
        """
        Metoda, která vypíše základní informace o soustavě, tj. kladná/záporná báze, její hodnota a rovnice.
        :param rovnice (string), baze (SymPy), znamenko
        """
        self.f.write("Vytvořili jsme soustavu ")
        if zn < 0:
            self.f.write("se zápornou bází ")
        else:
            self.f.write("s kladnou bází ")
        self.f.write("z rovnice $")
        self.prevod_vyrazu_na_latex(rovnice)
        self.f.write("$. \\\\ Báze $\\beta = ")
        self.f.write(latex(baze))
        self.f.write("\doteq {}$. ".format(N(baze, n=3)))

    # def vypis_baze(self, baze):
    #     self.f.write("Báze $")
    #     self.prevod_vyrazu_na_latex("beta")
    #     self.f.write("=")
    #     self.f.write(latex(baze))
    #     self.f.write("\doteq {}".format(N(baze, n=3)))

    def vypis_levy(self, levy_symbol, levy_kraj):
        """
        Metoda, která vypíše informace o levém kraji, jeho vyjádření pomocí báze i jeho přibližnou hodnotu
        """
        self.f.write("Levý kraj $\ell = ")
        self.prevod_x_na_beta(levy_symbol)
        self.f.write("\doteq {} $. \n\n".format(N(levy_kraj, n=3, chop=True)))
        #self.f.write("$.\n\n")

    def vypis_perioda(self, perioda):
        """
        Funkce, která vypíše vše při výpočtu period; tj. rovnici, ze které vycházíme, bázi, znaménko, jednotlivé hodnoty
         levého kraje, které se pro danou periodu a předperiodu našli, jejich rozvoj, a následně i rozvoj pravého kraje.
        :param perioda: instance třídy Perioda
        """
        self.vypis_rovnice(perioda.fce, perioda.baze, perioda.znamenko)
        self.f.write("Počítáme rozvoje, které mají {} dlouhou předperiodu a {} délku periody. ".format(perioda.k, perioda.p))
        self.f.write("Levý kraj je pak ve tvaru $$\ell=")
        self.f.write(latex(perioda.vyraz))
        self.f.write("$$")
        moznosti = len(perioda.A)**(perioda.k+perioda.p)
        if moznosti<5:
            self.f.write("Celkem jsme prošli {} možnosti.\n\n".format(len(perioda.A) ** (perioda.k + perioda.p)))
        else:
            self.f.write("Celkem jsme prošli {} možností.\n\n".format(len(perioda.A) ** (perioda.k + perioda.p)))
        if len(perioda.hodnoty)>0:
            self.nalezene_periody(perioda.leve_kraje, perioda.leve_kraje_symbolicky, perioda.hodnoty, perioda.p, perioda.prave_kraje, perioda.prave_kraje_perioda)
        else:
            self.f.write("Bohužel ani jedna z možností nebyla rozvojem levého kraje s danou předperiodou a periodou. ")
        print("Výsledky byly úspěšně zapsány do souboru ",self.nazev)

    def nalezene_periody(self, leve_kraje, leve_kraje_symbolicke, hodnoty, p, prave_kraje, perioda_praveho):
        """
        Funkce, která vypíše jednotlivé hodnoty levého kraje, vyjádřeného bází i přibližnou hodnotu, jejich periodický
        rozvoj s danou délkou předperiody a periody i hodnoty pravého kraje pro dané l.
        :param leve_kraje: hodnota levého kraje, leve_kraje_symbolicke: hodnota levého kraje vyjádřena pomocí báze,
        hodnoty: rozvoje levých krajů s periodou p, prave_kraje: rozvoje pravých krajů s periodami perioda_praveho
        """
        self.f.write("\\begin{itemize} ")
        for i in range(len(hodnoty)):
            self.f.write("\item $\ell = ")
            self.f.write(latex(leve_kraje_symbolicke[i]))
            self.f.write("\doteq {} $ \n\n".format(N(leve_kraje[i], n=3)))
            self.vypis_rozvoj_leveho(hodnoty[i], p)
            self.vypis_rozvoj_praveho(prave_kraje[i], perioda_praveho[i])
        self.f.write("\end{itemize}")

    def vypis_cas(self, cas):
        """
        Metoda pro výpis času stráveného nad danným výpočtem.
        """
        self.f.write("Celé to trvalo {0:.2f} sekund. ".format(cas))

    def vypis_rozvoj_vse(self, soustava):
        """
        Funkce, která vypíše vše při výpočtu rozvoje konkrétní soustavy; tj. rovnici, ze které vycházíme, bázi, znaménko,
        hodnotu levého kraje, jeho rozvoj a následně i rozvoj pravého kraje. Pokud bylo spočteno mink, maxk, pak i jejich
        hodnoty.
        :param soustava: instance třídy Soustava
        """
        self.vypis_rovnice(soustava.fce, soustava.baze, soustava.znamenko)
        self.vypis_levy(soustava.symbol_levy_kraj, soustava.levy_kraj)
        if not(soustava.rozvoj_leveho_kraje==None):
            self.vypis_rozvoj_leveho(soustava.rozvoj_leveho_kraje, soustava.perioda_leveho_kraje)
        if not(soustava.rozvoj_praveho_kraje==None):
            self.vypis_rozvoj_praveho(soustava.rozvoj_praveho_kraje, soustava.perioda_praveho_kraje)
        if not(soustava.mink == None):
            print(soustava.vzdalenosti)
            self.vypis_minmax(soustava.mink, soustava.maxk, soustava.vzdalenosti)