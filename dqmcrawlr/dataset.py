import json
import re

import cernrequests

from dqmcrawlr.dqm import get_offline_session_url
from dqmcrawlr.exceptions import RunDoesNotExist


def translate_reconstruction_type(reconstruction_type):
    """
    Returns the correct reconstruction type name

    :param reconstruction_type: "Express" or "Prompt"
    :return: list of possible reconstruction types
    """

    reco = reconstruction_type.lower()

    if reco == "express":
        return ["StreamExpressCosmics", "StreamExpress"]
    if reco == "prompt":
        return ["Cosmics", "ZeroBias"]
    return None


def get_available_datasets(run_number):
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

    # TODO reuse session when multiple datasets are retrieved

    base_url = get_offline_session_url()

    first_step = "/chooseSample?vary=run;order=dataset"
    second_step = "/modify?vary=any;pat={}".format(run_number)

    cernrequests.get("{}{}".format(base_url, first_step))
    response = cernrequests.get("{}{}".format(base_url, second_step))

    # Make response json compatible
    text = re.sub("'", '"', response.text)[1:-1]
    json_response = json.loads(text)

    try:
        items = json_response[1]["items"][0]["items"]
    except IndexError:
        raise RunDoesNotExist("Unable to find datasets for run {}".format(run_number))
    datasets = [item["dataset"] for item in items]

    return datasets


def _extract_dataset(datasets, possible_reco_types):
    # TODO replace with filter and any
    for reco in possible_reco_types:
        for dataset in datasets:
            if reco in dataset:
                return dataset
    return None

def _extract_run_type(dataset):
    """
    :param dataset: dataset
    :return: "Cosmics" or "Collisions"
    """

def get_dataset(run_number, reconstruction_type):
    datasets = get_available_datasets(run_number)
    recos = translate_reconstruction_type(reconstruction_type)
    return _extract_dataset(datasets, recos)
