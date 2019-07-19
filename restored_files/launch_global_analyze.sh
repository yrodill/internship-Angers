#!/bin/bash

: 'multiline comment:
/!\ WARNING /!\
# Be sure not to have important files with a name starting with tmp_ as it would be deleted (else comment line 70)

#Bash file to launch the GO enrichment
# Required Arguments :
# $1 : method used (GENIE3/MI/PC)
# $2 : data used (Ratio/ISample/IRef)
# $3 : type of stress (biotic/abiotic/chemical/development)
# $4 : threshold for link selection
# $5 : hrr (yes/no)
# $6 : original file
# $7 : List of genes links to evaluate
# $8 : GO file for reference

# Optional Arguments :
# $9 : threshold for cluster size
# $10 : filter for the GO terms (biological process/cellular component/molecular fct°) (BP/CC/MF)
# $11 : filter for the evidence codes
'

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
python files_parsing_global.py $6 $7 $8 --threshold ${9:-100} --specific

if [ $5 = 'HRR' ]
    then
	python ./goatools/scripts/find_enrichment.py --ev_inc=${11:-Experimental} --pval=1 --ns=${10:-BP} --pval_field=fdr_bh --outfile=$PWD/xls/result_$1_$2_$3_$4_$5.xlsx --no_propagate_counts --method=fdr_bh --obo=go-basic.obo study_$7 population_$6 tmp_$8
    else
	python ./goatools/scripts/find_enrichment.py --ev_inc=${11:-Experimental} --pval=1 --ns=${10:-BP} --pval_field=fdr_bh --outfile=$PWD/xls/result_$1_$2_$3_$4.xlsx --no_propagate_counts --method=fdr_bh --obo=go-basic.obo study_$7 population_$6 tmp_$8
fi

python EGAD_preprocessing.py $7 $8 --process ${10:-BP} --ev_inc ${11:-Experimental} --specific
Rscript --vanilla GO_enrichment.R tmp_adj_matrix.csv tmp_GO_matrix.csv AUROC_$6 PR_$6
if [ $5 = 'HRR' ]
    then
        python GO_comparison_global.py AUROC_$6 PR_$6 ./xls/result_$1_$2_$3_$4_$5.xlsx $1 $2 $3 $4 tmp_adj_matrix.csv --$5
    else
        python GO_comparison_global.py AUROC_$6 PR_$6 ./xls/result_$1_$2_$3_$4.xlsx $1 $2 $3 $4 tmp_adj_matrix.csv
    fi

#Cleaning
rm tmp_*
