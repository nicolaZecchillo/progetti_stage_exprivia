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
df_temperatura.to_csv('output/temperatura.csv', index=False)
# %%

# %%
df_precipitazioni = df.loc[:, ['COMUNI'] + list(df.columns[18:])]
df_precipitazioni = cambia_header(df_precipitazioni)
df_precipitazioni.head(100)
df_precipitazioni.to_csv('output/precipitazioni.csv', index=False)
# %%
