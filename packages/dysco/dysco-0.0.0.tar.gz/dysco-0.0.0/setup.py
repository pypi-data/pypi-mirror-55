# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dysco']

package_data = \
{'': ['*']}

install_requires = \
['python-slugify>=4.0,<5.0']

setup_kwargs = {
    'name': 'dysco',
    'version': '0.0.0',
    'description': 'Dysco provides configurable dynamic scoping behavior in Python.',
    'long_description': None,
    'author': 'Evan Sangaline',
    'author_email': 'evan@intoli.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
