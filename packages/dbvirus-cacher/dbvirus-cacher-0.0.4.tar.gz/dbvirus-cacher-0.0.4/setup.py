# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dbvirus_cacher']

package_data = \
{'': ['*']}

install_requires = \
['mongoengine>=0.18.2,<0.19.0', 'pymongo>=3.9,<4.0', 'pytz>=2019.3,<2020.0']

setup_kwargs = {
    'name': 'dbvirus-cacher',
    'version': '0.0.4',
    'description': '',
    'long_description': '# DBVirus - Cacher\n\nSimple MongoDB structures that are shared between the parts of [DBVirus](https://github.com/dbvirus/)\n',
    'author': 'Felipe Rodrigues',
    'author_email': 'felipe@felipevr.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
