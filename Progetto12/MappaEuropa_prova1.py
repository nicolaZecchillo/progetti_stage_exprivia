#%%
import geopandas as gpd
import pandas as pd
import os

#%%
coordinate = gpd.read_file("CNTR_RG_20M_2024_4326.geojson")
print(coordinate)
# %%
stati_europei = [
    "Albania", "Andorra", "Austria", "Azerbaijan", "Belarus", "Belgium", 
    "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", 
    "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary", 
    "Iceland", "Ireland", "Italy", "Kazakhstan", "Kosovo", "Latvia", "Liechtenstein", 
    "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", 
    "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", 
    "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", 
    "Switzerland", "Türkiye", "Ukraine", "United Kingdom", "Vatican City"
]


coordinate_europa = coordinate[coordinate["NAME_ENGL"].isin(stati_europei)]
russia_cntr = coordinate[coordinate["NAME_ENGL"] == "Russian Federation"]
coordinate_europa.head()
# %%

mappa_europa = coordinate_europa[["ISO3_CODE","NAME_ENGL", "geometry"]]
mappa_europa.rename(columns={"ISO3_CODE": "ISO", "NAME_ENGL": "NAME_1"}, inplace=True)
mappa_europa.head()

# %%
geojson_files = [f for f in os.listdir("Russia")]

mappe_russia = [gpd.read_file(os.path.join("Russia", file)) for file in geojson_files]

russia_europea = pd.concat(mappe_russia, ignore_index=True)

russia_union = russia_europea.geometry.unary_union

russia_final = gpd.GeoDataFrame(geometry=[russia_union])

russia_final["ISO"] = "RUS"
russia_final["NAME_1"] = "European Russia"

russia_final = russia_final[["ISO", "NAME_1", "geometry"]]
russia_final.head()
# %%
russia_final.to_file("Russia.geojson", driver="GeoJSON")
# %%
mappa_europa = pd.concat([mappa_europa, russia_final], ignore_index=True)
# %%
mappa_europa.to_file("MappaEuropa_Prova1.geojson", driver="GeoJSON")
# %%
