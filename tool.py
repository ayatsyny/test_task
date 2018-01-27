import requests


def requests_responce(url, method='get', data_json=None):
    if method != 'get' and method != 'post':
        raise print('You get not support method for this application')
    resp = getattr(requests, method)(url, json=data_json)
    if resp.status_code != 200:
        return False, resp
    return True, resp
