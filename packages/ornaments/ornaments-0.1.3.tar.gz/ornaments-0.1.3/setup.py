# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ornaments']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ornaments',
    'version': '0.1.3',
    'description': 'A package of useful decorators',
    'long_description': '# ornaments\n\nA package of useful decorators - lets decorate with ornaments',
    'author': 'James Simpson',
    'author_email': 'james.simpson@securetrading.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
