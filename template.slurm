#!/bin/bash -l

#SBATCH -J $RUN_ID
#SBATCH -N 1
#SBATCH -o eagle_box.%j.out
#SBATCH -e eagle_box.%j.err
#SBATCH -p cosma7
#SBATCH -A dp004
#SBATCH --exclusive

#SBATCH -t 72:00:00

$SWIFT_PATH --eagle --cosmology --threads=28 $PARAMETER_FILE