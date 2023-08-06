# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['measurement',
 'measurement.plugins',
 'measurement.plugins.download_speed',
 'measurement.plugins.download_speed.tests']

package_data = \
{'': ['*']}

install_requires = \
['six>=1.12,<2.0', 'validators>=0.13.0,<0.14.0']

extras_require = \
{':python_version == "3.6"': ['dataclasses>=0.6.0,<0.7.0']}

setup_kwargs = {
    'name': 'honestybox-measurement',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Stuart Dines',
    'author_email': 'me@stuartdines.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
