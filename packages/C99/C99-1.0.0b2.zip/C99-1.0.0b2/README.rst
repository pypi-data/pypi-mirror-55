C99
===

C99 headers and libraries that are missing from the C compilers for Python2.

Overview
========

TODO...

Installation
============

Prerequisites:

+ Python 2.7

  * https://www.python.org/

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

.. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Visit `development page`_.

Installation from sources:

clone the sources:

.. parsed-literal::

    git clone |respository| |package|

and run:

.. parsed-literal::

    python -m pip install ./|package|

or on development mode:

.. parsed-literal::

    python -m pip install --editable ./|package|

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

License
=======

  | Copyright (c) 2018-2019 Adam Karpierz
  |
  | Licensed under the zlib/libpng License
  | https://opensource.org/licenses/zlib/
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: C99
.. |package_bold| replace:: **C99**
.. |respository| replace:: https://github.com/karpierz/C99.git
.. _development page: https://github.com/karpierz/C99/
