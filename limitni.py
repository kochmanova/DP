import numpy as np
import sympy as sp


from sympy.abc import x

EPS = 9e-17
MALO = 2e-8

class Limitni_rozvoj(object):
    """Třída pro rozvoj libovolného čísla v intervalu <l,l+1), nutno znát kladnou/zápornou (znaménko)
     bázi beta, bod, l, a počet cifer"""

    def __init__(self, baze, levy_kraj, znamenko=1, pocet_cifer=30):
        """funkce, která se spustí automaticky s vytvořením instance Rozvoj, uloží si jednotlivé hodnoty a spočte
        rozvoj bodu s jeho periodou"""
        self.baze = baze
        self.znamenko = znamenko
        self.levy_kraj = levy_kraj
        self.perioda = None
        self.rozvoj_bodu = None
        self.pocet_cifer = pocet_cifer

    def limitni_rozvoj(self):
        """pomocná limitní funkce, která by pro pravý kraj měla spočítat limitní rozvoj v dané bázi na pocet_cifer

        :param pocet_cifer: počet míst, na který chceme vyčíslit rozvoj pravého kraje, defaultně nastaven na 30
        """
        perioda = False
        transformace = list()
        rozvoj = list()
        #symbol='-'

        #změna
        #transformace.append(self.levy_kraj + x)
        transformace.append(self.levy_kraj+1)

        print("Levý kraj :")
        print(self.levy_kraj)
        print("Báze: ")
        print(self.baze)
        i = 1
        cifra = sp.floor(self.znamenko * self.baze * x - self.levy_kraj)
        pomoc = self.znamenko * self.baze * x -self.levy_kraj
        while (not perioda) and (i < self.pocet_cifer):
            print("Počítáme {0:.0f}.cifru ".format(i))

            #změna
            #cifra = self.znamenko * self.baze * transformace[i - 1] - self.levy_kraj
            #pomocne = sp.floor(cifra)

            #změna
            #rozvoj.append(sp.limit(pomocne, x, self.levy_kraj+1, dir="-"))
            if (self.znamenko<0) and (i % 2 == 0):
                rozvoj.append(sp.limit(cifra,x,transformace[i-1],dir='+'))
                #print("+")
            else:
                #print((sp.limit(pomoc,x,transformace[i-1],dir='-')))
                rozvoj.append(sp.limit(cifra,x,transformace[i-1],dir='-'))

            nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
            transformace.append((nova_transformace))
            for j in range(len(transformace)):
                if (abs(sp.N((transformace[j] - transformace[i]).subs({x:self.levy_kraj+1}))) < MALO) and (j != i):
                    perioda = True
                    self.perioda = i - j
            i += 1
        self.rozvoj_bodu = rozvoj
        #print(sp.limit(sp.floor(x),x,1,dir='-'))
        #print(sp.limit(sp.floor(self.baze*(self.baze**2-self.baze-1)*x),x,1,dir='-'))

    #def pomoc(self):
    #    cifra =sp.floor(self.znamenko * self.baze * x - self.levy_kraj)
    #    print(sp.series(cifra,x,self.baze**2-self.baze-1))



    def limitni_posloupnost(self):
        """posloupnost, která spočte rozvoj bodu, který se blíží k pravému kraji

        :param pocet_cifer: počet míst, na který chceme vyčíslit rozvoj pravého kraje, defaultně nastaven na 30
        """
        periody_posl = list()
        rozvoje_posl = list()
        print(self.levy_kraj)
        for lim in range(7, 17):  # [2, ..., 9]
            perioda = False
            transformace = list()
            rozvoj = list()
            print(type(self.levy_kraj))
            bod = self.levy_kraj + 1 - sp.nsimplify(1 / 10 ** lim, tolerance=None)
            print(type(bod))
            print(bod)
            transformace.append(bod)
            i = 1
            periody_posl.append(0)
            while (not perioda) and (i < self.pocet_cifer):
                print("Počítáme {0:.0f}. cifru".format(i))
                cifra = self.znamenko * self.baze * transformace[i - 1] - self.levy_kraj
                rozvoj.append(sp.floor(cifra))
                nova_transformace = self.znamenko * self.baze * transformace[i - 1] - rozvoj[i - 1]
                transformace.append((nova_transformace))
                for j in range(len(transformace)):
                    if (abs(transformace[j] - transformace[i]) < MALO) and (j != i):
                        perioda = True
                        periody_posl[lim - 7] = i - j
                i += 1
            rozvoje_posl.append(rozvoj)
            #            self.rozvoj_bodu = rozvoj
        print(rozvoje_posl)
        print("Periody: ")
        print(periody_posl)
