import cernrequests

from dqmcrawlr.dqm import DQM_Session

BASE_URL = "https://cmsweb.cern.ch/dqm/offline/jsonfairy/archive/"


class JSON_Fairy:
    def __init__(self, dataset_cache=None):
        self.dqm_session = DQM_Session()
        if dataset_cache:
            self.dqm_session.cache.datasets.update(dataset_cache)

    def _construct_url(self, run_number, reconstruction_type, resource):
        dataset = self.dqm_session.get_dataset(run_number, reconstruction_type)
        return "{}{}{}{}".format(BASE_URL, run_number, dataset, resource)

    def get_json(self, run_number, reconstruction_type, resource):
        url = self._construct_url(run_number, reconstruction_type, resource)
        return cernrequests.get(url).json()

    def get_TrackEtaPhi_ImpactPoint_GenTk(self, run_number, reconstruction_type):
        resource = "/Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
        return self.get_json(run_number, reconstruction_type, resource)
