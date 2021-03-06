#!/bin/bash

# Run this script to launch the setup for the different runs in the CSV file.
# Run the script in the following order:
# - create_parameter_files.py
# - create_slurm_scripts.py
# - create_vr_slurm_scripts.py

data_directory="/cosma7/data/dp004/dc-alta2/xl-zooms/hydro"

# Set-up the submission by storing the original directory and the start time
old_directory=$(pwd)
template_directory="$old_directory/calibration"
cd $data_directory

# Make a dmo/hydro switch
if [[ $(pwd) == *"hydro"* ]]; then
  switch_mode="hydro"                 # If this file in "/hydro" subdirectory, use hydro VR and hydro parameter file
else
  switch_mode="dmo"                   # If this file in "/dmo" subdirectory, use dmo VR and hydro parameter file
fi

# Create parameter files
python3 "$old_directory"/create_parameter_files.py \
    --spreadsheet "$template_directory"/calibration_-8res.csv \
    --parameter-file "$template_directory"/swift_params_-8res.yml

cd $data_directory

python3 "$old_directory"/create_slurm_scripts.py \
    --spreadsheet "$template_directory"/calibration_-8res.csv \
    --parameter-file "$template_directory"/swift_params_-8res.yml \
    --template "$template_directory"/swift.slurm \
    --swift-path "/cosma7/data/dp004/dc-alta2/xl-zooms/$switch_mode/swiftsim/examples/swift"

#python3 "$old_directory"/create_vr_slurm_scripts.py \
#    --spreadsheet          "$template_directory"/calibration_-8res.csv \
#    --template             "$template_directory"/velociraptor.slurm \
#    --velociraptor-path    "/cosma7/data/dp004/dc-alta2/xl-zooms/$switch_mode/VELOCIraptor-STF/stf" \
#    --config               "./config/vr_config_$switch_mode.cfg" \
#    --catalogue            "snap" \
#    --output-list          "$template_directory"/output_list.txt \
#    --basename             "snap"

cd "$old_directory"
