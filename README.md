# **Election Scraper**
## Třetí projekt pro Engeto Online Python Akademii

### **Popis projektu**
Tento skript slouží k extrakci výsledků parlamentních voleb z roku 2017 pro vybraný územní celek. Skript stahuje data z oficiálního webu volby.cz a ukládá je do CSV souboru pro další analýzu. Program prochází všechny obce v daném územním celku a pro každou obec získává:

- Kód obce
- Název obce
- Počet voličů v seznamu
- Počet vydaných obálek
- Počet platných hlasů
- Počty hlasů pro jednotlivé politické strany

### **Instalace knihoven**
Pro běh programu je nutné mít nainstalované knihovny uvedené v souboru `requirements.txt`. Knihovny nainstalujete pomocí příkazu:

pip install -r requirements.txt
Seznam použitých knihoven je uveden v souboru `requirements.txt`.

### **Spuštění souboru**
Program se spouští z příkazové řádky a vyžaduje dva povinné argumenty:

python projekt_3.py <odkaz_uzemniho_celku> <vystupni_soubor>
kde:
- `<odkaz_uzemniho_celku>` je URL adresa s výsledky voleb pro vybraný územní celek (okres)
- `<vystupni_soubor>` je název výstupního CSV souboru

Pokud nejsou zadány oba argumenty nebo nejsou správné, program upozorní uživatele a ukončí se.

### **Ukázka projektu**
Příklad použití pro okres Louny:
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4204" "vysledky_louny.csv"



STAHUJI DATA Z VYBRANÉHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4204
Nalezeno 70 obcí
STAHUJI DATA Z URL: https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=565997&xvyber=4204
Zpracovávám 1/70: Bitozeves
STAHUJI DATA Z URL: https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=566004&xvyber=4204
Zpracovávám 2/70: Blatno
STAHUJI DATA Z URL: https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=566012&xvyber=4204
Zpracovávám 3/70: Blažim
...
UKLÁDÁM DO SOUBORU: vysledky_louny.csv
UKONČUJI: election_scraper.py


### **Ukázka výstupu**
code;location;registered;envelopes;valid;Občanská demokratická strana;Řád národa - Vlastenecká unie;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Česká str.sociálně demokrat.;STAROSTOVÉ A NEZÁVISLÍ;Komunistická str.Čech a Moravy;Strana zelených;ROZUMNÍ-stop migraci,diktát.EU;Strana svobodných občanů;Blok proti islam.-Obran.domova;Občanská demokratická aliance;Česká pirátská strana;Referendum o Evropské unii;TOP 09;ANO 2011;Dobrá volba 2016;SPR-Republ.str.Čsl. M.Sládka;Křesť.demokr.unie-Čs.str.lid.;Česká strana národně sociální;REALISTÉ;SPORTOVCI;Dělnic.str.sociální spravedl.;Svob.a př.dem.-T.Okamura (SPD);Strana Práv Občanů
565997;Bitozeves;343;167;165;10;0;0;8;3;25;3;0;0;0;0;14;0;2;74;1;0;4;0;0;0;1;19;1
566004;Blatno;455;254;252;14;0;0;15;7;64;2;4;4;1;0;13;0;6;75;0;0;6;0;0;0;6;33;2
566012;Blažim;192;99;99;15;0;0;10;3;8;2;4;6;0;0;6;0;9;20;0;0;0;0;0;0;0;14;2
566021;Blšany;797;450;449;28;0;0;40;7;46;3;4;3;1;0;35;0;6;224;0;1;4;2;0;1;1;41;2
542547;Blšany u Loun;251;155;155;19;0;0;10;5;16;1;1;4;1;0;8;0;14;54;0;1;0;0;1;0;0;19;1



### **Závěr**
Tento projekt ukazuje základní schopnosti práce se scraperskými nástroji v Pythonu, včetně stahování dat z webu, jejich zpracování a ukládání do strukturovaného formátu (CSV). V budoucnu by bylo možné tento scraper upravit pro další volební obvody nebo jiné webové stránky s volebními výsledky.
