# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['patroni_notifier']

package_data = \
{'': ['*'], 'patroni_notifier': ['templates/*']}

install_requires = \
['boto3>=1.10.12,<2.0.0',
 'click>=7.0,<8.0',
 'python-consul>=1.1.0,<2.0.0',
 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['swarm-ctl = swarm_controller.core:swarm_ctl']}

setup_kwargs = {
    'name': 'patroni-notifier',
    'version': '0.0.1',
    'description': 'Patoni notification system using jinja2 templates',
    'long_description': '# Swarm Controller\n\n![](https://github.com/jaredvacanti/swarm-controller/workflows/Publish%20to%20PyPI/badge.svg)\n![PyPI](https://img.shields.io/pypi/v/swarm-controller?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/swarm-controller?style=flat-square)\n\nThis is a simple package to manage the bootstrapping \nand maintenance of a Docker Swarm Cluster.\n\nCurrently only AWS is supported (requiring access to the \nmetadata service). Eventually we will allow other metadata\nstores like etcd or Consul.\n\n## Installation\n\n```\npip install swarm-controller\n```\n\n## Usage\n\nBootstrap a node:\n```\nswarm-ctl bootstrap\n```\n\nCleanup & Maintenance\n```\nswarm-ctl cleanup\nswarm-ctl relabel\n```\n\n## Tests\n\n```\npoetry run tox\n```\n\n## License\n \nThe MIT License (MIT)\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWAR',
    'author': 'Jared Vacanti',
    'author_email': 'jaredvacanti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaredvacanti/patroni-notifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
