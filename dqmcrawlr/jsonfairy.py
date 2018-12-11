from dqmcrawlr import cernrequests
from dqmcrawlr.dataset import get_dataset

BASE_URL = "https://cmsweb.cern.ch/dqm/offline/jsonfairy/archive/"


def construct_url(run_number, reconstruction_type, resource):
    dataset = get_dataset(run_number, reconstruction_type)
    return "{}{}{}{}".format(BASE_URL, run_number, dataset, resource)


def get_TrackEtaPhi_ImpactPoint_GenTk(run_number, reconstruction_type):
    resource = "/Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
    url = construct_url(run_number, reconstruction_type, resource)
    return cernrequests.get(url).text
