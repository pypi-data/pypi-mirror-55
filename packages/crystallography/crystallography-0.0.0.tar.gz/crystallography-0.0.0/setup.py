# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['crystallography']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'crystallography',
    'version': '0.0.0',
    'description': 'Library for dealing with crystallography.',
    'long_description': 'crystallography\n===============\n\nLibrary for dealing with crystallography.\n',
    'author': 'Dominik Steinberger',
    'author_email': 'crystallography@steinberger.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
