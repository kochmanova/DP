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

    def vypis_levy_kraj(self,list, perioda):
        self.f.write("Rozvoj levého kraje: ")
        self.list_s_periodou(list,perioda)
        self.f.write(" \n\n")

    def vypis_pravy_kraj(self, list, perioda):
        self.f.write("Limitní rozvoj pravého kraje: ")
        self.list_s_periodou(list, perioda)
        self.f.write(" \n\n")

    def list_s_periodou(self,list,perioda):
        self.f.write("$")
        #print(len(list))
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
                if i == 0 or i == 1:
                    self.f.write("{}".format(i))
                else:
                    self.f.write("\overline{1}")
                j+=1
            self.f.write(")^\omega")
        self.f.write("$\n")

    def list_na_retezec(self,list):
        #self.f.write("$$")
        #print(len(list))
        for i in list:
            if i == 0 or i == 1:
                self.f.write("{}".format(i))
            else:
                self.f.write("\overline{1}")
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

    def vypis_baze(self,baze,levy, levy_kraj):
        self.f.write("Báze $")
        self.uprava_znaku("beta")
        self.f.write("=")
        #self.f.write(latex("beta="))
        #self.f.write(latex(simplify(baze)))
        self.f.write(latex(baze))
        self.f.write("\doteq {}".format(N(baze,n=3)))
        self.f.write("$ a levý kraj $\ell = ")
        self.zmena_znaku(levy)
        self.f.write("\doteq {}".format(N(levy_kraj,n=3)))
        self.f.write("$.\n\n")
