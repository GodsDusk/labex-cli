import os
import json
from rich import print
from .utils.github_api import GitHub


class AddContributors:
    def __init__(self, ghtoken: str) -> None:
        self.github = GitHub(token=ghtoken)

    def get_index_json(self, path: str) -> list:
        # get all index.json from the directory and subdirectories
        idx = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file == "index.json":
                    idx.append(os.path.join(root, file).replace("./", ""))
        return idx

    def add_contributors(self, path: str, repo: str) -> None:
        idx = self.get_index_json(path=path)
        i = 1
        for file in idx:
            # read index.json
            with open(file, "r") as f:
                index = json.load(f)
                is_confirm = index.get("is_confirm", True)
            # Skip unconfirmed labs
            if not is_confirm:
                print(f"{i}/{len(idx)}: [yellow]SKIPPED[/yellow] {file} UNCONFIRMED")
                i += 1
                continue
            # original contributors
            original_contributors = index.get("contributors", [])
            if len(original_contributors) > 0:
                print(
                    f"{i}/{len(idx)}: [yellow]SKIPPED[/yellow] {file} ALREADY HAS CONTRIBUTORS"
                )
                i += 1
                continue
            # get contributors
            status_code, contributors = self.github.get_contributors(
                repo_name=repo, file_path=file
            )
            if status_code == 403:
                print(
                    "[red]CANCELED[/red] API rate limit exceeded, cancel add contributors"
                )
                break
            if len(contributors) == 0:
                continue
            # update contributors
            now_contributors = list(set(original_contributors + contributors))
            # remove name contains
            remove_list = [
                "bot",
                "huhuhang",
            ]
            now_contributors = [
                x for x in now_contributors if not any([y in x for y in remove_list])
            ]
            # sort contributors
            now_contributors.sort()
            # add contributors
            index["contributors"] = now_contributors
            # write index.json
            with open(file, "w") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
            print(
                f"{i}/{len(idx)}: [green]ADDED[/green] {file} new contributors {len(now_contributors) - len(original_contributors)}, total {len(now_contributors)}"
            )
            i += 1
        # prettify index.json
        print("Prettify index.json")
        os.system(f"npx prettier --log-level silent --write {path}/**/*.json")
