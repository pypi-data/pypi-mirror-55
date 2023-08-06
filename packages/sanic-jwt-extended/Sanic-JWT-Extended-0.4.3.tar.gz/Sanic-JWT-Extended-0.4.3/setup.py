# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sanic_jwt_extended']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=1.6.4,<2.0.0', 'sanic>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'sanic-jwt-extended',
    'version': '0.4.3',
    'description': 'Extended JWT integration with Sanic',
    'long_description': '# Sanic-JWT-Extended (NOW PREPARING 1.0 RELEASE WITH MAJOR CHANGES)\n[![Downloads](https://pepy.tech/badge/sanic-jwt-extended)](https://pepy.tech/project/sanic-jwt-extended)\n![PyPI](https://img.shields.io/pypi/v/sanic-jwt-extended.svg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-jwt-extended.svg)\n![code style](https://img.shields.io/badge/code%20style-black-black.svg)\n[![Documentation Status](https://readthedocs.org/projects/sanic-jwt-extended/badge/?version=latest)](https://sanic-jwt-extended.readthedocs.io/en/latest/?badge=latest)\n\n## What is Sanic-JWT-Extended?\nSanic-JWT-Extended is port of Flask-JWT-Extended for Sanic.\n\n## When to use Sanic-JWT-Extended?\nSanic-JWT-Extended not only adds support for using JSON Web Tokens (JWT) to Sanic for protecting views,\nbut also many helpful (and **optional**) features  built in to make working with JSON Web Tokens\neasier. These include:\n\n* Support for adding custom claims to JSON Web Tokens\n* [Refresh tokens](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)\n* Token freshness and separate view decorators to only allow fresh tokens\n* Role-based access control\n* ~~built-in blacklist support~~ <= WIP\n\n## Installation\n```bash\npip install sanic-jwt-extended\n```\n\n## Usage\n[View the documentation online](http://sanic-jwt-extended.readthedocs.io/en/latest/)\n\n## Generating Documentation\nYou can generate a local copy of the documentation. After installing the requirements,\ngo to the `docs` directory and run:\n```\n$ make clean && make html\n```\n',
    'author': 'Seonghyeon Kim',
    'author_email': 'kim@seonghyeon.dev',
    'url': 'https://github.com/NovemberOscar/Sanic-JWT-Extended',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
