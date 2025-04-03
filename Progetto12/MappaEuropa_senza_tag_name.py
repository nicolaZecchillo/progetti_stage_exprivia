#%%
import geopandas as gpd
import pandas as pd
import json
import os
#%%
def save_geojson_without_name(gdf, path):
    """Salva un GeoDataFrame in GeoJSON rimuovendo SOLO il campo 'name' dal FeatureCollection."""
    # Salvataggio temporaneo per preservare il CRS
    temp_file = "temp.geojson"
    gdf.to_file(temp_file, driver="GeoJSON")
    
    # Leggi e modifica il JSON
    with open(temp_file, 'r') as f:
        geojson_data = json.load(f)
    
    # Rimuovi il campo 'name' dal FeatureCollection
    if 'name' in geojson_data:
        del geojson_data['name']
    
    # Salva il risultato finale
    with open(path, 'w') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=4)
    
    # Elimina il file temporaneo
    os.remove(temp_file)

def transcontinental_country(country_map, european_povinces, ISO, NAME_1):
    
    country_europe = country_map[country_map["ISO"].isin(european_povinces)]
    # Combine all geometries of the European provinces into a single unified geometry polygon 
    polygons_union = country_europe.geometry.union_all()
    # Create a GeoDataFrame with the unified geometry of European provinces
    country_final = gpd.GeoDataFrame(geometry=[polygons_union])
    
    # Add ISO and NAME_1 columns to the GeoDataFrame and set the crs to EPSG:4326
    country_final["ISO"] = ISO
    country_final["NAME_1"] = NAME_1
    country_final = country_final.set_crs("EPSG:4326")
    
    # Save the GeoDataFrame to a GeoJSON file to verify the result
    save_geojson_without_name(
        country_final, 
        f"output/{NAME_1}_Europea.geojson"
    )
    
    return country_final

#%%
coordinate = gpd.read_file("input/CNTR_RG_03M_2024_4326.geojson")

stati_europei = [
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", 
    "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", 
    "Estonia", "Finland", "Germany", "Greece", "Hungary", 
    "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", 
    "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", 
    "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", 
    "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", 
    "Switzerland", "Ukraine", "United Kingdom", "Vatican City","Isle of Man"
]

coordinate_europa = coordinate[coordinate["NAME_ENGL"].isin(stati_europei)]

mappa_europa = coordinate_europa[["CNTR_ID","NAME_ENGL", "geometry"]].copy()
mappa_europa.rename(columns={"CNTR_ID": "ISO", "NAME_ENGL": "NAME_1"}, inplace=True)

# --------------------------------------------------------------------------- #
# ------------------------------ RUSSIA ------------------------------------- #
# --------------------------------------------------------------------------- #

province_russia_europea = [
    "RU-AD", "RU-ARK", "RU-AST", "RU-BEL", "RU-BRY", "RU-CE", "RU-CU",
    "RU-SPE","RU-DA", "RU-IN", "RU-IVA", "RU-KB", "RU-KGD", "RU-KL",
    "RU-KLU", "RU-KC", "RU-KR", "RU-KIR", "RU-KO", "RU-KOS", "RU-KDA",
    "RU-KRS", "RU-LEN", "RU-LIP", "RU-ME", "RU-MO", "RU-MOS", "RU-MOW",
    "RU-MUR", "RU-NEN", "RU-NIZ", "RU-SE", "RU-NGR", "RU-ORL", "RU-PNZ",
    "RU-PER", "RU-PSK", "RU-ROS", "RU-RYA", "RU-SAM", "RU-SAR", "RU-SMO", 
    "RU-STA", "RU-SVE", "RU-TAM", "RU-TA", "RU-TUL", "RU-TVE", "RU-UD",
    "RU-ULY", "RU-VLA", "RU-VGG", "RU-VLG", "RU-VOR", "RU-YAR"
]

russia_superset = gpd.read_file("input/russia_superset.geojson")

russia_final = transcontinental_country(russia_superset, province_russia_europea, "RU", "Russia")

# --------------------------------------------------------------------------- #
# ------------------------------ TURCHIA ------------------------------------ #
# --------------------------------------------------------------------------- #

province_turchia_europea = [
    "TR-34", "TR-39", "TR-22", "TR-59", "TR-17", "TR-41", "TR-77"
]

turchia_superset = gpd.read_file("input/turkey_superset.geojson")

turchia_final = transcontinental_country(turchia_superset, province_turchia_europea, "TR", "Türkiye")

# --------------------------------------------------------------------------- #
# --------------------------- AZERBAIJAN ------------------------------------ #
# --------------------------------------------------------------------------- #

province_azerbaijan_europea = [
    "AZ-QUS","AZ-XAC","AZ-QBA","AZ-SBN","AZ-SIY"
]

azerbaijan_superset = gpd.read_file("input/azerbaijan_superset.geojson")

azerbaijan_final = transcontinental_country(azerbaijan_superset, province_azerbaijan_europea, "AZ", "Azerbaijan")

# --------------------------------------------------------------------------- #
# ---------------------------- Kazakhstan ----------------------------------- #
# --------------------------------------------------------------------------- #

province_kazakhstan_europea = ["KZ-ZAP", "KZ-ATY"]

kazakhstan_superset = gpd.read_file("input/kazakhstan_superset.geojson")

kazakhstan_final = transcontinental_country(kazakhstan_superset, province_kazakhstan_europea, "KZ", "Kazakhstan")

# --------------------------------------------------------------------------- #
# ------------------------------ FRANCIA ------------------------------------ #
# --------------------------------------------------------------------------- #

province_francia_europea = [
    "FR-ARA", "FR-BFC", "FR-BRE", "FR-CVL", "FR-GES", "FR-HDF",
    "FR-IDF", "FR-NOR", "FR-NAQ", "FR-OCC", "FR-PAC", "FR-PDL","FR-COR"
]

france_superset = gpd.read_file('input/france_regions.geojson')

france_final = transcontinental_country(france_superset, province_francia_europea, "FR", "France")

#%%
mappa_europa = pd.concat([
    mappa_europa, 
    russia_final, 
    turchia_final, 
    azerbaijan_final, 
    kazakhstan_final, 
    france_final
    ], ignore_index=True)

save_geojson_without_name(mappa_europa, "output/MappaEuropa.geojson")
# %%
