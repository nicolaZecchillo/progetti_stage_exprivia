# %%
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import camelot

# %% Utilizzo le librerie urlopen per aprire una pagina web e BeautifulSoup per mostrarne il codice html
url = "https://www.istat.it/notizia/confini-delle-unita-amministrative-a-fini-statistici-al-1-gennaio-2018-2/"
html_page = urlopen(url)
soup = BeautifulSoup(html_page)
print(soup.prettify())
# %% Cerco la tabella contenente i link per il download dei file con confini amministrativi per ogni anno,
# seleziono la terza riga della tabella (che conterrà i dati più recenti) e ne estraggo il link 
table = soup.find('table')
riga_confini_recenti = table.find_all('tr')[2]
link_confini = riga_confini_recenti.find('a', href=True).get('href')
print(link_confini)
# %% Dopo aver ispezionata la pagina web da browser 
# utilizzo la classe del divisore contenente il link del file che contiene il pdf con la descrizione dei dati
div_descrizione_dati = soup.find('div', class_="lista_media_link mt-3") 
link_descrizione_dati = div_descrizione_dati.find('a').get('href')
print(link_descrizione_dati)
# %%Metoso alternativo per trovare il link del file pdf con la descrizione dei dati
tutti_i_link = soup.find_all('a', href=True)
link_pdf = [a['href'] for a in tutti_i_link if a['href'].endswith('.pdf')][0]
print(link_pdf)
# %%
response = requests.get(link_pdf)
with open("document.pdf", "wb") as f:
    f.write(response.content)
tables = camelot.read_pdf("document.pdf", pages="5", flavor="stream")

for i, table in enumerate(tables):
    df = table.df
    new_columns = []
    new_columns.append(df.iloc[1, 0] + ' ' + df.iloc[3, 0])
    new_columns.extend(df.iloc[2, 1:]) 

    df.columns = new_columns

    df = df[4:].reset_index(drop=True)

    colonna0 = df.columns[0]
    df[colonna0] = df[colonna0].replace('', None).bfill()

    df[colonna0] = df[colonna0].bfill()
    df.to_csv('tabelle/prova%d.csv' % (i+1), index=False)

# %%
