# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kmanga_mobi']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=6.2.1,<7.0.0']

setup_kwargs = {
    'name': 'kmanga-mobi',
    'version': '0.1.0',
    'description': 'mobi package extracted from kmanga',
    'long_description': None,
    'author': 'Alberto Planas',
    'author_email': 'aplanas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whtsky/kmanga_mobi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
