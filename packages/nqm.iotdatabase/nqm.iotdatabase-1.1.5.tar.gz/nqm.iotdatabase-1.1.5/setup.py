# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nqm', 'nqm.iotdatabase', 'nqm.iotdatabase.ndarray']

package_data = \
{'': ['*']}

install_requires = \
['future>=0.18.2,<0.19.0',
 'mongosql>=2.0.8,<3.0.0',
 'numpy>=1.17.4,<2.0.0',
 'shortuuid>=0.5.0,<0.6.0',
 'sqlalchemy>=1.3.11,<2.0.0']

setup_kwargs = {
    'name': 'nqm.iotdatabase',
    'version': '1.1.5',
    'description': 'Library for accessing a local nqm-iot-database',
    'long_description': '# nqm-iot-database-utils-python\n\nPython port of\n[`nqminds/nqm-iot-database-utils`][1]\n\n[1]: https://github.com/nqminds/nqm-iot-database-utils\n\n## Installing\n\nUse the below to install as a library using `pip`:\n\n```bash\npip3 install nqm.iotdatabase\n# installing the latest git version:\n# pip3 install git+https://github.com/nqminds/nqm-iot-database-py.git#egg=nqm.iotdatabase\n```\n\nYou can replace `pip3` with `poetry` if you prefer.\n\nTo download the library, install dependencies for running tests, and build\ndocumentation, do:\n\n```bash\ngit clone https://github.com/nqminds/nqm-iot-database-py.git\ncd nqm-iot-database-py/\npoetry install\n```\n\n## Documentation\n\nWe use Sphinx, Autodoc, Napoleon, and\n[`sphinx_autodoc_typehints`](https://github.com/agronholm/sphinx-autodoc-typehints)\nto make our documentation.\n\nThe below creates html.\n\n```bash\npoetry run make html\n```\n\n## Tests\n\n### Unittests\n\n```bash\npoetry run python -m pytest\n```\n\n### Unittests Coverage\n\n```bash\npoetry run coverage run --source=nqm -m pytest && poetry run coverage report\n```\n\n### Typetests\n\n```bash\npoetry run mypy -m nqm.iotdatabase && echo -e "\\e[1;32mPass! \\e[0m"\n```\n\n### Doctests\n\n```bash\npoetry run make doctest\n```\n\n### Linting\n\n```bash\npoetry run pre-commit run --all-files\n```\n\n## Possible upgrades to make in SQLAlchemy\n\n- Add sorting on Primary Keys (SQLite feature)\n- allow using SQLite URI connections (for read-only)\n',
    'author': 'Alois Klink',
    'author_email': 'alois.klink@gmail.com',
    'url': 'https://github.com/nqminds/nqm-iot-database-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
