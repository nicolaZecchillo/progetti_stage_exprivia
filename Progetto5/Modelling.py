# %%
import pandas as pd
import numpy as np

# %%
df = pd.read_excel('Tavole-Dati-Meteoclimatici-Anno-2021.xlsx', sheet_name='Tavola_1', header=2, nrows=110)
df.head(110)

# %%
def cambia_header(df):
    df.iloc[1:, 1:] = df.iloc[1:, 1:].replace('....', np.nan).astype(float)
    header = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df.columns = header
    df = df.rename(columns={df.columns[0]: 'COMUNI'})
    
    return df
# %%
df_temperatura = df.iloc[ : , :17]
df_temperatura = cambia_header(df_temperatura)
df_temperatura.head(100)
# %%
comuni_senza_dati_temperatura = df_temperatura[df_temperatura.iloc[:, 1:].isna().all(axis=1)].index
Fermo = comuni_senza_dati_temperatura[0]
Nuoro = comuni_senza_dati_temperatura[1]
print(comuni_senza_dati_temperatura)
# %%
df_precipitazioni = df.loc[:, ['COMUNI'] + list(df.columns[18:])]
df_precipitazioni = cambia_header(df_precipitazioni)
df_precipitazioni.head(100)
# %%
Gorizia = df_precipitazioni[df_precipitazioni.iloc[:, 1:].isna().all(axis=1)].index[0]
print(Gorizia)
# %%
dim_geografia = pd.read_csv('../Progetto2/output/dim_geografia.csv')
dim_geografia.head()
# %%
dim_geografia_filtered = dim_geografia[dim_geografia['tipo_geografico'] == 'Provincia']
df_temperatura_merged = pd.merge(df_temperatura, dim_geografia_filtered, left_on='COMUNI', right_on='den_geografica', how='left')
df_precipitazioni_merged = pd.merge(df_precipitazioni, dim_geografia_filtered, left_on='COMUNI', right_on='den_geografica', how='left')
df_temperatura_merged.head()

# %%
def sostituzione_media_regionale(df, comune):
    anni = df.columns[1:17]
    
    valori_medi = df.groupby('parent_id')[anni].transform('mean').round(2)
    df.loc[comune, anni] = df.loc[comune, anni].fillna(valori_medi.loc[comune])
    
    return df

# %%
df_temperatura_merged = sostituzione_media_regionale(df_temperatura_merged, Fermo)
df_temperatura_merged = sostituzione_media_regionale(df_temperatura_merged, Nuoro)
df_precipitazioni_merged = sostituzione_media_regionale(df_precipitazioni_merged, Gorizia)
# %%
df_temperatura_merged.iloc[:,:17].to_csv('temperatura.csv', index=False)
df_precipitazioni_merged.iloc[:,:17].to_csv('precipitazioni.csv', index=False)
# %%
