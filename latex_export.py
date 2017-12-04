from sympy import latex, sympify, N
from sympy.abc import x, beta

class Soubor(object):

    def __init__(self, nazev):
        self.nazev = nazev
        self.otevri_soubor()
        #print("Soubor se otevrel")
        self.napis_hlavicku()
        #print("Soubor ma hlavicku")
        #self.ukonceni_souboru()
        #print("Soubor se zavrel")

    def otevri_soubor(self):
        f = open(self.nazev,"w")
        self.f = f

    # UDĚLAT, ABY PO ZÁPISU SE SOUBOR SÁM BZEPEČNĚ UZAVŘEL A PŘI DALŠÍM ZÁPISU SE ZAS OTEVŘEL.

    # hlavičku a tabulku dát do RESOURCE

    # PROFILY - zjistit, jak to udělat, aby se na dvou počítačích a ty adresáře...
    def napis_hlavicku(self):
        hl = open("/home/mysska/Plocha/DP/vystup/hlavicka.tex","r")
        radky = hl.readlines()
        #for i in radky:
        self.f.writelines(radky)
            #print(radky[i])
        hl.close()

    def ukonceni_souboru(self):
        self.f.write("\n \end{document}")
        self.f.close()

    def vypis_rozvoj_leveho(self, list, perioda):
        self.f.write("Rozvoj levého kraje: ")
        self.list_s_periodou(list,perioda)
        self.f.write(" \n\n")

    def vypis_pravy_kraj(self, list, perioda):
        self.f.write("Limitní rozvoj pravého kraje: ")
        self.list_s_periodou(list, perioda)
        self.f.write(" \n\n")

    def vypis_minmax(self,mink, maxk, gamma):
        hl = open("/home/mysska/Plocha/DP/vystup/tabulka.tex", "r")
        radky = hl.readlines()
        self.f.writelines(radky)

        for i in range(1,len(gamma)):
            self.f.write("{}".format(i))
            self.f.write(" & ")
            self.list_na_retezec(mink[i])
            self.f.write(" & ")
            self.list_na_retezec(maxk[i])
            self.f.write(" & {0:.5f} \\\\ ".format(gamma[i]))
            #TU TO NEFACHA

        self.f.write(" \end{tabular}\end{center}\end{table} ")


    def list_s_periodou(self,list,perioda):
        self.f.write("$")
        #print((list))
        if perioda==None:
            self.list_na_retezec(list)
        elif len(list)==perioda:
            self.f.write("(")
            self.list_na_retezec(list)
            self.f.write(")^\omega")
        else:
            j=0
            zav=len(list)-perioda
            for i in list:
                if j==zav:
                    self.f.write("(")
                if i < 0:
                    self.f.write("\overline {} ".format(i))
 #                   self.f.write("{}".format(i))
                else:
                    self.f.write("{}".format(i))
#                    self.f.write("\overline{1}")
                j+=1
            self.f.write(")^\omega")
        self.f.write("$\n")

    def list_na_retezec(self,list):
        #self.f.write("$$")
        #print(len(list))
        #if len(list)>2:
        #    print(list[2])
        for i in list:
            if i < 0:
                self.f.write("\overline {} ".format(-i))
                #                   self.f.write("{}".format(i))
            else:
                self.f.write("{}".format(i))
        #self.f.write("$$\n")

    def uprava_znaku(self,znaky):
        prevod = sympify(znaky)
        #self.f.write("$")
        self.f.write(latex(prevod))
        #self.f.write("$")

    def zmena_znaku(self,znaky):
        prevod = sympify(znaky)
        prevod = prevod.subs(x,beta)
        #self.f.write("$")
        self.f.write(latex(prevod))
        #self.f.write("$")


    def vypis_rovnice(self,rovnice,zn):
        self.f.write("Vytvořili jsme soustavu ")
        if zn<0:
            self.f.write("se zápornou bází ")
        else:
            self.f.write("s kladnou bází ")
        self.f.write("z rovnice $")
        self.uprava_znaku(rovnice)
        self.f.write("$.\n\n")

    def vypis_baze(self,baze):
        self.f.write("Báze $")
        self.uprava_znaku("beta")
        self.f.write("=")
        #self.f.write(latex("beta="))
        #self.f.write(latex(simplify(baze)))
        self.f.write(latex(baze))
        self.f.write("\doteq {}".format(N(baze,n=3)))

    def vypis_levy(self,levy,levy_kraj):
        self.f.write("$ a levý kraj $\ell = ")
        self.zmena_znaku(levy)
        self.f.write("\doteq {}".format(N(levy_kraj,n=3)))
        self.f.write("$.\n\n")

    def vypis_perioda(self,k,p, vyraz, moznosti):
        self.f.write("Počítáme rozvoje , které mají {} dlouhou předperiodu a {} délku periody. ".format(k,p))
        self.f.write("Levý kraj je pak ve tvaru $$\ell=")
        self.f.write(latex(vyraz))
        self.f.write("$$")
        self.f.write("Celkem jsme prošli {} možností.\n\n".format(moznosti))

    def vypis_periody_nalezene(self, leve_kraje, leve_kraje_symbolicke, hodnoty, p, prave_kraje, perioda_praveho, prave_pom, pom_perioda):
        self.f.write("\\begin{itemize} ")
        for i in range(len(hodnoty)):
#            self.f.write("Nalezli jsme řetězec, který to splňuje. Tento řetězec má $$\ell = ")
            self.f.write("\item $\ell = ")
            self.f.write(latex(leve_kraje_symbolicke[i]))
            #self.f.write(" = ")
            #self.f.write(latex(leve_kraje[i]))
            self.f.write("\doteq {} $ \n\n".format(N(leve_kraje[i],n=3)))
            self.vypis_rozvoj_leveho(hodnoty[i],p)
            self.vypis_pravy_kraj(prave_kraje[i],perioda_praveho[i])
            self.vypis_pravy_kraj(prave_pom[i],pom_perioda[i])
        self.f.write("\end{itemize}")

    def vypis_cas(self, cas):
        self.f.write("Celé to trvalo {0:.2f} sekund. ".format(cas))
