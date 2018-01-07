import Soustava
import time
import latex_export

if __name__ == "__main__":

    rovnice = 'x**2-x-1'
    znamenko = 1
    levy_kraj = '-1/(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3)) - 1/(1/3 + ' \
                '4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**2 - (1/3 + 4/(9*(sqrt(33)/9 ' \
                '+ 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) +' \
                ' (sqrt(33)/9 + 19/27)**(1/3))**4) + 1/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 +' \
                ' 19/27)**(1/3))**4)'
    Zn = [1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    levy = ['0', '-1/2', '-x/(x+1)', '-x/3', '-0.6', '(x-3)/2', '-4*x/13', '(2-2*x)/3', '-0.55', '-1/x', '-0.5',
            '(1-x)/2']
    poc = 8 #0,1,2,3,4,5,6,7
    znamenko = Zn[poc]
    levy_kraj = levy[poc]
    max_cifer = 25
    k = 10

    # následuje část, kdy se volají jednotlivé metody, tedy dále není potřeba cokoliv upravovat
    cas = time.localtime()
    if znamenko > 0:
        nazev = "rozvoj_kladny_{}_{}_{}_{}_{}".format(cas.tm_year, cas.tm_mon, cas.tm_mday, cas.tm_hour,
                                                      cas.tm_min)
    else:
        nazev = "rozvoj_zaporny_{}_{}_{}_{}_{}".format(cas.tm_year, cas.tm_mon, cas.tm_mday, cas.tm_hour,
                                                       cas.tm_min)

    soubor = "vystup/" + nazev + ".tex"
    file = latex_export.LatexExport(soubor)

    rozvoj = Soustava.Soustava(rovnice, znamenko, levy_kraj)

    file.vypis_rovnice(rovnice,rozvoj.baze,znamenko)
    file.vypis_levy(levy_kraj,rozvoj.levy_kraj)

    for i in range(5,max_cifer,5):
        # nalezení rozvoje pro levý i limitní pravý kraj
        zacatek_vypoctu = time.time()
        rozvoj.spocitej_rozvoj_leveho_kraje(False, i)
        file.vypis_rozvoj_leveho(rozvoj.rozvoj_leveho_kraje,rozvoj.perioda_leveho_kraje)
        stred = time.time()
        file.vypis_cas(stred-zacatek_vypoctu)
        file.f.write("\n\n")

        rozvoj.spocitej_rozvoj_praveho_kraje(i)
        file.vypis_rozvoj_praveho(rozvoj.rozvoj_praveho_kraje,rozvoj.perioda_praveho_kraje)
        konec = time.time()
        file.vypis_cas(konec - stred)
        file.f.write("\n\n")

        if rozvoj.perioda_praveho_kraje is not None and rozvoj.perioda_leveho_kraje is not None:
            break

    for i in range(5,max_cifer,5):
        # nalezení rozvoje pro levý i limitní pravý kraj
        zacatek = time.time()
        rozvoj.spocitej_rozvoj_leveho_kraje(True, i)
        file.vypis_rozvoj_leveho(rozvoj.rozvoj_leveho_kraje,rozvoj.perioda_leveho_kraje)
        stred = time.time()
        file.vypis_cas(stred-zacatek)
        file.f.write("\n\n")

        if rozvoj.perioda_leveho_kraje is not None:
            break

    konec_vypoctu = time.time() - zacatek_vypoctu
    file.vypis_cas(konec_vypoctu)
    file.ukonceni_souboru()

    print("Cely vypocet trval {0:.2f} sekund".format(konec_vypoctu))
