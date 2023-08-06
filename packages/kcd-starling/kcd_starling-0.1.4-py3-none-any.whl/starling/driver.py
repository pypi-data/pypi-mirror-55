from typing import Text

import requests
from bs4 import BeautifulSoup


def get_soap(url: Text, **kw) -> BeautifulSoup:
    # TODO Retry Logic required and add test case
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'})
    return BeautifulSoup(res.content, "html.parser")


def get_selenium(url: Text, **kw) -> None:
    # TODO Implementation required
    pass
