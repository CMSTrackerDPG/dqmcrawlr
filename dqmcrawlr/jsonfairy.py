import cernrequests

from dqmcrawlr.dqm import DQM_Session


class OfflineJSONFairy:
    BASE_URL = "https://cmsweb.cern.ch/dqm/offline/jsonfairy/archive/"

    def __init__(self, dataset_cache=None):
        self.dqm_session = DQM_Session()
        if dataset_cache:
            self.dqm_session.cache.datasets.update(dataset_cache)

    def _construct_url(self, run_number, reconstruction_type, resource):
        dataset = self.dqm_session.get_dataset(run_number, reconstruction_type)
        return "{}{}{}{}".format(self.BASE_URL, run_number, dataset, resource)

    def get_json(self, run_number, reconstruction_type, resource):
        url = self._construct_url(run_number, reconstruction_type, resource)
        json_response = cernrequests.get(url).json()

        if json_response["hist"] == "unsupported type":
            raise ValueError("Unable to find plot for run '{}'".format(run_number))
        return json_response

    def get_TrackEtaPhi_ImpactPoint_GenTk(self, run_number, reconstruction_type):
        resource = "/Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
        return self.get_json(run_number, reconstruction_type, resource)


class OnlineJSONFairy:
    BASE_URL = "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/"

    def _construct_url(self, run_number, resource):
        dataset = "/Global/Online/ALL"
        return "{}{}{}{}".format(self.BASE_URL, run_number, dataset, resource)

    def get_json(self, run_number, resource):
        url = self._construct_url(run_number, resource)
        json_response = cernrequests.get(url).json()

        if json_response["hist"] == "unsupported type":
            raise ValueError("Unable to find plot for run '{}'".format(run_number))
        return json_response

    def get_TrackEtaPhi_ImpactPoint_GenTk(self, run_number):
        resource = (
            "/Tracking/TrackParameters/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
        )
        return self.get_json(run_number, resource)
