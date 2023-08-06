# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['uea_ucr_datasets']

package_data = \
{'': ['*']}

install_requires = \
['sktime>=0.3,<0.4']

setup_kwargs = {
    'name': 'uea-ucr-datasets',
    'version': '0.1.2',
    'description': 'A small package for loading and handling UEA UCR time series classification datasets.',
    'long_description': "# uea_ucr_datasets\n\nThis package contains convenience functions and classes to access the UEA UCR\ntime series classification archive.\n\nCurrently it contains the following functionalities:\n - `Dataset` class: Loads UEA UCR dataset stored in the `sktime` format \n   from `~/.data/UEA_UCR/` or path provided via the `UEA_UCR_DATA_DIR`\n   environment variable. This class is compatible with the pytorch `DataLoader`\n   class.\n - `list_datasets`: List datasets available in the `~/.data/UEA_UCR/` folder or\n   path provided via the `UEA_UCR_DATA_DIR`\n\n## Example usage\n\nDownload the `sktime` version of the UEA and UCR datasets. And unpack them.\nMove the folders of the individual datasets to the path `~/.data/UEA_UCR`.\n\n```python\n>>> import uea_ucr_datasets\n>>> uea_ucr_datasets.list_datasets()\n['LSST',..]\n>>> d = uea_ucr_datasets.Dataset('UWaveGestureLibrary', train=True)\n>>> first_instance = d[0]\n>>> instance_x, instance_y = first_instance\n```\n\n## Alternative data paths\n\nYou can also store the data at another location, then it is required to set the\nenvironment variable `UEA_UCR_DATA_DIR` appropriately such that the package can\nfind the datasets.\n",
    'author': 'Max Horn',
    'author_email': 'max.horn@bsse.ethz.ch',
    'url': 'https://github.com/BorgwardtLab/uea_ucr_datasets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
