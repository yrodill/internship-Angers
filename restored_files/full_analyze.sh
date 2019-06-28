#!/bin/bash

#$1 : file containing the matrix genes*genes with genes names for headers/indexes
#$2 : njobs to use for parallel computation (default = 1)
#$3 : GO file to use for the stufy of the GO terms
#$4 : cluster size threshold (default = 100)
#$5 : process to study (BP/CC/MF) (default = BP)
#$6 : evidence codes to keep (default = Experimental) - mroe infos at the end of the script
#$7 : clustering method to use (greedy/edge_betweenness)

read -p "Do you want to use HRR ranking ? (Y/N): " hrr

for seuil in 0.05 0.1 0.2 0.5
    do
        next="n"
        if [ $hrr = "y" -o $hrr = "Y" ]
            then
                python filter_links.py $1 --POBL=${seuil} --threshold=5 --njobs=${2:-1} --HRR --fill
            else
                python filter_links.py $1 --POBL=${seuil} --threshold=5 --njobs=$2 --fill
        fi
        bash launch_GO_analyze.sh tmp_$1 $3 ${4:-100} ${5:-BP} ${6:-Experimental} ${7:-greedy}
        while [ $next != "y" ]
            do 
                read -p "Save your results in a safe place (BECAUSE IM GONNA ERASE ALL TO CONTINUE). Are you done ?
                No ? What takes you so long... What about now ?? 
                Still a no ! I'll force to continue soon [...]
                Are you ready !? (Y/N)" next
            done
    done