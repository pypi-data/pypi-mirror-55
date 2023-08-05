# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['arus_components_hci']

package_data = \
{'': ['*']}

install_requires = \
['arus>=0.4.6,<0.5.0', 'pysimplegui>=4.4,<5.0']

setup_kwargs = {
    'name': 'arus-components-hci',
    'version': '0.1.1',
    'description': 'arus plugins that include streams, pipelines and broadcasters that may include human computer interactions through GUI, voice or other interfaces.',
    'long_description': None,
    'author': 'qutang',
    'author_email': 'tqshelly@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
