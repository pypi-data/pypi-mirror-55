# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['omnio']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.10,<2.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'omnio',
    'version': '1.0.0',
    'description': 'Python 3 library for opening URIs as streaming file-like objects',
    'long_description': None,
    'author': 'Bob Green',
    'author_email': 'rgreen@goscoutgo.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
