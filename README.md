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
usage: dqmcrawl [-h] (--resource RESOURCE | --trackingmap)
                [--force-online | --no-cache]
                input

CMS Data Quality Monitor crawler.

positional arguments:
  input                input file containing one run number and reconstruction
                       type per line

optional arguments:
  -h, --help           show this help message and exit
  --resource RESOURCE  name of the resource/ histogram
  --trackingmap        Shortcut for the TrackEtaPhi_ImpactPoint_GenTk resource
  --force-online       Use only online DQM and ignore reconstruction type.
  --no-cache           Don't use dataset cache for offline DQM.
```

### Example

```bash
dqmcrawl example/runs.txt --trackingmap
```

Output:

```
Crawling 13 runs of the resource TrackEtaPhi_ImpactPoint_GenTk

321012 Express... OK    0.22s
321012 Online...  OK    0.23s
325310 Prompt...  OK    0.35s
321012 Express... OK    0.21s
321012 reReco...  ERROR
reReco dataset does not exist for run '321012'
325309 Prompt...  OK    0.24s
306631 reReco...  OK    0.22s
306631 Express... OK    0.22s
306631 Prompt...  OK    0.22s
327244 Express... ERROR
Unable to find plot 'TrackEtaPhi_ImpactPoint_GenTk' for run '327244'
327244 Prompt...  ERROR
Unable to find plot 'TrackEtaPhi_ImpactPoint_GenTk' for run '327244'
825310 Prompt...  ERROR
Unable to find datasets for run '825310'
325310 SomethingWrong... ERROR
Unknown reconstruction type: 'somethingwrong'
Done.

All files have been saved in the folder 'TrackEtaPhi_ImpactPoint_GenTk'

Saving dataset cache...
Done.

=== Errors ===
RunDoesNotExist:          [('825310', 'Prompt')]
DatasetDoesNotExist:      [('321012', 'reReco')]
UnknownReconstruction:    [('325310', 'SomethingWrong')]
JSONNotFound:             [('327244', 'Express'), ('327244', 'Prompt')]
```

Alternatively you can use ```--resource``` to be more specific about the plot:

```
dqmcrawl example/runs.txt --resource "/Tracking/TrackParameters/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
```

### Online Example

**Note**: When you are only interested in the Online DQM and dont want to modify your runs.txt then you can use the ```--force-online``` parameter. The reconstruction type will then be ignored and duplicate run numbers are removed.

```bash
dqmcrawl example/runs.txt --trackingmap --force-online
```

Output:

```
Crawling 6 runs of the resource TrackEtaPhi_ImpactPoint_GenTk

306631 online...  OK    0.24s
321012 online...  OK    0.37s
325309 online...  OK    0.23s
325310 online...  OK    0.24s
327244 online...  ERROR
Unable to find plot 'TrackEtaPhi_ImpactPoint_GenTk' for run '327244'
825310 online...  ERROR
Unable to find plot 'TrackEtaPhi_ImpactPoint_GenTk' for run '825310'
Done.

All files have been saved in the folder 'TrackEtaPhi_ImpactPoint_GenTk'

=== Errors ===
JSONNotFound:             [('327244', 'online'), ('825310', 'online')]
```

## Notes

The resource name is a little bit different between the Online and the Offline in the CMS GUI.

For example, the resource name of the tracking map lacks a "generalTracks" in the name.

Online name:
- /Tracking/TrackParameters/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk

Offline name:
- /Tracking/TrackParameters/**generalTracks**/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk

## More Examples

The following commands will download the "Quick collection" page of the CMS GUI:

```bash
# 02a - Tracks (pp collisions)
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/NumberOfTracks_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/NumberOfRecHitsPerTrack_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackPt_ImpactPoint_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/Chi2oNDF_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackPhi_ImpactPoint_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackEta_ImpactPoint_GenTk"

# 02b - Total Hits Strip and Pixel (pp)
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/generalTracks/TrackBuilding/NumberOfSeeds_initialStepSeeds_initialStep"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/Pixel/NumberOfRecHitsPerTrack_Pixel_GenTk"

# 06 - Number of Seeds (pp collisions)
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/generalTracks/TrackBuilding/NumberOfSeeds_initialStepSeeds_initialStep"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/generalTracks/TrackBuilding/NumberOfSeeds_lowPtTripletStepSeeds_lowPtTripletStep"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/generalTracks/TrackBuilding/NumberOfSeeds_pixelPairStepSeeds_pixelPairStep"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/generalTracks/TrackBuilding/NumberOfSeeds_detachedTripletStepSeeds_detachedTripletStep"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/generalTracks/TrackBuilding/NumberOfSeeds_mixedTripletStepSeeds_mixedTripletStep"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/generalTracks/TrackBuilding/NumberOfSeeds_pixelLessStepSeeds_pixelLessStep"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/generalTracks/TrackBuilding/NumberOfSeeds_tobTecStepSeeds_tobTecStep"
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