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

module purge
module load intel_comp/2018
module load intel_mpi/2018
module load parmetis/4.0.3
module load parallel_hdf5/1.10.3
module load gsl/2.4
module load fftw/3.3.7
module load cosma/2018
module load cmake

$SWIFT_PATH \
    -v 1 \
    --cosmology \
    --eagle \
    --pin \
    --threads=$SLURM_CPUS_PER_TASK \
    $PARAMETER_FILE

echo "Job done, info follows."
sacct -j $SLURM_JOBID --format=JobID,JobName,Partition,AveRSS,MaxRSS,AveVMSize,MaxVMSize,Elapsed,ExitCode