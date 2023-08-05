# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['uea_ucr_datasets']

package_data = \
{'': ['*']}

install_requires = \
['sktime>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'uea-ucr-datasets',
    'version': '0.1.0',
    'description': 'A small package for loading and handling UEA UCR time series classification datasets.',
    'long_description': None,
    'author': 'Max Horn',
    'author_email': 'max.horn@bsse.ethz.ch',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
