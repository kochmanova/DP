import rozvoj
import time
import periody
import math
import limitni
import sympy as sp

from sympy.abc import a

if __name__ == "__main__":
    #zacatek = time.time()

    Zn = [1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    levy = ['0', '-1/2', '-x/(x+1)', '-x/3', '-0.6', '(x-3)/2', '-4*x/13', '(2-2*x)/3', '-0.55', '-1/x', '-0.5',
            '(1-x)/2']

    for i in [2]: #číslo v hranatých závorkách představuje pro jaký levý kraj se bude počítat rozvoj pravého kraje z pole levy
        zacatek = time.time()
        tribonaci = rozvoj.Soustava('x**3-x**2-x-1', znamenko=Zn[i], levy_kraj=levy[i])
        pravy = limitni.Limitni_rozvoj(tribonaci.beta,tribonaci.levy_kraj,Zn[i],8) # ta 8 představuje na kolik cifer chci udělat rozvoj
        pravy.limitni_rozvoj()
        print("Limitní rozvoj pravého kraje: ")
        print(pravy.rozvoj_bodu)
        print("S periodou delky {}".format(pravy.perioda))

        print("No a nepřesne, pravý kraj:")
        print(tribonaci.rozvoj_praveho_kraje.rozvoj_bodu)
        print("S periodou delky {}".format(tribonaci.rozvoj_praveho_kraje.perioda))
        konec = time.time() - zacatek
        print("Cyklus trval {0:.2f} s".format(konec))

    # print("Nyni se podíváme na fibonacciho koren: ")

    Z=[1]
    lev=['0','-1/x','(1-x)/2','-x/2','-(1/2 + sqrt(5)/2)**2/(-1 + (1/2 + sqrt(5)/2)**3) + (1/2 + sqrt(5)/2)/(-1 + (1/2 + sqrt(5)/2)**3)']
    # for i in [2,4]:  # číslo v hranatých závorkách představuje pro jaký levý kraj se bude počítat rozvoj pravého kraje z pole levy
    #     zacatek = time.time()
    #     fibonaci = rozvoj.Soustava('x**2-x-1', znamenko=Z[0], levy_kraj=lev[i])
    #     pravy = limitni.Limitni_rozvoj(fibonaci.beta, fibonaci.levy_kraj, Z[0], 10)  # ta 8 představuje na kolik cifer chci udělat rozvoj
    #     pravy.limitni_rozvoj()
    #     print("Limitní rozvoj pravého kraje: ")
    #     print(pravy.rozvoj_bodu)
    #     print("S periodou delky {}".format(pravy.perioda))
    #
    #     print("No a nepřesne, pravý kraj:")
    #     print(fibonaci.rozvoj_praveho_kraje.rozvoj_bodu)
    #     print("S periodou delky {}".format(fibonaci.rozvoj_praveho_kraje.perioda))
    #
    #     konec = time.time() - zacatek
    #     print("Cyklus trval {0:.2f} s".format(konec))




    # print("Jsem tu.")
    # vyraz = a+5
    # print(vyraz)
    # dosazeni = vyraz.subs(a, 5)
    # print(dosazeni)




    # # cyklus = zacatek
    # for i in [0]: #range(12):
    #     start_cyklu = time.time()
    #     print("Vytvářím základní soustavu znamenko {} a okraj {}".format(Zn[i], levy[i]))
    #     tribonacci = rozvoj.Soustava('x**3-x**2-x-1', znamenko=Zn[i], levy_kraj=levy[i])
    #     print(tribonacci.beta)
    #     print("Rozvoj leveho kraje: ")
    #     print(tribonacci.rozvoj_leveho_kraje.rozvoj_bodu)
    #     print(tribonacci.rozvoj_leveho_kraje.perioda)
    #     print("Snaha o rozvoj praveho kraje:")
    #     print(tribonacci.rozvoj_praveho_kraje.rozvoj_bodu)
    #     print(tribonacci.rozvoj_praveho_kraje.perioda)
    #     # print("Následuje po řádcích mink, maxk, vzdálenosti:")
    #     # tribonacci.vytvoreni_mink_maxk(15)
    #     # print(tribonacci.mink)
    #     # print(tribonacci.maxk)
    #     # tribonacci.spocteni_vzdalenosti(15)
    #     # print(tribonacci.delta)
    #     cyklus = time.time() - start_cyklu
    #     print("Cyklus trval {0:.2f} s".format(cyklus))
    #
    # #print(tribonacci.levy_kraj)
    # #j=2
    # #tribonacci_rozvoj=rozvoj.Rozvoj(tribonacci.beta,tribonacci.levy_kraj+1,tribonacci.levy_kraj,Zn[j],True,30)
    # #print("Máme bázi {}, {} bázi a levý kraj je {}".format(tribonacci.beta, tribonacci.znamenko,tribonacci.levy_kraj))
    # #tribonacci_rozvoj.limitni_rozvoj_pk()
    # #print("Rozvoj praveho kraje limitni:")
    # #print(tribonacci_rozvoj.rozvoj_pk)
    # #print("Perioda: ")
    # #print(tribonacci_rozvoj.perioda_pk)
    #
    # konec = time.time() - zacatek
    # print("Celé to trvalo {0:.2f} s".format(konec))
    #
    #
    ### pro nalezení periodických rozvojů levého kraje
    # start= time.time()
    # fibonacci = periody.Rozvoj_periodicky('x**2-x-1',1)
    # kp=periody.Perioda(0,3,1)
    # kp.cely_vyraz() # získám vyraz
    # kp.vycisleny_vyraz(fibonacci.beta)
    # kp.dosazeni_vse('x**2-x-1')
    # #print(len(kp.hodnoty))
    # konec = time.time() - start
    # print("Celé to trvalo {0:.2f} s".format(konec))
    #
    # #### pro určení přesnosti
    # # fibonacci = presnost.presnost('x**3-x**2-x-1',1)
    # # for i in range(1,5):
    # #     print("Pro {0:.0f} cifer je nután přesnost na ".format(i))
    # #     fibonacci.kladna(i)
    # # for i in range(10,110,10):
    # #     print("Pro {0:.0f} cifer je nután přesnost na ".format(i))
    # #     fibonacci.kladna(i)
    # #
    # # fibonacci.kladna(500)
    # # fibonacci.kladna(1000)
    #
    # #print((-(1/2 + math.sqrt(5)/2)**2/(-1 + (1/2 + math.sqrt(5)/2)**3) + (1/2 + math.sqrt(5)/2)/(-1 + (1/2 + math.sqrt(5)/2)**3)) == (-(1/2 + math.sqrt(5)/2)/2+1/2))