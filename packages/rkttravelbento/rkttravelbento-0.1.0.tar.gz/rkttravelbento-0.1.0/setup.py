# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rkttravelbento']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rkttravelbento',
    'version': '0.1.0',
    'description': 'bento for customers',
    'long_description': None,
    'author': 'siva',
    'author_email': 'sivakon@outlook.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
