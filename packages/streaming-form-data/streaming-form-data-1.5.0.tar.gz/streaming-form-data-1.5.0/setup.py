# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['streaming_form_data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'streaming-form-data',
    'version': '1.5.0',
    'description': 'Streaming parser for multipart/form-data',
    'long_description': None,
    'author': 'Siddhant Goel',
    'author_email': 'me@sgoel.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
