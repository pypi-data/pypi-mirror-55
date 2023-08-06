# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pinboard_to_sqlite']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.22.0,<3.0.0',
 'sqlite-utils>=1.12.1,<2.0.0']

entry_points = \
{'console_scripts': ['pinboard-to-sqlite = pinboard_to_sqlite.cli:cli']}

setup_kwargs = {
    'name': 'pinboard-to-sqlite',
    'version': '1.0',
    'description': 'Save data from Pinboard to a SQLite database',
    'long_description': None,
    'author': 'Jacob Kaplan-Moss',
    'author_email': 'jacob@jacobian.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
