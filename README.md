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
 resource=download a scopo creazione di diagramma ER, definizione di chiavi primarie ed esterne, studio sul tipo di relazioni e definizione del    livello di normalizzazione al fine di rendere tutto 3NF.
4. Progetto4 (da completare):
 - Utilizzato e modellato le tabelle facenti riferimento i dati della popolazione per cercare di costruire un modello previsionale effettuando vari test su diverse metodologie di ML
5. Progetto5 (da completare):
 - Modellato dataset https://www.istat.it/wp-content/uploads/2023/05/Tavole-Dati-Meteoclimatici-Anno-2021.xlsx, dividendolo in due file .csv contenenti rispettivamente i dati delle temperature medie e quelli delle precipitazioni, sostituendo i valori delle righe totalmente vuote con le medie anno per anno delle provincie della stessa regione, utilizzando il campo 'parent_id' della tabella dim_geografia creata nel Progetto2
 - (da implementare) Sostituzione valori mancanti attraverso modello di ML
6. Esercizi in SQL:
 - Tramite utilizzo di SQL Server su database NorthWind su diversi livelli di difficoltà.
7. Progetto8:
 - Conversione del file '143.Packaged hamburger bun, bread production.xlsx' in formato .csv tramite utilizzo di codice Python in modo dinamico
8. Progetto10:
 - Ottenimento del link di download del file 'Confini amministrativi' più recente e del link del pdf contenente la Descrizione dei dati dal sito https://www.istat.it/notizia/confini-delle-unita-amministrative-a-fini-statistici-al-1-gennaio-2018-2/ attraverso l'utilizzo delle librerie BeautifulSoup e urlopen