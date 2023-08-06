# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ffmirror', 'ffmirror.handlers']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0',
 'beautifulsoup4>=4.7,<5.0',
 'click>=7.0,<8.0',
 'html2text>=2019.9,<2020.0',
 'html5lib>=1.0,<2.0',
 'python-dateutil>=2.7,<3.0',
 'requests>=2.22,<3.0',
 'sqlalchemy>=1.2,<2.0']

entry_points = \
{'console_scripts': ['ffdb = ffmirror.cli:run_db_op',
                     'ffdl = ffmirror.cli:run_dl']}

setup_kwargs = {
    'name': 'ffmirror',
    'version': '0.3.0',
    'description': 'Local mirror for Internet fiction sites',
    'long_description': None,
    'author': 'alethiophile',
    'author_email': 'tomdicksonhunt@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
