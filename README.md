# Progetti_stage_Exprivia
1. Progetto1:
 - File .csv risultato del merge tra i dati scaricati alla pagina: https://demo.istat.it/app/?i=POS&l=it e file .csv ottenuto tramide modellamento dati reperibili sulla pagina Wikipedia: https://it.wikipedia.org/wiki/ISO_3166-2:IT.
 - Visualizzazione grafica su dashboard ottenuta tramite utilizzo di Apache Superset.
2. Progetto2:
 - Conversione tramite codice Python e della libreria geopandas di file .shp scaricati dalla pagina https://www.istat.it/notizia/confini-delle-unita-amministrative-a-fini-statistici-al-1-gennaio-2018-2/ in file .csv contenenti i dati e le cordinate dei confini geografici di ripartizioni, regioni, provincie e comuni italiani.
 - Creazione di una tabella dimensioni contenete le suddette divisioni e dipendenze (parent_id) e una tabella dei fatti contenente i dati facenti riferimento a gli id della tabella precedente.
 - Visualizzazione grafica su dashboard ottenuta tramite utilizzo di Apache Superset e creazione di filtro che rende la tabella dinamica.
3. Progetto3:
 - Analisi del dataset scaricabile al link https://www.kaggle.com/datasets/ahmadrafiee/airports-airlines-planes-and-routes-update-2024
 resource=download a scopo creazione di diagramma ER, definizione di chiavi primarie ed esterne, studio sul tipo di relazioni e definizione del livello di normalizzazione al fine di rendere tutto 3NF.
4. Progetto4:
 - Utilizzato e modellato le tabelle facenti riferimento i dati della popolazione per cercare di costruire un modello previsionale effettuando vari test su diverse metodologie di ML fino alla scelta finale del modello previsionale Prophet
5. Progetto5:
 - Modellato dataset https://www.istat.it/wp-content/uploads/2023/05/Tavole-Dati-Meteoclimatici-Anno-2021.xlsx, dividendolo in due file .csv contenenti rispettivamente i dati delle temperature medie e quelli delle precipitazioni, sostituendo i valori delle righe totalmente vuote con le medie anno per anno delle provincie della stessa regione, utilizzando il campo 'parent_id' della tabella dim_geografia creata nel Progetto2
 - Sostituzione valori mancanti attraverso modello di ML Random Forest
6. Progetto6:
 - Analisi del Dataset: Scuola.zip a scopo creazione di diagramma ER, definizione di chiavi primarie ed esterne, studio sul tipo di relazioni e definizione del livello di normalizzazione al fine di rendere tutto 3NF.
7. Progetto7:
 - Creazione di mappe regionali e provinciali italiane tramite utilizzo di script in bash 
8. Progetto8:
 - Conversione del file '143.Packaged hamburger bun, bread production.xlsx' in formato .csv tramite utilizzo di codice Python in modo dinamico
9. Progetto9:
 - Creazione di due container docker contenenti l'immagine di un database postgers di input ed uno di output, caricamento dei dati prensenti sul sito eurostat per esempio al link: https://ec.europa.eu/eurostat/cache/metadata/en/nama10_esms.htm sul database di input migrazione dei dati sul database di output e analisi della similarità dei dati presenti tramite tecniche di NLP 
10. Progetto10:
 - Ottenimento del link di download del file 'Confini amministrativi' più recente e del link del pdf contenente la Descrizione dei dati dal sito https://www.istat.it/notizia/confini-delle-unita-amministrative-a-fini-statistici-al-1-gennaio-2018-2/ attraverso l'utilizzo delle librerie BeautifulSoup e urlopen + tentativi di recupero informazioni tabelle in formato pd.DataFrame
11. Progetto11:
 - Esercizi in SQL tramite utilizzo di SQL Server su database NorthWind su diversi livelli di difficoltà.
12. Progetto12:
 - Creazione di una mappa Europea in formato geojson da caricare come mappa customizzata in Apache Superset partendo dai dati prenenti al link: https://ec.europa.eu/eurostat/web/gisco/geodata/administrative-units/countries
13. Progetto13: 
- Controllo della correttezza del file: cod_unita_amministrative_centroidi.csv allo scopo di verificare in Apache Superset la correttezza dei dati riguardanti i centroidi delle aree geografiche di riferimento