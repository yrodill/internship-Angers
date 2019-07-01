#!/bin/bash

# /!\ WARNING /!\
# Be sure not to have important files with a name starting with tmp_ as it would be deleted (else comment line 63)

#Bash file to launch the GO enrichment
# Required Arguments :
# $1 : method used (GENIE3/MI/PC)
# $2 : data used (Ratio/ISample/IRef)
# $3 : type of stress (biotic/abiotic/chemical/development)
# $4 : threshold for link selection
# $5 : hrr (yes/no)
# $6 : List of genes links to evaluate
# $7 : GO file for reference

# Optional Arguments :
# $8 : threshold for cluster size
# $9 : filter for the GO terms (biological process/cellular component/molecular fct°) (BP/CC/MF)
# $10 : filter for the evidence codes
# $11 : clustering method to use (greedy or betweeness)

#Folders check and clean
for folder in xls cluster_links AUROC_cluster_links study PR_cluster_links
      do
        if [ -d ${folder} ]
        then
          rm ${folder}/*
        else
          mkdir ${folder}
        fi
      done

#Part for GOATOOLS
if [ $5 = "HRR" ]
  then
    Rscript --vanilla clustering.R $6 ${6:-greedy} tmp_$6
    python files_parsing.py $1 tmp_$6 $7 --threshold ${8:-100} --specific
  else
    Rscript --vanilla clustering.R $6 ${6:-greedy} tmp_$6
    python files_parsing.py $1 tmp_$6 $7 --threshold ${8:-100}
fi

# if [ $? -eq 0 ] #exit if the clustering failed
# then
#   echo "Starting GOATOOLS analysis..."
# else
#   exit 1
# fi
for file in study/*
    do  
        python /home/bothorel/goatools/scripts/find_enrichment.py --ev_inc=${10:-Experimental} --pval=1 --ns=${9:-BP} --pval_field=fdr_bh --outfile=$PWD/xls/$(echo $file | cut -d/ -f2).xlsx --no_propagate_counts --method=fdr_bh --obo=go-basic.obo ${file} population_tmp_$6 tmp_$7
    done

#Part for EGAD on each cluster
for file2 in cluster_links/*
    do
      python EGAD_preprocessing.py ${file2} $7 --process ${$9:-BP} --ev_inc ${10:-Experimental}
      Rscript --vanilla GO_enrichment.R tmp_adj_matrix.csv tmp_GO_matrix.csv AUROC_${file2} PR_${file2}
      if [ $5 == 'HRR' ]
        then
          python GO_comparison.py AUROC_${file2} PR_${file2} $1 $2 $3 $4 --$5
        else
          python GO_comparison.py AUROC_${file2} PR_${file2} $1 $2 $3 $4
      fi
    done

#Cleaning
rm tmp_*