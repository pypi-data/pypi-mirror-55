# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dysco']

package_data = \
{'': ['*']}

install_requires = \
['python-slugify>=4.0,<5.0']

setup_kwargs = {
    'name': 'dysco',
    'version': '0.0.7',
    'description': 'Dysco provides configurable dynamic scoping behavior in Python.',
    'long_description': '# Dysco\n\n\n## Development\n\nTo install the dependencies locally, you need [poetry](https://poetry.eustace.io/docs/#installation) to be installed.\nYou can then run\n\n```bash\n# This is optional, but highly recommended.\n# It tells poetry to place the virtual environment in `.venv`.\npoetry config settings.virtualenvs.in-project true\n\n# Install all of the dependencies.\npoetry install\n```\n\nto install the project dependencies.\n\nThe library is tested against Python versions 3.7 and 3.8.\nThese are most easily installed using [pyenv](https://github.com/pyenv/pyenv#installation) with the following command.\n\n```bash\n# Install the supported Python versions.\npyenv install --skip-existing 3.7.5\npyenv install --skip-existing 3.8.0\n```\n\nTesting, linting, and document generation can then be run via [tox](https://tox.readthedocs.io/en/latest/).\nThe bare `tox` command will run everything in all environments, or you can break it down by Python version and task.\nFor example, you could run the individual Python 3.8 tasks manually by running the following.\n\n```bash\n# Install the project dependencies in `.tox/py38/`.\ntox -e py38-init\n\n# Run black, flake8, isort, and mypy.\ntox -e py38-lint\n\n# Run the tests and generate a coverage report.\ntox -e py38-test --coverage\n\n## Build the project documentation.\ntox -e py38-docs\n```\n\n## Deployment\n\nYou first need to configure your credentials with poetry.\n\n```bash\npoetry config http-basic.pypi intoli <pypi-password>\n```\n\nYou can then use invoke to bump the version number, commit the changes, tag the version, and deploy to pypi.\n\n```bash\n# Bumps the patch version and deploys the package.\n# Valid options are major, minor, and patch.\ninvoke bump patch\n```\n',
    'author': 'Evan Sangaline',
    'author_email': 'evan@intoli.com',
    'url': 'https://github.com/intoli/dysco/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
