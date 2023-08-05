# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['aiocqlengine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiocqlengine',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Darren',
    'author_email': 'charact3@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
