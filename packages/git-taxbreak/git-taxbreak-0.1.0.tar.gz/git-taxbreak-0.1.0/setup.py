# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['git_taxbreak', 'git_taxbreak.modules']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3,<4', 'pre-commit>=1.20,<2.0']

entry_points = \
{'console_scripts': ['git-taxbreak = git_taxbreak.cmd:main']}

setup_kwargs = {
    'name': 'git-taxbreak',
    'version': '0.1.0',
    'description': 'Tool for collect artifacts from git for register creative work',
    'long_description': 'Git taxbreak\n------------\n\n.. image:: https://github.com/kamil1b/git-taxbreak/workflows/Master/badge.svg\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/ambv/black\n\n.. image:: https://api.codeclimate.com/v1/badges/6ad9e9549fdf496138c6/maintainability\n   :target: https://codeclimate.com/github/kamil1b/git-taxbreak/maintainability\n   :alt: Maintainability\n\n.. image:: https://codecov.io/gh/kamil1b/git-taxbreak/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/kamil1b/git-taxbreak\n\nTool for collect artifacts from git for register creative work\n\nInstall\n-------\n\n.. code-block:: sh\n\n   pip install git+https://github.com/kamil1b/git-taxbreak.git\n',
    'author': 'Luczak Kamil',
    'author_email': 'kamilluczak@luczakweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kamil1b/git-taxbreak',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
