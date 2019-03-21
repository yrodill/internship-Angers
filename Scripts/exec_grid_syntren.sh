#!/bin/bash

#source activate py35

for i in 1 2 3 4 5
  do
    python gridsearch_1.py /home/bothorel/internship-Angers/tests/benchmark/DREAM4/insilico_size100_${i}_multifactorial.tsv /home/bothorel/internship-Angers/tests/benchmark/DREAM4/insilico_size100_multifactorial_${i}_goldstandard.tsv "--nruns" 16 "--njobs" 3 "--tsv" "--gpus" 1 
  done

#python gridsearch_1.py syntren/100_probaComplexInter1/syntrenHop1_100_0_data.csv syntren/100_probaComplexInter1/syntrenHop1_100_0_target.csv "--nruns" 8 "--njobs" 1 "--gpus" 1 


