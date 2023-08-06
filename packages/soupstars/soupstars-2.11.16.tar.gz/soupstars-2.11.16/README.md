# Soup Stars :stew: :star: :boom:

[![Build Status](https://travis-ci.org/soupstars/soupstars.svg?branch=master)](https://travis-ci.org/soupstars/soupstars)
<!-- [![Coverage Status](https://coveralls.io/repos/github/tjwaterman99/soupstars/badge.svg?branch=master)](https://coveralls.io/github/tjwaterman99/soupstars?branch=master) -->
<!-- [![Docs](https://readthedocs.org/projects/soupstars/badge/?version=latest)](https://soupstars.readthedocs.io/en/latest/?badge=latest) -->
[![Version](https://badge.fury.io/py/soupstars.svg)](https://badge.fury.io/py/soupstars)
[![Python](https://img.shields.io/pypi/pyversions/soupstars.svg)](https://pypi.org/project/soupstars/)

Soup Stars is a framework for building web parsers with Python. It is designed to make building, deploying, and scheduling web parsers easier by simplifying what you need to get started.

## Quickstart

```
pip install soupstars
```

The client is also available as a docker image.

```
docker pull soupstars/client
```

### Building a parser

Create a new parser using the `soupstars` command. The `create` command will use a template parser.

```
soupstars create -m myparser.py
```

Parsers are simple python modules.

```
cat myparser.py
```

Notice that the only set up required is the special `parse` decorator and a variable named `url` for the web page you want to parse.

```python
from soupstars import parse

url = "https://corbettanalytics.com/"

@parse
def h1(soup):
    return soup.h1.text
```

You can test that the parser functions correctly.

```
soupstars run -m myparser.py
```

Use `soupstars --help` to see a full list of available commands.

More documentation is available [here](http://soupstars-docs.s3-website-us-west-2.amazonaws.com/).

## Development

Start the docker services.

```
docker-compose up -d
```

Run the tests.

```
docker-compose run --rm client pytest -vs
```

## Releasing

New tags that pass on CI will automatically be pushed to docker hub.

To deploy to PyPI requires manually running the following commands.

```
pip3 install twine
python3 setup.py sdist bdist_wheel
twine upload dist/*
```
