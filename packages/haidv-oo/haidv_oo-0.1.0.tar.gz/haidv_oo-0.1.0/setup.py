# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haidv_oo']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.0.5,<3.0.0']

setup_kwargs = {
    'name': 'haidv-oo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'naviat',
    'author_email': 'haidv.ict@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
