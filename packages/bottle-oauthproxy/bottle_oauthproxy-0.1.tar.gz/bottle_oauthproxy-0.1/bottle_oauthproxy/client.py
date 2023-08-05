import os
import requests


class Client:
    def __init__(self, url):
        self.url = url
        self.__info = None

    @property
    def info(self):
        if self.__info is None:
            response = requests.get(os.path.join(self.url, "info"))
            response.raise_for_status()
            self.__info = response.json()
        return self.__info

    @property
    def providers(self):
        return self.info.get("providers")

    @property
    def verify_key(self):
        return self.info.get("verify_key")
