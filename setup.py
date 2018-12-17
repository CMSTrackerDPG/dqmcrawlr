from setuptools import setup, find_packages

setup(
    name="dqmcrawlr",
    version="0.3",
    desription="CERN CMS Data Quality Monitor JSON crawler.",
    url="https://github.com/ptrstn/dqmcrawlr",
    author="Peter Stein",
    author_email="peter.stein@cern.ch",
    packages=find_packages(),
    install_requires=["requests", "cernrequests"],
    dependency_links=[
        'git+https://github.com/ptrstn/cernrequests.git@master#egg=cernrequests-0.1'
    ],
    entry_points={"console_scripts": ["dqmcrawl=dqmcrawlr.main:main"]},
)
