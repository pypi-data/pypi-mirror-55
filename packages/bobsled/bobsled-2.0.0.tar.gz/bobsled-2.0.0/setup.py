# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bobsled',
 'bobsled.callbacks',
 'bobsled.environments',
 'bobsled.runners',
 'bobsled.tasks',
 'bobsled.tests']

package_data = \
{'': ['*'], 'bobsled': ['templates/*']}

install_requires = \
['aiofiles>=0.4.0,<0.5.0',
 'aiosqlite>=0.10.0,<0.11.0',
 'argon2_cffi>=19.1,<20.0',
 'asyncpg>=0.19.0,<0.20.0',
 'attrs>=19.3,<20.0',
 'boto3>=1.9,<2.0',
 'databases>=0.2.5,<0.3.0',
 'docker>=4.1,<5.0',
 'flake8>=3.7,<4.0',
 'github3.py>=1.3,<2.0',
 'jinja2>=2.10,<3.0',
 'moto>=1.3,<2.0',
 'passlib>=1.7,<2.0',
 'psycopg2-binary>=2.8,<3.0',
 'pyjwt>=1.7,<2.0',
 'pytest-asyncio>=0.10.0,<0.11.0',
 'pytest>=5.2,<6.0',
 'python-multipart>=0.0.5,<0.0.6',
 'pyyaml>=5.1,<6.0',
 'pyzmq>=18.1,<19.0',
 'starlette>=0.12.10,<0.13.0',
 'uvicorn>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'bobsled',
    'version': '2.0.0',
    'description': '',
    'long_description': None,
    'author': 'James Turk',
    'author_email': 'dev@jamesturk.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
