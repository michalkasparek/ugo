Jednoduchý skript pro vystavování faktur neplátců DPH. Z CSV tabulky s daňovou evidencí generuje faktury v PDF i základní statistiky, umí násobit nalogovaný čas hodinovkou.

Výhody: rychlý workflow. Faktura je sakumprásk hotová za 30 sekund.

Nevýhody: vše ostatní.

Jde o osobní projekt bez velkých ambicí, motivovaný poměrem ceny a kvality služeb iDokladu. Publikuji spíše pro inspiraci a jako materiál k výrobě odvozenin než jako nástroj, na který by se šlo dlouhodobě spolehnout.

Jak na to:

1. Naklonovat repozitář.
2. Nainstalovat prerekvizity: '''pandas''' a '''fpdf'''.  
2. Přejmenovat '''konfigurace-ukazka.json''' na '''konfigurace.json'''.
3. V '''konfigurace.json''' vyplnit 1/ vlastní fakturační údaje, 2/ cestu ke složce s tabulkou s evidencí, 3/složce pro export faktur, 4/ souboru s fontem (počítá s fontem o pevné šířce – monospace). Volitelně 5/ je možné změnit "historie_spolupráce" na "True" a v "důchod" vyplnit datum odchodu do důchodu (YYYY-MM-DD), na fakturách se pak objeví jednoduchá vizualizace probíhající spolupráce.
4. V první zmíněné složce vytvořit tabulku '''faktury.csv''' se sloupci "číslo", "vystavení", "splatnost", odběratel", "popis", "částka". Data musí být ve formátu YYYY-MM-DD. IČ, DIČ a adresa musejí být v uvozovkách. Do této tabulky bude přicházet obsah faktur, na každý řádek jedna faktura.
5. Tamtéž vytvořit tabulku '''klienti.csv''' se sloupci "odběratel", "název", "ič", "dič", "sídlo". Odtud se budou do faktur kopírovat fakturační údaje klientů, takže je není nutné neustále opakovat. Tabulky se párují přes sloupec "odběratel". Toto (typicky krátké) označení bude vidět i v názvu souboru s exportovanou fakturou. Pokud je "historie_spolupráce" v konfiguraci nastavená na "True", pak je zde nutné ještě vytvořit tabulku '''klienti_zacatek_spoluprace.csv''' se sloupci "odběratel" a "začátek", ve kterém bude datum začátku spolupráce s konkrétním klientem.

Ovládání:

- Příkaz '''ugo.py -p číslo''' vyexportuje do PDF konkrétní fakturu.
- Příkaz '''ugo.py -p''' vyexportuje všechny faktury s datem vystavení v posledních dvou týdnech.
- Příkaz '''ugo.py -s''' vypíše základní statistiky.
- Příkaz '''ugo.py -h hh:mm:ss sazba''' vynásobí čas naměřený v Togglu (nebo jinde) hodinovkou a vypíše výslednou částku.
- Příkaz '''ugo.py -c''' ('''ugo.py -k''') načte všechny bankovní výpisy v podsložce '''vypisy''' v účetnictví, zkontroluje chybějící variabilní symboly a vypíše (zřejmě) neuhrazené faktury po splatnosti. (Výpisy musejí být v textovém formátu, např. csv, html či txt.)

## To-do

- src/
- víc položek na jednu fakturu
- víc statistik: roky, year-to-date, velikost klientů
- podpora více měn
    - pohlídat ve statistikách
- víc vstupních tabulek: 2022.csv, 2023.csv atd.
- cross-platform kompatibilita (zatím testováno jen na Windows)
    - cesta k souborům
    - font