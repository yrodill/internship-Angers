# M2 Internship Repositery

## This repositery is meant to store all the work that will be done during the 6 months internship at Angers

- Day 1 :
  - Discovery of the CausalDiscoveryToolbox(CDT) (https://github.com/Diviyan-Kalainathan/CausalDiscoveryToolbox)
  - test_CDT.py : Test of the CDT using dataset from Syntren generator

- Day 2 :
  - Started test of the GENIE3 package (https://bioconductor.org/packages/release/bioc/html/GENIE3.html)
  - test_GENIE3.py and test_GENIE3.R

- Day 3 :
  - To do : Adjacency Matrix extracted from "nn100_nbgr100_hop0.3_bionoise0.1_expnoise0.1_corrnoise0.1_neighAdd_network.sif" file. (parsing + comparison with weightMat given by GENIE3) and use scikit-learn to make the precision and recall test (np.ravel(weightMat) => conversion into n² vector size)
  - Done : test_GENIE3.py plotting the precision/recall curve calculated from Syntren data
  - Reading : https://arxiv.org/pdf/1709.05321.pdf , https://arxiv.org/pdf/1202.3775.pdf
  - KCI-test (independance test)
  
- Day 4 :
  - Meeting at 2:30pm
  - Try to implement GENIE3 test into the CDT
  - Adding arguments, which are the parameters of the Syntren generator used by the user, to the test_GENIE3.py