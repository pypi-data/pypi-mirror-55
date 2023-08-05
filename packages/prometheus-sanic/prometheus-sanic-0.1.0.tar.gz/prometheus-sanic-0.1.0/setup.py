# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['prometheus_sanic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'prometheus-sanic',
    'version': '0.1.0',
    'description': 'Exposes Prometheus monitoring metrics of Sanic apps.',
    'long_description': None,
    'author': 'skar404',
    'author_email': 'skar404@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
