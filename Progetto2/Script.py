#%%
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os 

#%% Lettura shape file
comuni_shp = gpd.read_file('../input/Com01012024_g/Com01012024_g_WGS84.shp')
province_shp = gpd.read_file('../input/ProvCM01012024_g/ProvCM01012024_g_WGS84.shp')
regioni_shp = gpd.read_file('../input/Reg01012024_g/Reg01012024_g_WGS84.shp')
ripartizioni_shp = gpd.read_file('../input/RipGeo01012024_g/RipGeo01012024_g_WGS84.shp')

#%% Trasfromazione in df e aggiunta cod_geografico, tipo_geografico e parent_id
ripartizioni = pd.DataFrame(ripartizioni_shp)
ripartizioni['cod_geografico'] = 'IT-' + ripartizioni['COD_RIP'].astype(str)
ripartizioni.rename(columns={'DEN_RIP': 'den_geografica'}, inplace=True)
ripartizioni['tipo_geografico'] = 'Ripartizione'
ripartizioni['parent_id'] = None
num_ripartizioni = len(ripartizioni) #variabile per incrementare il calcolo del parent_id
# %% Come per ripartizioni ma utilizzando il cile ISO_Regioni.csv per recuperare il codice ripartizione
ISO_regioni = pd.read_csv('../input/ISO_Regioni.csv')

regioni = pd.DataFrame(regioni_shp)
regioni = regioni.merge(ISO_regioni, left_on='DEN_REG', right_on='DEN_REG', how='inner')
regioni.rename(columns={'COD_RIP': 'parent_id', 'DEN_REG': 'den_geografica'}, inplace=True)
regioni['tipo_geografico'] = 'Regione'
num_regioni = len(regioni) #variabile per incrementare il calcolo del parent_id
# %% Il codice geografico qui viene ottenuto tramite aggiunta di 'IT-' alla sigla provinciale
province = pd.DataFrame(province_shp)
province['cod_geografico'] = 'IT-' + province['SIGLA']
province.rename(columns={'COD_REG': 'parent_id', 'DEN_UTS': 'den_geografica'}, inplace=True)
province['tipo_geografico'] = 'Provincia'
province['parent_id'] = province['parent_id'] + num_ripartizioni
# %% 
comuni = pd.DataFrame(comuni_shp)
comuni.rename(columns={'COD_PROV': 'parent_id', 'COMUNE': 'den_geografica', 'PRO_COM':'cod_geografico'}, inplace=True)
comuni['tipo_geografico'] = 'Comune'
comuni['parent_id'] = comuni['parent_id'] + num_regioni + num_ripartizioni
# %% Concatenazione di tutti i df con le divisioni geografice con l'aggiunra della colonna id come incrementale e filtro su colonne
dim_geografia = pd.concat([ripartizioni, regioni, province, comuni], ignore_index=True)
dim_geografia['id'] = range(1, len(dim_geografia) + 1)
dim_geografia = dim_geografia[['id','parent_id','tipo_geografico','cod_geografico','den_geografica']]
# %% Import dei dati per ogni divisione geografica
dati_ripartizioni = pd.read_csv('../input/POSAS_2024_it_Ripartizioni.csv', sep=';', header=1)
dati_regioni = pd.read_csv('../input/POSAS_2024_it_Regioni.csv', sep=';', header=1)
dati_province = pd.read_csv('../input/POSAS_2024_it_Province.csv', sep=';', header=1)
dati_comuni = pd.read_csv('../input/POSAS_2024_it_Comuni.csv', sep=';', header=1, na_values='', keep_default_na=False)

#%% Unione dei dati con la dimensione appena creata e drop delle colonne da non utilizzare
fct_residente_ripartizioni = dim_geografia.merge(dati_ripartizioni, left_on='den_geografica', right_on='Ripartizione', how='right')
fct_residente_ripartizioni = fct_residente_ripartizioni.drop(['parent_id', 'tipo_geografico', 'cod_geografico', 'den_geografica', 'Codice ripartizione', 'Ripartizione'], axis=1)
# %% Come per ripartizione ma controllando le regioni con id nullo, non corrispondenze
fct_residente_regioni = dim_geografia.merge(dati_regioni, left_on='den_geografica', right_on='Regione', how='right')
fct_residente_regioni.info()
print(fct_residente_regioni[fct_residente_regioni['id'].isnull()]['Regione'].unique())
# %% Sostituzione dei nomi delle regioni con quelli che trovano corrispondenza, ri-merge e pulizia df
dati_regioni.loc[dati_regioni['Regione'] == "Valle d'Aosta/Vallée d'Aoste", 'Regione'] = "Valle d'Aosta"
dati_regioni.loc[dati_regioni['Regione'] == "Trentino-Alto Adige/Südtirol", 'Regione'] = "Trentino-Alto Adige"
fct_residente_regioni = dim_geografia.merge(dati_regioni, left_on='den_geografica', right_on='Regione', how='right')
fct_residente_regioni = fct_residente_regioni.sort_values(by=['id','Età'])
fct_residente_regioni = fct_residente_regioni.drop(['parent_id', 'tipo_geografico', 'cod_geografico', 'den_geografica', 'Codice regione', 'Regione'], axis=1)
fct_residente_regioni.info()
# %% 
province = dim_geografia[dim_geografia['tipo_geografico'] == 'Provincia']
fct_residente_province = province.merge(dati_province, left_on='den_geografica', right_on='Provincia', how='right')
fct_residente_province.info()
print(fct_residente_province[fct_residente_province['id'].isnull()]['Provincia'].unique())
# %%
dati_province.loc[dati_province['Provincia'] == "Valle d'Aosta/Vallée d'Aoste", 'Provincia'] = "Aosta"
dati_province.loc[dati_province['Provincia'] == 'Forlì-Cesena', 'Provincia'] = "Forli'-Cesena"
dati_province.loc[dati_province['Provincia'] == 'Massa-Carrara', 'Provincia'] = 'Massa Carrara'
dati_province.loc[dati_province['Provincia'] == 'Bolzano/Bozen', 'Provincia'] = 'Bolzano'
fct_residente_province = province.merge(dati_province, left_on='den_geografica', right_on='Provincia', how='right')
fct_residente_province = fct_residente_province.drop(['parent_id', 'tipo_geografico', 'cod_geografico', 'den_geografica', 'Codice provincia', 'Provincia'], axis=1)
fct_residente_province = fct_residente_province.sort_values(by=['id','Età'])
fct_residente_province.info()
# %%
fct_residente_comuni = dim_geografia[dim_geografia['tipo_geografico'] == 'Comune'].merge(dati_comuni, left_on='den_geografica', right_on='Comune', how='right')
fct_residente_comuni.info()
print(fct_residente_comuni[fct_residente_comuni['id'].isnull()]['Comune'].unique())
# %%
dati_comuni.loc[dati_comuni['Comune'] == "Savogna d'Isonzo-Sovodnje ob Soci", 'Comune'] = "Savogna d'Isonzo-Sovodnje ob Soči"
dati_comuni.loc[dati_comuni['Comune'].isin(['Uggiate-Trevano', 'Ronago']), 'Comune'] = 'Uggiate con Ronago'
dati_comuni.loc[dati_comuni['Comune'] == 'Popoli', 'Comune'] = 'Popoli Terme'
dati_comuni.loc[dati_comuni['Comune'] == 'Montemagno', 'Comune'] = 'Montemagno Monferrato'
dati_comuni.loc[dati_comuni['Comune'] == 'Montagna sulla Strada del Vino/Montan an der Weinstraße', 'Comune'] = 'Montagna sulla strada del vino/Montan an der Weinstraße'
fct_residente_comuni = dim_geografia[dim_geografia['tipo_geografico'] == 'Comune'].merge(dati_comuni, left_on='den_geografica', right_on='Comune', how='right')
fct_residente_comuni = fct_residente_comuni.drop(['parent_id', 'tipo_geografico', 'cod_geografico', 'den_geografica', 'Codice comune', 'Comune'], axis=1)
fct_residente_province = fct_residente_province.sort_values(by=['id','Età'])
fct_residente_comuni = fct_residente_comuni.fillna(0)
fct_residente_comuni.info()
# %% Creazione della tabella dei fatti unendo i df creati
fct_residente = pd.concat([fct_residente_ripartizioni, fct_residente_regioni, fct_residente_province, fct_residente_comuni], ignore_index=True)
fct_residente = fct_residente.sort_values(by=['id','Età'])

#%% Dotenv permette di recuperare le variabili d'ambiente da un file .env, in qiesto caso quello del Progetto9 in cui viengono
# inficati i criteri di connessione al db input
load_dotenv("../.env")

INPUT_DB_HOST = os.getenv("INPUT_DB_HOST")
INPUT_DB_NAME = os.getenv("INPUT_DB_NAME")
INPUT_DB_USER = os.getenv("INPUT_DB_USER")
INPUT_DB_PASSWORD = os.getenv("INPUT_DB_PASSWORD")
INPUT_DB_PORT = int(os.getenv("INPUT_DB_PORT"))

username = INPUT_DB_USER
password = INPUT_DB_PASSWORD
host = INPUT_DB_HOST
port = INPUT_DB_PORT
database = INPUT_DB_NAME

# Il metodo create_engine stabilisce una connessione al db attraverso le variabili create
engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Si vanno a creare delle tabelle di db dei df strutturati in precedenza utilizzando il motore e con la clausola sostituisci se già esistentigit 
dim_geografia.to_sql("dim_geografia", con=engine, if_exists="replace", index=False)
fct_residente.to_sql("fct_residente", con=engine, if_exists="replace", index=False)
# %%
