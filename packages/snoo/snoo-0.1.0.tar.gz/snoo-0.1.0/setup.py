# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['snoo']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.4,<0.16.0', 'pyxdg>=0.26,<0.27', 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['snoo = src.snoo:run']}

setup_kwargs = {
    'name': 'snoo',
    'version': '0.1.0',
    'description': 'Wrapper around the (undocumented) SNOO Smart Bassinet API',
    'long_description': '# SNOO\n\nThis is an API client to the [SNOO Smart Bassinet](https://www.happiestbaby.com/products/snoo-smart-bassinet). The SNOO is a bassinet that will rock your baby to sleep, and responds to the baby by trying to sooth it with different rocking motions and sounds when it detects crying.\n\nCurrently, it supports getting the current session data from SNOO, and historic data. It does not allow you to control the SNOO (the control API is provided by [PubNub](https://www.pubnub.com) and is different from the read-only data API hosted by happiestbaby.com)\n\n# A word of caution\n\nThe SNOO API is undocumented. Using it might or might not violate Happiest Baby, Inc [Terms of Service](https://www.happiestbaby.com/pages/terms-of-service). Use at your own risk.\n\n# Usage\n\n## Installation\n\n```sh\npip install snoo\n```\n\n## Command line usage\n\nTo get the status of your snoo, simply run\n\n```\n$ snoo\n```\n\nThe first time you run it, it will prompt for your username and password. These will be stored in either `~/.snoo_config` or `~/.config/snoo/snoo.config`, depending on your system. The output of the `snoo` command is the status (`Awake`, `Asleep`, or `Soothing`), and the duration of the current session.\n\n## Programmatic usage\n\n```python\nfrom snoo import Client\n\nclient = Client()\n# Find out where your config is stored\nprint(client.config_path)\n# Get data from your current session\ncurrent_session = client.get_current_session()\n# Print the status of the current session.\nprint(client.status())\n```\n',
    'author': 'Manuel Ebert',
    'author_email': 'manuel@1450.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maebert/snoo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
