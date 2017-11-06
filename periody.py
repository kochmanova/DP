import numpy as np
import sympy as sp

import rozvoj

from itertools import product
from sympy.abc import beta,a,b,c,d,e,f,g,h,i,j,x

class Rozvoj_periodicky(object):
    """pro zadanou fci, levý kraj a sgn báze vypočte bázi, rozvoj levého a pravého kraje
    s možností spočítat mink, maxk a jejich vzdálenosti"""

    def __init__(self, fce='x**3-x**2-x-1', znamenko=1):
        """funkce, která se zavolá sama, jakmile vytvořím instanci třídy Soustava, v rámci dané instance si uloží
         znaménko, bázi, levý kraj, rozvoje"""
        # inicializace proměnných
        self.beta = None
        self.fce = fce
        if (znamenko != 1) and (znamenko != -1):
            raise ValueError("Báze může být kladná s hodnotou 1 nebo záporná s hodnotou -1.")
        self.znamenko = znamenko
        self.spocitej_bazi_beta()

    def spocitej_bazi_beta(self):
        """tato funkce je zavolaná v __init__, pro danou rovnici spočte bázi, se kterou budeme počítat a uloží si ji

        :raises: ValueError - v případě, že báze beta nesplňuje námi zadané požadavky
        """
        reseni = sp.solve(self.fce, x)
        polebazi = [i for i in reseni if np.isreal(np.complex(i))]
        if len(polebazi) < 1:
            raise ValueError("Špatně zvolená rovnice. Rovnice musí mít alespoň jeden reálný kořen.")
        baze = [i for i in polebazi if i > 1]
        if len(baze) != 1:
            # může mít báze více reálných kořenů > 1 ?
            raise ValueError(
                "Bázi je nutno volit tak, aby měla jeden reálný kořen větší jak 1. Špatně zvolená rovnice.")
        self.beta = baze[0]

class Perioda(object):

    def __init__(self, k, p,znamenko=1):
        """funkce, která se spustí automaticky s vytvořením instance Rozvoj, uloží si jednotlivé hodnoty a spočte
        rozvoj bodu s jeho periodou"""
        #self.baze = baze
        self.znamenko = znamenko
        self.k = k
        self.p = p
        self.symboly = [a,b,c,d,e,f,g,h,i,j]
        self.mocnina=1
        self.hodnoty=list()
        self.levy_kraj=list()

    def predperioda(self):
        vyraz = 0
        if self.k > 0:
            pomocna = self.k
            while pomocna > 0:
                vyraz = vyraz + self.symboly.pop(0)/beta**self.mocnina
                self.mocnina = self.mocnina+1
                pomocna = pomocna-1
        self.vyraz_pred = vyraz

    def perioda(self):
        vyraz = 0
        pomocna = self.p
        while pomocna > 0:
            vyraz = vyraz +self.symboly.pop(0)/beta**(self.mocnina-self.p)*1/(beta**self.p-1)
            self.mocnina= self.mocnina+1
            pomocna -= 1
        self.vyraz_perioda = vyraz

    def cely_vyraz(self):
        self.predperioda()
        self.perioda()
        self.vyraz= self.vyraz_pred + self.vyraz_perioda
        print(self.vyraz)

    def vycisleny_vyraz(self,baze):
        vycisleny = self.vyraz.subs(beta, baze)
        print(vycisleny)
        self.vycisleny = vycisleny
        self.baze = baze

    # Bylo by hezké mít funkci, která dosadí všechny hodnoty krom bety abychom viděli, jak vypadá levý kraj vyjádřen s pomocí bety

    def dosazeni(self,hodnoty, fce):
        symboly=[a,b,c,d,e,f,g,h,i,j]
        #pomocne = self.k+self.p
        vyraz=self.vycisleny
        pom_hodnoty = list(hodnoty)
        while len(pom_hodnoty) > 0: #pomocne > 0:
            vyraz=vyraz.subs(symboly.pop(0),pom_hodnoty.pop(0))
        #print(vyraz)
        levy_kraj = sp.N(vyraz, n=1000)
        if levy_kraj <= 0 and levy_kraj >= -1:
            retezec = list(hodnoty)
            #print(vyraz)
            prosel = self.zpetne_overeni(retezec, vyraz, fce)
            # dodatečná podmínka pro tuto konkrétní bázi
            #if prosel and (levy_kraj > -1/self.baze and levy_kraj <= 1/self.baze-1):
            # TU PODMÍNKU JSEM POKANHALA
            #    print("Daný řetězec neleží v L_beta, tedy má Z_b jen s 0.")
                # self.hodnoty.append(list(hodnoty))
                # self.levy_kraj.append(vyraz)
                # levy_kraj = sp.N(vyraz,n=20)
                # print(hodnoty)
                # print(levy_kraj) # mít to ve formatu je problém s nulou...nevim proč

    def dosazeni_vse(self, fce):
        A=[-1,0,1]
        delka = self.k + self.p
        hodnoty=list(product(A,repeat=delka))
        # já to tak chci yeld!!!!
        #print(hodnoty)
        print("Celkem máme {0:.0f} řetezců".format(len(hodnoty)))
        #self.hodnoty=hodnoty
        for retezec in hodnoty:
            #print(retezec)
            self.dosazeni(retezec, fce)

    def zpetne_overeni(self, hodnoty, levy, fce): # hodnoty jsou list!!
        hledany_rozvoj = rozvoj.Soustava(fce, self.znamenko, levy)
        #print(levy)
        #print(hodnoty)
        #print(hledany_rozvoj.rozvoj_leveho_kraje.rozvoj_bodu)
        if hodnoty == hledany_rozvoj.rozvoj_leveho_kraje.rozvoj_bodu :
            if self.p == hledany_rozvoj.rozvoj_leveho_kraje.perioda:
                self.hodnoty.append(hodnoty)
                self.levy_kraj.append(levy)
                print("Retezec, ktery ma {} predperiodu a {} periodu je (retezec, levy kraj):".format(self.k, self.p))
                print(hodnoty)
                #print(self.p)
                print(levy)
                print("Tento retezec ma pak rozvoj praveho kraje a periodu: ")
                print(hledany_rozvoj.rozvoj_praveho_kraje.rozvoj_bodu)
                print(hledany_rozvoj.rozvoj_praveho_kraje.perioda)
                return True
        return False













