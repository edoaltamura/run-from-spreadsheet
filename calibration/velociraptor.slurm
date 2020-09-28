#!/bin/bash -l

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=28
#SBATCH --exclusive
#SBATCH -J VR_$RUN_ID
#SBATCH -o ./logs/%x.%J.vr.out
#SBATCH -e ./logs/%x.%J.vr.err
#SBATCH -p cosma7
#SBATCH -A dp004
#SBATCH -t 60:00:00

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module purge
module load intel_comp/2018
module load intel_mpi/2018
module load parmetis/4.0.3
module load parallel_hdf5/1.10.3
module load gsl/2.4
module load fftw/3.3.7
module load python/3.6.5
module load cosma/2018
module load cmake

function get_snap_index
{
  filename=$1
  tmp=${filename#*_}
  num=${tmp%.*}
  echo "$num"
}

mkdir -p "$PWD/stf"

# Make a dmo/hydro switch
if [[ $PWD == *"hydro"* ]]; then
  switch_mode="hydro"                 # If this file in "/hydro" subdirectory, use hydro VR and hydro parameter file
else
  switch_mode="dmo"                   # If this file in "/dmo" subdirectory, use dmo VR and hydro parameter file
fi

config_template="./config/vr_config_zoom_$switch_mode.cfg"

$VELOCIRAPTOR_INVOCATION

echo "Job done, info follows."
sacct -j $SLURM_JOBID --format=JobID,JobName,Partition,AveRSS,MaxRSS,AveVMSize,MaxVMSize,Elapsed,ExitCode
