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

- **Day 21** :
  - Tout savoir sur les puces à ADN => http://biochimej.univ-angers.fr/Page2/COURS/9ModulGenFoncVeg/5MethEtudGenFonc/3PucesADN/1PucesADN.htm
  - Script relancé, bug à cause d'une erreur debile pour la sauvegarde des résultats de GENIE3
  - Début de script pour récupérer la liste des liens entre gènes avec get_link_list de GENIE3

- **Day 22** :
  - Résultats obtenus pour tout sauf la catégorie "biotic" (relancée)
  - Scripts pour run les algos MI et PearsonCor sur les matrices des tests pour GENIE3 et DREAM4
  - GENIE3 lancé sur DREAM4
  - TO DO : Finir le script pour avoir les link_list

- **Day 23** :
  - 2 new scripts : to get the links of the GENIE3's results & one to make a SIF file from those link list
  - Tomorrow try to use cytoscape with SIF format !
  - Launched GENIE3 on IRef (will have to launch on ratio too)

- **Day 24** :
  - Started to use Cytoscape to represent the networks
  - Launched GENIE3 on the ratio file.
  - Keep looking at the results on cytoscape.
  - Compare Iref & Isample ?

- **Day 25** :
  - Compared the results : Links between Isample and Ratio are conserved (5000 links)
  - Check for 5000 all with coloration (apparently it might be a bit messy here)
  - Monday 2pm meeting

- **Day 26** :
  - Meeting at 2pm : find a way to choose the cluster from genie3 results => (WGCNA ?)
  - How many links should be used to make the cluster => distribution of the scores
  - List of genes of interest for them => should be given soon
  - Check evidence codes for GO annot : filter transcriptomic
  - Look at a possible separation between root & leaf (if enough experiences for root)
  - Look at T.Dugé GO enrichment function

- **Day 27** :
  - script to plot the scores values from GENIE3 results => ~1000links max
  - igraph : clustering methods (R script to try it)
  - Cytoscape.js could be used for the clustering / representation (http://js.cytoscape.org/#nodes.hierarchicalClustering)
  - tried to use T.Dugé script ; problems with the R libraries and the arguments to pass to the script

- **Day 28** :
  - TO DO : try to use the part with GO & AUROC from network_analysis_v2.R
  - (Arrêt maladie jusqu'au vendredi inclus)
  - other methods for enrichment : https://bioinfo-fr.net/lannotation-de-regions-genomiques-et-les-analyses-denrichissement

- **Day 29** :
  - The results from the GO enrichment gives 0.5 => meaning that the terms would be the same if due to random picking. Investigate the problem.
  - Started a script to launch MI and PC on the data in order to compare with GENIE3 results.
  - TO DO : Maybe try to use HRR later to compare scores. => https://www.nature.com/articles/s41598-018-29077-3

- **Day 30** :
  - still working on the GO enrichment
  - find a way to paralellize the computations for MI and PearsonCorr on the full matrix
  - maybe foresee using another method to calculate genes correlation (from intensity & ratio)

- **Day 31** : 
  - Maybe the clustering isn't good before the GBA run.
  - To test : Pearson & MI on datasets.

- **Day 32** : 
  - Few more scripts to sort by genes of interest.
  - Launch SAM on those data filtered by genes/exp
  - Look at Pearson results ...

- **Day 33** :
  - SAM launched on Ratio filtered by gen/exp ; results available Tuesday
  - pearson/mi not working ...

- **Day 34** :
  - Sam still running on the dataset
  - Looking at DBSCAN and HDBSCAN for clustering (maybe another method must be used, on the dataset, to get a good distance matrix)
  - Must test MI/Pearson when the CPUs are free haha.

- **Day 35** :
  - SAM results on Ratio_filtered_by_exp_by_genes : ok
  - Glay algorithm used to make the clustering of the GENIE3 results
  - Glay uses edge betweeness (Girvan-Newman algorithm)
  - One cluster with the genes of interest found. (but only a few ~20/80)
  - Bingo on the subclusters found by Glay
  - Maybe try fast greedy on list link 5000 biotic ratio (R script)

- **Day 36** :
  - Some Cytoscape representations made : comparison between clusters from fast_greedy (igraph) and GLay
  - Meeting at 10am => work on the validation via GO enrichment (and pathways ?)
  - Analyzing the workflow of the validation test precisely (to be continued)

- **Day 37** :
  - First results from SAM are promising
  - Launching SAM on 117 genes of interest + biotic & 117 + all exp
  - Read more about NV

- **Day 38** :
  - MI/Pearson script corrected
  - More results
  - Starting to launch SAM on subclusters found with GLAY

- **Day 39** :
  - Pearson on ratio/biotic launched
  - MI on Ratio all (star245)
  - Script HRR-PCC.py to be continued...

- **Day 40** :
  - PCC-HRR launched for biotic/ratio
  - The script can be enhanced
  - MI still running on star245...

- **Day 41** :
  - Memory problems with the PCC-HRR ; working around with chunks and abusing parallel
  - MI failed ; too much time, I think there is a problem with the parallelization on the cluster
  - Explications about all the internship started (pipeline + algos ...)

- **Day 42** :
  - Helped Sébastien with Cytoscape to add new links to his preexistent network
  - PCC-HRR new version with double parallelization and no memory problems
  - bit of writing on the previous doc

- **Day 43** :
  - Final version of PCC-HRR.py
  - Writing

- **Day 44** :
  - Meeting with Béatrice => one new cytoscape session sent to Sébastien
  - Writing
  - To do : launch HRR for GENIE3 results + look at the results for ISample (GENIE3,PCC,MI,HRR,SAM)

- **Day 45** :
  - trying to improve the MI/PCC script
  - cytoscape session for PCC results started

- **Day 46** :
  - MI/HRR on star245
  - cytoscape

- **Day 47** :
  - Started a python script to make both clustering and GO terms analysis

- **Day 48** :
  - Python script updated (using a bash script to launch both R and python scripts for the GO analyze)

- **Day 49** :
  - MI results for Ratio_filtered (all ratio genes/xp) => 43h30 on 72 cpus
  - discovery of GOATOOLS => pythonic way to make the GO enrichment
  - script to use GOATOOLS almost done ; few errors to debug

- **Day 50** :
  - MI results for ISample (all genes/xp) => 43h on 72cpus
  - PC results for Isample (all genes/xp) => 34min on 72cpus
  - script to make GO enrichment with GOATOOLS done

- **Day 51** :
  - searching new algorithms for Gaussian Mixtures
  - DP_GP_cluster not usable (cant process that much genes/exp)
  - KINC : https://github.com/SystemsGenetics/KINC => C++ maybe?
  - from scikit-learn ?

- **Day 52** :
  - gaussian mixtures problems ...
  - WGCNA ?

- **Day 53** :
  - Mission : Make run_GBA work for all subclusters/network
  - check MI_HRR results from Stargate
  - Done : one script to find the cluster with the most identity with a list of genes of reference

- **Day 54** :
  - HRR improved for MI results => completing the other half of the matrix (caused a bug giving empty results)
  - EGAD_preprocessing.py => file formatting to run EGAD with R
  - TO DO : options for the script (filter GO terms by "Biological Process"? / allow to choose between directed/undirected links?)
  - Make the R script for EGAD and one bash script to englobe both python and R process

- **Day 55** :
  - huge problems with the run_GBA() function

- **Day 56** :
  - run_GBA() fixed , R script done
  - improvement of the EGAD_preprocessing.py script : filters for GO !
  - to do : filter rare terms and over-representated terms

- **Day 57** :
  - all filters added
  - bash script ready
  - to complete : get all genes links from each cluster

- **Day 58** :
  - EGAD and GOATOOLS regrouped in one script + adding exception holder for empty clustering
  - to do : comparison between both results