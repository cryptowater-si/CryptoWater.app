import requests
from os import getenv
from lib.logger import log


class CryptoID(object):
    def __init__(self):
        self.api_key = getenv("CRYPTOID_TOKEN", None)
        self.base_url = "https://chainz.cryptoid.info/"

    def _make_request(self, url):
        if self.api_key:
            url = url + "&key={0}".format(self.api_key)
        return requests.get(url)

    def address_info(self, coin, address):
        method = "/api.dws?q=addressinfo&a="
        url = self.base_url + coin.lower() + method + address
        respond = self._make_request(url)
        if respond.status_code == 200:
            try:
                address_info = respond.json()
                address_info["coin"] = coin.upper()
                return address_info
            except Exception as err:
                log.warning("Can't convert data to json: {0}".format(respond.text))
        return False
