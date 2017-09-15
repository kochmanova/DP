import rozvoj
import time
import periody
import presnost
import math

if __name__ == "__main__":
    zacatek = time.time()
    Zn = [1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    levy = ['0', '-1/2', '-x/(x+1)', '-x/3', '-0.6', '(x-3)/2', '-4*x/13', '(2-2*x)/3', '-0.55', '-1/x', '-0.5',
            '(1-x)/2']
    # cyklus = zacatek
    for i in [0]: #range(12):
        start_cyklu = time.time()
        #print("Vytvářím základní soustavu znamenko {} a okraj {}".format(Zn[i], levy[i]))
        #tribonacci = rozvoj.Soustava('x**3-x**2-x-1', znamenko=Zn[i], levy_kraj=levy[i])
        tribonacci = rozvoj.Soustava('x**2-x-1', 1, '-(1/2 + sqrt(5)/2)**2/(-1 + (1/2 + sqrt(5)/2)**3) + (1/2 + sqrt(5)/2)/(-1 + (1/2 + sqrt(5)/2)**3)')
        print(tribonacci.beta)
        print("Rozvoj leveho kraje: ")
        print(tribonacci.rozvoj_leveho_kraje.rozvoj_bodu)
        print(tribonacci.rozvoj_leveho_kraje.perioda)
        print("Snaha o rozvoj praveho kraje:")
        print(tribonacci.rozvoj_praveho_kraje.rozvoj_bodu)
        print(tribonacci.rozvoj_praveho_kraje.perioda)
        # print("Následuje po řádcích mink, maxk, vzdálenosti:")
        # tribonacci.vytvoreni_mink_maxk(15)
        # print(tribonacci.mink)
        # print(tribonacci.maxk)
        # tribonacci.spocteni_vzdalenosti(15)
        # print(tribonacci.delta)
        cyklus = time.time() - start_cyklu
        print("Cyklus trval {0:.2f} s".format(cyklus))
        #print(tribonacci.levy_kraj)
        #print(tribonacci.pravy_kraj)
        #print(tribonacci.levy_kraj+1)

    #print(tribonacci.levy_kraj)
    #j=2
    #tribonacci_rozvoj=rozvoj.Rozvoj(tribonacci.beta,tribonacci.levy_kraj+1,tribonacci.levy_kraj,Zn[j],True,30)
    #print("Máme bázi {}, {} bázi a levý kraj je {}".format(tribonacci.beta, tribonacci.znamenko,tribonacci.levy_kraj))
    #tribonacci_rozvoj.limitni_rozvoj_pk()
    #print("Rozvoj praveho kraje limitni:")
    #print(tribonacci_rozvoj.rozvoj_pk)
    #print("Perioda: ")
    #print(tribonacci_rozvoj.perioda_pk)

    konec = time.time() - zacatek
    print("Celé to trvalo {0:.2f} s".format(konec))


    #### pro nalezení periodických rozvojů levého kraje
    start= time.time()
    fibonacci = periody.Rozvoj_periodicky('x**2-x-1',1)
    kp=periody.Perioda(0,2,1)
    kp.cely_vyraz() # získám vyraz
    kp.vycisleny_vyraz(fibonacci.beta)
    kp.dosazeni_vse('x**2-x-1')
    #print(len(kp.hodnoty))
    konec = time.time() - start
    print("Celé to trvalo {0:.2f} s".format(konec))

    #### pro určení přesnosti
    # fibonacci = presnost.presnost('x**3-x**2-x-1',1)
    # for i in range(1,5):
    #     print("Pro {0:.0f} cifer je nután přesnost na ".format(i))
    #     fibonacci.kladna(i)
    # for i in range(10,110,10):
    #     print("Pro {0:.0f} cifer je nután přesnost na ".format(i))
    #     fibonacci.kladna(i)
    #
    # fibonacci.kladna(500)
    # fibonacci.kladna(1000)

    #print((-(1/2 + math.sqrt(5)/2)**2/(-1 + (1/2 + math.sqrt(5)/2)**3) + (1/2 + math.sqrt(5)/2)/(-1 + (1/2 + math.sqrt(5)/2)**3)) == (-(1/2 + math.sqrt(5)/2)/2+1/2))