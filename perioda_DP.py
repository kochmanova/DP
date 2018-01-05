import Soustava
import time
import latex_export
import Perioda

if __name__ == "__main__":

    predperioda = 2
    perioda = 6
    rovnice = 'x**2-x-1'
    znamenko = 1
    presnost_limit = True

    # následuje část, kdy se volají jednotlivé metody, tedy dále není potřeba cokoliv upravovat

    zacatek_vypoctu = time.time()
    rozvoj = Soustava.Soustava(rovnice, znamenko, symbol_levy_kraj=None)

    periodicke_leve_kraje = Perioda.Perioda(rovnice, rozvoj.baze, znamenko, predperioda, perioda, presnost_limit)
    periodicke_leve_kraje.dosazeni_vse()

    # export výsledků do LaTeXového souboru
    if znamenko > 0:
        nazev = "DP_kladne_{}_{}".format(predperioda, perioda)
    else:
        nazev = "DP_zap{}_{}".format(predperioda, perioda)

    soubor = "vystup/" + nazev + ".tex"
    file = latex_export.Soubor(soubor)
    #file.vypis_perioda(periodicke_leve_kraje)

    konec_vypoctu = time.time() - zacatek_vypoctu
    file.vypis_cas(konec_vypoctu)
    file.f.write("\n\n")

    file.vypis_perioda_DP(periodicke_leve_kraje)

    file.ukonceni_souboru()

    print("Cely vypocet trval {0:.2f} sekund".format(konec_vypoctu))
