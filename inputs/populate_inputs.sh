
python3 populate_inputs.py split-reference \
  --regions-file "split_reference_panel_genetic_map_inputs.tsv" \
  --seed 3242342 \
  --output split_reference_inputs.json \
  --docker "us-central1-docker.pkg.dev/neale-pumas-bge/glimpse2/glimpse2:odelaneau_bd93ade"

python3 populate_inputs.py split-reference \
  --regions-file "split_reference_panel_genetic_map_inputs.tsv" \
  --region "chr22" \
  --seed 3242342 \
  --output split_reference_inputs_chr22.json \
  --docker "us-central1-docker.pkg.dev/neale-pumas-bge/glimpse2/glimpse2:odelaneau_bd93ade"
