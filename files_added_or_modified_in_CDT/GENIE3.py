"""GENIE3 algorithm.

Imported from the Pcalg package.
Author: Diviyan Kalainathan

.. MIT License
..
.. Copyright (c) 2018 Diviyan Kalainathan
..
.. Permission is hereby granted, free of charge, to any person obtaining a copy
.. of this software and associated documentation files (the "Software"), to deal
.. in the Software without restriction, including without limitation the rights
.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
.. copies of the Software, and to permit persons to whom the Software is
.. furnished to do so, subject to the following conditions:
..
.. The above copyright notice and this permission notice shall be included in all
.. copies or substantial portions of the Software.
..
.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
.. SOFTWARE.
"""
import os
import uuid
import warnings
import networkx as nx
from shutil import rmtree
from .model import GraphModel
from pandas import read_csv
from ...utils.Settings import SETTINGS
from ...utils.R import RPackages, launch_R_script


def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning


class GENIE3(GraphModel):
    r"""GENIE3 algorithm.

    Args:
        exprMatrix (df): Expression matrix (genes x samples). Every row is a gene, every column is a sample.
        regulators (vector): Subset of genes used as candidate regulators.
        targets (vector): Subset of genes to which potential regulators will be calculated.
        treeMethod (str): Tree-based method used. 
        K (str or int): Number of candidate regulators randomly selected at each tree node (for the determination of the best split)..
        nTrees (int): Number of trees in an ensemble for each target gene. Default: 1000.
        nb_jobs(int): Number of jobs to run in parallel.
        verbose (bool): Sets the verbosity of the output.

    Available Tree-based methods:
       + Random Forest': 'RF'
       + Extra-trees' : 'ET'

    Available K values:
       + square root' : 'sqrt'
       + All : 'all'
       + number : X > 0

    Default Parameters:
       + FILE: '/tmp/cdt_GENIE3/data.csv'
       + REGULATORS : 'NULL'
       + TARGETS : 'NULL'
       + TREEMETHOD : 'RF'
       + K : 'sqrt'
       + NTREES : str(1000)
       + NJOBS: str(SETTINGS.NB_JOBS)
       + VERBOSE: 'FALSE'
       + OUTPUT: '/tmp/cdt_GENIE3/result.csv'

    .. note::
       Ref:
       J. Peters, J. Mooij, D. Janzing, B. Schölkopf:
       Causal Discovery with Continuous Additive Noise Models,
       JMLR 15:2009-2053, 2014.

    .. warning::
       This implementation of GENIE3 does not support starting with a graph.
       The adaptation will be made at a later date.
    """

    def __init__(self,regulators='NULL',targets='NULL', treeMethod='RF', K='sqrt', nTrees=1000,
                 nb_jobs=None, verbose=None):
        """Init the model and its available arguments."""
        if not RPackages.GENIE3:
            raise ImportError("R Package GENIE3 is not available.")

        super(GENIE3, self).__init__()
        self.arguments = {'{FOLDER}': '/tmp/cdt_GENIE3/',
                          '{FILE}': 'data.csv',
                          '{REGULATORS}': 'NULL',
                          '{TARGETS}': 'NULL',
                          '{TREEMETHOD}': 'RF',
                          '{K}': 'sqrt',
                          '{NTREES}': str(1000),
                          '{NJOBS}': str(SETTINGS.NB_JOBS),
                          '{VERBOSE}': 'FALSE',
                          '{OUTPUT}': 'result.csv'}
        self.regulators = regulators
        self.targets = targets
        self.treeMethod = treeMethod
        self.K = K
        self.nTrees = nTrees
        self.nb_jobs = SETTINGS.get_default(nb_jobs=nb_jobs)
        self.verbose = SETTINGS.get_default(verbose=verbose)

    def orient_undirected_graph(self, data, graph, score='obs',
                                verbose=False, **kwargs):
        """Run GENIE3 on an undirected graph."""
        # Building setup w/ arguments.
        raise ValueError("GENIE3 cannot (yet) be ran with a skeleton/directed graph.")

    def orient_directed_graph(self, data, graph, *args, **kwargs):
        """Run GENIE3 on a directed_graph."""
        raise ValueError("GENIE3 cannot (yet) be ran with a skeleton/directed graph.")

    def create_graph_from_data(self, data, **kwargs):
        """Apply causal discovery on observational data using GENIE3.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Solution given by the GENIE3 algorithm.
        """
        # Building setup w/ arguments.
        self.arguments['{REGULATORS}'] = str(self.regulators).upper()
        self.arguments['{TARGETS}'] = str(self.targets).upper()
        self.arguments['{TREEMETHOD}'] = str(self.treeMethod).upper()
        self.arguments['{K}'] = str(self.K)
        self.arguments['{NTREES}'] = str(self.nTrees)
        self.arguments['{NJOBS}'] = str(self.nb_jobs)
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        results = self._run_GENIE3(data, verbose=self.verbose)

        return nx.relabel_nodes(nx.DiGraph(results),
                                {idx: i for idx, i in enumerate(data.columns)})

    def _run_GENIE3(self, data, fixedGaps=None, verbose=True):
        """Setting up and running GENIE3 with all arguments."""
        # Run GENIE3
        id = str(uuid.uuid4())
        os.makedirs('/tmp/cdt_GENIE3' + id + '/')
        self.arguments['{FOLDER}'] = '/tmp/cdt_GENIE3' + id + '/'

        def retrieve_result():
            print (self.arguments)
            input('PAUSE')
            return read_csv('/tmp/cdt_GENIE3' + id + '/result.csv', delimiter=',').values

        try:
            data.to_csv('/tmp/cdt_GENIE3' + id + '/data.csv', header=False, index=False)
            GENIE3_result = launch_R_script("{}/R_templates/GENIE3.R".format(os.path.dirname(os.path.realpath(__file__))),
                                         self.arguments, output_function=retrieve_result, verbose=verbose)
        # Cleanup
        except Exception as e:
            rmtree('/tmp/cdt_GENIE3' + id + '')
            raise e
        except KeyboardInterrupt:
            rmtree('/tmp/cdt_GENIE3' + id + '/')
            raise KeyboardInterrupt
        rmtree('/tmp/cdt_GENIE3' + id + '')
        return GENIE3_result
