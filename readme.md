# M2 Internship Repositery

## This repositery is meant to store all the work that will be done during the 6 months internship at Angers

- **Day 1** :
  - Discovery of the CausalDiscoveryToolbox(CDT) (https://github.com/Diviyan-Kalainathan/CausalDiscoveryToolbox)
  - test_CDT.py : Test of the CDT using dataset from Syntren generator

- **Day 2** :
  - Started test of the GENIE3 package (https://bioconductor.org/packages/release/bioc/html/GENIE3.html)
  - test_GENIE3.py and test_GENIE3.R

- **Day 3** :
  - To do : Adjacency Matrix extracted from "nn100_nbgr100_hop0.3_bionoise0.1_expnoise0.1_corrnoise0.1_neighAdd_network.sif" file. (parsing + comparison with weightMat given by GENIE3) and use scikit-learn to make the precision and recall test (np.ravel(weightMat) => conversion into n² vector size)
  - Done : test_GENIE3.py plotting the precision/recall curve calculated from Syntren data
  - Reading : https://arxiv.org/pdf/1709.05321.pdf , https://arxiv.org/pdf/1202.3775.pdf
  - ~~KCI-test (independance test)~~
  
- **Day 4** :
  - Meeting at 2:00pm
  - ~~Try to implement GENIE3 test into the CDT~~ -> later
  - Reading : deeplearningbook.pdf (keep reading at page 90)
  - Adding arguments, which are the parameters of the Syntren generator used by the user, to the test_GENIE3.py
  - New dataset given by the biologists : file CoRGI_data_Catma5_intensities.tar.gz
  
- **Day 5** :
  - Keep reading the deeplearningbook.pdf
  - ~~Test Syntren data on SAM (helped by O.Goudet)~~
  - ~~Try to implement GENIE3 in the CDT => day 4 renewal~~
  - Think about the data (i.e what we could use from the json metadata file)

- **Day 6** :
  - Still reading the deeplearningbook.pdf !
  - Still trying to make the toolbox work on the computer ; stupid R dependencies!
  - All issues fixed for the computer, ready to start.

- **Day 7** :
  - Implementation of GENIE3 into the CDT
  - Started the list of abreviations from metadata.json (in case we have to use those for representations)
  - Reading : https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0012776&type=printable
  - To be implemented : find_MCE.py ; find the matrice of co-expression using biological data.
  - Thought : using CATdb to validate the results ?

- **Day 8** :
  - Tested GENIE3 : problem with the AUPR result (too low ?)
  - Checked the matrice adjacency between the 2 methods (86.25% of identity)
  - Maybe it's related to the data and not the algorithms.
  - Meeting skype with Thomas Dugé de Bernonville de l'Université de Tours (about the paper "Ranking genome-wide correlation measurements improves microarray and RN-seq based global and targeted co-expression networks")

- **Day 9** :
  - Repaired GENIE3, GENIE3 was sorting the genes by name (the modification is in the R script, reading the gene's order from file then comparing both file and genie3 output and reordering columns/rows according to the file)
  - Tested GENIE3 on 20/100 datasets : On 20 => AUPR 0.15 to 0.32. On 100 => AUPR ~0.12
  - Meeting => EGAD/H2O R packages - scripts will be sent soon / they used GO terms to build ref networks and compared their results with those networks.
  - /!\ The arguments of GENIE3 might not work properly. To check !

- **Day 10** :
  - Started a R script to filter the data from the biologists (removing lines with missing data) can be all lines or lines with more then 10% missing data
  - Testing GENIE3 on the data (might be too long)
  - Packages used by Thomas Dugé => corpcor / Parmigene knni.all
  - Ran SAM on DREAM4 dataset (only 1 at the moment ; AUPR = 0.13)

- **Day 11** :
  - Improved R script for running tests on the real data previously filtered.
  - Launched test of GENIE3 with relatively "low" parameters (K=5,nTrees=10) ~2h20 (run over 18 424 genes & 1042 exp)
  - Relaunch SAM on the 5 datasets from DREAM4 => results tomorrow
  - Reading : https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5135122/#b19-bbi-10-2016-237 , https://ac.els-cdn.com/S1476927104001082/1-s2.0-S1476927104001082-main.pdf?_tid=3774c203-5cca-46dd-93d0-23153fcf1ac6&acdnat=1552917008_260409a181b0c2af90185c5fd11e871c
  - From scikitlearn watch DBSCAN. (clustering method)