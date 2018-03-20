
from tkinter import *
import limitni
import rozvoj
import periody
import time
import latex_export
root = Tk()
#root.resizable(width=500, height=200)
# theLabel = Label(frame1, text = "Toto je program pro vytváření (+-beta,ell)-rozvojů")
# theLabel.pack(fill=X)

# Nultý řádek
nadpis=Label(root, text = "Toto je program pro vytváření (+-beta,ell)-rozvojů")
nadpis.grid(row=0, columnspan=4)

# První řádek
rovnice = Entry(root)
rovnice.insert(10,"x**3-x**2-x-1")
rovnice.grid(row=1,column=1)
rovnice_L = Label(root, text = "Rovnice: ")
rovnice_L.grid(row=1, column=0, sticky=E)




# Druhý řádek
levy = Entry(root)
levy.grid(row=2,column=1)
levy_L=Label(root, text="levý kraj: (místo bety použijte x)")
levy_L.grid(row=2,column=0, sticky=E)
levy_rozvoj=Label(root)
levy_rozvoj.grid(row=2, column=2)
levy_perioda=Label(root)
levy_perioda.grid(row=2, column=3)

# Třetí řádek
pravy = Label(root, text="Limitní rozvoj pravého kraje: ")
pravy.grid(row=3, column=0, sticky=E)
pravy_rozvoj=Label(root)
pravy_rozvoj.grid(row=3, column=2)
pravy_perioda=Label(root)
pravy_perioda.grid(row=3, column=3)

# Čtvrtý řádek
# tlačítko na pozici 2
znamenko_hodnota=IntVar()
znamenko = Checkbutton(root, text = "Záporná báze", onvalue=-1, offvalue=1, variable=znamenko_hodnota)
znamenko.grid(row=4, column=0, sticky=W)

#Pátý řádek
def zmen_hodnota_k():
    if mink_hodnota.get():
        hodnota_k.configure(state='normal')
    else:
        hodnota_k.configure(state='disabled')


mink_hodnota=IntVar()
minmax_pocitat = Checkbutton(root, text="Spočítat mink a maxk", variable=mink_hodnota, command = zmen_hodnota_k)
minmax_pocitat.grid(row=5, column=0, sticky=W)
minmax_L=Label(root, text="Hodnota k: ")
minmax_L.grid(row=5, column=1, sticky=E)
hodnota_k= Entry(root, state='disabled')
hodnota_k.grid(row=5, column=2)

#Šestý řádek
def zmen_levy_kraj():
    if perioda_hodnota_check.get():
        levy.configure(state='disabled')
        minmax_pocitat.configure(state='disabled')
        predperioda_hodnota.configure(state='normal')
        perioda_hodnota.configure(state='normal')
        if mink_hodnota.get():
            hodnota_k.configure(state='disabled')
            #minmax_pocitat.invoke()

    else:
        levy.configure(state='normal')
        minmax_pocitat.configure(state='normal')
        predperioda_hodnota.configure(state='disabled')
        perioda_hodnota.configure(state='disabled')
        if mink_hodnota.get():
            hodnota_k.configure(state='normal')

perioda_hodnota_check=IntVar()
periodu_spocitat = Checkbutton(root, text="Nalézt periody", variable=perioda_hodnota_check, command=zmen_levy_kraj)
periodu_spocitat.grid(row=6, column=0, sticky=W)

predperioda_L=Label(root, text="Předperiodu délky: ")
predperioda_hodnota = Entry(root, state='disabled')
predperioda_L.grid(row=6, column=1, sticky=E)
predperioda_hodnota.grid(row=6, column=2)



#Sedmý řádek
perioda_L=Label(root, text="Periodu délky: ")
perioda_hodnota = Entry(root, state='disabled')
perioda_L.grid(row=7, column=1, sticky=E)
perioda_hodnota.grid(row=7, column=2)


# Osmý řádek
def zmen_vystup():
    if vystup_hodnota.get():
        vystup_nazev.configure(state='normal')
    else:
        vystup_nazev.configure(state='disabled')


vystup_hodnota=IntVar()
vystup = Checkbutton(root, text = "Výstup do LaTeXu", variable=vystup_hodnota, command = zmen_vystup)
vystup.grid(row=8, column=0, sticky=W)
vystup_L= Label(root, text="Název souboru: ")
vystup_L.grid(row=8, column=1, sticky=E)
vystup_nazev= Entry(root, state='disabled')
vystup_nazev.grid(row=8,column=2)






status = Label(root)
status.grid(row=9, sticky=W)

def ziskat_vstup():
    # TOHLE nefunguje, ten status Počítám
    #status.config(text="Počítám...")
    start=time.time()
    #print(rovnice.get())
    fce=rovnice.get()
    zn=znamenko_hodnota.get()
    if zn==0:
        zn=1
    levy_kraj = levy.get()

    pocitame_periody = perioda_hodnota_check.get()
    if pocitame_periody:
        k=int(predperioda_hodnota.get())
        p=int(perioda_hodnota.get())
        print("Počítáme periody s před {} a periodou {}".format(k,p))
        rozvoj_period=periody.Rozvoj_periodicky(fce, zn)
        kp=periody.Perioda(k,p,zn)
        kp.cely_vyraz()
        kp.vycisleny_vyraz(rozvoj_period.beta)
        kp.dosazeni_vse(fce)
        # TODO výpis do Latexu

    else:
        pocitame=rozvoj.Soustava(fce,zn,levy_kraj)
        levy_rozvoj.config(text=pocitame.rozvoj_leveho_kraje.rozvoj_bodu)
        levy_perioda.config(text="s periodou {}".format(pocitame.rozvoj_leveho_kraje.perioda))
        limita = limitni.Limitni_rozvoj(pocitame.beta,pocitame.levy_kraj,zn,8)
        limita.limitni_rozvoj()
        pravy_rozvoj.config(text=limita.rozvoj_bodu)
        pravy_perioda.config(text="S periodou {}".format(limita.perioda))

        # výstup do Latexu
        if vystup_hodnota.get():
            soubor = "/home/mysska/Plocha/DP/vystup/" + vystup_nazev.get() + ".tex"
            file = latex_export.Soubor(soubor)
            file.vypis_rovnice(fce, zn)
            file.vypis_baze(pocitame.beta, levy_kraj, pocitame.levy_kraj)
            file.vypis_levy_kraj(pocitame.rozvoj_leveho_kraje.rozvoj_bodu, pocitame.rozvoj_leveho_kraje.perioda)
            file.vypis_pravy_kraj(limita.rozvoj_bodu, limita.perioda)
            #file.ukonceni_souboru()

        if mink_hodnota.get():
            k = int(hodnota_k.get()) + 1
            pocitame.vytvoreni_mink_maxk(k)
            print(pocitame.mink)
            print(pocitame.maxk)
            pocitame.spocteni_vzdalenosti(k)

            if vystup_hodnota.get():
                file.vypis_minmax(pocitame.mink, pocitame.maxk, pocitame.delta)

        if vystup_hodnota.get():
            file.ukonceni_souboru()

    konec=time.time()-start




    status.config(text="Dopočítáno. Celé to trvalo {0:.2f} s".format(konec))


tlacitko = Button(root, text="Spočítat", command=ziskat_vstup)
#bottom1.bind("<Button-1>",vypis()
tlacitko.grid(row=4,column=2)





root.mainloop()