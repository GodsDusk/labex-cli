import os
import json
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
            # get contributors
            status_code, contributors = self.github.get_contributors(
                repo_name=repo, file_path=file
            )
            if status_code == 403:
                print("API rate limit exceeded, cancel add contributors")
                break
            if len(contributors) == 0:
                continue
            # read index.json
            with open(file, "r") as f:
                index = json.load(f)
            # original contributors
            original_contributors = index.get("contributors", [])
            # update contributors
            now_contributors = list(set(original_contributors + contributors))
            # remove name contains bot
            now_contributors = [c for c in now_contributors if "bot" not in c]
            # remove huhuhang
            if len(now_contributors) > 1 and "huhuhang" in now_contributors:
                now_contributors.remove("huhuhang")
            # sort contributors
            now_contributors.sort()
            # add contributors
            index["contributors"] = now_contributors
            # write index.json
            with open(file, "w") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
            print(
                f"{i}/{len(idx)}: {file} add new contributors {len(now_contributors) - len(original_contributors)}, total {len(now_contributors)}"
            )
            i += 1
