# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['click_trig']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'emoji>=0.5.4,<0.6.0',
 'ipython>=7.9,<8.0',
 'jupyterlab>=1.2,<2.0']

entry_points = \
{'console_scripts': ['trig = click_trig.trig:main']}

setup_kwargs = {
    'name': 'click-trig',
    'version': '0.1.4',
    'description': 'Simple Click app using Trigonometric functions.',
    'long_description': None,
    'author': 'Evan Baird',
    'author_email': 'mrcartoonster@gmail.com',
    'url': 'https://github.com/mrcartoonster/trig_click',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
