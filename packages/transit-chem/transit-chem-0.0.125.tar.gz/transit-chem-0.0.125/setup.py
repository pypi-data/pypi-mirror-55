# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['transit_chem']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'numba>=0.43.0,<0.44.0',
 'numpy>=1.17,<2.0',
 'scipy>=1.3,<2.0']

setup_kwargs = {
    'name': 'transit-chem',
    'version': '0.0.125',
    'description': 'Quantifying Probabilistic Electron Transit times.',
    'long_description': None,
    'author': 'Evan Curtin',
    'author_email': 'fakeemail@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
