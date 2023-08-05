# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['click_trig']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'emoji>=0.5.4,<0.6.0']

entry_points = \
{'console_scripts': ['trig = click_trig.trig:main']}

setup_kwargs = {
    'name': 'click-trig',
    'version': '0.1.7',
    'description': 'Simple Click app using Trigonometric functions.',
    'long_description': '# trig(beta!!!)\n\n> Trigonometric functions to your command line!\n\n[![CircleCI](https://circleci.com/gh/mrcartoonster/trig_click.svg?style=svg)](https://circleci.com/gh/mrcartoonster/trig_click) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) [![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/mrcartoonster/trig_click.svg)](https://github.com/mrcartoonster/trig_click) ![GitHub commit activity](https://img.shields.io/github/commit-activity/w/mrcartoonster/trig_click)\n\nSimple Cli built that does trigonometric functions right in the command line.\nBrings [OminCalculator.com](https://www.omnicalculator.com/math/sin) to the\ncommand line.\n\n<p align="center">\n    <img\n    src="/notebooks/animation.svg">\n</p>\n\n\n\n![](header.png)\n\n## Installation\n\nOS X & Linux:\n\nUsing [pip](https://pip.pypa.io/en/stable/)\n\n```sh\npip3 install click-trig\n```\n\nUsing [Poetry](https://poetry.eustace.io/docs/)\n\n```sh\npoetry add click-trig\n```\n\nUsing [Pipenv](https://pipenv.readthedocs.io/en/latest/install/)\n```sh\npipenv install --python three click-trig\n```\n\n## Usage example\n\nHave you ever found your self saying "What\'s the length of the Hypotenuse of\nthis triangle that\'s before me or is in my head". Okay, you\'ve never thought of\nthat. If you have, you\'re cool(nerd!!!). But if you\'ve found your self in front\nof a Terminal... Great news, everyone!!! Just pip install my library and type:\n\n```sh\n$ trig pythagoras 22 55\n```\n\n... and Boom! You\'ve answered your question. WITH EMOJIS!!! Soon, you\'ll be able to do all\nyour Trignoemtric functions right from the command line too! You\'ll never forget\nSOH CAH TOA again! It\'ll be in your command line! Enjoy!!! Okay, put in a lot\nof exclamtion points in this README. I\'ll fix that someday.\n\n\n## Development setup\n\nStill developing. Will add how to contribute and set up dev environment in a\nbit. \n\n```sh\npip install something something\n```\n\n### Release History\n\nCan view complete changes at [Changelog](https://github.com/mrcartoonster/trig_click/blob/master/CHANGELOG.md)\n\n### [0.0.1] - 2019-04-17\n#### Added\n- `.gitignore`\n- Added `CHANGELOG.md` and `LICENSE` usin MIT\n\n### [0.0.2] - 2019-04-18\n#### Added\n- Rise notebook\n- Removed non-needed notebooks and scripts\n\n### [0.0.3] - 2019-05-29\n#### Added\n- Stackprinter to code and link list.\n  \n### [0.1.4] - 2019-05-31\n#### Added\n- Implementing Dan Bader\'s readme template\n\n### [0.1.5] - 2019-11-01\n#### Added\n- Added to Pypi\n\n### [0.1.6] - 2019-11-02\n#### Added\n- Added Dan Bader style README.md\n\n## Meta\n\nYour Name \xe2\x80\x93 [@mrcartoonster](https://twitter.com/mrcartoonster) \xe2\x80\x93 mrcartoonster@gmail.com\n\nDistributed under the MIT license. See ``LICENSE`` for more information.\n\n[https://github.com/mrcartoonster/trig_click](https://github.com/mrcartoonster/)\n\n## Contributing\n\n\n1. Fork it (<https://github.com/yourname/yourproject/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am \'Add some fooBar\'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new Pull Request\n\n## [Hub](https://hub.github.com/) instructions below\n\nWill add [Hub](https://hub.github.com/) instructions below so all can be down\nright from the command line quickly and easily. \n',
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
