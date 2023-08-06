# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['escarpolette',
 'escarpolette.admin',
 'escarpolette.api',
 'escarpolette.models']

package_data = \
{'': ['*']}

install_requires = \
['flask-cors>=3.0,<4.0',
 'flask-migrate>=2.5,<3.0',
 'flask-restplus>=0.12.1,<0.13.0',
 'flask-sqlalchemy>=2.3,<3.0',
 'flask>=1.0,<2.0',
 'sqlalchemy>=1.2,<2.0',
 'youtube-dl>=2019.1,<2020.0']

setup_kwargs = {
    'name': 'escarpolette',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alexandre Morignot',
    'author_email': 'erdnaxeli@cervoi.se',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
