===========
cnewtonprop
===========

.. image:: https://img.shields.io/badge/github-qucontrol/cnewtonprop-blue.svg
   :alt: Source code on Github
   :target: https://github.com/qucontrol/cnewtonprop
.. image:: https://img.shields.io/pypi/v/cnewtonprop.svg
   :alt: cnewtonprop on the Python Package Index
   :target: https://pypi.python.org/pypi/cnewtonprop

.. image:: https://img.shields.io/travis/qucontrol/cnewtonprop.svg
   :alt: Travis Continuous Integration
   :target: https://travis-ci.org/qucontrol/cnewtonprop
.. image:: https://img.shields.io/badge/appveyor-no%20id-red.svg
   :alt: AppVeyor Continuous Integration
   :target: https://ci.appveyor.com/project/qucontrol/cnewtonprop
.. image:: https://img.shields.io/coveralls/github/qucontrol/cnewtonprop/master.svg
   :alt: Coveralls
   :target: https://coveralls.io/github/qucontrol/cnewtonprop?branch=master
.. image:: https://readthedocs.org/projects/cnewtonprop/badge/?version=latest
   :alt: Documentation Status
   :target: https://cnewtonprop.readthedocs.io/en/latest/?badge=latest
.. image:: https://img.shields.io/badge/License-BSD-green.svg
   :alt: BSD License
   :target: https://opensource.org/licenses/BSD-3-Clause

Cython implementation of the `Newton propagator <newtonprop package_>`_, for QuTiP ``Qobj``'s

Development of ``cnewtonprop`` happens on `Github`_.

.. You can read the full documentation at `ReadTheDocs`_.

⚠️  **WARNING**: This implementation is work in progress. No public release is
available at this time, nor should the current development version (``master``)
be considered functional.

.. _ReadTheDocs: https://cnewtonprop.readthedocs.io/en/latest/


Installation
------------
..  To install the latest released version of ``cnewtonprop``, run this command in your terminal:


    .. code-block:: console

        $ pip install cnewtonprop

    This is the preferred method to install ``cnewtonprop``, as it will always install the most recent stable release.

    If you don't have `pip`_ installed, the `Python installation guide`_, respectively the `Python Packaging User Guide`_  can guide
    you through the process.

    .. _pip: https://pip.pypa.io
    .. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
    .. _Python Packaging User Guide: https://packaging.python.org/tutorials/installing-packages/


To install the latest development version of ``cnewtonprop`` from `Github`_.

.. code-block:: console

    $ pip install git+https://github.com/qucontrol/cnewtonprop.git@master#egg=cnewtonprop

.. _Github: https://github.com/qucontrol/cnewtonprop


Usage
-----

The ``cnewtonprop`` can be used as a drop-in replacement for the |newtonprop package|_::

    import cnewtonprop as newtonprop

.. |newtonprop package| replace:: ``newtonprop`` package
.. _newtonprop package: https://github.com/qucontrol/newtonprop
