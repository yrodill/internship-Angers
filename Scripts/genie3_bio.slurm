#!/bin/bash

#SBATCH --job-name=Genie3
#SBATCH --output=genie3.out
#SBATCH --error=genie3.err
#SBATCH --time=3-10:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=benbotho@gmail.com
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=std
#SBATCH --cpus-per-task=70
#SBATCH --nodelist=star245

source activate py35


#Rscript --vanilla test_GENIE3_biological.R ~/internship-Angers/catma5/changedNames.csv $SLURM_CPUS_PER_TASK
for i in "biotic" "abiotic" "development" "chemical treatment" "all"
do
  for j in 0 0.1 0.2 0.3 0.4 0.5
  do
    Rscript --vanilla test_GENIE3_biological.R changedNames.csv sorted_exp_by_stress.json $SLURM_CPUS_PER_TASK ${j} ${i} 0.8 filtered_data_${j}_${i}_genie3.csv NULL
    python run_GENIE3.py filtered_data_${j}_${i}_genie3.csv $SLURM_CPUS_PER_TASK wmat_${j}_${i}_.csv
  done
done