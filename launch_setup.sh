#!/bin/bash

# Run this script to launch the setup for the different runs in the CSV file.
# Run the script in the following order:
# - create_parameter_files.py
# - create_slurm_scripts.py
# - create_vr_slurm_scripts.py

old_directory=$(pwd)

cd /cosma7/data/dp004/dc-alta2/xl-zooms/hydro || exit

# Make a dmo/hydro switch
if [[ $PWD == *"hydro"* ]]; then
  switch_mode="hydro"                 # If this file in "/hydro" subdirectory, use hydro VR and hydro parameter file
else
  switch_mode="dmo"                   # If this file in "/dmo" subdirectory, use dmo VR and hydro parameter file
fi

python3 "$old_directory"/create_parameter_files.py \
    --spreadsheet          calibration_-8res.csv \
    --parameter-file       swift_params_-8res.yml \

python3 "$old_directory"/create_slurm_scripts.py \
    --spreadsheet          calibration_-8res.csv \
    --parameter-file       swift_params_-8res.yml \
    --template             swift.slurm \
    --swift-path           /cosma7/data/dp004/dc-alta2/xl-zooms/"$switch_mode"/swiftsim/examples/swift \
#    --submit

python3 "$old_directory"/create_vr_slurm_scripts.py \
    --spreadsheet          calibration_-8res.csv \
    --template             velociraptor.slurm \
    --velociraptor-path    /cosma7/data/dp004/dc-alta2/xl-zooms/"$switch_mode"/VELOCIraptor-STF/stf \
    --config               ./config/vr_config_"$switch_mode".cfg \
    --catalogue            halo \
    --output-list          output_list.txt \
    --run-on               Snapshot \
    --basename             snap \
    --overwrite
#    --submit \

cd "$old_directory" || exit
