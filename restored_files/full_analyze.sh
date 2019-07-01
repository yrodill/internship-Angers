#!/bin/bash

# Required Arguments :
# $1 : method used (GENIE3/MI/PC)
# $2 : data used (Ratio/ISample/IRef)
# $3 : type of stress (biotic/abiotic/chemical/development)
# $4 : HRR (HRR or anything if not used)
# $5 : file containing the matrix genes*genes with genes names for headers/indexes
# $6 : GO file to use for the stufy of the GO terms
 
#  Optionnal Arguments :
# $7 : njobs to use for parallel computation (default = 1)
# $8 : cluster size threshold (default = 100)
# $9 : process to study (BP/CC/MF) (default = BP)
# $10 : evidence codes to keep (default = Experimental) - mroe infos at the end of the script
# $11 : clustering method to use (greedy/edge_betweenness)

for seuil in 0.05 0.1 0.2 0.5
    do
        if [ $4 == 'HRR' ]
            then
                if [ $1 == 'GENIE3' ]
                    then
                        python filter_links.py $5 --POBL=${seuil} --threshold=5 --njobs=${7:-1} --HRR
                    else
                        python filter_links.py $5 --POBL=${seuil} --threshold=5 --njobs=${7:-1} --HRR --fill
                fi
            else
                if [ $1 == 'GENIE3' ]
                    then
                        python filter_links.py $5 --POBL=${seuil} --threshold=5 --njobs=${7:-1}
                    else
                        python filter_links.py $5 --POBL=${seuil} --threshold=5 --njobs=${7:-1} --fill
                fi
        fi
        bash launch_GO_analyze.sh $1 $2 $3 ${seuil} $4 tmp_$5 $6 ${8:-100} ${9:-BP} ${10:-Experimental} ${11:-greedy}
    done