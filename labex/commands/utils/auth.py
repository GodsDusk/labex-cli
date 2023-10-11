import os
import json
import click
import requests
from rich import print
from .version import CheckUpdate


class LabExLogin:
    """LabEx Login"""

    def __init__(self) -> None:
        # account.json config file path
        self.account_file_path = f"{os.path.dirname(__file__)}/account.json"
        # account cookie config file path
        self.cookie_file_path = f"{os.path.dirname(__file__)}/config.json"

    def read_account_cookies(self) -> str:
        """Read Cookies"""
        try:
            with open(self.cookie_file_path) as f:
                config = json.load(f)
            return config
        except:
            print("[red]✗[/] No configuration file detected, please log in first.")

    def write_account_cookies(self, cookies: str) -> None:
        """Save account Cookies information
        Args:
            cookies (str): [LabEx cookies]
            file_path (str): [Configuration file address]
        """
        config = {"cookie": None}
        config["cookie"] = cookies
        with open(self.cookie_file_path, "w") as f:
            f.write(json.dumps(config))

    def read_account_info(self) -> str:
        """Read account username and password.
        Args:
            file_path (str): [Configuration file address]
        """
        with open(self.account_file_path) as f:
            account = json.load(f)
            username = account["username"]
            password = account["password"]
        return username, password

    def write_account_info(self, un: str, pw: str) -> str:
        """Save account username and password.
        Args:
            file_path (str): [Configuration file address]
        """
        if un == None or pw == None:
            username = click.prompt("→ Email", type=str)
            password = click.prompt("→ Password", type=str, hide_input=True)
        else:
            # Read account password from parameters.
            username, password = un, pw
        account = {
            "username": username,
            "password": password,
        }
        with open(self.account_file_path, "w") as f:
            f.write(json.dumps(account))
        return username, password

    def login_account(self, un: str, pw: str, check: bool) -> None:
        """Log in to the LabEx account.

        Args:
            un (str): Parameter passed in: username
            pw (str): Password passed in as parameter
            check (bool): Check for version updates
        """
        try:
            # Attempt to retrieve local account information.
            username, password = self.read_account_info()
            print("[green]✔ Automatic login[/]")
        except:
            # No local account information, login required.
            print(
                "[green]→ Please login your LabEx account. Third-party is not supported.[/]"
            )
            username, password = self.write_account_info(un, pw)
        r = requests.post(
            url="https://labex.io/api/v2/auth/login",
            headers={
                "Content-Type": "application/json;charset=UTF-8",
            },
            data=json.dumps({"username": username, "password": password}),
        )
        if r.status_code == 200:
            print(f"[green]✔[/] Login successful: {username}")
            # Cache the token locally for future use.
            self.write_account_cookies(r.headers["Set-Cookie"])
            if check:
                CheckUpdate().check_version()  # Check for version updates.
        else:
            print(f"[red]✗[/] Login failed: {r.json()['message']}")
            self.write_account_info()


class AuthGitHub:
    """GitHub Account authentication"""

    def __init__(self) -> None:
        # GitHub Token 配置文件
        self.github_file_path = f"{os.path.dirname(__file__)}/github.json"

    def write_github_token(self) -> str:
        """
        Write GitHub account Token
        """
        token = click.prompt("→ Please enter GitHub Token", type=str)
        github = {
            "access-token": token,
        }
        with open(self.github_file_path, "w") as f:
            f.write(json.dumps(github))
        return github

    def read_github_token(self) -> None:
        """
        Read GitHub account Token
        """
        while True:
            try:
                with open(self.github_file_path, "r") as f:
                    token = json.load(f)["access-token"]
                return token
            except:
                self.write_github_token()
