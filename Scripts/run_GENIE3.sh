#!/bin/bash

#Run GENIE3 on the biological data

srun -n1 -N25 /home/bothorel/catma5/changedNames.csv -threads $SLURM_CPUS_PER_TASK &