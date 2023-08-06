# nqm-iot-database-utils-python

Python port of
[`nqminds/nqm-iot-database-utils`][1]

[1]: https://github.com/nqminds/nqm-iot-database-utils

## Installing

Use the below to install as a library using `pip`:

```bash
pip3 install nqm.iotdatabase
# installing the latest git version:
# pip3 install git+https://github.com/nqminds/nqm-iot-database-py.git#egg=nqm.iotdatabase
```

You can replace `pip3` with `poetry` if you prefer.

To download the library, install dependencies for running tests, and build
documentation, do:

```bash
git clone https://github.com/nqminds/nqm-iot-database-py.git
cd nqm-iot-database-py/
poetry install
```

## Documentation

We use Sphinx, Autodoc, Napoleon, and
[`sphinx_autodoc_typehints`](https://github.com/agronholm/sphinx-autodoc-typehints)
to make our documentation.

The below creates html.

```bash
poetry run make html
```

## Tests

### Unittests

```bash
poetry run python -m pytest
```

### Unittests Coverage

```bash
poetry run coverage run --source=nqm -m pytest && poetry run coverage report
```

### Typetests

```bash
poetry run mypy -m nqm.iotdatabase && echo -e "\e[1;32mPass! \e[0m"
```

### Doctests

```bash
poetry run make doctest
```

### Linting

```bash
poetry run pre-commit run --all-files
```

## Possible upgrades to make in SQLAlchemy

- Add sorting on Primary Keys (SQLite feature)
- allow using SQLite URI connections (for read-only)
