# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['zipload']
setup_kwargs = {
    'name': 'zipload',
    'version': '0.1.0',
    'description': 'A simply python module to load zip archives into your python path',
    'long_description': None,
    'author': 'Eli Uriegas',
    'author_email': 'eliasuriegas@gmail.com',
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
