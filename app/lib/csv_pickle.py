import pickle
import arrow

from os.path import exists
from os import getenv

from lib.logger import log


class PickleThis(object):
    def __init__(self):
        self.pickle_file = getenv("CSV_PATH", "/home/appdata/address.pickle")
        self.loaded_data = []

    def _load_file(self):
        if not self.loaded_data and exists(self.pickle_file):
            with open(self.pickle_file, "rb") as p:
                self.loaded_data = pickle.load(p)

    def _save_file(self):
        if self.loaded_data:
            with open(self.pickle_file, "wb") as p:
                pickle.dump(self.loaded_data, p)

    def _save_data(self, data_dict):
        try:
            self._load_file()
            self.loaded_data.append(data_dict)
            self._save_file()
        except Exception as err:
            log.error(err)

    @staticmethod
    def save_dict(data_dict):
        p = PickleThis()
        p._save_data(data_dict)

    @staticmethod
    def get_dict():
        p = PickleThis()
        p._load_file()
        return p.loaded_data


class ValidateDownload(object):
    @staticmethod
    def get_ip_addr(user_request):
        ip = user_request.headers.get("X-real-IP", None)
        if not ip:
            ip = user_request.remote_addr
        if ip:
            return ip
        return False

    @staticmethod
    def get_user_agent(user_request):
        return user_request.headers.get("User-Agent")

    @staticmethod
    def validate_un_pw(un, pw):
        eun = getenv("CSV_UN", None)
        epw = getenv("CSV_PW", None)
        # Check if un/pw are set to avoid Null credentials
        if not eun and not epw:
            log.warning("Downloading credentials are not set.")
            return False
        # Check correctness
        if un == eun and pw == epw:
            log.debug("Authorized csv download")
            return True
        log.warning("Username Password does not match")
        return False

    @staticmethod
    def normalize_data(data, request):
        """
        {
            "scanTimeUTC": "",
            "coin": "",
            "address": "",
            "ip": "",
            "browser": "",
        }
        """
        formated_data = {
            "scanTimeUTC": arrow.utcnow().format("YYYY-MM-DD HH:mm:ss"),
            "coin": data["coin"],
            "address": data["address"],
            "ip": ValidateDownload.get_ip_addr(request),
            "browser": ValidateDownload.get_user_agent(request),
        }
        return formated_data
