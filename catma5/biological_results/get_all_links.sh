#!/usr/bin/bash

#Usage : bash get_all_links.sh [FOLDER]

#Get all link list from an experience

for i in "biotic" "abiotic" "all" "development" "chemical"
    do
        python process.py $1 ${i} --nLinks 2500
    done