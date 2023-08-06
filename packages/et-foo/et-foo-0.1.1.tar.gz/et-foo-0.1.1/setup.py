# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['et_foo', 'et_foo.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'cookiecutter>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'et-foo',
    'version': '0.1.1',
    'description': '<Enter a one-sentence description of this project here.>',
    'long_description': '======\net-foo\n======\n\n\n\n<Enter a one-sentence description of this project here.>\n\n\n* Free software: MIT license\n* Documentation: https://et-foo.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n',
    'author': 'Engelbert Tijskens',
    'author_email': 'engelbert.tijskens@uantwerpen.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etijskens/et-foo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
