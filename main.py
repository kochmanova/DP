import rozvoj
import time
import latex_export

from sympy import latex, simplify

if __name__=="__main__":
    Zn = [1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    levy = ['0', '-1/2', '-x/(x+1)', '-x/3', '-0.6', '(x-3)/2', '-4*x/13', '(2-2*x)/3', '-0.55', '-1/x', '-0.5',
            '(1-x)/2']
    ## Kod pro ověření funkčnosti d(l), d*(l+1)
    # for i in [0]:
    #
    #     tribonaci = rozvoj.Soustava('x**3-x**2-x-1', znamenko=Zn[i], symbol_levy_kraj=levy[i])
    #
    #     print("LEVÝ KRAJ")
    #     zacatek = time.time()
    #     tribonaci.spocitej_rozvoj_leveho_kraje(True,10)
    #     konec=time.time()-zacatek
    #     zacatek=time.time()
    #     print("Celé to trvalo {0:.2f}".format(konec))
    #     tribonaci.spocitej_rozvoj_leveho_kraje(False,10)
    #     konec = time.time()-zacatek
    #     print("Celé to trvalo {0:.2f}".format(konec))
    #
    #     print("PRAVÝ KRAJ")
    #     zacatek = time.time()
    #     tribonaci.spocitej_rozvoj_praveho_kraje(True,10)
    #     konec = time.time() - zacatek
    #     zacatek = time.time()
    #     print("Celé to trvalo {0:.2f}".format(konec))
    #     tribonaci.spocitej_rozvoj_praveho_kraje(False,10)
    #     konec = time.time() - zacatek
    #     print("Celé to trvalo {0:.2f}".format(konec))
    #     print("###################################################################################################")

    # Kód pro ověření funkčnosti Periody(2,4) a (0,3) - funguje
    zac = time.time()
    rovnice = 'x**3-x**2-x-1'
    znamenko = 1
    k=0
    p=2
    tribonaci = rozvoj.Soustava(rovnice, znamenko,symbol_levy_kraj='0')
    period = rozvoj.Perioda(rovnice, tribonaci.baze, znamenko, k,p, presnost=False)
    period.dosazeni_vse()
    #period = rozvoj.Perioda()
    mezicas = time.time()-zac
    print("Výpočet trval {0:.2f} sekund".format(mezicas))
    soubor = "/home/mysska/Plocha/DP/vystup/pokus_period.tex"
    file = latex_export.Soubor(soubor)
    file.vypis_rovnice(rovnice,znamenko)
    file.vypis_perioda(k,p,period.vyraz,3**(k+p))
    #file.vypis_periody_cele(period.hodnoty,period.leve_kraje,period.leve_kraje_symbolicky,p)
    file.vypis_periody_nalezene(period.leve_kraje, period.leve_kraje_symbolicky, period.hodnoty, p, period.prave_kraje, period.prave_kraje_perioda, period.prave_kraje_pomoc)

    file.ukonceni_souboru()
    konec=time.time()-zac
    print("Cele to trvalo {0:.2f} sekund".format(konec))

    ###########################################################################

    ## Případ u periody
    # levyk = '-1/(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3)) - 1/(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**2 - (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**4) + 1/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**4)'
    # hodnota = [-1,-1,-1,1,0,0]

    levyk = '-(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**2/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**3) + 1/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**3)'
    hodnota=[-1,0,1]

    levyk2= '-(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**4) + 1/((-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**4)*(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**2) + 1/((-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**4)*(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))) + 1/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**4)'


    #
    # tribonaci = rozvoj.Soustava('x**3-x**2-x-1', znamenko=1,symbol_levy_kraj=levyk)
    # zac = time.time()
    # tribonaci.spocitej_rozvoj_leveho_kraje(False, 5) # True funguje
    # kon = time.time()
    # print("Cele to trvalo presne {0:.2f} s".format(kon-zac))
    # tribonaci.spocitej_rozvoj_leveho_kraje(False, 5)
    # pom = time.time()-kon
    # print("Cele to trvalo {0:.2f} s".format(pom))

    # period = rozvoj.Perioda('x**3-x**2-x-1', tribonaci.baze, 1, 0,3, False)
    # print("Jdu na to")
    # period.zpetne_overeni(hodnota,levyk)
    # l = period.vycisleni_vyrazu_abc(period.vyraz, hodnota)
    # print(latex(l))

    #########################################################################
    ## Dříve POKAŇHANÉ, teraz fungující :D
    # lev = ['0','-1/x','(1-x)/2','-x/2','-(1/2 + sqrt(5)/2)**2/(-1 + (1/2 + sqrt(5)/2)**3) + (1/2 + sqrt(5)/2)/(-1 + (1/2 + sqrt(5)/2)**3)']
    # for i in [2,4]:
    #     zac = time.time()
    #     fibanaci = rozvoj.Soustava('x**2-x-1', znamenko=1, symbol_levy_kraj=lev[i])
    #
    #     fibanaci.spocitej_rozvoj_leveho_kraje(True,10)
    #     fibanaci.spocitej_rozvoj_leveho_kraje(False,10)
    #
    #     fibanaci.spocitej_rozvoj_praveho_kraje(True,10)
    #     fibanaci.spocitej_rozvoj_praveho_kraje(False,10)
    #     kon = time.time() - zac
    #     print("Celé to trvalo {0:.2f}".format(kon))