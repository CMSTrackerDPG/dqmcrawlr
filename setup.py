import codecs
import os
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="dqmcrawlr",
    version=find_version("dqmcrawlr", "__init__.py"),
    desription="CERN CMS Data Quality Monitor JSON crawler.",
    url="https://github.com/ptrstn/dqmcrawlr",
    author="Peter Stein",
    author_email="peter.stein@cern.ch",
    packages=find_packages(),
    install_requires=["requests", "cernrequests"],
    entry_points={"console_scripts": ["dqmcrawl=dqmcrawlr.main:main"]},
)
