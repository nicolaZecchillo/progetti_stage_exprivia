import os
import geopandas as gpd 

comuni = gpd.read_file('input/Com01012024_g/Com01012024_g_WGS84.shp')
comuni.to_csv('Progetto2/output/shp_to_csv/comuni.csv', index=False)

province = gpd.read_file('input/ProvCM01012024_g/ProvCM01012024_g_WGS84.shp')
province.to_csv('Progetto2/output/shp_to_csv/province.csv', index=False)

regioni = gpd.read_file('input/Reg01012024_g/Reg01012024_g_WGS84.shp')
regioni.to_csv('Progetto2/output/shp_to_csv/regioni.csv', index=False)

ripartizioni = gpd.read_file('input/RipGeo01012024_g/RipGeo01012024_g_WGS84.shp')
ripartizioni.to_csv('Progetto2/output/shp_to_csv/ripartizioni.csv', index=False)
