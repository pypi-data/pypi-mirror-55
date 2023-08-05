# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nbwatch']

package_data = \
{'': ['*'], 'nbwatch': ['static/css/*', 'templates/*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'flask>=1.1.1,<2.0.0', 'nbconvert>=5.6.1,<6.0.0']

entry_points = \
{'console_scripts': ['nbwatch = nbwatch:run']}

setup_kwargs = {
    'name': 'nbwatch',
    'version': '0.1.0',
    'description': 'Preview IPython notebooks in your browser.',
    'long_description': None,
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
