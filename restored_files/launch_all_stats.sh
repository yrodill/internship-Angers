#!/usr/bin/bash

#You must provide one argument corresponding to the algorithm used : MI or PC

for i in "IRef" "ISample" "Ratio"
    do
        python run_stats.py ${i} $1
    done