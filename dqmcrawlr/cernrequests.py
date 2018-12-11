import os

import requests


def _find_user_certificate():
    file_path = os.getenv("HOME") + "/private/usercert.pem"
    assert os.path.isfile(file_path)
    return file_path


def _find_user_certificate_key():
    file_path = os.getenv("HOME") + "/private/userkey.pem"
    assert os.path.isfile(file_path)
    return file_path


def _find_root_certificate():
    file_path = os.getenv("HOME") + "/private/root.pem"
    assert os.path.isfile(file_path)
    return file_path


def get(url):
    """
    :param url: CERN URL
    :return: response from a CERN url
    """
    # TODO handle invalid certificates

    user_certificate = _find_user_certificate()
    user_certificate_key = _find_user_certificate_key()
    root_certificate = _find_root_certificate()

    return requests.get(
        url, cert=(user_certificate, user_certificate_key), verify=root_certificate
    )
