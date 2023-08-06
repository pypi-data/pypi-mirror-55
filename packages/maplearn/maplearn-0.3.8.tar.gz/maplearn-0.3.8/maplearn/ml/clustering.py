# -*- coding: utf-8 -*-
"""

**Clustering (unsupervised classification)**

A clustering algorithm groups the given samples, each represented as a vector x
in the N-dimensional feature space, into a set of clusters according to their
spatial distribution in the N-D space. Clustering is an unsupervised
classification as no a priori knowledge (such as samples of known classes) is
assumed to be available.

Clustering is unsupervised and does not need samples for fitting. The output
will be a matrix with integer values.

Example:
    >>> from maplearn.datahandler.loader import Loader
    >>> from maplearn.datahandler.packdata import PackData
    >>> loader = Loader('iris')
    >>> data = PackData(X=loader.X, Y=loader.Y, data=loader.aData)
    >>> lst_algos = ['mkmeans', 'birch']
    >>> dir_out = os.path.join('maplean_path', 'tmp')
    >>> cls = Clustering(data=data, dirOut=dir_out, algorithm='mkmeans')
    >>> cls.run()
"""

from __future__ import print_function

import numpy as np
import pandas as pd


from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import kneighbors_graph

from maplearn.ml.machine import Machine
from maplearn.ml.algos_clustering import ALGOS
from maplearn import logger


class Clustering(Machine):
    '''
    Apply one or several methods of clustering onto a dataset

    Args:
        * data (PackData): dataset to play with
        * algorithm (str or list): name of algorithm(s) to use
        * **kwargs: more parameters about clustering. The 'metric' to use, the
          number of clusters expected ('n_clusters')
    
    '''

    def __init__(self, data=None, algorithm=None, **kwargs):
        if 'metric' in kwargs:
            Machine._params['metric'] = kwargs['metric']
        else:
            Machine._params['metric'] = 'euclidean'
        # n_clusters = nombre de clusters attendus
        if 'n_clusters' in kwargs:
            Machine._params['n_clusters'] = kwargs['n_clusters']
            self.n_cluster = {'f': kwargs['n_clusters']}
        else:
            self.n_cluster = {'f': 15}
        logger.info('%i clusters wanted', self.n_cluster['f'])
        self.__connectivity = None
        self.__data = None

        # LISTE DES ALGOS EN STOCK
        Machine.ALL_ALGOS = ALGOS
        Machine.__init__(self, data, algorithm=algorithm, **kwargs)
        self.algorithm = algorithm

    def __compute_connectivity(self):
        logger.debug('Computing connectivity...')
        if self.__connectivity is None:
            __nn_graph = kneighbors_graph(self.__data, n_neighbors=10,
                                          n_jobs=-1, include_self=False)
            self.__connectivity = __nn_graph.astype('float16')
        if 'ward' in self.algorithm:
            self._algorithm['ward'].set_params(connectivity=self.__connectivity)
        logger.info('Connectivity computed')

    def _check(self):
        """
        Check parameters
        """
        Machine._check(self)
        # number of clusters (n_clusters)
        if not isinstance(self.n_cluster['f'], int):
            str_msg = 'n_clusters is supposed to be an integer value. \
                       Got "%s"' % str(self.n_cluster['f'])
            logger.critical(str_msg)
            raise TypeError(str_msg)

        if self.n_cluster['f'] < 2:
            str_msg = 'n_clusters is supposed to be >= 2. Got "%i"' \
                       % self.n_cluster['f']
            logger.critical(str_msg)
            raise ValueError(str_msg)

    def load(self, data):
        """
        Loads necessary data for clustering: no samples are needed.

        Arg:
            * data (PackData): data to play with
        """
        Machine.load(self, data)
        
        if self._data.data is None:
            self._data.data = self._data.X
        
        _scaler = StandardScaler()
        _scaler.fit(self._data.data)

        # distance matrix        
        self._data.data = _scaler.transform(self._data.data)
        if self._data.X is None:
            self._data.X = self._data.data
        else:
            self._data.X = _scaler.transform(self._data.X)
        
        # connectivity (needed by some algorithm(s))
        if 'ward' in self.algorithm:
            self.__compute_connectivity()
        return 0

    def fit_1(self, algo, verbose=True):
        """
        Fits one clustering algorithm

        Arg:
            * algo (str): name of the algorithm to fit
        """
        Machine.fit_1(self, algo)
        __msg = '\n####%s - Entrainement clustering####' % algo

        try:
            self.algo.fit(self._data.X)
        except Exception as ex:
            logger.error(ex)
        else:
            self._fitted = True
            logger.info('Algorithm %s fitted', algo)

        if hasattr(self.algo, 'score'):
            __msg += '\n * Score : %.2f' % self.algo.score(self._data.X)

        if hasattr(self.algo, 'labels_'):
            result = self.algo.labels_.astype(np.int8)
            try:
                score = metrics.silhouette_score(self._data.X, result,
                                                 metric=Machine._params['metric'])
            except MemoryError:
                logger.error('Not enough memory to compute score for %s', algo)
            else:
                __msg += '\n * Silhouette Score : %.2f' % score

        if verbose:
            print(__msg)

    def predict_1(self, algo, export=False, verbose=True):
        """
        Makes clustering prediction using one algorithme

        Args:
            * algo (str): name of the algorithm to use
            * export (bool): should the result be exported?
        """
        Machine.predict_1(self, algo)
        logger.info('Going to predict with %s algorithm', algo)
        #if hasattr(self.algo, 'labels_'):
        #    result = self.algo.labels_.astype(np.int8)
        if hasattr(self.algo, 'predict'):
            result = self.algo.predict(self._data.data).astype(np.int8)
        else:
            result = self.algo.fit_predict(self._data.data).astype(np.int8)
        n_clusters = np.unique(result).size
        __msg = '\n%i Clusters expected - Got %i clusters\n' \
                % (self.n_cluster['f'], n_clusters)
        logger.info('Predictions done with %s algorithm', algo)
        
        score = metrics.calinski_harabaz_score(self._data.data, result)
        __msg += '\n * Calinski and Harabaz score : %.2f' % score
        logger.info('Score computed with %s algorithm', algo)
        
        # Table of results (created or new results are appended)
        if self.result is None:
            self.result = pd.DataFrame(data=result, columns=[algo, ],
                                       dtype=np.int8)
        else:
            self.result[algo] = result
        if verbose:
            print(__msg)