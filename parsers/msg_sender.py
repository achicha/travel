import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
):
    """
        create session with retry
    :param retries: total retries
    :param backoff_factor:
    :param status_forcelist: 5xx statuses will retry
    :param session:
    :return:
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def send(URL, msg):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {'message':
                {'text': msg}
            }
    jdata = json.dumps(data)
    requests.post(URL, headers=headers, data=jdata)

