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
mkdir -p ~/private
openssl pkcs12 -clcerts -nokeys -in myCertificate.p12 -out ~/private/usercert.pem
openssl pkcs12 -nocerts -in myCertificate.p12 -out ~/private/userkey.tmp.pem
openssl rsa -in ~/private/userkey.tmp.pem -out ~/private/userkey.pem
```

The certificates have to be **passwordless**.

Then download the [CERN ROOT certificate](https://cafiles.cern.ch/cafiles/certificates/CERN%20Root%20Certification%20Authority%202.crt) at [https://cafiles.cern.ch/cafiles/](https://cafiles.cern.ch/cafiles/certificates/Download.aspx?ca=grid) and copy into ```~/private/root.crt```:

```bash
wget https://cafiles.cern.ch/cafiles/certificates/CERN%20Root%20Certification%20Authority%202.crt -O ~/private/root.crt
```

After that you have to convert into a PEM format with:

```bash
cd ~/private/
openssl x509 -inform der -in root.crt -out root.pem
```


## Usage

After you have installed dqmcrawlr with pip the dqmcrawlr cli script should be available.

```bash
dqmcrawlr --help
```

### Example

```bash
dqmcrawl --input example/runs.txt --resource "/Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
```

Output:
```
Crawling 5 runs of the resource /Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk
Crawling 321012 Express... OK
Crawling 825310 Prompt... ERROR
Crawling 325310 Prompt... OK
Crawling 321012 Express... OK
Crawling 325309 Prompt... OK
Done.

All files have been saved in the folder 'TrackEtaPhi_ImpactPoint_GenTk'
```

## Development

```bash
git clone https://github.com/ptrstn/dqmcrawlr
cd dqmcrawlr
python3 -m venv venv
. venv/bin/active
pip install -r requirements.txt
pip install -r testing-requirements.txt
pip install -e .
pytest
```

## References

- https://twiki.cern.ch/twiki/bin/viewauth/CMS/DQMToJSON
