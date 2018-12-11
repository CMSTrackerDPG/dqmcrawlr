from setuptools import setup, find_packages

setup(
    name="dqmcrawlr",
    packages=find_packages(),
    entry_points={"console_scripts": ["dqmcrawl=dqmcrawlr.main:main"]},
)
