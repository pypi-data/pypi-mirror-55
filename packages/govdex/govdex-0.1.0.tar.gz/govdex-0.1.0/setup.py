# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['govdex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'govdex',
    'version': '0.1.0',
    'description': 'Indexing the government',
    'long_description': None,
    'author': 'Yehuda Deutsch',
    'author_email': 'yeh@uda.co.il',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://govdex.org',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
