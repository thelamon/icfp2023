import requests as rq
from loguru import logger

api_endpoint = "https://api.icfpcontest.com/"
cdn_endpoint = "https://cdn.icfpcontest.com/"

# USE MY TOKEN LUKE
token = '<>'


def make_get(path, params=dict(), data=dict()):
    r = rq.get(api_endpoint + path, params=params, data=data, headers={'Authorization': 'Beaver ' + token})
    logger.debug(f"[get] -> request url -> {r.url}")
    logger.debug(f"[get] <- response code: {r.status_code}")
    return r.content


def make_cdn_get(path):
    r = rq.get(cdn_endpoint + path)
    logger.debug(f"[get] -> request url -> {r.url}")
    logger.debug(f"[get] <- response code: {r.status_code}")
    return r.content


def make_post(path, params=dict(), data=dict()):
    r = rq.post(api_endpoint + path, params=params, data=data, headers={'Authorization': 'Beaver ' + token})
    logger.debug(f"[post] request url -> {r.url}")
    return r.content
