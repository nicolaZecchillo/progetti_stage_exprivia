import os
import geopandas as gpd 

comuni = gpd.read_file('Progetto2/input/Limiti01012024_g/Com01012024_g/Com01012024_g_WGS84.shp')
comuni.to_csv('Progetto2/output/comuni.csv', index=False)

provincie = gpd.read_file('Progetto2/input/Limiti01012024_g/ProvCM01012024_g/ProvCM01012024_g_WGS84.shp')
provincie.to_csv('Progetto2/output/provincie.csv', index=False)

regioni = gpd.read_file('Progetto2/input/Limiti01012024_g/Reg01012024_g/Reg01012024_g_WGS84.shp')
regioni.to_csv('Progetto2/output/regioni.csv', index=False)

ripartizioni = gpd.read_file('Progetto2/input/Limiti01012024_g/RipGeo01012024_g/RipGeo01012024_g_WGS84.shp')
ripartizioni.to_csv('Progetto2/output/ripartizioni.csv', index=False)
