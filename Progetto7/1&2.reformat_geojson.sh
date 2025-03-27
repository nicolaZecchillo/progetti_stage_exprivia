#!/bin/bash

# Definire la variabile per la cartella di output
output_folder="geojson_converted"

# Creazione delle cartelle di output: geojson_converted, tmp e csv se non esistono
mkdir -p "$output_folder/step2_geojson_converted"
mkdir -p "$output_folder/step1_identical_convert"
# mkdir -p "$output_folder/csv"

# Funzione per convertire shapefile in GeoJSON e trasformarlo
converti_geojson() {
    local input_file=$1
    local tmp_file=$2
    local prefix=$3
    local output_ok_file="$output_folder/step2_geojson_converted/$(basename "$tmp_file")"
    # local output_csv_file="$output_folder/csv/$(basename "${tmp_file%.geojson}.csv")"

    echo "Inizio conversione: $input_file a $tmp_file"

    # Usa ogr2ogr per convertire il file shapefile in GeoJSON con trasformazione a EPSG:4326
    ogr2ogr -f "GeoJSON" -t_srs EPSG:4326 "$tmp_file" "$input_file"

    echo "Conversione completata: $input_file a $tmp_file"

    # Usa jq per trasformare e minimizzare il GeoJSON in base al prefisso del file
    echo "Inizio trasformazione e minimizzazione del file GeoJSON: $tmp_file"
    
    if [[ "$prefix" == "Com" ]]; then
        # Regola per i file che iniziano con 'Com' (Comuni)
        jq -c '{
            type: .type,
            crs: .crs,
            features: [.features[] | {
                type: .type,
                properties: {
                    ISO: .properties.PRO_COM,
                    NAME_1: .properties.COMUNE
                },
                geometry: {
                    type: .geometry.type,
                    coordinates: .geometry.coordinates
                }
            }]
        }' "$tmp_file" > "$output_ok_file"

    elif [[ "$prefix" == "Pro" ]]; then
        # Regola per i file che iniziano con 'Pro' (Province)
        jq -c '{
            type: .type,
            crs: .crs,
            features: [.features[] | {
                type: .type,
                properties: {
                    ISO: ("IT-" + (.properties.SIGLA | tostring)),
                    NAME_1: .properties.DEN_UTS
                },
                geometry: {
                    type: .geometry.type,
                    coordinates: .geometry.coordinates
                }
            }]
        }' "$tmp_file" > "$output_ok_file"

    elif [[ "$prefix" == "Reg" ]]; then
        # Regola per i file che iniziano con 'Reg' (Regioni)
        jq -c '{
            type: .type,
            crs: .crs,
            features: [.features[] | {
                type: .type,
                properties: {
                    ISO: (
                        { # Mappatura manuale presa da https://it.wikipedia.org/wiki/ISO_3166-2:IT
                            "1": "IT-21", 
                            "2": "IT-23", 
                            "3": "IT-25", 
                            "4": "IT-32", 
                            "5": "IT-34", 
                            "6": "IT-36", 
                            "7": "IT-42", 
                            "8": "IT-45", 
                            "9": "IT-52", 
                            "10": "IT-55", 
                            "11": "IT-57", 
                            "12": "IT-62", 
                            "13": "IT-65", 
                            "14": "IT-67", 
                            "15": "IT-72", 
                            "16": "IT-75", 
                            "17": "IT-77", 
                            "18": "IT-78", 
                            "19": "IT-82", 
                            "20": "IT-88"
                        }[(.properties.COD_REG | tostring)] // "IT-Unknown"
                    ),
                    NAME_1: .properties.DEN_REG
                },
                geometry: {
                    type: .geometry.type,
                    coordinates: .geometry.coordinates
                }
            }]
        }' "$tmp_file" > "$output_ok_file"

    elif [[ "$prefix" == "Rip" ]]; then
        # Regola per i file che iniziano con 'Rip' (RIPartizioni)
        jq -c '{
            type: .type,
            crs: .crs,
            features: [.features[] | {
                type: .type,
                properties: {
                    ISO: ("IT-" + (.properties.COD_RIP | tostring)),
                    NAME_1: .properties.DEN_RIP
                },
                geometry: {
                    type: .geometry.type,
                    coordinates: .geometry.coordinates
                }
            }]
        }' "$tmp_file" > "$output_ok_file"

    else
        echo "Formato di file sconosciuto: $input_file"
    fi

    echo "Trasformazione e minimizzazione completata: $tmp_file"

    # Converte il GeoJSON finale in CSV usando ogr2ogr
    # echo "Inizio conversione in CSV: $output_ok_file a $output_csv_file"
    # ogr2ogr -f "CSV" "$output_csv_file" "$output_ok_file" -lco GEOMETRY=AS_WKT
    # echo "Conversione in CSV completata: $output_csv_file"
}

# Trova tutti i file .shp nelle sottocartelle e convertili in GeoJSON
find . -type f -name "*.shp" | while read shp_file; do
    # Estrai il prefisso dal nome del file (prima parte del nome, ad esempio Com, Pro, Reg, Rip)
    filename=$(basename "$shp_file")
    prefix=$(echo "$filename" | cut -c1-3)  # Estrai i primi 3 caratteri del nome del file

    # Creazione del nome del file temporaneo di output GeoJSON
    tmp_file="$output_folder/step1_identical_convert/$(basename "${shp_file%.shp}.geojson")"
    
    # Converti e trasforma il file
    converti_geojson "$shp_file" "$tmp_file" "$prefix"
done
