# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['mario', 'mario.plugins']

package_data = \
{'': ['*'], 'mario': ['testing/*']}

install_requires = \
['appdirs==1.4.3',
 'asks==2.3.6',
 'async_exit_stack==1.0.1',
 'async_generator==1.10',
 'attrs==19.3.0',
 'bump2version==0.5.11',
 'click==7.0',
 'docutils==0.14',
 'importlib_metadata==0.23',
 'marshmallow==3.2.1',
 'parso==0.5.1',
 'pyrsistent==0.14.11',
 'pytest>=5.0.0,<6.0.0',
 'pyyaml==5.1.1',
 'toml==0.10.0',
 'toolz>=0.10.0,<0.11.0',
 'trio==0.11.0',
 'trio_typing==0.2.0',
 'xmltodict==0.12.0']

extras_require = \
{'docs': ['sphinx==2.1.2',
          'sphinx-rtd-theme>=0.4.3,<0.5.0',
          'sphinx-autodoc-typehints>=1.7,<2.0',
          'sphinx-click>=2.2,<3.0',
          'marshmallow-jsonschema>=0.8.0,<0.9.0',
          'sphinx-jsonschema>=1.9,<2.0']}

entry_points = \
{'console_scripts': ['mario = mario.cli:cli'],
 'mario_plugins': ['basic = mario.plugins']}

setup_kwargs = {
    'name': 'mario',
    'version': '0.0.154',
    'description': '',
    'long_description': '``````````````````````````````````````````````````````\nMario: Shell pipes in Python\n``````````````````````````````````````````````````````\n\n\n\n.. image:: https://img.shields.io/github/stars/python-mario/mario?style=social\n   :target: https://github.com/python-mario/mario\n   :alt: GitHub\n\n.. image:: https://readthedocs.org/projects/python-mario/badge/?style=flat\n   :target: https://readthedocs.org/projects/python-mario\n   :alt: Documentation Status\n\n.. image:: https://img.shields.io/travis/com/python-mario/mario/master\n   :target: https://travis-ci.com/python-mario/mario#\n   :alt: Build status\n\n.. image:: https://img.shields.io/pypi/v/mario.svg\n   :target: https://pypi.python.org/pypi/mario\n   :alt: PyPI package\n\n.. image:: https://img.shields.io/codecov/c/github/python-mario/mario.svg\n   :target: https://codecov.io/gh/python-mario/mario\n   :alt: Coverage\n\nHave you ever wanted to use Python functions directly in your Unix shell? Mario can read and write csv, json, and yaml; traverse trees, and even do xpath queries. Plus, it supports async commands right out of the box. Build your own commands with a simple configuration file, and install plugins for even more!\n\nMario is the plumbing snake 🐍🔧 helping you build data pipelines in your shell 🐢.\n\n\n.. image:: https://raw.githubusercontent.com/python-mario/mario/master/docs/time.png\n   :alt: What time is it in Sydney?\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\nFeatures\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n\n- Execute Python code in your shell.\n- Pass Python objects through multi-stage pipelines.\n- Read and write csv, json, yaml, toml, xml.\n- Run async functions natively.\n- Define your own commands in a simple configuration file or by writing Python code.\n- Install plugins to get more commands.\n- Enjoy high test coverage, continuous integration, and nightly releases.\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\nInstallation\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n\n..\n    installation-inclusion-start\n\nMario\n***********************************************************\n\n\nWindows support is hopefully coming soon. Linux and MacOS are supported now.\n\nGet Mario with pip:\n\n.. code-block:: bash\n\n   python3.7 -m pip install mario\n\nIf you\'re not inside a virtualenv, you might get a ``PermissionsError``. In that case, try using:\n\n.. code-block:: bash\n\n    python3.7 -m pip install --user mario\n\nor for more isolation, use `pipx <https://github.com/pipxproject/pipx/>`_:\n\n.. code-block:: bash\n\n     pipx install --python python3.7 mario\n\n\n\nMario addons\n***********************************************************\n\nThe `mario-addons <https://mario-addons.readthedocs.io/>`__ package provides a number of useful commands not found in the base collection.\n\n\nGet Mario addons with pip:\n\n.. code-block:: bash\n\n   python3.7 -m pip install mario-addons\n\nIf you\'re not inside a virtualenv, you might get a ``PermissionsError``. In that case, try using:\n\n.. code-block:: bash\n\n    python3.7 -m pip install --user mario-addons\n\nor for more isolation, use `pipx <https://github.com/pipxproject/pipx/>`_:\n\n.. code-block:: bash\n\n     pipx install --python python3.7 mario\n     pipx inject mario mario-addons\n\n\n\n..\n    installation-inclusion-end\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\nQuickstart\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\nBasics\n***********************************************************\n\nInvoke with  ``mario`` at the command line.\n\n.. code-block:: bash\n\n    $ mario eval 1+1\n    2\n\n\nGiven a csv like this:\n\n\n.. code-block:: bash\n\n    $ cat <<EOF > hackers.csv\n    name,age\n    Alice,21\n    Bob,22\n    Carol,23\n    EOF\n\nUse ``read-csv-dicts`` to read each row into a dict:\n\n.. code-block:: bash\n\n    $ mario read-csv-dicts < hackers.csv\n    {\'name\': \'Alice\', \'age\': \'21\'}\n    {\'name\': \'Bob\', \'age\': \'22\'}\n    {\'name\': \'Carol\', \'age\': \'23\'}\n\n\nUse ``map`` to act on each input item ``x`` :\n\n.. code-block:: bash\n\n    $ mario read-csv-dicts map \'x["name"]\' < hackers.csv\n    Alice\n    Bob\n    Carol\n\nChain Python functions together with ``!``:\n\n.. code-block:: bash\n\n    $ mario read-csv-dicts map \'x["name"] ! len\' < hackers.csv\n    5\n    3\n    5\n\nor by adding another command\n\n.. code-block:: bash\n\n    $ mario read-csv-dicts map \'x["name"]\' map len < hackers.csv\n    5\n    3\n    5\n\n\nUse ``x`` as a placeholder for the input at each stage:\n\n.. code-block:: bash\n\n    $ mario read-csv-dicts map \'x["age"] ! int ! x*2\'  < hackers.csv\n    42\n    44\n    46\n\n\nAutomatically import modules you need:\n\n.. code-block:: bash\n\n    $ mario map \'collections.Counter ! dict\' <<<mississippi\n    {\'m\': 1, \'i\': 4, \'s\': 4, \'p\': 2}\n\n\nYou don\'t need to explicitly call the function with ``some_function(x)``; just use the function\'s name, ``some_function``. For example, instead of\n\n.. code-block:: bash\n\n    $ mario map \'len(x)\' <<EOF\n    a\n    bb\n    EOF\n    1\n    2\n\ntry\n\n.. code-block:: bash\n\n    $ mario map len <<EOF\n    a\n    bb\n    EOF\n    1\n    2\n\n\n\n\nMore commands\n***********************************************************\n\nHere are a few commands. See `Command reference <https://python-mario.readthedocs.io/en/latest/cli_reference.html>`_ for the complete set, and get even more from `mario-addons <https://mario-addons.readthedocs.org/>`__.\n\n\n``eval``\n----------------------------------------------------\n\n\nUse ``eval`` to evaluate a Python expression.\n\n.. code-block:: bash\n\n    % mario eval \'datetime.datetime.utcnow()\'\n   2019-01-01 01:23:45.562736\n\n\n\n``map``\n----------------------------------------------------\n\nUse ``map`` to act on each input item.\n\n.. code-block:: bash\n\n    $ mario map \'x * 2\' <<EOF\n    a\n    bb\n    EOF\n    aa\n    bbbb\n\n``filter``\n----------------------------------------------------\n\n\nUse ``filter`` to evaluate a condition on each line of input and exclude false values.\n\n.. code-block:: bash\n\n    $ mario filter \'len(x) > 1\' <<EOF\n    a\n    bb\n    ccc\n    EOF\n    bb\n    ccc\n\n\n``apply``\n----------------------------------------------------\n\nUse ``apply`` to act on the sequence of items.\n\n.. code-block:: bash\n\n    $ mario apply \'len(x)\' <<EOF\n    a\n    bb\n    EOF\n    2\n\n\n\n\n``chain``\n----------------------------------------------------\n\nUse ``chain`` to flatten a list of lists into a single list, like `itertools.chain.from_iterable <https://docs.python.org/3/library/itertools.html#itertools.chain.from_iterable>`_.\n\nFor example, after generating a several rows of items,\n\n.. code-block:: bash\n\n\n    $ mario read-csv-tuples <<EOF\n    a,b,c\n    d,e,f\n    g,h,i\n    EOF\n    (\'a\', \'b\', \'c\')\n    (\'d\', \'e\', \'f\')\n    (\'g\', \'h\', \'i\')\n\n\n\nuse ``chain`` to put each item on its own row:\n\n.. code-block:: bash\n\n    $ mario read-csv-tuples chain <<EOF\n    a,b,c\n    d,e,f\n    g,h,i\n    EOF\n    a\n    b\n    c\n    d\n    e\n    f\n    g\n    h\n    i\n\n\n\n``async-map``\n----------------------------------------------------\n\n..\n    async-inclusion-start\n\nMaking sequential requests is slow. These requests take 16 seconds to complete.\n\n.. code-block:: bash\n\n\n       % time mario map \'await asks.get ! x.json()["url"]\'  <<EOF\n       http://httpbin.org/delay/5\n       http://httpbin.org/delay/1\n       http://httpbin.org/delay/2\n       http://httpbin.org/delay/3\n       http://httpbin.org/delay/4\n       EOF\n       https://httpbin.org/delay/5\n       https://httpbin.org/delay/1\n       https://httpbin.org/delay/2\n       https://httpbin.org/delay/3\n       https://httpbin.org/delay/4\n       0.51s user\n       0.02s system\n       16.460 total\n\n\nConcurrent requests can go much faster. The same requests now take only 6 seconds. Use ``async-map``, or ``async-filter``, or ``reduce`` with ``await some_async_function`` to get concurrency out of the box.\n\n\n.. code-block:: bash\n\n\n       % time mario async-map \'await asks.get ! x.json()["url"]\'  <<EOF\n       http://httpbin.org/delay/5\n       http://httpbin.org/delay/1\n       http://httpbin.org/delay/2\n       http://httpbin.org/delay/3\n       http://httpbin.org/delay/4\n       EOF\n       https://httpbin.org/delay/5\n       https://httpbin.org/delay/1\n       https://httpbin.org/delay/2\n       https://httpbin.org/delay/3\n       https://httpbin.org/delay/4\n       0.49s user\n       0.03s system\n       5.720 total\n\n..\n    async-inclusion-end\n\n.. _config-intro:\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\nConfiguration\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n\nDefine new commands and set default options. See `Configuration reference <config_reference.html>`_ for details.\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\nPlugins\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\nAdd new commands like ``map`` and ``reduce`` by installing Mario plugins. You can try them out without installing by adding them to any ``.py`` file in your ``~/.config/mario/modules/``.\n\nShare popular commands by installing the `mario-addons <https://mario-addons.readthedocs.io/en/latest/readme.html>`_ package.\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\nQ & A\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n\n..\n    Q&A-inclusion-start\n\n\n\nWhat\'s the status of this package?\n***********************************************************\n\n* This package is experimental and is subject to change without notice.\n* Check the `issues page <https://www.github.com/python-mario/mario/issues>`_ for open tickets.\n\n\nWhy another package?\n***********************************************************\n\nA number of cool projects have pioneered in the Python-in-shell space. I wrote Mario because I didn\'t know these existed at the time, but now Mario has a bunch of features the others don\'t (user configuration, multi-stage pipelines, async, plugins, etc).\n\n* https://github.com/Russell91/pythonpy\n* http://gfxmonk.net/dist/doc/piep/\n* https://spy.readthedocs.io/en/latest/intro.html\n* https://github.com/ksamuel/Pyped\n* https://github.com/ircflagship2/pype\n* https://code.google.com/archive/p/pyp/\n\n\n..\n    Q&A-inclusion-end\n',
    'author': 'akb',
    'author_email': 'uBX6aXPqDSRrt92kha28@cordaz.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
