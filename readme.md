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
  - ~~From scikitlearn watch DBSCAN. (clustering method)~~ => using distance matrix; cannot be used with our co-expression matrix

- **Day 12** :
  - Clust didn't work on the biological data => why?
  - GENIE3 made R crash when trying to compute the getListLink() function on the biological data
  - Python script to create clusters of genes from GOSlim Annotation of AT
  - R package WGCNA (clustering method) => R script test_WGCNA to be continued
  - https://horvath.genetics.ucla.edu/html/CoexpressionNetwork/Rpackages/WGCNA/ , https://www.rdocumentation.org/packages/WGCNA/versions/1.66 , http://pklab.med.harvard.edu/scw2014/WGCNA.html
  - Connection to cluster of calc presented by O.Goudet !

- **Day 13** :
  - Tried to install R/Rstudio on the SSH (conda py35 env) => ulimit to low to launch R on the env and R version to old to install all the required packages
  - genie3_gathered_results.py => script that calculate mean and std dev for each exp (mean over 10 datasets)
  - Add a line in cdt_algs.py (123) to store the matrix used for AUPR plot
  - GENIE3 running on size100 (~1h10/file)

- **Day 14** :
  - Problem with the compilation of hrr (tried to install openmpi/mpicc)
  - 2 little scripts to normalize files downloaded to the same format as T.Dugé. (GO annot/PPI interactions)
  - Couldn't use the cluster (JM not here today)
  - Ran GENIE3 on all syntren data
  - Launching GENIE3 on the biological data

- **Day 15** :
  - Launched DREAM4 on all alg
  - GENIE3 still running on the 18 424 genes
  - Installed R 3.5 on star242 => GENIE3 should be launchable

- **Day 16** :
  - All results for DREAM4 but a few bugged (look into it)
  - All data written in the paper for GENIE3
  - Launched gSAM-lin
  - Tomorrow gSAM-mse && mse-lin

- **Day 17** :
  - GENIE3 running on star245 (with 36cores) removed all missing values
  - Launched all SAM algs on DREAM4 with star245
  - Updated GO scripts to write json data that can be further used to comparate results with known GO annotations
  - TO DO : abiotic/biotic stresses => sort by experience type
  - launch GENIE3 on data but with 10% threshold for missing values and bootstrap option + random value for NAN

- **Day 18** :
  - DONE: R script for GENIE3 on biological updated / missing values / bootstrap
  - GENIE3 re-launched on 36cores with 10% missing values.
  - SAM DREAM4 almost done (missing multi 5)

- **Day 19 & 20** :
  - All DREAM4 results for SAM done.
  - I used the python script from https://github.com/vahuynh repositery and adapted the R script that filters the data.
  - Launched the "genie3_bio.slurm" script for the weekend
  - All results are in (Stargate/GENIE3/biological_results or in catma5 directory)