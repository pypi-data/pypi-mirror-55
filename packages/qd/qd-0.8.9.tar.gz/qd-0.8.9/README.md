# qd - a CAE Python Library

[![Build Status](https://travis-ci.org/qd-cae/qd-cae-python.svg?branch=master)](https://travis-ci.org/qd-cae/qd-cae-python)
[![Join the chat at https://gitter.im/sahat/hackathon-starter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/qd-cae-python/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link)

> **WARNING**: This library is only maintained for bugfixes. Migrate to [lasso-python](https://github.com/lasso-gmbh/lasso-python) if possible (not all features are available though).

This Python3 library is an open source software package with utility functions regarding engineering, especially Simulation and Computer Aided Engineering (CAE).
The library is still young, so features drop in over time depending on the needs of the persons who contribute. Visit our website at http://www.qd-eng.de/

CAE suffers greatly from expensive tools with bad or moderate scripting access and utility. Also many algorithms developed in research never get published due to licensing or being very specific regarding a certain software environment. Engineering is lacking behind here in contrast to modern informatics.

<p style="text-align: center;"><b>"We don't want to provide another software solution, 
<br>we want, that people can build their own solutions quickly"</b></p>

We believe, that CAE can not evolve, if people do not get comfortable access to the raw data and start doing their own stuff, because

<p style="text-align: center;"><b>"Creativity originates from freedom and simplicity."</b></p>

This core idea keeps us pushing forward.

# Support this project

[![Become a Patron](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/bePatron?u=8375141)

# What's new?

_Changelog 06.10.2019_
Version 0.8.9

KeyFile:
 - Fixed a bug with extra lines of the element keyword

 D3plot:
 - updated femzip decompression to version 10

_Changelog 26.04.2019_ ✿✿✿
Version 0.8.8

KeyFile:
 - Fixed a bug when loading deeply nested include structures

# Documentation

You can find the [full Documentation here](https://qd-cae.github.io/qd-cae-python/build/html/index.html). Brief module and feature list:

1. [qd.cae.dyna ](https://qd-cae.github.io/qd-cae-python/build/html/qd_cae_dyna.html)

- Read D3plot
- Read Binouts
- Read KeyFiles

2. [qd.numerics](https://qd-cae.github.io/qd-cae-python/build/html/qd_numerics.html)

- Submodule: sampling

3. [qd.cae.beta](https://qd-cae.github.io/qd-cae-python/build/html/qd_cae_beta.html)

- MetaCommunicator (control META remotely)

# Installation

## Windows

For **Windows** (x64 Python 3.5 and higher) install by using pip. The precompiled wheels are always compiled with FEMZIP support, allowing you to read compressed files directly. Since the package is uploaded to pipy, the following should work:

```
pip install qd
```

or

```
python -m pip install qd
```

The wheels, which are used by pip, can also be found here in the [dist folder](https://github.com/qd-cae/qd-cae-python/tree/master/dist). If neccessary download the appropriate one and install it with:

```python
python -m pip install [path/to/downloaded/wheel]
```

The precompiled wheels include femzip decompression, which require the intel libraries `libmmd.dll` and `libiomp5.dll` to be present on your machine. You can install them in Anaconda through:

```python
conda install icc_rt mkl
```

Note that your windows python distribution might not neccessarily find an appropriate version and fail. In that case one has three options:

- Download and use [Anaconda Python x64](https://www.continuum.io/downloads#windows)
- Compile it yourself (see the [compilation guide](https://qd-cae.github.io/qd-cae-python/build/html/compilation_guide.html))
- Open a request for compilation of a specific distribution

## Linux

In the [dist folder](https://github.com/qd-cae/qd-cae-python/tree/master/dist) usually are some precompiled Linux wheels for installation with pip. Note that Linux wheels rarely work accross different systems, so do not expect them to work and in case of trouble see the [compilation guide](https://qd-cae.github.io/qd-cae-python/build/html/compilation_guide.html). It's quite simple to compile it yourself on Linux (❤).

For your info the library is about **2-3 times faster on Linux than on Windows**.

# Compilation

If you are bold enough to compile it yourself, then follow the [compilation guide](https://qd-cae.github.io/qd-cae-python/build/html/compilation_guide.html).

# License

See the license file.

# Authors

- codie
- towelie
- bala
