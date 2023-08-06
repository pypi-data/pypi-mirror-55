# -*- coding: utf-8 -*-
from setuptools import setup

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
    'version': '1.2.0',
    'description': 'Save data from Pinboard to a SQLite database',
    'long_description': "# Save data from Pinboard to a SQLite database.\n\nInspired by (and using libraries from) [Simon Willison's Dogsheep\nproject](https://github.com/dogsheep). You're probably going to want to run\n[Datasette](https://github.com/simonw/datasette) on the resulting db.\n\n## How to install\n\n```\n$ pip install pinboard-to-sqlite\n```\n\n## Authentication\n\nRun:\n\n```\n$ pinboard-to-sqlite auth\n```\n\nThis will direct you to https://pinboard.in/settings/password to find your API\ntoken, which you'll then paste into the terminal. This'll get saved in an\n`auth.json` file, which subsequent commands will pick up.\n\nTo save to a different file, see the `-a` / `--auth` flag.\n\n## Fetching posts\n\nRun:\n\n```\n$ pinboard-to-sqlite posts pinboard.db\n```\n\nWhere `pinboard.db` is the name of the database you'd like to save posts to.\nNote that the API this uses has a rate limit of once per minute, so don't run\nthis command more than once per minute (I don't know why you would). This\ndoesn't seem to be enforced fairly loosely, but be careful anyway.\n",
    'author': 'Jacob Kaplan-Moss',
    'author_email': 'jacob@jacobian.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jacobian/pinboard-to-sqlite/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
