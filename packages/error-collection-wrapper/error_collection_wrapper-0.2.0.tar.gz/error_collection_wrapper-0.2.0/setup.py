# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['error_collection_wrapper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'error-collection-wrapper',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'anshu3769',
    'author_email': 'at3769@nyu.edu',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
