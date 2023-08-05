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
    'version': '0.1.5',
    'description': 'Simple Click app using Trigonometric functions.',
    'long_description': '# trig(beta!!!)\n\n> Trigonometric functions to your command line!\n\n[![CircleCI](https://circleci.com/gh/mrcartoonster/trig_click.svg?style=svg)](https://circleci.com/gh/mrcartoonster/trig_click) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) [![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/mrcartoonster/trig_click.svg)](https://github.com/mrcartoonster/trig_click) ![GitHub commit activity](https://img.shields.io/github/commit-activity/w/mrcartoonster/trig_click)\n\nSimple Cli built that does trigonometric functions right in the command line.\nBrings [OminCalculator.com](https://www.omnicalculator.com/math/sin) to the\ncommand line.\n\n<p align="center">\n    <img\n    src="/notebooks/animation.svg">\n</p>\n\n# [PyGirls 04/29/19 Meetup](https://www.meetup.com/Salt-Lake-Pyladies/events/259042408/) Learning Click!\n\n\n## Hosted Live\n\nThis repo is hosted live on [mybinder.org](https://mybinder.org/) so you won\'t\nhave to fork, download or print anything. You don\'t even need Python, Jupyter\nNotebook/Lab/Anaconda installed on your machine to view this repo to go\nthrough the notebooks and code. Just click the cool mybinder badge and\nyou\'ll have access to the notebooks and code live! You\'ll be able to edit them\nand print them if you\'d like.\n\nWill take a while to load the first time but will load quicker on the next load.\nProvided I don\'t make major changes...\n\n## Goals\n\nTo have an easy access to material covered at the meet up and have a live\nversion whereever you are.\n\n## License\n\nBSD licensed\n\n## Changelog\n\nThe format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\nand this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n',
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
