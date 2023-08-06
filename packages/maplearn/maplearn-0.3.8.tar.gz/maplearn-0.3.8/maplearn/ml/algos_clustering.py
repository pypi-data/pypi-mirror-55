# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 19:45:09 2018

@author: thomas_a
"""
from sklearn import cluster

ALGOS = dict(
            mkmeans=cluster.MiniBatchKMeans(max_iter=100),
            kmeans=cluster.KMeans(),
            birch=cluster.Birch(),
            ms=cluster.MeanShift(bin_seeding=True),
            ward=cluster.AgglomerativeClustering(linkage='ward'),
            spectral=cluster.SpectralClustering(affinity='rbf', eigen_tol=0.25,
                                                eigen_solver='arpack',
                                                assign_labels="kmeans"),
            dbscan=cluster.DBSCAN(),
            propa=cluster.AffinityPropagation(max_iter=100, damping=0.8,
                                              preference=None), 
            )