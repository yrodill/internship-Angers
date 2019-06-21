#!/bin/bash

# /!\ WARNING /!\
# Be sure not to have important files with a name starting with tmp_ as it would be deleted (else comment line 54)

#Bash file to launch the GO enrichment
#Usage : sh launch_GO_analyze.sh list_of_genes_links.csv GO_file.txt threshold_clusters_size [optional arguments]
# $1 : List of genes links to evaluate
# $2 : GO file for reference
# $3 : threshold for cluster size
# $4 : filter for the GO terms (biological process/cellular component/molecular fct°) (BP/CC/MF)
# $5 : filter for the evidence codes
# $6 : minimum value for a term to be considered (underrepresented term)
# $7 : maximum value for a term to be considered (overrepresented term)
# $8 : clustering method to use (greedy or betweeness)

#Folders check and clean
read -p "You are about to clean 4 folders (study, xls, cluster_links, EGAD_cluster_links)
Save your older results to another folder before continuing.
Continue? (Y/N): " confirm
if [ $confirm = "y" ]
  then
    for folder in xls cluster_links EGAD_cluster_links study
      do
        if [ -d ${folder} ]
        then
          rm ${folder}/*
        else
          mkdir ${folder}
        fi
      done
  else
    exit 1
fi

#Part for GOATOOLS
read -p "Are you using a specific GO file (one obtained with parse_GO.py) ? (Y/N): " sp
if [ $sp = "y" ]
  then
    Rscript --vanilla clustering.R $1 ${8:-greedy} tmp_$1
    python files_parsing.py $1 tmp_$1 $2 --threshold $3 --specific
  else
    Rscript --vanilla clustering.R $1 ${8:-greedy} tmp_$1
    python files_parsing.py $1 tmp_$1 $2 --threshold $3
fi

if [ $? -eq 0 ] #exit if the clustering failed
then
  echo "Starting GOATOOLS analysis..."
else
  exit 1
fi
for file in study/*
    do  
        python /home/bothorel/goatools/scripts/find_enrichment.py --ev_inc=$5 --pval=0.05 --ns=$4 --pval_field=fdr_bh --outfile=$PWD/xls/$(echo $file | cut -d/ -f2).xlsx --no_propagate_counts --method=fdr_bh --obo=go-basic.obo ${file} population_tmp_$1 tmp_$2
    done

#Part for EGAD on each cluster
for file2 in cluster_links/*
    do
      if [ $sp = "y" ]
        then
          python EGAD_preprocessing.py ${file2} $2 --process ${4:-all} --ev_inc ${5:-all} --min ${6:-0} --max ${7:-10000} --specific
        else
          python EGAD_preprocessing.py ${file2} $2 --process ${4:-all} --ev_inc ${5:-all} --min ${6:-0} --max ${7:-10000}
      fi
      Rscript --vanilla GO_enrichment.R tmp_adj_matrix.csv tmp_GO_matrix.csv EGAD_${file2}
      python GO_comparison.py EGAD_${file2}  
    done

#Cleaning
#rm tmp_*