# %%
from bs4 import BeautifulSoup
from urllib.request import urlopen

# %% Utilizzo le librerie urlopen per aprire una pagina web e BeautifulSoup per mostrarne il codice html
url = "https://www.istat.it/notizia/confini-delle-unita-amministrative-a-fini-statistici-al-1-gennaio-2018-2/"
html_page = urlopen(url)
soup = BeautifulSoup(html_page)
print(soup.prettify())
# %% Cerco la tabella contenente i link per il download dei file con confini amministrativi per ogni anno,
# seleziono la terza riga della tabella (che conterrà i dati più recenti) e ne estraggo il link 
table = soup.find('table')
riga_confini_recenti = table.find_all('tr')[2]
link_confini = riga_confini_recenti.find('a').get('href')
print(link_confini)
# %% Dopo aver ispezionata la pagina web da browser 
# utilizzo la classe del divisore contenente il link del file che contiene il pdf con la descrizione dei dati
div_descrizione_dati = soup.find('div', class_="lista_media_link mt-3") 
link_descrizione_dati = div_descrizione_dati.find('a').get('href')
print(link_descrizione_dati)
# %%
