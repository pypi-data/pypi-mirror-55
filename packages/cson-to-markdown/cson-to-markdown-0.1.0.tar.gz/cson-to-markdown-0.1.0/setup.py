# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cson_to_markdown']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.2.1,<0.3.0', 'pyyaml>=5.1,<6.0', 'smart-getenv>=1.1,<2.0']

entry_points = \
{'console_scripts': ['cson_to_markdown = cson_to_markdown:main']}

setup_kwargs = {
    'name': 'cson-to-markdown',
    'version': '0.1.0',
    'description': 'Extracts the markdown section from .cson files.',
    'long_description': None,
    'author': 'Bram Vereertbrugghen',
    'author_email': 'bramvereertbrugghen@live.be',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
