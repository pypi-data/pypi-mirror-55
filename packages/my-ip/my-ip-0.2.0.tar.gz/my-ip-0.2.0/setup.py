# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['my_ip']

package_data = \
{'': ['*'], 'my_ip': ['data/*']}

install_requires = \
['asks>=2.3,<3.0',
 'click>=7.0,<8.0',
 'importlib_metadata>=0.23.0,<0.24.0',
 'loguru>=0.3.2,<0.4.0',
 'pydantic>=1.0,<2.0',
 'pyxdg>=0.26.0,<0.27.0',
 'toml>=0.10.0,<0.11.0',
 'trio>=0.12.1,<0.13.0']

entry_points = \
{'console_scripts': ['mip = my_ip.console:cli']}

setup_kwargs = {
    'name': 'my-ip',
    'version': '0.2.0',
    'description': 'Get your internet IP. Fast.',
    'long_description': '\n============================================\n``my-ip``: Get your public IP address. Fast.\n============================================\n\n|Codacy Badge|\n|Black Badge|\n|Dependabot Badge|\n\n.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/683afc5412064a7da45b9b50ccd79975\n   :target: https://www.codacy.com/manual/lainiwa/my-ip?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=lainiwa/my-ip&amp;utm_campaign=Badge_Grade\n   :alt: Code quality\n\n.. |Black Badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Code style: black\n\n.. |Dependabot Badge| image:: https://api.dependabot.com/badges/status?host=github&repo=lainiwa/my-ip\n   :target: https://dependabot.com\n   :alt: Dependabot\n\n\n.. short-description\n\n``my-ip`` is a simple CLI script,\nthat finds out your public IP\nby asynchronously requesting multiple services.\n\n.. short-description-end\n\n\n\nInstallation and Usage\n======================\n\n.. installation-and-usage\n\n``my-ip`` is a Python-only package `hosted on PyPI`_.\nThe recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing it:\n\n.. _hosted on PyPI: https://pypi.org/project/my_ip/\n\n.. code-block:: console\n\n   $ pip install my_ip\n\n\nNow run it to get your public address!\n\n.. code-block:: console\n\n   $ mip\n   2019-10-12 08:19:58.070 | INFO     | my_ip.console:cli:76 - Standard config not found. Creating new\n   First run.\n   Installing config to `/home/lain/.config/my_ip/config.toml`... Done!\n   185.xxx.xxx.xxx\n\n\nAs you can see, the script installed the configuration script on the first run.\nThe second run will be less verbose though:\n\n.. code-block:: console\n\n   $ mip\n   185.xxx.xxx.xxx\n\n.. installation-and-usage-end\n\n\n\nGetting Help\n============\n\nHave a question? Spotted a bug? File a `new issue`_!\n\n.. _new issue: https://github.com/lainiwa/my-ip/issues/new\n',
    'author': 'lainiwa',
    'author_email': 'kirrik96@gmail.com',
    'url': 'https://github.com/lainiwa/my-ip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
