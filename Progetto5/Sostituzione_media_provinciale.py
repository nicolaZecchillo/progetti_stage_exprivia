#%%
import geopandas as gpd
import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

# Caricamento dei dati
df_temperatura = pd.read_csv('output/temperatura_completo.csv')
df_precipitazioni = pd.read_csv('output/precipitazioni_completo.csv')
confini_province = gpd.read_file('../input/ProvCM01012024_g/ProvCM01012024_g_WGS84.shp')
confini_province = confini_province[['DEN_UTS', 'geometry']]

confini_province.loc[confini_province['DEN_UTS'] == "Verbano-Cusio-Ossola", 'DEN_UTS'] = "Verbania"
confini_province.loc[confini_province['DEN_UTS'] == "Forli'-Cesena", 'DEN_UTS'] = "Forlì"
confini_province.loc[confini_province['DEN_UTS'] == "Sud Sardegna", 'DEN_UTS'] = "Carbonia"

# Funzione per il fuzzy merge
def fuzzy_merge(df, gdf, left_on, right_on):
    merged = pd.merge(df, gdf, left_on=left_on, right_on=right_on, how='left')

    miss = merged[merged[right_on].isna()]
    if not miss.empty:
        matches = []
        for index, row in miss.iterrows():
            nome = row[left_on]

            result = process.extractOne(nome, gdf[right_on].dropna().tolist(), scorer=fuzz.token_set_ratio)

            if isinstance(result, tuple) and len(result) == 2:
                match, score = result
                matches.append(match if score > 80 else None)  
            else:
                matches.append(None)  

        merged.loc[merged[right_on].isna(), right_on] = matches

        merged = pd.merge(
            merged.drop(columns='geometry'),
            gdf,
            on=right_on,
            how='left'
        )
    return merged


df_temperatura_merged = fuzzy_merge(df_temperatura, confini_province, 'COMUNI', 'DEN_UTS')
df_precipitazioni_merged = fuzzy_merge(df_precipitazioni, confini_province, 'COMUNI', 'DEN_UTS')

# %%
df_temperatura_merged = gpd.GeoDataFrame(df_temperatura_merged, geometry=df_temperatura_merged['geometry'])
df_precipitazioni_merged = gpd.GeoDataFrame(df_precipitazioni_merged, geometry=df_precipitazioni_merged['geometry'])

def get_neighbors(geo_df, comune_geom):
    return geo_df[geo_df.geometry.touches(comune_geom)]

val_columns = [col for col in df_temperatura_merged.columns if col not in ['COMUNI', 'DEN_UTS', 'geometry']]

def fill_missing_values(gdf):
    for index, row in gdf.iterrows():
        for col in val_columns:
            if pd.isna(row[col]):  
                neighbors = get_neighbors(gdf, row.geometry)
                if not neighbors.empty:
                    gdf.at[index, col] = neighbors[col].mean()
    return gdf

df_temperatura_filled = fill_missing_values(df_temperatura_merged)
df_precipitazioni_filled = fill_missing_values(df_precipitazioni_merged)

df_temperatura_filled[val_columns] = df_temperatura_filled[val_columns].round(2)
df_precipitazioni_filled[val_columns] = df_precipitazioni_filled[val_columns].round(2)

df_temperatura_filled = df_temperatura_filled.drop(columns=['DEN_UTS', 'geometry'])
df_precipitazioni_filled = df_precipitazioni_filled.drop(columns=['DEN_UTS', 'geometry'])

df_temperatura_filled.to_csv('output/temperatura_filled.csv', index=False)
df_precipitazioni_filled.to_csv('output/precipitazioni_filled.csv', index=False)
#%%