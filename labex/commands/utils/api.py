import json
import requests
from rich import print
from retrying import retry
from .auth import LabExLogin


class HTTP:
    def __init__(self, url) -> None:
        self.url = url
        self._timeout = 15
        self._headers = LabExLogin().read_account_cookies()

    @retry(stop_max_attempt_number=3)
    def get_data(self) -> dict:
        """HTTP GET"""
        r = requests.get(
            self.url,
            headers=self._headers,
            timeout=self._timeout,
        )
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            print("Please Set LABEX_COOKIE env using `export LABEX_COOKIE=xxx`")
        else:
            print(r.json())

    @retry(stop_max_attempt_number=3)
    def put_data(self, _payloads) -> dict:
        """HTTP PUT"""
        r = requests.put(
            self.url,
            headers=self._headers,
            data=_payloads,
            timeout=self._timeout,
        )
        return r.json()

    @retry(stop_max_attempt_number=3)
    def post_data(self, _payloads) -> dict:
        """HTTP POST"""
        r = requests.post(
            self.url,
            headers=self._headers,
            data=_payloads,
            timeout=self._timeout,
        )
        return r.json()

    @retry(stop_max_attempt_number=3)
    def patch_data(self, _payloads) -> dict:
        """HTTP POST"""
        r = requests.patch(
            self.url,
            headers=self._headers,
            data=_payloads,
            timeout=self._timeout,
        )
        return r.json()

    @retry(stop_max_attempt_number=3)
    def delete_data(self) -> dict:
        """HTTP DELETE"""
        r = requests.delete(
            self.url,
            headers=self._headers,
            timeout=self._timeout,
        )
        return r.json()


class UserData:
    """User Data"""

    def __init__(self) -> None:
        self.base_url = "https://labex.io/api/v2"

    def get_all_path(self) -> list:
        url = f"{self.base_url}/paths/"
        return HTTP(url).get_data()

    def get_path_labs(self, path_alias: str, params: str) -> list:
        url = f"{self.base_url}/paths/{path_alias}/labs/{params}"
        return HTTP(url).get_data()


class AdminData:
    """Admin Data"""

    def __init__(self) -> None:
        self.base_url = "https://labex.io/api/v2/admin"

    def get_skilltree_notify(self) -> list:
        url = f"{self.base_url}/skilltree/notify"
        return HTTP(url).get_data()

    def get_skilltree_notify_by_id(self, _id: str) -> list:
        url = f"{self.base_url}/skilltree/notify/{_id}"
        return HTTP(url).get_data()

    def get_namespaces(self) -> list:
        url = f"https://labex.io/api/v2/namespace?only_main=true"
        return HTTP(url).get_data()["list"]

    def get_namespace_labs(self, namespace: str) -> list:
        url = f"https://labex.io/api/v2/namespace/{namespace}/labs"
        return HTTP(url).get_data()["list"]
