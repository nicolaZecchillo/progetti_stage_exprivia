#!/bin/bash

# Define the variable for the output folder
output_folder="geojson_converted"

# Input folder
input_folder="$output_folder/step1_identical_convert"

# Output folder for geojson files
output_folder_reg="$output_folder/step4_mappe_provinciali"
mkdir -p "$output_folder_reg"  # Ensure the output folder exists

# Find the first file that starts with "Reg" (to extract COD_REG -> DEN_REG mapping)
sample_file_reg=$(find "$input_folder" -name "Reg*.geojson" | head -n 1)

# Extract the mapping COD_REG -> DEN_REG from the first "Reg*.geojson" file
declare -A reg_mapping

# Mapping COD_REG -> DEN_REG, ensuring to handle spaces in DEN_REG
echo "Mapping COD_REG to DEN_REG:"

# Extract and process the mapping
while IFS= read -r line; do
    cod_reg=$(echo "$line" | awk '{print $1}')
    den_reg=$(echo "$line" | awk '{$1=""; print substr($0,2)}')  # Capture everything after the first space

    # Replace non-alphanumeric characters in DEN_REG with underscores
    sanitized_den_reg=$(echo "$den_reg" | sed 's/[^a-zA-Z0-9]/_/g')

    reg_mapping["$cod_reg"]="$sanitized_den_reg"
    echo "$cod_reg -> $sanitized_den_reg"
done < <(jq -r '.features[] | "\(.properties.COD_REG) \(.properties.DEN_REG)"' "$sample_file_reg")

# Find the first file that starts with "Prov" (to extract COD_REG -> DEN_REG mapping)
sample_file_prov=$(find "$input_folder" -name "Prov*.geojson" | head -n 1)

# Extract the mapping COD_PROV -> DEN_UTS from the first "Prov*.geojson" file
declare -A prov_mapping

# Mapping COD_PROV -> DEN_UTS, ensuring to handle spaces in DEN_UTS
echo "Mapping COD_PROV to DEN_UTS:"

# Extract and process the mapping
while IFS= read -r line; do
    cod_prov=$(echo "$line" | awk '{print $1}')
	cod_reg_prov=$(echo "$line" | awk '{print $2}')
    den_prov=$(echo "$line" | awk '{$1=$2=""; print substr($0,3)}')  # Capture everything after the first space

    # Replace non-alphanumeric characters in DEN_REG with underscores
    sanitized_den_prov=$(echo "$den_prov" | sed 's/[^a-zA-Z0-9]/_/g')

    prov_mapping["$cod_prov"]="$cod_reg_prov:$sanitized_den_prov"
    echo "$cod_prov -> $sanitized_den_prov"
done < <(jq -r '.features[] | "\(.properties.COD_PROV) \(.properties.COD_REG) \(.properties.DEN_UTS)"' "$sample_file_prov")

# Loop through each input file that starts with "Com" in the input folder
for input_file in "$input_folder"/Com*.geojson; do
    echo "Processing file: $input_file"

    # Extract the base name of the file (without path and extension)
    base_filename=$(basename "$input_file" .geojson)

    # Loop through each unique COD_REG and create the corresponding GeoJSON file
    for cod_prov in "${!prov_mapping[@]}"; do
		cod_reg="${prov_mapping[$cod_prov]%%:*}"
		den_prov="${prov_mapping[$cod_prov]#*:}"
		if [[ -n "${reg_mapping[$cod_reg]}" ]]; then
			den_reg="${reg_mapping[$cod_reg]}"
			echo "Creating GeoJSON for COD_PROV: $cod_prov with DEN_UTS: $den_prov"

			# Define the output GeoJSON file path using sanitized DEN_REG, sanitized DEN_UTS and the base file name
			output_file="$output_folder_reg/${base_filename}_${den_reg}_${den_prov}.geojson"

			# Start the GeoJSON structure (minimized output)
			echo '{"type":"FeatureCollection","name":"Com01012024_g_WGS84","crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}},"features":[' > "$output_file"

			# Extract features with the specific COD_REG and minimize the output
			jq --arg cod_prov "$cod_prov" '.features | map(select(.properties.COD_PROV == ($cod_prov | tonumber)))' "$input_file" | \
			jq -c '.[]' | while read -r feature; do
				echo "$feature," >> "$output_file"
			done

			# Remove the trailing comma and close the JSON structure
			sed -i '$ s/,$//' "$output_file"
			echo ']}' >> "$output_file"

			# Apply the additional jq transformation rule
			tmp_transformed_file="${output_file}.tmp"
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
			}' "$output_file" > "$tmp_transformed_file"

			# Replace the original file with the transformed file
			mv "$tmp_transformed_file" "$output_file"

			echo "Transformed GeoJSON for COD_PROV $cod_prov ($den_prov): $output_file"
		fi	
    done

done

echo "GeoJSON files have been created and transformed for all COD_PROV values."
