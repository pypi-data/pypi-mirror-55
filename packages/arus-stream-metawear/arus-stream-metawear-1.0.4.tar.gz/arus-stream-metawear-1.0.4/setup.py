# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['arus_stream_metawear']

package_data = \
{'': ['*']}

install_requires = \
['arus>=0.4.0,<0.5.0', 'pymetawear>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'arus-stream-metawear',
    'version': '1.0.4',
    'description': 'arus plugin that helps creating stream for metawear devices',
    'long_description': '## Overview\n\n`arus-stream-metawear` package is a plugin for [`arus`](https://qutang.github.io/arus/) package. It provides extra functionality to stream data from metawear devices in real-time.\n\n[![PyPI version](https://badge.fury.io/py/arus-stream-metawear.svg)](https://badge.fury.io/py/arus-stream-metawear)\n[![Downloads](https://pepy.tech/badge/arus-stream-metawear)](https://pepy.tech/project/arus-stream-metawear)\n[![Build Status](https://github.com/qutang/arus/workflows/Continuous%20integration/badge.svg)](https://github.com/qutang/arus/actions)\n\n### Get started\n\n#### Prerequistes\n\n```bash\npython >= 3.6\n```\n\n##### Linux\n\n```bash\nlibbluetooth-dev\nlibboost-all-dev\nbluez\n```\n\n##### Windows\n\n```bash\nVisual Studio C++ SDK\nWindows SDK (10.0.16299.0)\nWindows SDK (10.0.17763.0)\n```\n\n#### Installation\n\n```bash\n> pip install arus-stream-metawear\n```\n\nOr `pipenv`\n\n```bash\n> pipenv install arus-stream-metawear\n```\n\nOr `poetry`\n\n```bash\n> poetry add arus-stream-metawear\n```\n\n\n### Development\n\n#### Prerequists\n\n```bash\npython >= 3.6\npoetry >= 0.12.17\n```\n\n#### Set up development environment\n\n```bash\n> git clone https://github.com/qutang/arus-stream-metawear.git\n> cd arus-stream-metawear\n> poetry install\n```',
    'author': 'qutang',
    'author_email': 'tqshelly@gmail.com',
    'url': 'https://github.com/qutang/arus-stream-metawear',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
