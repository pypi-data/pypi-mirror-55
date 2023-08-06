# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 18:57:34 2016

@author: thomas_a
"""
import os
import unittest
import random
import time

import numpy as np
import pandas as pd

from test import DIR_DATA, DIR_TMP
from maplearn.datahandler.loader import Loader
from maplearn.datahandler.writer import Writer
from maplearn.filehandler.shapefile import Shapefile
from maplearn.filehandler.imagegeo import ImageGeo
from maplearn.filehandler.excel import Excel
from maplearn.filehandler.csv import Csv

SLOW_TEST_THRESHOLD = 0.5

class TestWriter(unittest.TestCase):
    """
    Unit tests about writing data into a file
    """
    def setUp(self):
        loader = Loader(random.choice(['boston', 'iris']))
        self.__data = loader.df
        self._started_at = time.time()

    def test_missing_file(self):
        """
        Writes using a missing file as origin
        """
        self.assertRaises(IOError, Writer, origin='/fichier/inexistant.shp')

    def test_unknown_format(self):
        """
        Writes an unknown format
        """
        str_file = os.path.join(DIR_TMP, 'ex.fmt23')
        self.assertRaises(IOError, Writer, str_file)

    def test_existing_file(self):
        """
        Access to an already existing file
        """
        str_file = os.path.join(DIR_DATA, 'ex1.xlsx')
        try:
            Writer(str_file)
        except:
            self.fail('Unable to get access to %s' % str_file)

    def test_write_dataset(self):
        """
        Loads a known dataset (included in Scikit-learn) and writes it into an
        excel file.
        """
        out_file = os.path.join(DIR_TMP, 'dataset.xls')
        writer = Writer()
        writer.run(data=self.__data, path=out_file)
        
        self.assertTrue(os.path.exists(out_file))
        _driver = Excel(out_file)
        _driver.read()
        self.assertEqual(self.__data.shape, _driver.data.shape)

    def test_write_from_scratch(self):
        """
        Creates an Excel File from scratch
        """
        out_file = os.path.join(DIR_TMP, 'scratch2.xlsx')
        # creates a dataframe
        df = pd.DataFrame({ 'A' : 1,
                            'B' : pd.Timestamp('20130102'),
                            'C' : pd.Series(2,index=list(range(4)),dtype='int64'),
                            'D' : np.array([3] * 4,dtype='int64')})
        w = Writer(path=out_file)
        w.run(data=df)
        self.assertTrue(os.path.exists(out_file))
        _driver = Excel(out_file)
        _driver.read()
        self.assertEqual(df.shape, _driver.data.shape)
        self.assertSequenceEqual(set(df.columns), set(_driver.data.columns))

    def test_write_Excel(self):
        """
        Writes into an Excel File
        """
        out_file = os.path.join(DIR_TMP, 'excel.xls')
        w = Writer(path=out_file)
        w.run(data=self.__data)
        self.assertTrue(os.path.exists(out_file))
        _driver = Excel(out_file)
        _driver.read()
        self.assertEqual(self.__data.shape, _driver.data.shape)
        self.assertSequenceEqual(set(self.__data.columns),
                                 set(_driver.data.columns))

    def test_write_Csv(self):
        """
        Writes into an csv File
        """
        out_file = os.path.join(DIR_TMP, 'csv.csv')
        w = Writer(path=out_file)
        w.run(data=self.__data)
        self.assertTrue(os.path.exists(out_file))
        _driver = Csv(out_file)
        _driver.read()
        self.assertEqual(self.__data.shape, _driver.data.shape)
        self.assertSequenceEqual(set(self.__data.columns),
                                 set(_driver.data.columns))

    def test_write_image(self):
        """
        Writes into an image File
        """
        out_file = os.path.join(DIR_TMP, 'cp_landsat_rennes.tif')
        src = os.path.join(DIR_DATA, 'landsat_rennes.tif')
        img = ImageGeo(src)
        img.read()
        data = img.img_2_data()
        w = Writer(origin=src)
        w.run(path=out_file, data=data)
        self.assertTrue(os.path.exists(out_file))

    def test_write_shapefile(self):
        """
        Writes into a shapefile
        """
        out_file = os.path.join(DIR_TMP, 'shp.shp')
        src = os.path.join(DIR_DATA, 'echantillon_rennes.shp')
        _driver = Shapefile(src)
        _driver.read()
        w = Writer(origin=src)
        w.run(path=out_file, data=_driver.data)
        self.assertTrue(os.path.exists(out_file))

    def tearDown(self):
        elapsed = time.time() - self._started_at
        if elapsed > SLOW_TEST_THRESHOLD:
            print('{} ({}s)'.format(self.id(), round(elapsed, 2)))
        
if __name__ == '__main__':
    unittest.main()
