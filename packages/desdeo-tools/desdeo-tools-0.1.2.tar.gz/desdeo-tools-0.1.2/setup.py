# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['desdeo_tools', 'desdeo_tools.interaction', 'desdeo_tools.scalarization']

package_data = \
{'': ['*'], 'desdeo_tools': ['utils/*']}

install_requires = \
['jupyter>=1.0,<2.0', 'numpy>=1.17,<2.0', 'pandas>=0.25.3,<0.26.0']

setup_kwargs = {
    'name': 'desdeo-tools',
    'version': '0.1.2',
    'description': 'Generic tools and design language used in the DESDEO framework',
    'long_description': None,
    'author': 'Bhupinder Saini',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
