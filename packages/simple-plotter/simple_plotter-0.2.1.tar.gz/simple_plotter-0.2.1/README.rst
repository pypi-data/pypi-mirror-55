Getting started
===============

simple_plotter is a code-generator and minimal GUI frontend for plotting functional 2D x,y-plots.
The function equation has to be entered in python syntax (allowing the use of numpy statements).

Besides saving and loading projects to/from a JSON file, simple_plotter also provides the possibility to export the
project as python code.

simple_plotter is released under GPLv3.

.. image:: https://readthedocs.org/projects/simple-plotter/badge/?version=latest
    :target: https://simple-plotter.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://gitlab.com/thecker/simple-plotter/badges/master/pipeline.svg
    :target: https://gitlab.com/thecker/simple-plotter/commits/master
    :alt: pipeline status

How to install
--------------

simple_plotter can either installed via pip or conda.

For pip use:

::

    pip install simple-plotter

or for conda:

::

    conda install -c thecker simple_plotter

Requirements
------------
simple_plotter is written in python3 and requires following packages:

* pyqt >= 5
* jsonpickle
* numpy
* matplotlib
* setuptools_scm
* jinja2

Usage
-----

To launch simple_plotter just call

::

    python -m simple_plotter.gui

For detailed usage instructions see the user guide at https://simple-plotter.readthedocs.io/.


Developer information
---------------------

The source code can be obtained from:

https://gitlab.com/thecker/simple-plotter

For code documentation see the API documentation at https://simple-plotter.readthedocs.io/.