# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zuid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zuid',
    'version': '0.1.1',
    'description': 'Random prefixed ids',
    'long_description': "# zuid\n\nGenerates URL-safe random ids with a prefix and optional timestamp.\n\n\n## Installing\n\n```\npip install zuid\n```\n\n## Usage\n\nThe `ZUID` class works as a callable id factory for a given prefix:\n\n```\n>>> from zuid import ZUID\n>>> generator = ZUID(prefix='user_')\n>>> generator()\n'user_03QewpfEIpPWUICXdgtvdR'\n>>> generator()\n'user_1LJSXMoyH6p7VsiL8wwIm1'\n```\n\nThe factory generates ids that are 22 chars long by default, which in\nbase 62 corresponds to 131 random bits. For comparison, a v4 UUID has\n122 random bits. It can be changed with the `length` parameter:\n\n```\n>>> generator = ZUID(prefix='user_', length=27)\n>>> generator()\n'user_X5fSIStIKpYWcg07nqEfPbMvmME'\n```\n\nWith the `timestamped` parameter, the factory uses the current nanoseconds since epoch as the first 8 bytes, preserving the order when sorting by id.\n\n```\n>>> generator = ZUID(prefix='user_', timestamped=True)\n>>> generator()\n'user_1qzuvBwgHdQVO2gA4GelYX'\n>>> generator()\n'user_1qzuvCscVyClzGaqakgvsl'\n>>> generator()\n'user_1qzuvDb0TuCuIJJON103Of'\n>>> generator()\n'user_1qzuvES4mTQ7fWykywvjNb\n\n```\n",
    'author': 'Pedro Werneck',
    'author_email': 'pjwerneck@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
