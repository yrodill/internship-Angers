#!/bin/bash

: 'Required Arguments :
 $1 : file to study (original matrix with genes * exp)
 $2 : json file containing the experiences sorted by stress
 $3 : ncores to use for parallel computation
 $4 : GO file to use (please use GO_Slim.csv)
'

for stress in all biotic abiotic development chemical
    do
        for method in GENIE3 MI PC
            do
                Rscript --vanilla filter_original_data.R $1 $2 0.1 ${stress} data/filtered_$(echo $1 | cut -d/ -f2).csv
                if [ ${method} = 'GENIE3' ]
                    then
                        python run_GENIE3.py filtered_$1 $3 ${method}_$(echo $1 | cut -d_ -f2)_${stress}.csv
                    else
                        if [ ${method} = 'MI' ]
                            then
                                python run_MI_PC.py filtered_$1 MI ${method}_$(echo $1 | cut -d_ -f2)_${stress}.csv --header --njobs=$3
                            else
                                python run_MI_PC.py filtered_$1 PC ${method}_$(echo $1 | cut -d_ -f2)_${stress}.csv --header --njobs=$3
                        fi
                fi
                for hrr in HRR nothing
                    do  
                        sh full_analyze.sh ${method} $(echo $1 | cut -d_ -f2) ${stress} ${hrr} ${method}_$(echo $1 | cut -d_ -f2)_${stress}.csv $4 $3
                    done
            done
    done