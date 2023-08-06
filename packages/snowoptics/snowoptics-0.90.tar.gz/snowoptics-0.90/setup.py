# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['snowoptics']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.10,<2.0']

setup_kwargs = {
    'name': 'snowoptics',
    'version': '0.90',
    'description': 'Set of functions to compute spectral albedo and extinction of snow, and to correct albedo measurements from slope distortion.',
    'long_description': None,
    'author': 'Ghislain Picard',
    'author_email': 'ghislain.picard@univ-grenoble-alpes.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
