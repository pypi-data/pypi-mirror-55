# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['generic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'generic',
    'version': '1.0.0b1',
    'description': 'Generic programming library for Python',
    'long_description': '# Generic programming library for Python\n\nGeneric is trying to provide a Python programmer with primitives for creating\nreusable software components by employing advanced techniques of OOP and other\nprogramming paradigms.\n\nYou can read\n[documentation](http://generic.readthedocs.org/en/latest/index.html) hosted at\nexcellent readthedocs.org project. Development takes place on\n[github](http://github.com/gaphor/generic).\n\n',
    'author': 'Andrey Popp',
    'author_email': '8mayday@gmail.com',
    'maintainer': 'Arjan Molenaar',
    'maintainer_email': 'gaphor@gmail.com',
    'url': 'https://generic.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
