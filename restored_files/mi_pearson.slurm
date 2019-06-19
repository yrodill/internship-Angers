#!/bin/bash

#SBATCH --job-name=stats
#SBATCH --output=stats.out
#SBATCH --error=stats.err
#SBATCH --time=05:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=benbotho@gmail.com
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=std
#SBATCH --cpus-per-task=70
#SBATCH --nodelist=star245

source activate py35

python test_parallel.py IRef_filtered.csv PC $SLURM_CPUS_PER_TASK 
