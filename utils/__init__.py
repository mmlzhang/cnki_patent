
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from .pybloom import ScalableBloomFilter


class ResponseException(Exception):
    """请求响应异常"""


class DataException(Exception):
    """数据异常"""


def get_request_session():
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s


def request_url(url, args, method="GET", timeout=3):
    try:
        if method == "GET":
            response = requests.get(url, params=args, timeout=timeout)
        elif method == "POST":
            response = requests.delete(url, params=args, timeout=timeout)
        if response.status_code != 200:
            raise ResponseException("{} {}".format(response.status_code, response.text))
        return response.json()
    except requests.HTTPError as e:
        raise ResponseException("{}\n{}".format(str(e), url))


def get_bloom(bloom_file_path):
    if os.path.exists(bloom_file_path):
        with open(bloom_file_path, "rb") as f1:
            bloom = ScalableBloomFilter.fromfile(f1)
    else:
        bloom = ScalableBloomFilter(initial_capacity=1024, error_rate=1 / 10000 / 1000)
    return bloom


def save_bloom_to_file(bloom_file_path, bloom):
    with open(bloom_file_path, "wb") as f:
        bloom.tofile(f)
