#!/bin/bash

python EGAD_preprocessing.py $1 $2 --process ${3:-all} --ev_inc ${4:-all} --min ${5:-2} --max ${6:-301}
Rscript --vanilla GO_enrichment.R tmp_adj_matrix.csv tmp_GO_matrix.csv EGAD_$1
rm tmp_adj_matrix.csv tmp_GO_matrix.csv
python GO_comparison.py EGAD_$1 $2