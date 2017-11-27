import rozvoj
import time

if __name__=="__main__":
    Zn = [1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    levy = ['0', '-1/2', '-x/(x+1)', '-x/3', '-0.6', '(x-3)/2', '-4*x/13', '(2-2*x)/3', '-0.55', '-1/x', '-0.5',
            '(1-x)/2']
    #
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

    # zac = time.time()
    # tribonaci = rozvoj.Soustava('x**3-x**2-x-1', znamenko=1,symbol_levy_kraj='0')
    # period = rozvoj.Perioda('x**3-x**2-x-1', tribonaci.baze, 1, 2,4, False)
    # konec=time.time()-zac
    # print("Cele to trvalo {0:.2f} sekund".format(konec))

    levyk = '-1/(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3)) - 1/(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**2 - (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**4) + 1/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**4)'
    hodnota = [-1,-1,-1,1,0,0]

    tribonaci = rozvoj.Soustava('x**3-x**2-x-1', znamenko=1,symbol_levy_kraj=levyk)
    # zac = time.time()
    # tribonaci.spocitej_rozvoj_leveho_kraje(True, 5)
    kon = time.time()
    # print("Cele to trvalo presne {0:.2f} s".format(kon-zac))
    tribonaci.spocitej_rozvoj_leveho_kraje(False, 10)
    pom = time.time()-kon
    print("Cele to trvalo {0:.2f} s".format(pom))

    #period = rozvoj.Perioda('x**3-x**2-x-1', tribonaci.baze, 1, 2,4, False)
    #print("Jdu na to")
    #period.zpetne_overeni(hodnota,levyk)
