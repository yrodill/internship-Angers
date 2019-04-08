#!/usr/bin/bash

#Usage : bash get_all_links.sh [FOLDER] [NUMBER OF LINKS MAX]

#Get all link list from an experience
#"biotic" "abiotic" "all" "development" "chemical"
for i in "all"
    do
        python process.py $1 ${i} --nLinks $2
    done