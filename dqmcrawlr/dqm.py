import re

import cernrequests

OFFLINE_URL = "https://cmsweb.cern.ch/dqm/offline/"
ONLINE_URL = "https://cmsweb.cern.ch/dqm/online/"


def _get_session_url(base_url):
    request = cernrequests.get(base_url)
    page_content = request.content.decode("utf-8")

    session_id = re.search("session\/.*'", page_content).group()
    session_id = re.sub("'", "", session_id)

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
