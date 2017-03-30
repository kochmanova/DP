import rozvoj
# zjednodušení - from rozvoj import Soustava, pak mi stačí psát Soustava

if __name__ == "__main__":
    print("Vytvářím základní soustavu")
    zlaty_rez = rozvoj.Soustava('x**3-x**2-x-1',znamenko=-1,levy_kraj='(1-x)/2')
    #zlaty_rez.nalezeni_rozvoje_leveho_kraje(20)
    #zlaty_rez.nalezeni_rozvoje_praveho_kraje(20)
    print(zlaty_rez.rozvoj_leveho_kraje.rozvoj_bodu)
    print(zlaty_rez.rozvoj_leveho_kraje.perioda)
    print(zlaty_rez.rozvoj_praveho_kraje.rozvoj_bodu)
    print(zlaty_rez.rozvoj_praveho_kraje.perioda)
    #puvodni = [-1, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, 0, -1, 1, 0, -1, 0, 0, 0, 0, 1, -1, 0, 0, 1]
    #print(puvodni==zlaty_rez.rozvoj_leveho_kraje)
    #print(zlaty_rez.perioda_leveho_kraje)
    '''print(zlaty_rez.porovnej_retezce([],[]))
    print(zlaty_rez.porovnej_retezce([1],[]))
    print(zlaty_rez.porovnej_retezce([0,0],[0,1]))
    print(zlaty_rez.porovnej_retezce([0, 1,1], [0, 1,2]))
    print(zlaty_rez.je_retezec_zleva_pripustny([]))
    print(zlaty_rez.je_retezec_zprava_pripustny([]))
    print(zlaty_rez.je_retezec_zleva_pripustny([1,0,-1,0,1,0,-1,0]))
    print(zlaty_rez.je_retezec_zprava_pripustny([1,0,-1,0,1,0,-1,0]))
    print(zlaty_rez.je_retezec_zleva_pripustny([1,0,-1,-1,-1,-1]))
    print(zlaty_rez.je_retezec_zprava_pripustny([1,0,-1,-1,-1,-1]))
    print("Zkouška")
    print(zlaty_rez.je_retezec_pripustny([]))
    print(zlaty_rez.je_retezec_pripustny([1,0,-1,0,1,0,-1,0]))
    print(zlaty_rez.je_retezec_pripustny([1,0,-1,-1,-1,-1]))'''

    print(zlaty_rez.prilep_periodu([1,0,1,0,1,1],2,9))
    print(zlaty_rez.prilep_periodu([1,0,0,1,-1],None,8))



