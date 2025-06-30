.. PyCritic documentation master file, created by
   sphinx-quickstart on Mon Jun 30 09:29:04 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyCritic
========

PyCritic is a package created to simplify validation and estimation of small
pieces of a data.

For instance, it may be used to estimate answers of a
student's math test even if they are depend on his or her PE grade or any other
condition set.

Main components
---------------

Main components used to create an estimation function are:

* Estimation - a value representing the result of an estimation process.
* Estimand - a data to be validated by a criterion.
* Condition - a boolean function taking a single parameter.
* Criterion - a function returning an estimation (the BasicCriterion returns a bound estimation after asserting a bound condition).

PyCritic JSON
=============

PyCritic JSON is the add-on for the PyCritic project since it implements
functionality to create an estimation function from a dict data.
That allows a user to write his or her tests with JSON or YAML.

It implements condition and criterion building functors.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules


Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`