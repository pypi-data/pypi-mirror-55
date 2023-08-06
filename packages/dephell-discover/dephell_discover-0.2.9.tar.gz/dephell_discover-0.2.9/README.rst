
Dephell Discover
================


.. image:: https://travis-ci.org/dephell/dephell_discover.svg?branch=master
   :target: https://travis-ci.org/dephell/dephell_discover
   :alt: travis


.. image:: https://ci.appveyor.com/api/projects/status/github/dephell/dephell_discover?svg=true
   :target: https://ci.appveyor.com/project/orsinium/dephell-discover
   :alt: appveyor


.. image:: https://img.shields.io/pypi/l/dephell-discover.svg
   :target: https://github.com/dephell/dephell_discover/blob/master/LICENSE
   :alt: MIT License


Find project modules and data files (\ ``packages`` and ``package_data`` for ``setup.py``\ ).

Installation
------------

install from `PyPI <https://pypi.org/project/dephell-discover/>`_\ :

.. code-block:: bash

   python3 -m pip install --user dephell_discover

Usage
-----

Get root, packages, package_data, `package dir <https://docs.python.org/2/distutils/examples.html#pure-python-distribution-by-package>`_\ :

.. code-block:: python

   from pathlib import Path
   from dephell_discover import Root

   root = Root(path=Path('../dephell'))

   root.packages
   # [Package(path=Path('../dephell/dephell'), root=Path('../dephell')), ...]

   root.data
   # {Data(path=Path('../dephell/dephell/templates'), ext='.j2', package=Package(...)), ...}

   root.package_dir
   # {'': ''}

Package properties:

.. code-block:: python

   p = root.packages[-1]
   p.path    # Path('../dephell/dephell/commands')
   p.root    # Path('../dephell')
   p.module  # 'dephell.commands'
   str(p)    # 'dephell.commands'
   list(p)   # [Path('../dephell/dephell/commands/base.py'), ...]

Data properties:

.. code-block:: python

   d = next(iter(root.data))
   d.path      # Path('../dephell/dephell/templates')
   d.ext       # .j2
   d.package   # Package(path=Path('../dephell/dephell'), root=...)
   d.module    # 'dephell'
   # relative path from package root:
   d.relative  # 'templates/*.j2'
   str(d)      # 'templates/*.j2'
   list(d)     # [Path('../dephell/dephell/templates/python.html.j2'), ...]

Meta information:

.. code-block:: python

   root.metainfo.summary
   # 'Python project management.'

   root.metainfo.authors
   # ['Gram (@orsinium)']

   root.metainfo.license
   # 'MIT'

   root.metainfo.version
   # '0.7.0'
