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
    'version': '0.3.1',
    'description': 'Local mirror for Internet fiction sites',
    'long_description': "ffmirror is a program to create and maintain a local mirror of stories on\nfiction-publishing sites. It has functionality for downloading stories similar\nto FanFicFare or other projects, but the differentiating factor is support for\ncreating a local database that maintains downloaded metadata and can\nautomatically update authors that are followed.\n\nffmirror has two currently maintained script entry points:\n\n - ffdl is a simple one-story file downloader. It takes a single URL and writes\n   an HTML file story.\n - ffdb is the manager for local fanfic site mirrors. These maintain a local\n   copy of metadata for a set of followed users alongside copies of all their\n   stories.\n\nThe remaining entry points, ffadd, ffup, ffcache are designed for an older\nformat of mirror, and are now deprecated.\n\nffmirror can be installed via PyPI: ``pip install ffmirror``\n\nTo create a mirror, enter an empty directory and issue:\n\n.. code:: bash\n\n  $ ffdb init\n\nThis initializes the SQLite database that tracks metadata. You can now add\nauthors by issuing:\n\n.. code:: bash\n\n  $ ffdb add $AUTHOR_URL\n\nAdding an author will immediately download all their stories into the mirror.\nStories are stored under top-level directories per author.\n\nUpdating the mirror will recheck all authors that have been added and download\nany new or updated stories. To update the mirror, issue:\n\n.. code:: bash\n\n  $ ffdb update\n\nYou can update only one author by issuing:\n\n.. code:: bash\n\n  $ ffdb update $AUTHOR_DIR\n\nwhere AUTHOR_DIR is the directory with that author's stories.\n",
    'author': 'alethiophile',
    'author_email': 'tomdicksonhunt@gmail.com',
    'url': 'https://github.com/alethiophile/ffmirror',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
