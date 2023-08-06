# -*- coding: utf-8 -*-
"""
Machine Learning
----------------

**What is Machine Learning?**

From `Wikipedia <https://en.wikipedia.org/wiki/Machine_learning>`_: "Machine
learning algorithms build a mathematical **model** based on **sample** data,
known as "training data", in order to make **predictions** or decisions without
being explicitly programmed to perform the task."

.. image:: image/machine_learning_en.svg
    :align: center
    :width: 400px

|

So, we use Machine Learning to predict results about unknown data:

* Is this new email a spam?
* Is this an image of a cat or a dog?
* How many people are going to buy my new product?
* *Applications are infinite...*

To answer these questions, we will use mathematical models (the cloud in the 
above figure) that need to be trained (or **fitted**) prior to make
**predictions**.

**What to predict?**

Depending on the nature of the values to be predicted, we will talk about:

* **classification** when the values are discrete (also called categorical)
* **regression** when the values are continuous

.. image:: image/classif_reg.png
    :align: center

Classification and regression both needs some samples for training, they belong
to *supervised learning*. If you do not have samples, then you should consider
*unsupervised classification*, also called **clustering**. 

.. note:: On the other hand, a regression can't be made without samples.

**Maplearn: machine Learning modules**

.. image:: image/logo_scikit-learn.png
    :width: 80px
    :align: left

In *maplearn*, machine learning is empowered by **scikit-learn**. One reason  
is its great `documentation <https://scikit-learn.org/>`_. Have a look to go
further.

*Maplearn* provides 3 modules corresponding to each of these tasks:

1. **Classification**
2. **Clustering**
3. **Regression**

Two other modules are linked to these tasks:

* **Confusion**: confusion matrix (used to evaluate classifications)
* **Distance**: computes distance using different formulas

Another task that can accomplish machine learning is to reduce the number of
dimensions (also called *features*)

* **Reduction**: dimensionnality reduction

The last submodule is needed for programmation but should not be used itself:
    
* *Machine*: abstract class of a machine learning processor, one or more 
  algorithms can be applied

"""