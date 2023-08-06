
.. image:: https://circleci.com/gh/sdpython/pystrat2048/tree/master.svg?style=svg
    :target: https://circleci.com/gh/sdpython/pystrat2048/tree/master

strat_2048_rvk
===========

.. image:: https://raw.githubusercontent.com/kenzaa20/strat_2048_rvk/master/doc/_static/logo.png
    :width: 50

It implements basic CI and documentation. One example of use:
`plot_strategy.py
<https://github.com/kenzaa20/strat_2048_rvk/blob/master/examples/plot_strategy.py>`_.

Generate the setup in subfolder ``dist``:

::

    python setup.py sdist

Generate the documentation in folder ``dist/html``:

::

    python -m sphinx -T -b html doc dist/html

Run the unit tests:

::

    python -m unittest discover tests

Or:

::

    python -m pytest

To check style:

::

    python -m flake8 strat_2048_rvk tests examples
