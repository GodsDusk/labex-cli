import os
import json
from rich import print


class UpdateIndexTime:
    def __init__(self) -> None:
        pass

    def update_time(self, path: str) -> str:
        """Update lab time in index.json.

        Returns:
            str: _description_
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.startswith("index.json"):
                    index_json_path = os.path.join(root, file)
                    # read json file
                    with open(index_json_path, "r") as f:
                        data = json.load(f)
                    lab_time_old = data["time"]
                    # lab steps
                    steps = data["details"]["steps"]
                    lab_time_new = len(steps) * 5
                    if type(lab_time_old) is str or lab_time_old == 0:
                        data["time"] = lab_time_new
                        with open(index_json_path, "w") as f:
                            json.dump(data, f, indent=4)
                        print(f"➜ UPDATE: {index_json_path}")
                        os.system(
                            f"prettier --log-level silent --write {index_json_path}"
                        )
