# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ornaments']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ornaments',
    'version': '0.1.1',
    'description': 'A package of useful decorators',
    'long_description': '# ornaments\n\nA package of useful decorators - lets decorate with ornaments',
    'author': 'James Simpson',
    'author_email': 'james.simpson@securetrading.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
