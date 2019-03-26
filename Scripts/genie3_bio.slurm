#!/bin/bash

#SBATCH --job-name=Genie3_on_biological_data
#SBATCH --output=genie3.out
#SBATCH --error=genie3.err
#SBATCH --time=100:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=benbotho@gmail.com
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=intel-E5-2695
#SBATCH --cpus-per-task=24
#SBATCH --nodelist=star245

source activate py35


#Rscript --vanilla test_GENIE3_biological.R ~/internship-Angers/catma5/changedNames.csv $SLURM_CPUS_PER_TASK


Rscript --vanilla test_GENIE3_biological.R ~/internship-Angers/catma5/changedNames.csv 24 0.1


