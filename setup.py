from setuptools import setup, find_packages

setup(
    name="dqmcrawlr",
    version="0.3.2",
    desription="CERN CMS Data Quality Monitor JSON crawler.",
    url="https://github.com/ptrstn/dqmcrawlr",
    author="Peter Stein",
    author_email="peter.stein@cern.ch",
    packages=find_packages(),
    install_requires=["requests", "cernrequests"],
    entry_points={"console_scripts": ["dqmcrawl=dqmcrawlr.main:main"]},
)
