# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiocqlengine']

package_data = \
{'': ['*']}

install_requires = \
['aiocassandra>=2.0,<3.0', 'cassandra-driver>=3.20,<4.0']

setup_kwargs = {
    'name': 'aiocqlengine',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Darren',
    'author_email': 'charact3@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
