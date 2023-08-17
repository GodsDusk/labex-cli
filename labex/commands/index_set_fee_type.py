import os
import json
import argparse


class SetFeeType:
    def __init__(self) -> None:
        pass

    def __get_idxs(self, path, endswith="index.json"):
        # get all index.json files
        idxs = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file == endswith:
                    idxs.append(os.path.join(root, file))
        return idxs

    def __sort_json(self, data):
        data_sorted = {
            "type": data["type"],
            "title": data["title"],
            "description": data["description"],
            "difficulty": data["difficulty"],
            "time": data["time"],
            "hidden": data["hidden"] if "hidden" in data else False,
            "fee_type": data["fee_type"],
            "details": data["details"],
            "backend": data["backend"],
            "contributors": data["contributors"] if "contributors" in data else [],
        }
        if "license" in data:
            data_sorted["license"] = data["license"]
        return data_sorted

    def set(self, path, fee_type):
        # get all index.json files
        idxs = self.__get_idxs(path)
        print(f"Total {len(idxs)} index.json files in path {path}")
        # set pro
        for idx in idxs:
            with open(idx, "r") as f:
                idx_json = json.load(f)
            # if fee_type key exsits, pass
            if "fee_type" in idx_json:
                # save
                with open(idx, "w") as f:
                    json.dump(self.__sort_json(idx_json), f, indent=2)
                print(f"✕ fee_type key exists in {idx}")
            else:
                # set pro
                idx_json["fee_type"] = fee_type
                # save
                with open(idx, "w") as f:
                    json.dump(self.__sort_json(idx_json), f, indent=2)
                print(f"✓ set {fee_type} in {idx}")
