# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['beanbot']
install_requires = \
['django>=2.2.7,<3.0.0',
 'python-telegram-bot>=12.2.0,<13.0.0',
 'pytz>=2019.3,<2020.0']

setup_kwargs = {
    'name': 'beanbot',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kevin Zúñiga',
    'author_email': 'kevin.zun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
