import json
import re

import cernrequests

from .exceptions import RunDoesNotExist, DatasetDoesNotExist

OFFLINE_URL = "https://cmsweb.cern.ch/dqm/offline/"
ONLINE_URL = "https://cmsweb.cern.ch/dqm/online/"


class DQM_Cache:
    def __init__(self):
        self.datasets = {}
        self.lumis = {}  # TODO

    def update_datasets(self, run_number, datasets):
        self.datasets[str(run_number)] = datasets

    def get_datasets(self, run_number):
        return self.datasets.get(run_number, None)


class DQM_Session:
    def __init__(self):
        self.session_url = get_offline_session_url()
        self.cache = DQM_Cache()

    def get_available_datasets(self, run_number):
        """
        Retrieving a list of all available datasets for a specific run
        in a very painful and slow way

        First sets the Session to choose Samples by doing:
        '/chooseSample?vary=run;order=dataset'

        then sets the Session to click on the "any" checkbox by doing:
        "/modify?vary=any"

        then sets the Session to use the given run number by doing:
        "/modify?pat=321012"

        :param run_number: Run number
        :return: list of datasets
        """
        run_number = str(run_number)
        if run_number in self.cache.datasets:
            return self.cache.datasets[run_number]

        first_step = "/chooseSample?vary=run;order=dataset"
        second_step = "/modify?vary=any;pat={}".format(run_number)

        cernrequests.get("{}{}".format(self.session_url, first_step))
        response = cernrequests.get("{}{}".format(self.session_url, second_step))

        # Make response json compatible
        text = re.sub("'", '"', response.text)[1:-1]
        json_response = json.loads(text)

        try:
            items = json_response[1]["items"][0]["items"]
        except IndexError:
            raise RunDoesNotExist(
                "Unable to find datasets for run {}".format(run_number)
            )
        datasets = [item["dataset"] for item in items]

        self.cache.update_datasets(run_number, datasets)
        return datasets

    def get_dataset(self, run_number, reconstruction_type):
        datasets = self.get_available_datasets(run_number)
        return _extract_dataset(datasets, reconstruction_type)

    def get_lumisections(self, run_number, reconstruction_type):
        if run_number in self.cache.lumis:
            return self.cache.lumis[run_number]

        dataset = self.get_dataset(run_number, reconstruction_type)
        dataset_encoded = dataset.replace("/", "%2F")

        third_step = (
            "/state?auto=300000;latency=3685;call=852;server=778.517332;render=12"
        )
        fourth_step = "/select?type=offline_data;dataset={};runnr={};importversion=1".format(
            dataset_encoded, run_number
        )

        cernrequests.get("{}{}".format(self.session_url, third_step))
        response = cernrequests.get("{}{}".format(self.session_url, fourth_step))

        lumis = eval(response.text)[1]["lumi"]
        self.cache.lumis[run_number] = lumis

        return lumis


def _get_session_url(base_url):
    request = cernrequests.get(base_url)
    page_content = request.content.decode("utf-8")

    session_id = re.search(r"session\/.*'", page_content).group()
    session_id = re.sub(r"'", "", session_id)

    return "{}{}".format(base_url, session_id)


def get_offline_session_url():
    """
    Example:
    'https://cmsweb.cern.ch/dqm/offline/session/T9JQR0'

    :return: DQM offline GUI url containing a session
    """
    return _get_session_url(OFFLINE_URL)


def get_online_session_url():
    """
    Example:
    'https://cmsweb.cern.ch/dqm/online/session/BDjs3F'

    :return: DQM online GUI url containing a session
    """
    return _get_session_url(ONLINE_URL)


def _extract_dataset(datasets, reco):
    """
    This is horrible code, please improve it.
    """

    reco = reco.lower()
    filtered = None
    if "express" == reco:
        filtered = list(
            filter(
                lambda dataset: (
                    "/StreamExpress/" in dataset
                    or "/StreamExpressCosmics/" in dataset
                    or "/StreamHIExpress/" in dataset
                )
                and "-Express-" in dataset
                and "/DQM" in dataset,
                datasets,
            )
        )
    elif "prompt" == reco:
        # Done in multiple steps because there are weird runs that match all 3 filter sets e.g. "325680"
        filtered = list(
            filter(
                lambda dataset: "/Cosmics/" in dataset
                and "-PromptReco-" in dataset
                and "/DQM" in dataset,
                datasets,
            )
        )
        if not filtered:
            filtered = list(
                filter(
                    lambda dataset: "/ZeroBias/" in dataset
                    and "-PromptReco-" in dataset
                    and "/DQM" in dataset,
                    datasets,
                )
            )

        if not filtered:
            filtered = list(
                filter(
                    lambda dataset: "/MinimumBias/" in dataset
                    and "-PromptReco-" in dataset
                    and "/DQM" in dataset,
                    datasets,
                )
            )

        if not filtered:
            filtered = list(
                filter(
                    lambda dataset: "/HIMinimumBias" in dataset
                    and "-PromptReco-" in dataset
                    and "/DQM" in dataset,
                    datasets,
                )
            )
            # Use HIMinimumBias with biggest number e.g. HIMinimumBias1 instead of HIMinimumBias0
            filtered.sort(reverse=True)
            filtered = [filtered[0]]
    elif "rereco" == reco:
        filtered = list(
            filter(
                lambda dataset: "/SingleTrack/" in dataset
                and "-PromptReco-" not in dataset
                and "-Express-" not in dataset
                and "/DQM" in dataset,
                datasets,
            )
        )
    else:
        raise ValueError("Unknown reconstruction type: '{}'".format(reco))

    if not filtered:
        raise DatasetDoesNotExist("Unable to find '{}' dataset".format(reco))
    assert len(filtered) == 1
    return filtered[0]


def get_dataset(run_number, reconstruction_type):
    return DQM_Session().get_dataset(run_number, reconstruction_type)


def get_lumisections(run_number, reconstruction_type):
    return DQM_Session().get_lumisections(run_number, reconstruction_type)
