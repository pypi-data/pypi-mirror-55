pyhdfe
======

|docs-badge|_ |pypi-badge|_ |python-badge|_ |license-badge|_

.. |docs-badge| image:: https://img.shields.io/readthedocs/pyhdfe/stable.svg
.. _docs-badge: https://pyhdfe.readthedocs.io/en/stable/

.. |pypi-badge| image:: https://img.shields.io/pypi/v/pyhdfe.svg
.. _pypi-badge: https://pypi.org/project/pyhdfe/

.. |python-badge| image:: https://img.shields.io/pypi/pyversions/pyhdfe.svg
.. _python-badge: https://pypi.org/project/pyhdfe/

.. |license-badge| image:: https://img.shields.io/pypi/l/pyhdfe.svg
.. _license-badge: https://pypi.org/project/pyhdfe/

.. description-start

An overview of the package, examples, and other documentation can be found on `Read the Docs <https://pyhdfe.readthedocs.io/en/stable/>`_.

.. docs-start

The pyhdfe package is a Python 3 implementation of algorithms for absorbing high dimensional fixed effects. This package was created by `Jeff Gortmaker <https://jeffgortmaker.com>`_ in collaboration with Anya Tarascina.

What pyhdfe won't do is provide a convenient interface for running regressions. Instead, the package is meant to be incorporated into statistical projects that would benefit from performant fixed effect absorption. Another goal is facilitating fair comparison of algorithms that have been previously implemented in various languages with different convergence criteria.

Development of the package has been guided by code made publicly available by many researchers and practitioners. For a full list of papers and software cited in this documentation, refer to the `references <https://pyhdfe.readthedocs.io/en/stable/references.html>`_ section of the documentation.


Installation
------------

The pyhdfe package has been tested on `Python <https://www.python.org/downloads/>`_ versions 3.6 and 3.7. The `SciPy instructions <https://scipy.org/install.html>`_ for installing related packages is a good guide for how to install a scientific Python environment. A good choice is the `Anaconda Distribution <https://www.anaconda.com/distribution/>`_, since, along with many other packages that are useful for scientific computing, it comes packaged with pyhdfe's only required dependencies: `NumPy <https://numpy.org/>`_ and `SciPy <https://www.scipy.org/>`_.

You can install the current release of pyhdfe with `pip <https://pip.pypa.io/en/latest/>`_::

    pip install pyhdfe

You can upgrade to a newer release with the ``--upgrade`` flag::

    pip install --upgrade pyhdfe

If you lack permissions, you can install pyhdfe in your user directory with the ``--user`` flag::

    pip install --user pyhdfe

Alternatively, you can download a wheel or source archive from `PyPI <https://pypi.org/project/pyhdfe/>`_. You can find the latest development code on `GitHub <https://github.com/jeffgortmaker/pyhdfe/>`_ and the latest development documentation `here <https://pyhdfe.readthedocs.io/en/latest/>`_.


Bugs and Requests
-----------------

Please use the `GitHub issue tracker <https://github.com/jeffgortmaker/pyhdfe/issues>`_ to submit bugs or to request features.
