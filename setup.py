# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
    ['copycat',
     'copycat.models',
     'copycat.models.history',
     'copycat.models.move',
     'copycat.services',
     'copycat.shared',
     'copycat.shared.exceptions',
     'copycat.shared.utils',
     'copycat.tool']

package_data = \
    {'': ['*']}

install_requires = \
    ['joblib>=1.4.2,<2.0.0',
     'pyautogui>=0.9.54,<0.10.0',
     'pydantic>=2.4.2,<3.0.0',
     'pynput>=1.7.7,<2.0.0',
     'ttkthemes>=3.2.2,<4.0.0']

entry_points = \
    {'console_scripts': ['copycat = copycat:main']}

setup_kwargs = {
    'name': 'copycat',
    'version': '0.1.2',
    'description': 'A tool that record and replay keyboard and mouse macro.',
    'long_description': '# Copycat\n\n`copycat` is a tool that record and replay mouse and keyboard macro.\n\n## Demo\n\nThis is a short demo of the tool:\n\nhttps://github.com/user-attachments/assets/4ce6616e-8fa1-4efb-8c31-f31bfe8e827c\n\n## Installation\n\nThis tool uses [poetry](https://python-poetry.org/) to manage dependencies and packaging. To install all the\ndependencies simply run:\n\n``` shell\npoetry install\n```\n\n### Installation using pip \nYou can install the tool using pip:\n``` shell\npip install copycat\n```\n\n### Installation using AUR\nIf you are using an Arch-based distribution, you can install the tool using the AUR package:\n``` shell\nyay -S copycat\n```\nRemember to install the other dependencies from the AUR:\n``` shell\nyay -S python-pynput python-pyautogui python-ttkthemes\n```\n\n## Usage\n\nYou can run the tool using poetry:\n\n``` shell\npoetry run copycat --help\n```\n\nOr you can run the tool using python:\n\n``` shell\npython -m copycat --help\n```\n\nOr you can run the tool directly from the directory or add it to your path:\n\n``` shell\ncopycat --help\n```\n\n```shell\nusage: copycat [-h] [--verbose] [--debug] [--quiet | --no-quiet | -q] [--version] [--gui] [--theme THEME] [--speed SPEED] [--reply REPLY]\n\nCopycat is a tool that record and replay mouse and keyboard macro.\n\noptions:\n  -h, --help            show this help message and exit\n  --verbose, -v         Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).\n  --debug               Enable debug mode.\n  --quiet, --no-quiet, -q\n                        Do not print any output/log\n  --version, -V         Show version and exit.\n  --gui                 Run the tool in GUI mode.\n  --theme THEME, -t THEME\n                        Set the "ttkthemes" GUI theme. (Default: equilux)\n  --speed SPEED, -s SPEED\n                        Speed of the macro playback. (Default: 1.0)\n  --reply REPLY, -r REPLY\n                        Define macro name to reply.\n```\n\n### How it works\n\nFirst, you need to record a macro, you can do this by running the tool in GUI mode:\n\n``` shell\ncopycat --gui\n```\n\nIf you want to use a different theme, you can use the `--theme` option:\n\n``` shell\ncopycat --gui --theme "arc"\n```\n\nVisit the [ttkthemes](https://ttkthemes.readthedocs.io/en/latest/themes.html) documentation to see all the available\nthemes.\n\n#### Record a macro\n\nThen you can record a macro by clicking the `record` button. Once you start recording, the GUI will hide so you can\nperform any mouse and keyboard actions.\nIn every moment, press the `ESC` key to `pause` the recording.\nYou can resume the recording pressing again the `record` button, or you can complete the record process and save the\nmacro by clicking on the `save` button.\nSelect the name of the macro and click on the `save` button.\n\n#### Replay a macro\n\nOnce you have a macro saved, you can replay it in two ways:\n\n1. by clicking on the `replay` button, and selecting the macro you want to replay and the replay `speed` (1.0 is the\n   real record speed).\n2. by running the tool with the `--reply` option:\n\n``` shell\ncopycat --reply <macro_name> --speed <speed>\n```\n\n## Development\n\n### Testing\n\nTo run the tests simply run:\n\n``` shell\npoetry run test\n```\n\n### Update `setup.py`\n\nTo update the `setup.py` file with the latest dependencies and versions run:\n\n``` shell\npoetry run poetry2setup > setup.py\n```\n\n### Acknowledgements\n\nThis project was generated using powerful tools and libraries such as [poetry](https://python-poetry.org/),\n[pydantic](https://docs.pydantic.dev/latest/), [pytest](https://docs.pytest.org/en/stable/), [ttkthemes](https://ttkthemes.readthedocs.io/en/latest/authors.html), [pynput](https://pynput.readthedocs.io/en/latest/) [pyautogui](https://pyautogui.readthedocs.io/en/latest/)\nand more, I simply put the pieces together. Please check and support all the tools and libraries used in this project.\n',
    'author': 'ZappaBoy',
    'author_email': 'federico.zappone@justanother.cloud',
    'maintainer': 'ZappaBoy',
    'maintainer_email': 'federico.zappone@justanother.cloud',
    'url': 'https://github.com/ZappaBoy/copycat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.13',
}

setup(**setup_kwargs)
