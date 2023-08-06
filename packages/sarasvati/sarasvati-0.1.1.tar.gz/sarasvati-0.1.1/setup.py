# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sarasvati',
 'sarasvati.api',
 'sarasvati.brain',
 'sarasvati.brain.components',
 'sarasvati.brain.storage',
 'sarasvati.commands',
 'sarasvati.config',
 'sarasvati.packages',
 'sarasvati.packages.metadata',
 'sarasvati.plugins',
 'sarasvati.storage']

package_data = \
{'': ['*'], 'sarasvati': ['core/*']}

install_requires = \
['ansimarkup>=1.4,<2.0',
 'autoflake>=1.3,<2.0',
 'hashids>=1.2,<2.0',
 'munch>=2.3,<3.0',
 'prompt_toolkit>=2.0,<3.0',
 'pygments>=2.4,<3.0',
 'pyqt5>=5.13,<6.0',
 'pyyaml>=5.1,<6.0',
 'requests>=2.22,<3.0',
 'tinydb>=3.13,<4.0',
 'yapsy>=1.12,<2.0']

entry_points = \
{'console_scripts': ['sarasvati = sarasvati:main']}

setup_kwargs = {
    'name': 'sarasvati',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Advaita Krishna das',
    'author_email': 'advaita.krishna.das@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
