import os
import git
from rich import print
from pathlib import Path
from github import Github


class CheckUpdate:
    def __init__(self) -> None:
        # Define the path of the local repository
        self.git_path = Path(f"{os.path.dirname(__file__)}").parent.parent.parent

    def check_version(self) -> None:
        # Get the latest commit of the online repository
        repo_online = Github().get_repo("labex-labs/labex-cli")
        online_commit = repo_online.get_branch("master").commit
        # Get the latest commit of the local repository
        repo_local = git.Repo(self.git_path)
        local_commit = repo_local.head.commit
        # Compare the two commits
        if online_commit.sha != local_commit.hexsha:
            print("[yellow]→[/] LabEx CLI is updating...")
            print(git.Git(self.git_path).pull("origin", "master"))
            print("[green]✓[/] LabEx CLI has been updated.")
            print(
                "[yellow]→[/] Please cd to the labex-cli directory and run [bold]pip install -e .[/bold]"
            )
