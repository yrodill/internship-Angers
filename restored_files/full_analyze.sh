#!/bin/bash

# Required Arguments :
# $1 : method used (GENIE3/MI/PC)
# $2 : data used (Ratio/ISample/IRef)
# $3 : type of stress (biotic/abiotic/chemical/development)
# $4 : HRR (HRR or anything if not used)
# $5 : file containing the matrix genes*genes with genes names for headers/indexes
# $6 : GO file to use for the study of the GO terms
# $7 : Original filtered file (for global study)
 
#  Optionnal Arguments :
# $8 : njobs to use for parallel computation (default = 1)
# $9 : cluster size threshold (default = 100)
# $10 : process to study (BP/CC/MF) (default = BP)
# $11 : evidence codes to keep (default = Experimental) (see in EGAD_preprocessing.py for more infos)
# $12 : clustering method to use (greedy/edge_betweenness)

for seuil in 5000 10000 20000
    do
        if [ $4 = 'HRR' ]
            then
                if [ $1 = 'GENIE3' ]
                    then
                        python filter_links.py $5 --POBL=${seuil} --threshold=10 --njobs=${8:-1} --HRR
                    else
                        python filter_links.py $5 --POBL=${seuil} --threshold=10 --njobs=${8:-1} --HRR --fill
                fi
            else
                if [ $1 = 'GENIE3' ]
                    then
                        python filter_links.py $5 --POBL=${seuil} --threshold=10 --njobs=${8:-1}
                    else
                        python filter_links.py $5 --POBL=${seuil} --threshold=10 --njobs=${8:-1} --fill
                fi
        fi
        bash launch_GO_analyze.sh $1 $2 $3 ${seuil} $4 tmp_$5 $6 ${9:-100} ${10:-BP} ${11:-Experimental} ${12:-greedy}
	bash launch_global_analyze.sh $1 $2 $3 ${seuil} $4 $7 tmp_$5 $6 ${9:-100} ${10:-BP} ${11:-Experimental}
    done
