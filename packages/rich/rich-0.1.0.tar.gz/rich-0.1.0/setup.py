# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rich']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rich',
    'version': '0.1.0',
    'description': 'Rich Console',
    'long_description': None,
    'author': 'Will McGugan',
    'author_email': 'willmcgugan@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
