# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['phrases_case']

package_data = \
{'': ['*']}

install_requires = \
['six>=1.13,<2.0']

setup_kwargs = {
    'name': 'phrases-case',
    'version': '0.1.0',
    'description': 'Convert phrases between diffrent cases.',
    'long_description': '# phrases_case\n\nConvert phrases between different cases.\n',
    'author': 'NateScarlet',
    'author_email': 'NateScarlet@Gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
