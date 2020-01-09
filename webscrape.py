from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd

yahooFinance = 'https://finance.yahoo.com/quote/'
ticker = [] #I denne listen må tickernavn ligge, f.eks. AAPL, MSFT, osv..

def yahooScrape(bedriftListe):
    
    bedInfo = {} #En tom fortegnelse. Her skal bedriftsinformasjon ligge.
    
    for bedrift in bedriftListe: #itererer over listen.
        print('Henter for:',bedrift)
        
        bedInfo[bedrift] = {} #hver bedrift blir lagt til fortegnelsen med en tom fortegnelse (nøstet fortegnelse).
        
        side = yahooFinance+bedrift #her henter vi nettsiden fra Yahoo Finance.
        bedriftSide = req.get(side)
        soup = bs(bedriftSide.content, 'html.parser')
    
        for element in soup.find_all('td'): #itererer over HTML-koden til ønskede bedrifter.
    
            kolonneNavn = element.get('data-test') #Dette blir kolonnenavn i excelfilen vår.
            strElem = str(element) #Finner verdien til riktig kolonne for riktig bedrift.
            start = strElem.rfind('">')+2
            slutt = strElem.find('</')
            verdi = strElem[start:slutt]
    
            if kolonneNavn == None:continue #hvis kolonnenavn er None -> neste.
            else: bedInfo[bedrift][kolonneNavn]=verdi #legger til verdi i nøstet fortegnelse.


    dataRamme = pd.DataFrame.from_dict(bedInfo, orient='index') #lager dataframe av den nestede fortegnelsen.
    dataRamme.to_excel("aksjeInfo.xlsx") #skriver dataframe til excelfil.

yahooScrape(ticker)
