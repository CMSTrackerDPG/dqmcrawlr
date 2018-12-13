[![Build Status](https://travis-ci.com/ptrstn/dqmcrawlr.svg?branch=master)](https://travis-ci.com/ptrstn/dqmcrawlr)

# dqmcrawlr

Tool used to crawl a few plots from the CMS Data Quality Monitor web tool.

## Installation

```bash
pip install git+https://github.com/ptrstn/dqmcrawlr
```

## Prerequisites

Request a [Grid User Certificate](https://ca.cern.ch/ca/) and convert into public and private key:

```bash
mkdir -p ~/.globus
openssl pkcs12 -clcerts -nokeys -in myCertificate.p12 -out ~/.globus/usercert.pem
openssl pkcs12 -nocerts -in myCertificate.p12 -out ~/.globus/userkey.tmp.pem
openssl rsa -in ~/.globus/userkey.tmp.pem -out ~/.globus/userkey.pem
```

The certificates have to be **passwordless**.

## Usage

After you have installed dqmcrawlr with pip the dqmcrawlr cli script should be available.

```bash
dqmcrawl --help
```

### Example

```bash
dqmcrawl --input example/runs.txt --resource "/Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
```

Output:
```
Crawling 5 runs of the resource /Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk
Crawling 321012 Express... OK   1.96s
Crawling 825310 Prompt...  ERROR
Unable to find datasets for run 825310
Crawling 325310 Prompt...  OK   2.02s
Crawling 321012 Express... OK   2.11s
Crawling 325309 Prompt...  OK   2.13s
Done.

All files have been saved in the folder 'TrackEtaPhi_ImpactPoint_GenTk'
```

## Development

```bash
git clone https://github.com/ptrstn/dqmcrawlr
cd dqmcrawlr
python3 -m venv venv
. venv/bin/active
pip install --process-dependency-links -e .
pip install -r testing-requirements.txt
pytest
```

## References

- https://twiki.cern.ch/twiki/bin/viewauth/CMS/DQMToJSON