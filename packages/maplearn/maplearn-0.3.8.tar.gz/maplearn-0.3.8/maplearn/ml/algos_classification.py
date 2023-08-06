# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 19:23:07 2018

@author: thomas_a
"""
from sklearn import neighbors, linear_model, svm, tree, neural_network
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
#from sklearn.manifold.isomap import Isomap
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier
from sklearn.semi_supervised import LabelPropagation, LabelSpreading
from sklearn.linear_model import Perceptron, PassiveAggressiveClassifier

ALGOS = dict(
            knn=neighbors.KNeighborsClassifier(),
            log=linear_model.LogisticRegression(solver='lbfgs'),
            tree=tree.DecisionTreeClassifier(),
            gnb=GaussianNB(),
            mnb=MultinomialNB(),
            lda=LinearDiscriminantAnalysis(),
            nearestc=neighbors.NearestCentroid(),
            svm=svm.SVC(kernel='rbf', gamma='auto'),
            svc=svm.SVC(kernel='linear', gamma='auto'),
            gboost=GradientBoostingClassifier(n_estimators=100),
            bag=BaggingClassifier(),
            rforest=RandomForestClassifier(n_estimators=20, oob_score=True),
            extra=ExtraTreesClassifier(n_estimators=20,
                                       min_impurity_decrease=0.001),
            sgd=SGDClassifier(tol=0.001, max_iter=200),
            propag=LabelPropagation(),
            spreading=LabelSpreading(),
            ada=AdaBoostClassifier(),
            perceptron=Perceptron(tol=0.001, max_iter=200),
            passive=PassiveAggressiveClassifier(tol=0.001, max_iter=200),
            mlp=neural_network.MLPClassifier(tol=0.001, max_iter=200),
            )