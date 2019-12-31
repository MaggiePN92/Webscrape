from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd

yahooFin = 'https://finance.yahoo.com/quote/'
txtfil = open('symbol.txt', 'r')     #på denne filen ligger alle ticker-navnene til selskapene på 
symbol = [] #En tom liste.           S&P500 (Disse ble hentet med en mindre sofistikert webscraper)                            
bed = {} #en tom fortegnelse

for i in txtfil: #legger alle tickernavnene inn listen kalt symbol
    symbol.append(i.strip()) #vi fjerner linjehopp med .strip()

for symb in symbol: #itererer over listen med alle tickernavnene
    print('Henter for:', symb)
    bed[symb] = {} #lager en tom fortegnelse for hvert selskap
    side = yahooFin + symb #lager addressen for nettside for gitt selskap
    tick_side = req.get(side) #henter html-koden til nettsiden
    soup = bs(tick_side.content, 'html.parser') #renser html-koden med soup

    for elem in soup.find_all('td'): #itererer over alle linjer i koden som har 'td' i seg (dette vil være hvor data som f.eks.
                                     #market cap står skrevet)
        key = elem.get('data-test')  # navn på variabel
        strElem = str(elem) #gjør iterasjonene om til string slik at den kan manipulerers enklere
        start = strElem.rfind('">') + 2 #her starter verdien i html-koden
        slutt = strElem.find('</') #her slutter verdien
        verdi = strElem[start:slutt]

        if elem.get('data-test') == None or verdi == None: #legger ikke til dersom ingen verdier
            continue
        else:
            bed[symb][key] = verdi #legger til og skaper en nøstet fortegnelse

dataRamme = pd.DataFrame.from_dict(bed, orient='index') #lager en dataramme av variablene i bed fortegnelsen
dataRamme.to_excel("sp500.xlsx") #skriver datarammen ut til en xlsxfil (excel) med navn SP500
