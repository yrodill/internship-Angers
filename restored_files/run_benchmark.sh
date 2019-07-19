#!/bin/bash
# 96cores at max on the cluster (it is the number of cores to use for parallel computation)

# Before using this :
# Create a folder named "data" where you'll store your expression matrices
# Then just : sh run_benchmark.sh

conda activate py35

for file in data/*
    do
	sh the_most_automated_script_ever.sh ${file} sorted_exp_by_stress.json 96 GO_slim.csv
    done
