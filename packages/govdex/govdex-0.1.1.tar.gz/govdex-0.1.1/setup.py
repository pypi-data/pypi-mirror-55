# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['govdex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'govdex',
    'version': '0.1.1',
    'description': 'Indexing the government',
    'long_description': '# GovDex - Indexing the government\n\nIndexing government structure, points of service, persons of interest etc.\n\n## Roadmap\n\n* POC in Israel - Gathering data\n\n',
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
