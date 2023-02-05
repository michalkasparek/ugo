#!/usr/bin/env python

"""
Skript pro vystavování faktur

__version__ = "zárodek prototypu, uwaga uwaga"
__author__ = "Michal Kašpárek"
__email__ = "michal.kasparek@gmail.com"
__license__ = "MIT"
__status__ = "Development"
"""

import sys
import os
import json
from datetime import date
from datetime import timedelta
import pandas as pd

with open("konfigurace.json", 'r', encoding='utf-8') as k:
    konfigurace = json.loads(k.read())

podnikatel = konfigurace["podnikatel"]
skript = konfigurace["skript"]
historie = bool(skript["historie_spolupráce"])

faktury = pd.DataFrame(pd.read_csv(os.path.join(skript["cesta_evidence"], "faktury.csv"), sep=","))
klienti = pd.DataFrame(pd.read_csv(os.path.join(skript["cesta_evidence"], "klienti.csv"), sep=","))
faktury = faktury.merge(klienti, on = "odběratel", how="outer")
faktury["vystavení"] = pd.to_datetime(faktury["vystavení"])
faktury["splatnost"] = pd.to_datetime(faktury["splatnost"])

if historie == True:
    zacatek_spoluprace = pd.DataFrame(pd.read_csv(os.path.join(skript["cesta_evidence"], "klienti_zacatek_spoluprace.csv"), sep=","))
    zacatek_spoluprace["začátek"] = pd.to_datetime(zacatek_spoluprace["začátek"])
    faktury = faktury.merge(zacatek_spoluprace, on = "odběratel", how="outer")
    duchod = podnikatel["důchod"]

duplikaty = faktury[faktury.duplicated(['číslo'], keep=False)]

if len(duplikaty) > 0:
    print("POZOR, jedno nebo více čísel faktur se v evidenci opakuje:")
    print(duplikaty[["číslo","vystavení","název","částka"]])
    print("***")

def hodinovka(hms, sazba):

    cas = str(hms).split(":")
    hodiny = int(cas[0])
    minuty = int(cas[1])
    sekundy = int(cas[2])
    cas = hodiny + minuty/60 + sekundy/3600

    odmena = cas * int(sazba)
    odmena = str(odmena).split(".")[0]

    cas = round(cas, 3)

    print(str(hms) + " = " + str(cas).replace(".",",") + " h = " + odmena + " korun")

def stats():
    mesice = faktury.groupby([pd.Grouper(key = 'vystavení', freq = 'M')])["částka"].sum()
    print(mesice)

def progres(zacatek, vystaveni, duchod):

    zacatek = pd.to_datetime(zacatek)
    vystaveni = pd.to_datetime(vystaveni)
    duchod = pd.to_datetime(duchod)

    rok_zacatku = zacatek.year
    rok_vystaveni = vystaveni.year
    rok_konce = duchod.year

    tmave = (rok_vystaveni - rok_zacatku) + 1
    tmave = "▓" * tmave
    svetle = rok_konce - rok_vystaveni
    svetle = "▒" * svetle

    uplynulo_ratio = (vystaveni - zacatek).days / (duchod - zacatek).days
    zbyva_ratio = (duchod - vystaveni).days / (duchod - zacatek).days   

    bar = f"Děkuji za spolupráci. Až {int(zbyva_ratio * 100)} % jí může pořád být před námi!{os.linesep}{rok_zacatku} {tmave}{svetle} {rok_konce}"

    return(bar)

def tisk(cislo):

    import fpdf

    faktura = faktury[faktury["číslo"] == cislo]

    dodavatel = podnikatel["jméno"]
    dodavatel_ic = podnikatel["ič"]
    dodavatel_sidlo = podnikatel["sídlo"]
    dodavatel_ucet = podnikatel["účet"]
    dodavatel_banka = podnikatel["banka"]
    mena = podnikatel["výchozí_měna"]

    odberatel = faktura["název"].iloc[0]
    odberatel_kratce = faktura["odběratel"].iloc[0]
    odberatel_ic = faktura["ič"].iloc[0]
    odberatel_dic = faktura["dič"].iloc[0]
    odberatel_sidlo = faktura["sídlo"].iloc[0]

    popis = faktura["popis"].iloc[0]
    castka = faktura["částka"].iloc[0]

    vystaveni = faktura["vystavení"].dt.strftime('%d. %m. %Y').iloc[0]
    splatnost = faktura["splatnost"].dt.strftime('%d. %m. %Y').iloc[0]

    cara = "=" * (len("Faktura č.") + 1 + len(str(cislo)))

    filename = str(cislo) + "_" + odberatel_kratce + ".pdf"

    if historie == True:
        podekovani = progres(faktura["začátek"].iloc[0], faktura["vystavení"].iloc[0], duchod)
    else:
        podekovani = ""

    text = f"""FAKTURA Č. {cislo}{os.linesep}{cara}{os.linesep}{os.linesep}Datum vystavení: {vystaveni}{os.linesep}{os.linesep}Dodavatel:{os.linesep}{dodavatel}{os.linesep}{dodavatel_sidlo}{os.linesep}IČ: {dodavatel_ic}{os.linesep}(Není plátce DPH.){os.linesep}{os.linesep}Odběratel:{os.linesep}{odberatel}{os.linesep}{odberatel_sidlo}{os.linesep}IČ: {odberatel_ic}{os.linesep}DIČ: {odberatel_dic}{os.linesep}{os.linesep}Dodané služby:{os.linesep}{popis} ----> {castka} {mena}{os.linesep}{os.linesep}> Celkem k úhradě: {castka} {mena}{os.linesep}> Číslo účtu: {dodavatel_ucet} ({dodavatel_banka}){os.linesep}> Variabilní symbol: {cislo}{os.linesep}> Datum splatnosti: {splatnost}{os.linesep}{os.linesep}{podekovani}"""

    print(f"Export souboru {filename}…")

    try:

        pdf = fpdf.FPDF(format='A4')
        pdf.set_margins(20, 20)
        pdf.add_page()
        pdf.add_font(skript["font"],"",skript["cesta_font"],uni=True)
        pdf.set_font(skript["font"], size=12)
        pdf.multi_cell(200, 6, txt=text, align="L")
        pdf.output(os.path.join(skript["cesta_faktury"], filename))

    except Exception as e:

        print("Chyba:")
        print(e)

if sys.argv[1] == "-h":
    hodinovka(sys.argv[2], sys.argv[3])

if sys.argv[1] == "-s":
    stats()

if sys.argv[1] == "-p":

    if len(sys.argv) == 3:
        tisk(int(sys.argv[2]))
    
    else:
        posledni = pd.to_datetime(date.today() - timedelta(days=7)) 
        posledni = faktury[faktury["vystavení"] > posledni]
        posledni = posledni["číslo"].to_list()
        for f in posledni:
            tisk(f)