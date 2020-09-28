#!/bin/bash -l

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=28
#SBATCH -J $RUN_ID
#SBATCH -o ./logs/%x.%J.swift.out
#SBATCH -e ./logs/%x.%J.swift.err
#SBATCH -p cosma7
#SBATCH -A dp004
#SBATCH --exclusive
#SBATCH -t 72:00:00

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

# Make a dmo/hydro switch
if [[ $PWD == *"hydro"* ]]; then
  # If this file in "/hydro" subdirectory, use hydro SWIFT and hydro parameter file
  $SWIFT_PATH \
  -v 1 \
  --cosmology \
  --eagle \
  --pin \
  --threads=$SLURM_CPUS_PER_TASK \
  $PARAMETER_FILE
fi

if [[ $PWD == *"dmo"* ]]; then
  # If this file in "/dmo" subdirectory, use dmo SWIFT and dmo parameter file
  $SWIFT_PATH \
  -v 1 \
  --cosmology \
  --self-gravity \
  --pin \
  --threads=$SLURM_CPUS_PER_TASK \
  $PARAMETER_FILE
fi

echo "Job done, info follows."
sacct -j $SLURM_JOBID --format=JobID,JobName,Partition,AveRSS,MaxRSS,AveVMSize,MaxVMSize,Elapsed,ExitCode