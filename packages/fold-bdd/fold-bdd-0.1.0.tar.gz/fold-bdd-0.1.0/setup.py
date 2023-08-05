# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fold_bdd']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0', 'dd>=0.5.4,<0.6.0', 'funcy>=1.13,<2.0']

setup_kwargs = {
    'name': 'fold-bdd',
    'version': '0.1.0',
    'description': 'Library for folding (or reducing) over a Reduced Ordered Binary Decision Diagram.',
    'long_description': None,
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
