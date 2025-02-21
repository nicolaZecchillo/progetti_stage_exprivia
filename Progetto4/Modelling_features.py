#%%
import pandas as pd

#%%
anni = ['2020', '2021', '2022', '2023', '2024']
dataframes = [pd.read_csv(f'input/Popolazione_residente_{anno}.csv') for anno in anni]

df_trasformati = []

for df, anno in zip(dataframes, anni):
    df = df[['Età', 'Totale maschi', 'Totale femmine']].copy()
    df['Anno'] = anno

    df_melted = df.melt(
        id_vars=['Età', 'Anno'], 
        value_vars=['Totale maschi', 'Totale femmine'], 
        var_name='Sesso', 
        value_name='Totale'
    )

    df_melted['Sesso'] = df_melted['Sesso'].replace({
        'Totale maschi': 'Maschi', 
        'Totale femmine': 'Femmine'
    })

    df_trasformati.append(df_melted)

df_2020_2024 = pd.concat(df_trasformati, ignore_index=True)

df_2020_2024.head()

# %%
df_2002_2019 = pd.read_csv('input/Ricostruzione della popolazione 2002-2019.csv')
df_melted = df_2002_2019.melt(
        id_vars=['Età', 'Sesso'], 
        value_vars=df_2002_2019.columns[2:], 
        var_name='Anno', 
        value_name='Totale')
df_2002_2019 =  df_melted[df_melted['Sesso'] != 'Totale']
df_2002_2019
# %%
df_2002_2024 = pd.concat([df_2002_2019, df_2020_2024], ignore_index=True)
df_2002_2024 = df_2002_2024[~df_2002_2024['Età'].isin(['Totale', '100 e oltre'])]
df_2002_2024 = df_2002_2024.sort_values(by=['Anno', 'Età']).reset_index(drop=True)
df_2002_2024

# %%
df_2002_2024['Età'] = df_2002_2024['Età'].astype(int)
df_2002_2024['Anno'] = df_2002_2024['Anno'].astype(int)
df_2002_2024.info()
# %%
df_2002_2024.to_csv('outputModelling/Popolazione_residente_2002-2024_features.csv', index=False)
# %%
df_2002_2023 = df_2002_2024[df_2002_2024['Anno'] < 2024]
df_2002_2023.to_csv('outputModelling/Popolazione_residente_2002-2023_features.csv', index=False)
# %%
df_2015_2024 = df_2002_2024[df_2002_2024['Anno'] > 2014]
df_2015_2024.to_csv('outputModelling/Popolazione_residente_2015-2024_features.csv', index=False)
# %%
