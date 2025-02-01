#%%
import pandas as pd

# %% Carico il file e utilizzo una lambda per rimuovere gli spazzi
file_name = '143.Packaged hamburger bun, bread production'
file_path = '143.Packaged hamburger bun, bread production.xlsx'
df_iniziale = pd.read_excel(file_path, header=None)
df_iniziale = df_iniziale.applymap(lambda x: x.strip() if isinstance(x, str) else x)
print(df_iniziale)

# %% Creazione della funzione slicer che divide il df orizzontalmente 
# se cambiato il parametro 'orizontal' anche verticalmente fino alla prima colonna totalmente nulla
def slicer(df, start, end, orizontal=False):
    sliced_df = df.iloc[start:end]
    if orizontal is True:
        sliced_df = sliced_df.dropna(axis=1, how='all')
    return sliced_df

#%% Applico la funzione precedente su indici calcolati alla prima riga con colonna 0 valorizzata 
# fino alla riga con colonna 0 con valore 'Inputs and outputs' resettando gli indici dopo lo slicing
start_file = df_iniziale[df_iniziale[0].notna()].index[0]
input_and_outputs = (df_iniziale[df_iniziale[0] == 'Inputs and outputs'].index[0])
df_key_value = slicer(df_iniziale, start_file, input_and_outputs, orizontal=True).reset_index(drop=True)
df_key_value.columns = ['Key', 'Value']
df_key_value.head(65)

# %%Trovo le gerarchie
hierarchy = df_key_value.loc[df_key_value['Value'].isna(), 'Key']
print(hierarchy)

# %%Filtro le gerarchie scritte in maiuscolo
gerarchie1 = hierarchy[hierarchy.str.isupper()]
index_ger1 = hierarchy[hierarchy.str.isupper()].index
print(gerarchie1)

# %%Creo la funzione gerarchizzazione che divide il df per gerarchie,
#  aggiunge la gerarchia in una nuova colonna e riassembla il tutto
def gerarchizzazione (df, indici_gerarchia, nome_gerarchia, gerarchie):
    df_separati = []

    for i in range(len(indici_gerarchia)): 
        if i < len(indici_gerarchia) - 1:
            df_div = slicer(df, indici_gerarchia[i] +1, indici_gerarchia[i+1])
        else:
            df_div = slicer(df, indici_gerarchia[i] +1, len(df) + 1)

        df_div[nome_gerarchia] = gerarchie.iloc[i]
        df_separati.append(df_div)

    df_gerchizzato = pd.concat(df_separati, ignore_index=True)
    return df_gerchizzato 

#%%
df_ger1 = gerarchizzazione(df_key_value, index_ger1, 'ger1', gerarchie1)
df_ger1.head(70)       
# %%
gerarchie2 = df_ger1.loc[df_ger1['Value'].isna(), 'Key']
index_ger2 = gerarchie2.index
print(gerarchie2)
# %%
df_ger2 = gerarchizzazione(df_ger1, index_ger2, 'ger2', gerarchie2)
df_ger2 = df_ger2
df_ger2.head(70)

# %% Nella funzione creo una colonna temporanea in cui inserisco la frequenza cumulata dei valori duplicati,
# questa colonna verrà utilizzata nei suffissi e possiede un parametro per indicare da quale valore iniziare a contare
# se conta_da = 0 il primo duplicato non avrà suffisso (occorrenza 1), da secondo in poi avranno suffisso '_n'
# in questo modo se un camp è presente due volte il primo sarà droppato e il secondo non avrà suffisso

def rinomina_dupplicati(df, colonna, conta_da):
    duplicati = df[colonna].duplicated(keep=False)
    df['occorrenze'] = df.groupby(colonna).cumcount()
    
    if conta_da == 0:
        clausola = (df['occorrenze'] == 0) & duplicati
        df.loc[clausola, colonna] = df.loc[clausola, colonna] + '_0'
    
        clausola = (df['occorrenze'] >= 2) & duplicati
        df.loc[clausola, colonna] = df.loc[clausola, colonna] + '_' + df.loc[clausola, 'occorrenze'].astype(str)
        df = df.drop(df[df[0].str.contains('_0')].index)
    else:
        df['occorrenze'] += conta_da
        df.loc[duplicati, colonna] = df.loc[duplicati, colonna] + '_' + df.loc[duplicati, 'occorrenze'].astype(str)
    
    df = df.drop(columns='occorrenze')
    
    return df

#%%
df_ger2 = rinomina_dupplicati(df_ger2, colonna='Key', conta_da=1)
df_ger2.head(70)

#%% Ri-ordino il df e salvo in csv dopo aver sostituito tutti i ritorni a capo con uno spazio
df_finale = df_ger2[['Key', 'Value', 'ger2', 'ger1']]
df_finale = df_finale.replace({r'\n': ' ', r'\r': ' '}, regex=True)
df_finale.to_csv(file_name + '_metadata.csv', index=False, sep='|')
df_finale.head(60) 

#%% Uso la funzione slicer sul df_iniziale al fine di ottenere la seconda parte del file
df_tabellare = slicer(df_iniziale, input_and_outputs+1, len(df_iniziale)).reset_index(drop=True)
df_tabellare.head(60)

#%% Creo una funzione che cambia l'header del df con la prima riga e resetta gli indici
def cambia_header(df):
    header = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df.columns = header

    return df

#%% Applico la funzione slicer su indici inzio df_tabellare fino alla prima riga con colonna 1 nulla 
# e applico la funzione cambia_header
input_flows = df_tabellare[df_tabellare[0] == 'INPUT FLOWS'].index[0]
df_input_and_outputs = slicer(df_tabellare, 0, input_flows, orizontal=True)
df_input_and_outputs = cambia_header(df_input_and_outputs)
df_input_and_outputs.to_csv(file_name + '_input_output.csv', index=False, sep='|')
df_input_and_outputs.head()
# %% Applico la funzione slicer
output_flows = df_tabellare[df_tabellare[0] == 'OUTPUT FLOWS'].index[0]
df_input_flows = slicer(df_tabellare, input_flows+1, output_flows, orizontal=True)

#%% Creo una funzione che riempie le righe della colonna 0 con il valore non nullo precedente
# utilizzo la funzione rinomina_dupplicati spiegata a riga 65 e rimuovo le colonne con suffisso '_0'
# cambio l'header e rinomino le colonne 2 e 3
def tabelle_input_output(df):
    df[0] = df[0].fillna(method='ffill')
    df = rinomina_dupplicati(df, colonna=0, conta_da=0)
    df = cambia_header(df)
    df.columns.values[2:4] = ['Amount', 'Unit']

    return df

#%%
df_input_flows = tabelle_input_output(df_input_flows)
df_input_flows.to_csv(file_name + '_input_flows.csv', index=False, sep='|')
df_input_flows.head()

# %%
df_output_flows = slicer(df_tabellare, output_flows+1, len(df_tabellare), orizontal=True).reset_index(drop=True)
df_output_flows = tabelle_input_output(df_output_flows)
df_output_flows.to_csv(file_name + '_output_flows.csv', index=False, sep='|')
df_output_flows.head()

