import json
import requests
from retrying import retry


class GitHub:
    """GitHub 相关 API"""

    def __init__(self, token: str) -> None:
        self.token = token
        print(f"[green]✔ CONNECT[/green]: GitHub API")

    @retry(stop_max_attempt_number=2)
    def get_issue(self, repo_name: str, issue_number: int) -> str:
        url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}"
        headers = {
            "Authorization": "token " + self.token,
            "Accept": "application/vnd.github+json",
        }
        r = requests.get(url, headers=headers)
        return r.json()

    @retry(stop_max_attempt_number=2)
    def list_issue_comments(self, repo_name: str, issue_number: int) -> str:
        url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}/comments"
        headers = {
            "Authorization": "token " + self.token,
            "Accept": "application/vnd.github+json",
        }
        r = requests.get(url, headers=headers)
        comments = [c["body"] for c in r.json()]
        return comments

    @retry(stop_max_attempt_number=2)
    def patch_pr(self, repo_name: str, pr_number: int, payloads: dict) -> dict:
        url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}"
        r = requests.patch(
            url=url,
            headers={
                "Authorization": "token " + self.token,
                "Accept": "application/vnd.github+json",
            },
            data=json.dumps(payloads),
        )
        return r.json()

    @retry(stop_max_attempt_number=2)
    def comment_pr(self, repo_name: str, pr_number: int, comment_text: str) -> dict:
        url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
        r = requests.post(
            url=url,
            headers={
                "Authorization": "token " + self.token,
                "Accept": "application/vnd.github+json",
            },
            data=json.dumps(
                {
                    "body": comment_text,
                }
            ),
        )
        return r.json()

    @retry(stop_max_attempt_number=2)
    def get_pr_list(self, repo_name: str) -> list:
        """获取 pr 列表

        Args:
            repo_name (str): 仓库名称
        """
        url = f"https://api.github.com/repos/{repo_name}/pulls"
        headers = {
            "Authorization": "token " + self.token,
            "Accept": "application/vnd.github+json",
        }
        params = {
            "state": "all",
            "per_page": 100,
        }

        all_pulls = []
        page = 1

        while True:
            params["page"] = page
            print(f"→ Fetching page {page} of pulls...")
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(
                    f"Error retrieving pulls: {response.status_code}, {response.text}"
                )

            pulls = response.json()
            if not pulls:
                break

            all_pulls.extend(pulls)
            page += 1
        return all_pulls

    @retry(stop_max_attempt_number=2)
    def list_milestone(self, repo_name: str) -> list:
        """获取 milestone 列表"""
        url = f"https://api.github.com/repos/{repo_name}/milestones"
        headers = {
            "Authorization": "token " + self.token,
            "Accept": "application/vnd.github+json",
        }
        r = requests.get(url, headers=headers)
        # 获取 title 和 number 的字典
        title_nums = {m["title"]: m["number"] for m in r.json()}
        return title_nums

    @retry(stop_max_attempt_number=2)
    def create_milestone(self, repo_name: str, title: str, due_on: str) -> dict:
        """创建 milestone

        Args:
            repo_name (str): labex-labs/scenarios
            title (str): 2023W16
            due_on (str): 2023-04-21T07:06:13Z

        Returns:
            dict: milestone
        """
        url = f"https://api.github.com/repos/{repo_name}/milestones"
        headers = {
            "Authorization": "token " + self.token,
            "Accept": "application/vnd.github+json",
        }
        r = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(
                {
                    "title": title,
                    "state": "open",
                    "due_on": due_on,
                }
            ),
        )
        if r.status_code == 201:
            print(
                f"[green]✔ MILESTONE[/green]: {title} successfully created, due_on {due_on}"
            )
        else:
            print(f"[red]✘ MILESTONE[/red]: {title} failed to create, due_on {due_on}")
        return r.json()

    @retry(stop_max_attempt_number=2)
    def list_collaborators(self, repo_name: str) -> list:
        """获取仓库的协作者列表"""
        url = f"https://api.github.com/repos/{repo_name}/collaborators"
        headers = {
            "Authorization": "token " + self.token,
            "Accept": "application/vnd.github+json",
        }
        params = {
            "per_page": 100,
        }
        r = requests.get(url, headers=headers, params=params)
        names = [c["login"] for c in r.json()]
        return names

    @retry(stop_max_attempt_number=2)
    def pr_index_json(self, repo_name: str, pr_number: int) -> list:
        url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        response = requests.get(url, headers=headers)
        content_urls = []
        for file in response.json():
            if "index.json" in file["filename"]:
                content_url = file["contents_url"]
                filename = file["filename"]
                content_urls.append(
                    {
                        "content_url": content_url,
                        "filename": filename,
                    }
                )
        if len(content_urls) == 1:
            print(f"→ Found {len(content_urls)} index.json in PR#{pr_number}.")
            index_json_content_url = content_urls[0]["content_url"]
            # get download_url first
            index_json_download_url = requests.get(
                index_json_content_url, headers=headers
            ).json()["download_url"]
            # get index.json content
            index_json = requests.get(index_json_download_url, headers=headers).json()
            lab_path = content_urls[0]["filename"].removesuffix("/index.json")
            return index_json, lab_path
        elif len(content_urls) > 1:
            return len(content_urls), None
        else:
            return None, None

    @retry(stop_max_attempt_number=2)
    def pr_reviews(self, repo_name: str, pr_number: int) -> list:
        url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/reviews"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "token " + self.token,
        }
        response = requests.get(url, headers=headers)
        approved_by = []
        changes_requested_by = []
        review_state = "PENDING_REVIEW"
        for review in response.json():
            review_state = review.get("state")
            if review_state == "APPROVED":
                approved_by.append(review["user"]["login"])
            elif review_state == "CHANGES_REQUESTED":
                changes_requested_by.append(review["user"]["login"])
        return list(set(approved_by)), list(set(changes_requested_by)), review_state

    @retry(stop_max_attempt_number=2)
    def get_issues_list(self, repo_name: str) -> list:
        """获取 issues 列表

        Args:
            repo_name (str): 仓库名称
        """
        url = f"https://api.github.com/repos/{repo_name}/issues"
        headers = {
            "Authorization": "token " + self.token,
            "Accept": "application/vnd.github+json",
        }
        params = {
            "state": "all",
            "per_page": 100,
        }

        all_issues = []
        page = 1

        while True:
            params["page"] = page
            print(f"Fetching page {page} of issues...")
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(
                    f"Error retrieving issues: {response.status_code}, {response.text}"
                )

            issues = response.json()
            if not issues:
                break

            all_issues.extend(issues)
            page += 1

        # 仅保留 Issue，去掉 PR
        noly_issues = [i for i in all_issues if "pull_request" not in i.keys()]

        return noly_issues

    @retry(stop_max_attempt_number=2)
    def get_contributors(self, repo_name: str, file_path: str) -> str:
        # Set the API URL
        url = f"https://api.github.com/repos/{repo_name}/commits"
        # Set the headers for authentication
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
        }

        # Set the parameters to filter commits by file path
        params = {"path": file_path}

        # Send the request
        r = requests.get(url, headers=headers, params=params)
        # Check if the request was successful
        try:
            commits = r.json()
            contributors = set()
            # Iterate through the commits and extract the author's login
            for commit in commits:
                author = commit["author"]["login"]
                contributors.add(author)
            return list(contributors)
        except:
            return []
