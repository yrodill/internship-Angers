#!/bin/bash
# gridsearch.slurm
#SBATCH --job-name=SAM-lin
#SBATCH --output=sam-lin.out
#SBATCH --error=hello.err
#SBATCH --mail-type=end
#SBATCH --mail-user=benbotho@gmail.com
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=intel-E5-2695

source activate py35

for i in 1 2 3 4 5 
  do
    python gridsearch_1.py /home/ua24906/internship-Angers/tests/benchmark/DREAM4/insilico_size100_${i}_multifactorial.tsv /home/ua24906/internship-Angers/tests/benchmark/DREAM4/insilico_size100_multifactorial_${i}_goldstandard.tsv "--nruns" 16 "--njobs" 16 "--tsv" "--gpus" 1 
    python gridsearch_3.py /home/ua24906/internship-Angers/tests/benchmark/DREAM4/insilico_size100_${i}_multifactorial.tsv /home/ua24906/internship-Angers/tests/benchmark/DREAM4/insilico_size100_multifactorial_${i}_goldstandard.tsv "--nruns" 16 "--njobs" 16 "--tsv" "--gpus" 1 
    python gridsearch_4.py /home/ua24906/internship-Angers/tests/benchmark/DREAM4/insilico_size100_${i}_multifactorial.tsv /home/ua24906/internship-Angers/tests/benchmark/DREAM4/insilico_size100_multifactorial_${i}_goldstandard.tsv "--nruns" 16 "--njobs" 16 "--tsv" "--gpus" 1 
    python gridsearch_5.py /home/ua24906/internship-Angers/tests/benchmark/DREAM4/insilico_size100_${i}_multifactorial.tsv /home/ua24906/internship-Angers/tests/benchmark/DREAM4/insilico_size100_multifactorial_${i}_goldstandard.tsv "--nruns" 16 "--njobs" 16 "--tsv" "--gpus" 1 
  done



