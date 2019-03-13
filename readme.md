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
  - Maybe it's related to the data and not the algortihms.
  - Meeting skype with Thomas Duge de Bernonville de l'Université de Tours (about the paper "Ranking genome-wide correlation measurements improves microarray and RN-seq based global and targeted co-expression networks")