import re

from lib.logger import log


class AddressValidator(object):
    @staticmethod
    def _coin_re_expressions():
        return {
            "taj": "^[T][a-km-zA-HJ-NP-Z1-9]{23,34}$",
            "arco": "^[A][a-km-zA-HJ-NP-Z1-9]{23,34}$",
            "lana": "^[L][a-km-zA-HJ-NP-Z1-9]{23,34}$",
        }

    @staticmethod
    def _detect_coin(address):
        d = {
            "L": "lana",
            "A": "arco",
            "T": "taj",
        }
        if address[0] in d.keys():
            return d[address[0]]
        return None

    @staticmethod
    def validate_address(address):
        if type(address) != str:
            log.warning("Address is not string: {0}".format(address))
            return False, "Address not string"
        address = address.strip()
        coin = AddressValidator._detect_coin(address)
        if not coin:
            log.warning("Coin not known from address: {0}".format(address))
            return False, "Unknown coin"
        x = re.search(AddressValidator._coin_re_expressions()[coin], address)
        if not x:
            log.warning("Address invalid: {0}".format(address))
            return False, "Address invalid"
        log.info("Address: {0} is valid.".format(address))
        return True, coin

    @staticmethod
    def clean_address(address_string):
        try:
            addr = address_string.strip()
            address = addr.split(":")[1]
            return address
        except Exception as err:
            return address_string
