# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['parseridge',
 'parseridge.corpus',
 'parseridge.parser',
 'parseridge.parser.evaluation',
 'parseridge.parser.evaluation.callbacks',
 'parseridge.parser.modules.attention',
 'parseridge.parser.training',
 'parseridge.parser.training.callbacks',
 'parseridge.scripts',
 'parseridge.utils']

package_data = \
{'': ['*'], 'parseridge.parser': ['modules/*']}

install_requires = \
['conllu>=1.3,<1.4',
 'pygsheets>=2.0,<3.0',
 'pyyaml>=5.1,<6.0',
 'torchvision>=0.3.0,<0.4.0',
 'tqdm>=4.32,<5.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['torch==1.3.0',
                                                         'dataclasses>=0.7,<0.8'],
 ':python_version >= "3.7" and python_version < "4.0"': ['torch>=1.3.0,<2.0.0']}

setup_kwargs = {
    'name': 'parseridge',
    'version': '0.1.0',
    'description': 'A transition-based dependency parser backed by attention mechanisms.',
    'long_description': None,
    'author': 'Johannes Gontrum',
    'author_email': 'j@gontrum.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
