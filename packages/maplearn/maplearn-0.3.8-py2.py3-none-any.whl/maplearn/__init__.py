# -*- coding: utf-8 -*-
"""
.. note::

    Mapping Learning (also called *maplearn*) makes **use of 
    machine learning easy** (easier, at least). Initially designed for 
    geographical data (cartography based on remote sensing),
    *Maplearn* also deals very well with classical data (*ie* tabular). 


*NB: information in french is available in maplearn's* 
`wiki <https://bitbucket.org/thomas_a/maplearn/wiki/>`_ .

.. image:: ./image/logo_lGPL.png
    :align: left
    :width: 50px


*Maplearn* is a **free software and library**, distributed under lGPL v3
license.

|
.. image:: ./image/logo_python.png
    :align: left
    :width: 50px

Written in Python, *maplearn* can be used whichever your operation system 
(Linux, Mac, Windows).

|

Features
--------

* **many algorithms** to make predictions (classification, clustering or
  regression)
* look for best hyper-parameters to **improve accuracy** of your results
* generalize machine learning's best practices (k-fold...)
* several preprocessing tasks available : reduction of dimensions...
* reads/writes **several file formats** (*geographic or not*)
* synthetizes results in a **standardized report**
* statiscal and more empirical **advices** will help novice users

"""
import logging
from logging.config import fileConfig
from pkg_resources import resource_filename

# load logging configuration file
fileConfig(resource_filename('maplearn', 'logging.cfg'))
logger = logging.getLogger(__name__)
__version__ = '0.3.8'
