[![Build Status](https://travis-ci.com/ptrstn/dqmcrawlr.svg?branch=master)](https://travis-ci.com/ptrstn/dqmcrawlr)

# dqmcrawlr

Tool used to crawl a few plots from the CMS Data Quality Monitor web tool.

## Installation

```bash
pip install git+https://github.com/ptrstn/dqmcrawlr
```

### lxplus

Make sure that your Python version is at least ```2.7``` or ```3.4```. If not then [enable a newer version](https://cern.service-now.com/service-portal/article.do?n=KB0000730) with:

```bash
scl enable python27 bash
```

or 

```bash
scl enable rh-python36 bash
```

Then you can install dqmcrawlr it with:

```bash
virtualenv venv
. venv/bin/activate
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

```
usage: dqmcrawl [-h] [-i INPUT] [-r RESOURCE] [-c]

CMS Data Quality Monitor crawler.

optional arguments:
  -h, --help                        show this help message and exit
  -i INPUT, --input INPUT           input file containing one run number and
                                    reconstruction type per line
  -r RESOURCE, --resource RESOURCE  name of the resource/ histogram
  -c, --cached                      Use existing dataset cache to save time
```

### Example

```bash
dqmcrawl --cached --input example/runs.txt --resource "/Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
```

Output:
```
Crawling 11 runs of the resource /Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk

321012 Express... OK    0.28s
825310 Prompt...  ERROR
Unable to find datasets for run 825310
325310 Prompt...  OK    0.30s
321012 Express... OK    0.32s
321012 reReco...  ERROR
Unable to find 'rereco' dataset
325309 Prompt...  OK    0.28s
327244 Express... OK    0.37s
327244 Prompt...  OK    0.96s
306631 reReco...  OK    0.29s
306631 Express... OK    0.29s
306631 Prompt...  OK    0.29s
Done.

All files have been saved in the folder 'TrackEtaPhi_ImpactPoint_GenTk'

Saving dataset cache...
Done.
```

## Development

```bash
git clone https://github.com/ptrstn/dqmcrawlr
cd dqmcrawlr
python3 -m venv venv
. venv/bin/active
pip install -e .
pip install -r testing-requirements.txt
pytest
```

## References

- https://twiki.cern.ch/twiki/bin/viewauth/CMS/DQMToJSON