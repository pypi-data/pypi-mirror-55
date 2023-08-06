# -*- coding: utf-8 -*-
"""
Unitary tests about clustering

Created on Wed Aug 17 22:19:48 2016
@author: thomas_a
"""
import os
import unittest
import random

import numpy as np
from sklearn import datasets
from timeit import default_timer as timer
import time

from test import DIR_DATA, DIR_TMP, empty_folder
from maplearn.datahandler.loader import Loader
from maplearn.datahandler.packdata import PackData
from maplearn.filehandler.imagegeo import ImageGeo
from maplearn.ml.clustering import Clustering
from maplearn.filehandler.shapefile import Shapefile

SLOW_TEST_THRESHOLD = 0.5

class TestClustering(unittest.TestCase):
    """
    Unittary tests about the Clustering class
    Cluster data => predict labels without samples
    """

    def setUp(self):
        loader = Loader('iris')
        #WARNING: IRIS is fully konwn (ie data = samples ; X & data share same
        # number of features & indiviuals)
        empty_folder(DIR_TMP)
        self.__n_clusters = random.randint(3, 10)
        self.__data = PackData(X=loader.X[:, :2], Y=loader.Y,
                               data=loader.X[:, :2])
        self.__algos = ['mkmeans', 'birch']
        self.__algo = random.choice(self.__algos)
        self.__cls = Clustering(data=self.__data, algorithm=self.__algos,
                                n_clusters=self.__n_clusters, dirOut=DIR_TMP)
        self._started_at = time.time()

    def test_unknown_algo(self):
        """
        Try to use an unknown algorithm -> KeyError
        """
        self.assertRaises(KeyError, Clustering, self.__data, 'inexistant')

    def test_unknown_algos(self):
        """
        Try to use several algorithms. Some are available but some others are
        unknown -> KeyError
        """
        self.assertRaises(KeyError, Clustering, self.__data,
                          [self.__algo, 'inexistant', 'nimporte'])

    def test_wrong_nclusters(self):
        """
        n_clusters parameter is expected to be an integer >= 2. Set this
        parameter with something else than an interger should raise a
        TypeError. n_clusters <= 2 should raise a ValueError
        """
        self.assertRaises(TypeError, Clustering, self.__data, self.__algos,
                          n_clusters='string')
        self.assertRaises(ValueError, Clustering, self.__data, self.__algos,
                          n_clusters=1)


    def test_fit(self):
        """
        Training a clustering algorithm -> should not raise an exception +
        attribute _fitted = True
        """
        self.__cls.fit_1(self.__algo)
        self.assertTrue(self.__cls._fitted)

    def test_predict(self):
        """
        Cluster data using one algorihm -> should not raise exception
        """
        self.__cls.fit_1(self.__algo)
        self.__cls.predict_1(self.__algo)
        self.assertIn(self.__algo, self.__cls.result.keys())
        self.assertLessEqual(len(np.unique(self.__cls.result[self.__algo])),
                             self.__n_clusters)

    def test_few_algos(self):
        """
        Cluster data using some algorithms
        """
        for i in self.__cls.algorithm:
            self.__cls.fit_1(i)
            try:
                self.__cls.predict_1(i)
            except Exception as e:
                self.fail("Algo %s failed\n%s" % (i, e))
        for i in self.__cls.algorithm:
            self.assertIn(i, self.__cls.result.keys())
            self.assertLessEqual(len(np.unique(self.__cls.result[i])),
                                 self.__n_clusters)

    def test_all_algos(self):
        """
        Apply every clustering algorithms on a toy dataset
        """
        __blob = datasets.make_blobs(n_samples=30, n_features=3, 
                                     random_state=8)
        __data = PackData(data=__blob[0])
        __n_cluster = random.randint(3, 5)
        __cls = Clustering(data=__data, algorithm=None,
                           n_clusters=__n_cluster, dirOut=DIR_TMP)
        __thres = 4 # acceptable elapsed time (seconds)
        _timers = {}
        _longest = 0
        for i in __cls.algorithm:
            _time = timer()
            __cls.fit_1(i, verbose=False)
            _time = timer() - _time
            self.assertTrue(__cls._fitted)
            if _time > __thres:
                _timers[i] = '%.1f' % _time
            if _time > _longest:
                _longest = _time
            __cls.predict_1(i, verbose=False)
            self.assertIn(i, __cls.result.keys())
            if i != "dbscan":
                self.assertLessEqual(len(np.unique(__cls.result[i])),
                                         __n_cluster,
                                     'Not expected clusters with %s' % i)
        self.assertLessEqual(_longest, __thres, '%i algo(s) took too long:\n%s'\
                             % (len(_timers), str(_timers)))

    def test_image(self):
        """
        Apply clustering to an image. Clustering resulting can be exported as
        an image. Output image should contain n_clusters different values
        (or less)
        """
        src = os.path.join(DIR_DATA, 'landsat_rennes.tif')
        img = ImageGeo(src)
        img.read()
        _data=img.img_2_data()
        _X = _data.sample(n=self.__n_clusters * 100, replace=False)
        data = PackData(data=_data, X=_X, type="clustering")
        clf = Clustering(data=data, algorithm=self.__algo,
                         n_clusters=self.__n_clusters, dirOut=DIR_TMP)
        clf.fit_1(self.__algo, verbose=False)
        clf.predict_1(self.__algo, verbose=False)
        img.data_2_img(clf.result, True)
        out_file = os.path.join(DIR_TMP, 'clustering.tif')
        img.write(out_file)
        img = None
        img = ImageGeo(out_file)
        img.read()
        # check that the ouput image exists, and that the matrix only contain
        # integer values
        self.assertTrue(os.path.exists(out_file))
        self.assertLessEqual(len(np.unique(img.data)), self.__n_clusters)

    def test_shapefile(self):
        """
        Apply clustering to a shapefile
        """
        in_file = os.path.join(DIR_DATA, 'echantillon.shp')
        in_shp = Loader(in_file, features=['Brightness', ], label='ECH')
        in_shp.run()

        data = PackData(data=in_shp.aData,
                        type='clustering',)
        clf = Clustering(data=data, algorithm=self.__algo,
                         n_clusters=self.__n_clusters, dirOut=DIR_TMP)
        in_shp = None
        clf.run(True)
        out_file = os.path.join(DIR_TMP, 'cluster.shp')
        shp = Shapefile(in_file)
        shp.read()
        shp.write(out_file, clf.result)
        # check that the output shapefile exists
        self.assertTrue(os.path.exists(out_file))
        shp = Shapefile(out_file)
        shp.read()
        # check that number of classes in output file <= self.__n_clusters
        self.assertLessEqual(len(np.unique(shp.data)), self.__n_clusters)

    def tearDown(self):
        elapsed = time.time() - self._started_at
        if elapsed > SLOW_TEST_THRESHOLD:
            print('{} ({}s)'.format(self.id(), round(elapsed, 2)))

if __name__ == '__main__':
    unittest.main()
