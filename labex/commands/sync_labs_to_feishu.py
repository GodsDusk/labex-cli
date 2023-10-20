import re
import os
import json
from rich import print
from jsonschema import validate
from .utils.feishu_api import Feishu


class Schema:
    def __init__(self, schema_path: str) -> None:
        self.schema_path = schema_path

    def __load_schema(self) -> dict:
        with open(self.schema_path, "r") as f:
            schema = json.load(f)
        return schema

    def validate(self, json_file: str) -> None:
        schema = self.__load_schema()
        with open(json_file, "r") as f:
            data = json.load(f)
        try:
            validate(instance=data, schema=schema)
            return True
        except Exception as e:
            return False


class SyncLabsToFeishu:
    def __init__(self, app_id: str, app_secret: str, repo: str) -> None:
        """Sync labs to feishu

        Args:
            app_id (str): feishu app id
            app_secret (str): feishu app secret
            repo (str): github repo like "labex-dev/devops-labs"
        """
        self.feishu = Feishu(app_id, app_secret)
        lab_schema = os.path.join(os.path.dirname(__file__), "utils/lab_schema.json")
        self.schema = Schema(lab_schema)
        self.app_token = "bascnNz4Nqjqgqm1Nm5AYke6xxb"
        self.table_id = "tblW2umsCYJWzzUX"
        self.skills_table_id = "tblV5pGIsGZMxmE9"
        self.repo = repo

    def __parse_json(self, file_path: str, skills_dict: dict) -> dict:
        """Parse json file

        Args:
            file_path (str): index.json file path
            skills_dict (dict): feishu skills dict {skill_id: record_id}

        Returns:
            dict: feishu record payload
        """
        with open(file_path, "r") as f:
            index = json.load(f)
        direction = re.compile(r"\.\/[a-z1-9]+").findall(file_path)
        path_slug = file_path.removeprefix("./").removesuffix("/index.json")
        if len(direction) > 0:
            lab_direction = direction[0].replace("./", "")
        else:
            lab_direction = None
        lab_title = index.get("title", None)
        lab_desc = index.get("description", None)
        lab_type = index.get("type", None)
        lab_time = index.get("time", None)
        lab_difficulty = index.get("difficulty", None)
        lab_backend = index.get("backend").get("imageid", None)
        lab_steps = index.get("details").get("steps")
        lab_contributors = index.get("contributors", [])
        lab_hidden = index.get("hidden", False)
        lab_fee_type = index.get("fee_type", "free")
        # Count Verify scripts
        lab_scripts = sum(
            [
                len(step.get("verify"))
                for step in lab_steps
                if step.get("verify") != None
            ]
        )
        # Count words in description
        if len(lab_desc) > 1:
            lab_desc_words = len(lab_desc.split())
        else:
            lab_desc_words = 0
        # Get and merge skills
        lab_skills = []
        for i, step in enumerate(lab_steps):
            skills = step.get("skills")
            if skills:
                lab_skills.extend(skills)
        # Get record is from skills tree table
        in_skills_tree = []
        not_in_skills_tree = []
        if len(lab_skills) > 0:
            for skill in lab_skills:
                skill_id = skills_dict.get(skill)
                if skill_id != None:
                    in_skills_tree.append(skill_id)
                else:
                    not_in_skills_tree.append(skill)
        # is lanqiao source
        source = "LABEX"
        is_lanqiao = index.get("lqid")
        if is_lanqiao != None:
            source = "LANQIAO"
        # is open source
        is_open_source = index.get("license")
        if is_open_source != None:
            source = "OPEN SOURCE"
        data = {
            "PATH": path_slug,
            "TITLE": lab_title,
            "DIRECTION": lab_direction,
            "TYPE": lab_type,
            "TIME": lab_time,
            "DIFFICULTY": lab_difficulty,
            "STEPS": len(lab_steps),
            "SCRIPTS": lab_scripts,
            "BACKEND": lab_backend,
            "SKILLS_ID": list(set(lab_skills)),
            "SKILLS_TREE": list(set(in_skills_tree)),
            "SKILLS_ERROR": list(set(not_in_skills_tree)),
            "DESC_WORDS": lab_desc_words,
            "DESC": lab_desc,
            "SOURCE": source,
            "CONTRIBUTORS": list(lab_contributors),
            "GITHUB": {
                "link": f"https://github.com/{self.repo}/tree/master/{path_slug}",
                "text": "OPEN IN GITHUB",
            },
            "REPO_NAME": self.repo,
            "HIDDEN": lab_hidden,
            "FEE_TYPE": lab_fee_type.title(),
        }
        return data

    def sync_labs(self, skip: bool, full: bool, path: str) -> None:
        """Sync labs from github to feishu

        Args:
            skip (bool): skip the labs that already in feishu
            full (bool): synchronize all labs without checking for changes in record fields.
            path (str, optional): Defaults to ".".
        """
        print(f"[yellow]➜ TASK:[/yellow] Syncing {self.repo} to Feishu...")
        print(f"[yellow]➜ MODE:[/yellow] Skip: {skip}, Full: {full}")
        # Get all records from feishu
        records = self.feishu.get_bitable_records(
            self.app_token, self.table_id, params=""
        )
        print(f"Found {len(records)} labs in Feishu.")
        # Drop Duplicate records
        records = list({v["fields"]["PATH"]: v for v in records}.values())
        print(f"Found {len(records)} labs in Feishu after deduplication.")
        # Make a full dict of path and record_id and repo_name
        path_dicts = {
            r["fields"]["PATH"]: {
                "record_id": r["record_id"],
                "repo_name": r["fields"]["REPO_NAME"],
                "fields_data": r["fields"],
            }
            for r in records
        }
        # Get all skills from feishu
        skills = self.feishu.get_bitable_records(
            self.app_token, self.skills_table_id, params=""
        )
        # Make a dict of skill and record_id
        skills_dicts = {
            r["fields"]["SKILL_ID"][0]["text"]: r["record_id"] for r in skills
        }
        print(f"Found {len(skills_dicts)} skills in Feishu, start syncing...")
        # Walk through all index.json files
        # If path in path_dicts, update record
        # If path not in path_dicts, add record
        data_paths = []
        for dirpath, dirnames, filenames in os.walk(path):
            filenames = [f for f in filenames if f == "index.json"]
            for filename in filenames:
                try:
                    filepath = os.path.join(dirpath, filename)
                    data = self.__parse_json(filepath, skills_dicts)
                    # Validate index.json
                    s = self.schema.validate(json_file=filepath)
                    if s:
                        data["JSON_SCHEMA"] = "🟢 VALID"
                    else:
                        data["JSON_SCHEMA"] = "🔴 INVALID"
                    # Make payloads
                    payloads = {"fields": data}
                    # Get data path like "lab-hello-world"
                    data_path = data["PATH"]
                    # Add data path to list for deleting
                    data_paths.append(data_path)
                    # Compare path in feishu and path in repo
                    if data_path in path_dicts:
                        if skip:
                            # Skip record
                            print(f"↓ Skipping {data_path} because of skip=True")
                            continue
                        else:
                            if full:
                                # Update record with full=True
                                record_id = path_dicts[data_path]["record_id"]
                                r = self.feishu.update_bitable_record(
                                    self.app_token, self.table_id, record_id, payloads
                                )
                                print(f"→ Updating {data_path} {r['msg'].upper()}")
                            else:
                                # Update record with full=False
                                # Compare JSON to determine whether to update
                                feishu_fields_data = path_dicts[data_path][
                                    "fields_data"
                                ]
                                new_data = data
                                # Only compare the required fields
                                str_fields = [
                                    "TITLE",
                                    "DIRECTION",
                                    "BACKEND",
                                    "DIFFICULTY",
                                    "REPO_NAME",
                                    "HIDDEN",
                                    "FEE_TYPE",
                                ]
                                list_fields = ["SKILLS_ID"]
                                num_fields = ["STEPS", "SCRIPTS", "DESC_WORDS", "TIME"]
                                # Compare the fields, if any change, update
                                if (
                                    any(
                                        feishu_fields_data[field] != new_data[field]
                                        for field in str_fields
                                    )
                                    or any(
                                        sorted(feishu_fields_data.get(field, []))
                                        != sorted(new_data[field])
                                        for field in list_fields
                                    )
                                    or any(
                                        int(feishu_fields_data[field])
                                        != int(new_data[field])
                                        for field in num_fields
                                    )
                                ):
                                    # Update record
                                    record_id = path_dicts[data_path]["record_id"]
                                    r = self.feishu.update_bitable_record(
                                        self.app_token,
                                        self.table_id,
                                        record_id,
                                        payloads,
                                    )
                                    print(f"→ Updating {data_path} {r['msg'].upper()}")
                                else:
                                    print(
                                        f"↓ Skipping {data_path} because of no change"
                                    )
                    else:
                        # Add record
                        r = self.feishu.add_bitable_record(
                            self.app_token, self.table_id, payloads
                        )
                        print(f"↑ Adding {data_path} {r['msg'].upper()}")
                except Exception as e:
                    print(f"× Error {filepath} {e}")
        # Delete records not in this repo
        repo_path_dicts = [
            path for path in path_dicts if path_dicts[path]["repo_name"] == self.repo
        ]
        print(
            f"Found {len(repo_path_dicts)} labs in this Repo, checking if need delete..."
        )
        deleted = 0
        for path in repo_path_dicts:
            if path not in data_paths:
                record_id = path_dicts[path]["record_id"]
                r = self.feishu.delete_bitable_record(
                    self.app_token, self.table_id, record_id
                )
                print(f"× Deleting {record_id}-{path} {r['msg'].upper()}")
                deleted += 1
        print(f"Deleted {deleted} labs")
