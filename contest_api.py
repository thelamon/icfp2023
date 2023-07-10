import textwrap

import requests as rq
# from loguru import logger
import logging

api_endpoint = "https://api.icfpcontest.com/"
cdn_endpoint = "https://cdn.icfpcontest.com/"

# USE MY TOKEN LUKE
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2NGEyZDJmODhjNjg1MzEzZDFjNjBkODIiLCJpYXQiOjE2ODg4MzY1NzksImV4cCI6MTY4OTgzNjU3OX0.NtSWhDa7K82DrtBt2-8GgONOdcwXLTB-5cDHDD2G-Lk'


def print_roundtrip(response, *args, **kwargs):
    format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())
    print(textwrap.dedent('''
        ---------------- request ----------------
        {req.method} {req.url}
        {reqhdrs}

        {req.body}
        ---------------- response ----------------
        {res.status_code} {res.reason} {res.url}
        {reshdrs}

        {res.text}
    ''').format(
        req=response.request,
        res=response,
        reqhdrs=format_headers(response.request.headers),
        reshdrs=format_headers(response.headers),
    ))


def make_get(path, params=dict(), data=dict()):
    r = rq.get(api_endpoint + path, params=params, data=data, headers={'Authorization': token})
    logging.debug(f"[get] -> request url: {r.url}")
    logging.debug(f"[get] <- response code: {r.status_code}")
    if r.status_code != 200:
        raise BaseException(f"status_code={r.status_code}, text={r.text}")
    return r.content


def make_cdn_get(path):
    r = rq.get(cdn_endpoint + path)
    logging.debug(f"[get] -> request url -> {r.url}")
    logging.debug(f"[get] <- response code: {r.status_code}")
    return r.content


def make_post(path, params=dict(), data=dict()):
    r = rq.post(api_endpoint + path, params=params, json=data, headers={'Authorization': token}
                #, hooks={'response': print_roundtrip}
                )
    logging.debug(f"[post] -> request url: {r.url}")
    logging.debug(f"[post] <- response code: {r.status_code}")
    if r.status_code >= 300:
        raise BaseException(f"status_code={r.status_code}, text={r.text}")
    return r.content
