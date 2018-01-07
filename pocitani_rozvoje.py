import Soustava
import time
import latex_export

from sympy import cancel

if __name__ == "__main__":

    rovnice = 'x**2-x-1'
    znamenko = 1
    levy_kraj = '-1/x'
            # #'-1/(1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3)) - 1/(1/3 + ' \
            #     '4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))**2 - (1/3 + 4/(9*(sqrt(33)/9 ' \
            #     '+ 19/27)**(1/3)) + (sqrt(33)/9 + 19/27)**(1/3))/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) +' \
            #     ' (sqrt(33)/9 + 19/27)**(1/3))**4) + 1/(-1 + (1/3 + 4/(9*(sqrt(33)/9 + 19/27)**(1/3)) + (sqrt(33)/9 +' \
            #     ' 19/27)**(1/3))**4)'
    print(cancel(levy_kraj))
    levy_kraj = cancel(levy_kraj)
    presnost = True
    pocet_cifer = 10
    k = 5

    # následuje část, kdy se volají jednotlivé metody, tedy dále není potřeba cokoliv upravovat

    zacatek_vypoctu = time.time()
    rozvoj = Soustava.Soustava(rovnice, znamenko, levy_kraj)

    # nalezení rozvoje pro levý i limitní pravý kraj
    rozvoj.spocitej_rozvoj_leveho_kraje(presnost, pocet_cifer)
    rozvoj.spocitej_rozvoj_praveho_kraje(pocet_cifer)

    # nalezení mink, maxk řetězců a jejich vzdáleností
    rozvoj.spocitej_mink_maxk(k)

    # export výsledků do LaTeXového souboru
    cas = time.localtime()
    if znamenko > 0:
        nazev = "rozvoj_kladny_{}_{}_{}_{}_{}".format(cas.tm_year, cas.tm_mon, cas.tm_mday, cas.tm_hour,
                                                      cas.tm_min)
    else:
        nazev = "rozvoj_zaporny_{}_{}_{}_{}_{}".format(cas.tm_year, cas.tm_mon, cas.tm_mday, cas.tm_hour,
                                                       cas.tm_min)

    soubor = "vystup/" + nazev + ".tex"
    file = latex_export.LatexExport(soubor)
    file.vypis_rozvoj_vse(rozvoj)

    konec_vypoctu = time.time() - zacatek_vypoctu
    file.vypis_cas(konec_vypoctu)
    file.ukonceni_souboru()

    print("Cely vypocet trval {0:.2f} sekund".format(konec_vypoctu))
