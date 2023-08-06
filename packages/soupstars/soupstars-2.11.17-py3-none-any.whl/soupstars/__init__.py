"""
Soup Stars is a framework for building web parsers with Python. It is designed
to make building, deploying, and scheduling web parsers easier by simplifying
what you need to get started.
"""

from soupstars.version import __version__
from soupstars.api import run, fetch, parse
from soupstars.parsers import BeautifulSoupStar, Url
from soupstars.decorators import data, follow, exclude, links
