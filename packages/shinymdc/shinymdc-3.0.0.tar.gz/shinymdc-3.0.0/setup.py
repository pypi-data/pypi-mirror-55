# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mdc']

package_data = \
{'': ['*'], 'mdc': ['resources/*', 'templates/*']}

install_requires = \
['shinyutils>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['mdc = mdc.mdc:main']}

setup_kwargs = {
    'name': 'shinymdc',
    'version': '3.0.0',
    'description': 'Tool to compile markdown files to tex/pdf using pandoc, latexmk',
    'long_description': '# mdc\n\nMarkdown to tex/pdf compiler.\n',
    'author': 'Jayanth Koushik',
    'author_email': 'jnkoushik@gmail.com',
    'url': 'https://github.com/jayanthkoushik/mdc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
