from tkinter import *
import Soustava
import Perioda
import time
import latex_export

pocet_cifer = 20

root = Tk()
root.title('Program pro vytváření (\u00b1 \u03b2, \u2113)-rozvojů')
# root.resizable(width=500, height=200)
# theLabel = Label(frame1, text = "Toto je program pro vytváření (+-beta,ell)-rozvojů")
# theLabel.pack(fill=X)

# Nultý řádek
#nadpis = Label(root, text="Toto je program pro vytváření (+-beta,ell)-rozvojů")
nadpis = Label(root, text=" ")
nadpis.grid(row=0, columnspan=4)

# První řádek
rovnice = Entry(root)
rovnice.insert(10, "x**3-x**2-x-1")
rovnice.grid(row=1, column=1)
rovnice_L = Label(root, text="Rovnice: ")
rovnice_L.grid(row=1, column=0, sticky=E)

presnost_hodnota = IntVar()
presnost = Checkbutton(root, text="Přesnost výpočtu", variable=presnost_hodnota)
presnost.grid(row=1, column=2, sticky=W)


# Druhý řádek
levy = Entry(root)
levy.grid(row=2, column=1)
levy_L = Label(root, text="levý kraj \u2113: (místo \u03b2 použijte x)")
levy_L.grid(row=2, column=0, sticky=E)
levy_rozvoj = Label(root)
levy_rozvoj.grid(row=2, column=2)
levy_perioda = Label(root)
levy_perioda.grid(row=2, column=3)

# Třetí řádek
pravy = Label(root, text="Limitní rozvoj pravého kraje, tj. d*(\u2113+1)= ")
pravy.grid(row=3, column=1, sticky=E)
pravy_rozvoj = Label(root)
pravy_rozvoj.grid(row=3, column=2)
pravy_perioda = Label(root)
pravy_perioda.grid(row=3, column=3)

# Čtvrtý řádek
# tlačítko na pozici 2
znamenko_hodnota = IntVar()
znamenko = Checkbutton(root, text="Záporná báze", onvalue=-1, offvalue=1, variable=znamenko_hodnota)
znamenko.grid(row=3, column=0, sticky=W)


# Pátý řádek
def zmen_hodnota_k():
    if mink_hodnota.get():
        hodnota_k.configure(state='normal')
    else:
        hodnota_k.configure(state='disabled')


mink_hodnota = IntVar()
minmax_pocitat = Checkbutton(root, text="Spočítat mink a maxk", variable=mink_hodnota, command=zmen_hodnota_k)
minmax_pocitat.grid(row=5, column=0, sticky=W)
minmax_L = Label(root, text="Hodnota k: ")
minmax_L.grid(row=5, column=1, sticky=E)
hodnota_k = Entry(root, state='disabled')
hodnota_k.grid(row=5, column=2)


# Šestý řádek
def zmen_levy_kraj():
    if perioda_hodnota_check.get():
        levy.configure(state='disabled')
        minmax_pocitat.configure(state='disabled')
        predperioda_hodnota.configure(state='normal')
        perioda_hodnota.configure(state='normal')
        if mink_hodnota.get():
            hodnota_k.configure(state='disabled')
            # minmax_pocitat.invoke()

    else:
        levy.configure(state='normal')
        minmax_pocitat.configure(state='normal')
        predperioda_hodnota.configure(state='disabled')
        perioda_hodnota.configure(state='disabled')
        if mink_hodnota.get():
            hodnota_k.configure(state='normal')


perioda_hodnota_check = IntVar()
periodu_spocitat = Checkbutton(root, text="Nalézt periody", variable=perioda_hodnota_check, command=zmen_levy_kraj)
periodu_spocitat.grid(row=6, column=0, sticky=W)

predperioda_L = Label(root, text="Předperiodu délky: ")
predperioda_hodnota = Entry(root, state='disabled')
predperioda_L.grid(row=6, column=1, sticky=E)
predperioda_hodnota.grid(row=6, column=2)

# Sedmý řádek
perioda_L = Label(root, text="Periodu délky: ")
perioda_hodnota = Entry(root, state='disabled')
perioda_L.grid(row=7, column=1, sticky=E)
perioda_hodnota.grid(row=7, column=2)


# Osmý řádek
def zmen_vystup():
    if vystup_hodnota.get():
        vystup_nazev.configure(state='normal')
    else:
        vystup_nazev.configure(state='disabled')


vystup_hodnota = IntVar()
vystup = Checkbutton(root, text="Výstup do LaTeXu", variable=vystup_hodnota, command=zmen_vystup)
vystup.grid(row=8, column=0, sticky=W)
vystup_L = Label(root, text="Název souboru: ")
vystup_L.grid(row=8, column=1, sticky=E)
vystup_nazev = Entry(root, state='disabled')
vystup_nazev.grid(row=8, column=2)

status = Label(root)
status.grid(row=9, sticky=W)


def ziskat_vstup():

    levy_rozvoj.config(text=" ")
    levy_perioda.config(text=" ")
    pravy_rozvoj.config(text=" ")
    pravy_perioda.config(text=" ")

    start = time.time()
    fce = rovnice.get()
    zn = znamenko_hodnota.get()
    if zn == 0:
        zn = 1
    levy_kraj = levy.get()
    pocitame_presne = True
    if presnost_hodnota.get() == 0:
        pocitame_presne = False

    pocitame_periody = perioda_hodnota_check.get()
    if pocitame_periody:
        zacatek_vypoctu = time.time()
        predperioda = int(predperioda_hodnota.get())
        perioda = int(perioda_hodnota.get())
        print("Počítáme periody s před {} a periodou {}".format(predperioda, perioda))

        rozvoj = Soustava.Soustava(fce, zn, symbol_levy_kraj=None)

        periodicke_leve_kraje = Perioda.Perioda(fce, rozvoj.baze, zn, predperioda, perioda,
                                                pocitame_presne)
        periodicke_leve_kraje.dosazeni_vse()

        if vystup_hodnota.get():
            soubor = "vystup/" + vystup_nazev.get() + ".tex"
            file = latex_export.LatexExport(soubor)
            file.vypis_perioda(periodicke_leve_kraje)
            konec_vypoctu = time.time() - zacatek_vypoctu
            file.vypis_cas(konec_vypoctu)
            file.ukonceni_souboru()
        print("Vypočet dokončen.")

    else:
        zacatek_vypoctu = time.time()
        rozvoj = Soustava.Soustava(fce, zn, levy_kraj)
        rozvoj.spocitej_rozvoj_leveho_kraje(pocitame_presne, pocet_cifer)
        rozvoj.spocitej_rozvoj_praveho_kraje(pocet_cifer)
        levy_rozvoj.config(text=rozvoj.rozvoj_leveho_kraje)
        levy_perioda.config(text="s periodou {}".format(rozvoj.perioda_leveho_kraje))
        pravy_rozvoj.config(text=rozvoj.rozvoj_praveho_kraje)
        pravy_perioda.config(text="S periodou {}".format(rozvoj.perioda_praveho_kraje))

        if mink_hodnota.get():
            predperioda = int(hodnota_k.get())
            rozvoj.spocitej_mink_maxk(predperioda)

        # výstup do Latexu
        if vystup_hodnota.get():
            soubor = "vystup/" + vystup_nazev.get() + ".tex"
            file = latex_export.LatexExport(soubor)
            file.vypis_rozvoj_vse(rozvoj)
            konec_vypoctu = time.time() - zacatek_vypoctu
            file.vypis_cas(konec_vypoctu)
            file.ukonceni_souboru()

        print("Výpočet dokončen.")

    konec = time.time() - start

    status.config(text="Dopočítáno. Celé to trvalo {0:.2f} s".format(konec))


tlacitko = Button(root, text="Spočítat", command=ziskat_vstup)
# bottom1.bind("<Button-1>",vypis()
tlacitko.grid(row=4, column=2)

root.mainloop()
