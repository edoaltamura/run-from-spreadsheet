#!/bin/bash -l

#SBATCH -J VR_$RUN_ID
#SBATCH -N 1
#SBATCH -o velociraptor.%j.out
#SBATCH -e velociraptor.%j.err
#SBATCH -p cosma7
#SBATCH -A dp004
#SBATCH --exclusive

#SBATCH -t 2:00:00

export OMP_NUM_THREADS=28

$VELOCIRAPTOR_INVOCATION

