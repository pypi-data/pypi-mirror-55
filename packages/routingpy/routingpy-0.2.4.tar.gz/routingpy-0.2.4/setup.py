# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['routingpy', 'routingpy.routers']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'routingpy',
    'version': '0.2.4',
    'description': 'One lib to route them all.',
    'long_description': None,
    'author': 'Nils Nolde',
    'author_email': 'nils@gis-ops.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
