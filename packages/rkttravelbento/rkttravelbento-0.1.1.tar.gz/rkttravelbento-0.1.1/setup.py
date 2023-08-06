# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rkttravelbento']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0']

setup_kwargs = {
    'name': 'rkttravelbento',
    'version': '0.1.1',
    'description': 'bento for customers',
    'long_description': None,
    'author': 'siva',
    'author_email': 'sivakon@outlook.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
