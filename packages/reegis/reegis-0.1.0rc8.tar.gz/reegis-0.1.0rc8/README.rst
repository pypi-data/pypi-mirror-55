.. image:: https://travis-ci.org/reegis/reegis.svg?branch=master
    :target: https://travis-ci.org/reegis/reegis

.. image:: https://coveralls.io/repos/github/reegis/reegis/badge.svg?branch=master
    :target: https://coveralls.io/github/reegis/reegis?branch=master

.. image:: https://img.shields.io/lgtm/grade/python/g/reegis/reegis.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/reegis/reegis/context:python

.. image:: https://img.shields.io/lgtm/alerts/g/reegis/reegis.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/reegis/reegis/alerts/


Introduction
=============

The reegis repository provides tools to fetch, prepare and organise input data for heat and power models. At the moment the focus is on the territory of Germany but some tools can be used for european models as well.


Most tools use spatial data and can be used for arbitrary regions.

 * Feed-in time series using the HZG [coastdat2](https://www.earth-syst-sci-data.net/6/147/2014/) weather data set and the libraries [windpowerlib](https://github.com/wind-python/windpowerlib) and [pvlib](https://github.com/pvlib/pvlib-python).
 * Demand time series based on [OPSD](https://github.com/Open-Power-System-Data/national_generation_capacity), [openEgo](https://github.com/openego) and oemof demandlib
 * Powerplants based on [OPSD](https://github.com/Open-Power-System-Data).
 * Integration of open data from the german geo-data-platform of the  [BKG](http://www.geodatenzentrum.de/geodaten/gdz_rahmen.gdz_div?gdz_spr=deu&gdz_akt_zeile=5&gdz_anz_zeile=1&gdz_unt_zeile=0&gdz_user_id=0) and the energy ministry [BMWI](http://www.bmwi.de/Navigation/EN/Home/home.html).
 * Using prepared energy balances from Germany's federal states.



Documentation
==============

Full documentation can be found at `readthedocs <https://reegis.readthedocs.io/en/latest/>`_.

Go to the `download page <http://readthedocs.org/projects/reegis/downloads/>`_ to download different versions and formats (pdf, html, epub) of the documentation.


Installation
============

If you have a working Python 3 environment, use pypi to install the latest reegis version:

::

    pip install reegis

The reegis library is designed for Python 3 and tested on Python >= 3.6. We highly recommend to use virtual environments.
Please see the `installation page <http://oemof.readthedocs.io/en/stable/installation_and_setup.html>`_ of the oemof documentation for complete instructions on how to install python and a virtual environment on your operating system.


Basic usage
===========

Soon.


Contributing
==============

We are warmly welcoming all who want to contribute to the reegis library.


Citing reegis
========================

We use the zenodo project to get a DOI for each version. `Search zenodo for the right citation of your reegis version <https://zenodo.org/search?page=1&size=20&q=windpowerlib>`_.

License
============

Copyright (c) 2019 Uwe Krien, nesnoj

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.