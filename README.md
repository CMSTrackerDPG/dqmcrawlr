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

### Quick Collections

#### Offline

##### Tracking

The following commands will download all histograms of the "Quick collection" page of the Tracking workspace in the CMS GUI:

```bash
# 02a - Tracks (pp collisions)
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/NumberOfTracks_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/NumberOfRecHitsPerTrack_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackPt_ImpactPoint_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/Chi2oNDF_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackPhi_ImpactPoint_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackEta_ImpactPoint_GenTk"

# 02b - Total Hits Strip and Pixel (pp)
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/Strip/NumberOfRecHitsPerTrack_Strip_GenTk"
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

##### PixelPhase1

```bash
# Rate of Pixel Events by BX
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/eventrate_per_BX"

# **TProfile** !!! N dead ROCs
dqmcrawl runs.txt --resource "/PixelPhase1/deadRocTotal"

# PixelPhas1 Digi ADC Barrel
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_digis_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/adc_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_digis_per_LumiBlock_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/adc_per_LumiBlock_PXBarrel"

# PixelPhas1 Digi ADC Endcap
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_digis_PXForward"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/adc_PXForward"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_digis_per_LumiBlock_PXForward"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/adc_per_LumiBlock_PXForward"

# PixelPhase1 Cluster Number
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_clusters_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_clusters_PXForward"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_clusters_per_LumiBlock_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_clusters_per_LumiBlock_PXForward"

# ntracks
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/ntracks"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/ntracksinpixvolume"

# Charge and size
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/charge_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/charge_PXForward"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/size_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/size_PXForward"

# Cluster on track charge per Inner
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeInner_PXLayer_1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeInner_PXLayer_2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeInner_PXLayer_3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeInner_PXLayer_4"

# Cluster on track charge per Outer
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeOuter_PXLayer_1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeOuter_PXLayer_2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeOuter_PXLayer_3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeOuter_PXLayer_4"

# Cluster charge (on-track) per Disk
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_+1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_+2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_+3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_-1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_-2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_-3"

# PixelPhase1 Residuals
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/residual_x_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/residual_x_PXForward"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/residual_y_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/residual_y_PXForward"

# Cluster size (on-track) per  
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/size_PXLayer_1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/size_PXLayer_2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/size_PXLayer_3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/size_PXLayer_4"

# Cluster size (on-track) per Disk
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_+1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_+2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_+3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_-1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_-2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_-3"
```

##### SiStrip

```bash
# FED Detected Errors Summary
dqmcrawl runs.txt --resource "/SiStrip/ReadoutView/FED/nFEDErrors"
dqmcrawl runs.txt --resource "/SiStrip/ReadoutView/Fiber/nBadActiveChannelStatusBits"

# OnTrackCluster (StoN)
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TIB/Summary_ClusterStoNCorr_OnTrack__TIB"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TOB/Summary_ClusterStoNCorr_OnTrack__TOB"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TID/MINUS/Summary_ClusterStoNCorr_OnTrack__TID__MINUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TID/PLUS/Summary_ClusterStoNCorr_OnTrack__TID__PLUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TEC/MINUS/Summary_ClusterStoNCorr_OnTrack__TEC__MINUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TEC/PLUS/Summary_ClusterStoNCorr_OnTrack__TEC__PLUS"

# OffTrackCluster (Total Number)
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TIB/Summary_TotalNumberOfClusters_OffTrack__TIB"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TOB/Summary_TotalNumberOfClusters_OffTrack__TOB"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TID/MINUS/Summary_TotalNumberOfClusters_OffTrack__TID__MINUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TID/PLUS/Summary_TotalNumberOfClusters_OffTrack__TID__PLUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TEC/MINUS/Summary_TotalNumberOfClusters_OffTrack__TEC__MINUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TEC/PLUS/Summary_TotalNumberOfClusters_OffTrack__TEC__PLUS"
```


#### Online

##### Tracking

The following commands will download all histograms of the "Quick collection" page of the Tracking workspace in the CMS GUI:

```bash
# 02a - Tracks (pp collisions)
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/GeneralProperties/NumberOfTracks_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/HitProperties/NumberOfRecHitsPerTrack_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/GeneralProperties/TrackPt_ImpactPoint_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/GeneralProperties/Chi2oNDF_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/GeneralProperties/TrackPhi_ImpactPoint_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/GeneralProperties/TrackEta_ImpactPoint_GenTk"

# 02b - Total Hits Strip and Pixel (pp)
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/HitProperties/Strip/NumberOfRecHitsPerTrack_Strip_GenTk"
dqmcrawl runs.txt --resource "/Tracking/TrackParameters/HitProperties/Pixel/NumberOfRecHitsPerTrack_Pixel_GenTk"
```

##### PixelPhase1

```bash
# Rate of Pixel Events by BX
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/eventrate_per_BX"

# PixelPhas1 Digi ADC Barrel
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_digis_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/adc_PXBarrel"

# PixelPhas1 Digi ADC Endcap
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_digis_PXForward"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/adc_PXForward"

# PixelPhase1 Cluster Number
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_clusters_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Phase1_MechanicalView/num_clusters_PXForward"

# ntracks
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/ntracks"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/ntracksinpixvolume"

# Charge and size
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/charge_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/charge_PXForward"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/size_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/size_PXForward"

# Cluster on track charge per Inner
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeInner_PXLayer_1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeInner_PXLayer_2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeInner_PXLayer_3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeInner_PXLayer_4"

# Cluster on track charge per Outer
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeOuter_PXLayer_1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeOuter_PXLayer_2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeOuter_PXLayer_3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/chargeOuter_PXLayer_4"

# Cluster charge (on-track) per Disk
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_+1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_+2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_+3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_-1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_-2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/charge_PXDisk_-3"

# PixelPhase1 Residuals
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/residual_x_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/residual_x_PXForward"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/residual_y_PXBarrel"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/residual_y_PXForward"

# Cluster size (on-track) per  
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/size_PXLayer_1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/size_PXLayer_2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/size_PXLayer_3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXBarrel/size_PXLayer_4"

# Cluster size (on-track) per Disk
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_+1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_+2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_+3"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_-1"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_-2"
dqmcrawl runs.txt --resource "/PixelPhase1/Tracks/PXForward/size_PXDisk_-3"
```

##### SiStrip

```bash
# FED Detected Errors Summary
dqmcrawl runs.txt --resource "/SiStrip/ReadoutView/FED/nFEDErrors"
dqmcrawl runs.txt --resource "/SiStrip/ReadoutView/Fiber/nBadActiveChannelStatusBits"

# OnTrackCluster (StoN)
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TIB/Summary_ClusterStoNCorr_OnTrack__TIB"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TOB/Summary_ClusterStoNCorr_OnTrack__TOB"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TID/MINUS/Summary_ClusterStoNCorr_OnTrack__TID__MINUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TID/PLUS/Summary_ClusterStoNCorr_OnTrack__TID__PLUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TEC/MINUS/Summary_ClusterStoNCorr_OnTrack__TEC__MINUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TEC/PLUS/Summary_ClusterStoNCorr_OnTrack__TEC__PLUS"

# OffTrackCluster (Total Number)
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TIB/Summary_TotalNumberOfClusters_OffTrack__TIB"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TOB/Summary_TotalNumberOfClusters_OffTrack__TOB"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TID/MINUS/Summary_TotalNumberOfClusters_OffTrack__TID__MINUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TID/PLUS/Summary_TotalNumberOfClusters_OffTrack__TID__PLUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TEC/MINUS/Summary_TotalNumberOfClusters_OffTrack__TEC__MINUS"
dqmcrawl runs.txt --resource "/SiStrip/MechanicalView/TEC/PLUS/Summary_TotalNumberOfClusters_OffTrack__TEC__PLUS"
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
