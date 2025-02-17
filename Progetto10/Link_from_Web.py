# %%
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import spacy
from spacy_layout import spaCyLayout

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
# %%Metodo alternativo per trovare il link del file pdf con la descrizione dei dati
tutti_i_link = soup.find_all('a', href=True)
link_pdf = [a['href'] for a in tutti_i_link if a['href'].endswith('.pdf')][0]
print(link_pdf)
# %%
nlp = spacy.blank("it")
layout = spaCyLayout(nlp)
doc = layout(link_pdf)
# %%
'''pagina_7 = doc._.pages[6]
print(pagina_7[1])'''
# %%
tabelle = doc._.tables
for tabella in tabelle:
    dati = tabella._.data
    print(dati)
    #print(table._.data)
# %%    
for i, tabella in enumerate(tabelle):
    df = pd.DataFrame(tabella._.data)

    '''temp_col = df[df.columns[0]].copy()
    df[df.columns[0]] = df[df.columns[1]]
    df[df.columns[1]] = df[df.columns[2]]
    df[df.columns[2]] = temp_col'''

    df.to_csv('tabelle/tabella%d.csv' % (i+1), index=False)
# %%
