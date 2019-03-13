#!/bin/bash

# python grid_search.py 'test/G5_v1_numdata.tab' 'test/G5_v1_target.tab' --skeleton 'test/G5_v1_target.tab' --tsv --nruns 16 --njobs 4 --gpus 2 for folder in `find $1 -maxdepth 1 -type d`


# python cdt_algs.py expfinal/linear/20 $1 --adjmatrix --header --nv
#python cdt_algs.py syntren/100_probaComplexInter1 $1 --header --nv
python cdt_algs.py genie3_syntren $1 --header --nv

