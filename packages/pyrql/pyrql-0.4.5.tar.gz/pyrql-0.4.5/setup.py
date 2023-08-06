# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyrql']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=2.4,<3.0', 'python-dateutil>=2.8,<3.0']

setup_kwargs = {
    'name': 'pyrql',
    'version': '0.4.5',
    'description': 'RQL parsing',
    'long_description': None,
    'author': 'Pedro Werneck',
    'author_email': 'pjwerneck@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
