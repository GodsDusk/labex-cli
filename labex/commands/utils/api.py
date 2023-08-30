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

    def __status_code(self, r):
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            print(f"Unauthorized, type [yellow]labex login[/yellow] to login again.")
        else:
            print(r.json())

    @retry(stop_max_attempt_number=3)
    def get_data(self) -> dict:
        """HTTP GET"""
        r = requests.get(
            self.url,
            headers=self._headers,
            timeout=self._timeout,
        )
        return self.__status_code(r)

    @retry(stop_max_attempt_number=3)
    def put_data(self, _payloads) -> dict:
        """HTTP PUT"""
        r = requests.put(
            self.url,
            headers=self._headers,
            data=_payloads,
            timeout=self._timeout,
        )
        return self.__status_code(r)

    @retry(stop_max_attempt_number=3)
    def post_data(self, _payloads) -> dict:
        """HTTP POST"""
        self._headers["Content-Type"] = "application/json"
        r = requests.post(
            self.url,
            headers=self._headers,
            data=_payloads,
            timeout=self._timeout,
        )
        return self.__status_code(r)

    @retry(stop_max_attempt_number=3)
    def patch_data(self, _payloads) -> dict:
        """HTTP PATCH"""
        r = requests.patch(
            self.url,
            headers=self._headers,
            data=_payloads,
            timeout=self._timeout,
        )
        return self.__status_code(r)

    @retry(stop_max_attempt_number=3)
    def delete_data(self) -> dict:
        """HTTP DELETE"""
        r = requests.delete(
            self.url,
            headers=self._headers,
            timeout=self._timeout,
        )
        return self.__status_code(r)


class UserData:
    """User Data"""

    def __init__(self) -> None:
        self.base_url = "https://labex.io/api/v2"

    def get_all_path(self) -> list:
        url = f"{self.base_url}/paths/"
        return HTTP(url).get_data()

    def get_path_labs(self, path_alias: str, params: str) -> list:
        url = f"{self.base_url}/paths/{path_alias}/labs{params}"
        return HTTP(url).get_data()["labs"]

    def get_course_labs(self, course_alias: str) -> list:
        url = f"{self.base_url}/courses/{course_alias}/labs"
        return HTTP(url).get_data()["labs"]

    def set_top_labs(self, path_id: int, labs: list) -> list:
        url = f"{self.base_url}/paths/{path_id}/top-labs"
        payloads = {
            "lab_paths": labs
        }
        return HTTP(url).post_data(json.dumps(payloads))


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

    def get_lab_objects(self, params: str) -> list:
        url = f"{self.base_url}/lab_tpl/objects{params}"
        return HTTP(url).get_data()

    def get_show_nomal_paths(self) -> list:
        url = f"{self.base_url}/path/objects?pagination.current=1&pagination.size=100&filters=%7B%22Type%22%3A%5B0%5D%2C%22IsShow%22%3A%5Btrue%5D%7D&sort.field=id&sort.desc=true"
        return HTTP(url).get_data()["objects"]
