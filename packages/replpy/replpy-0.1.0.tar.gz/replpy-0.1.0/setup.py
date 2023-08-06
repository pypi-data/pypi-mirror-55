# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['replpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'replpy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ben G',
    'author_email': 'ben.gordon@toasttab.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
