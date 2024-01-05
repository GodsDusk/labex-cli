import re
import os
import json
from rich import print
from rich.progress import track
from jsonschema import validate
from .utils.feishu_api import Feishu
from .utils.labex_api import AdminData


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
    def __init__(
        self, app_id: str, app_secret: str, repo: str, is_sync_lab_id: bool
    ) -> None:
        """Sync labs to feishu

        Args:
            app_id (str): feishu app id
            app_secret (str): feishu app secret
            repo (str): github repo like "labex-dev/devops-labs"
            is_sync_lab_id (bool): sync lab id from labex
        """
        self.feishu = Feishu(app_id, app_secret)
        lab_schema = os.path.join(os.path.dirname(__file__), "utils/lab_schema.json")
        self.schema = Schema(lab_schema)
        self.app_token = "bascnNz4Nqjqgqm1Nm5AYke6xxb"
        self.lab_table_id = "tblW2umsCYJWzzUX"
        self.skills_table_id = "tblV5pGIsGZMxmE9"
        self.repo = repo
        self.is_sync_lab_id = is_sync_lab_id
        if self.is_sync_lab_id:
            self.labex_admin_data = AdminData()

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
            "CONTRIBUTORS": list(lab_contributors),
            "GITHUB": {
                "link": f"https://github.com/{self.repo}/tree/master/{path_slug}",
                "text": "OPEN IN GITHUB",
            },
            "REPO_NAME": self.repo,
            "HIDDEN": lab_hidden,
            "FEE_TYPE": lab_fee_type.title(),
        }
        # is lanqiao source
        source = "LABEX"
        is_lanqiao = index.get("lqid")
        if is_lanqiao != None:
            source = "LANQIAO"
            data["LQID"] = int(is_lanqiao)
        # is open source
        is_open_source = index.get("license")
        if is_open_source != None:
            source = "OPEN SOURCE"
        data["SOURCE"] = source
        return data

    def __get_labs_from_namespace(self, namespace_id: str, page_size: int) -> list:
        """Get labs from labex namespace"""
        params = f'?pagination.current=1&pagination.size={page_size}&filters=%7B"NamespaceID"%3A"{namespace_id}"%7D'
        first_page = self.labex_admin_data.get_lab_objects(params)
        total_pages = first_page["pagination"]["total_pages"]
        labs = first_page["objects"]
        for page in track(
            range(2, total_pages + 1),
            description=f"Namespace: {namespace_id}, Total Pages: {total_pages}",
        ):
            page_data = self.labex_admin_data.get_lab_objects(
                params=f'?pagination.current={page}&pagination.size={page_size}&filters=%7B"NamespaceID"%3A"{namespace_id}"%7D'
            )
            labs.extend(page_data["objects"])
        return labs

    def sync_labs(self, skip: bool, full: bool, dirpath: str) -> None:
        """Sync labs from github to feishu

        Args:
            skip (bool): skip the labs that already in feishu
            full (bool): synchronize all labs without checking for changes in record fields.
            dirpath (str, optional): Defaults to ".".
        """
        is_sync_lab_id = self.is_sync_lab_id
        print(f"[yellow]➜ TASK[/yellow]: Syncing {self.repo} to Feishu")
        print(
            f"[yellow]➜ MODE[/yellow]: Skip: {skip}, Full: {full}, Sync Lab ID: {is_sync_lab_id}"
        )
        # Get all records from feishu
        records = self.feishu.get_bitable_records(
            self.app_token, self.lab_table_id, params=""
        )
        print(f"[green]✔ Found[/green]: {len(records)} labs in Feishu.")
        # Drop Duplicate records
        records = list({v["fields"]["PATH"]: v for v in records}.values())
        print(
            f"[green]✔ Found[/green]: {len(records)} labs in Feishu after deduplication."
        )
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
        print(f"[green]✔ Found[/green]: {len(skills_dicts)} skills in Feishu.")
        # Get all labs from labex admin
        if is_sync_lab_id:
            try:
                # Get all namespaces
                objects = self.labex_admin_data.get_namespaces()
                namespaces = {f"{n['UserName']}/{n['Repo']}": n["id"] for n in objects}
                print(f"[green]✔ Found[/green]: {len(namespaces)} namespaces in LabEx.")
                # Get repo id
                namespace_id = namespaces.get(self.repo)
                if namespace_id == None:
                    is_sync_lab_id = False
                    print(
                        f"[red]× Error[/red]: {self.repo} not found in LabEx, skip sync lab id"
                    )
                else:
                    labs = self.__get_labs_from_namespace(namespace_id, 100)
                    labs_id_dict = {l["Path"]: l["id"] for l in labs}
                    print(
                        f"[green]✔ Found[/green]: {len(labs)} labs in {self.repo} namespace"
                    )
            except:
                is_sync_lab_id = False

        # Walk through all index.json files
        # If path in path_dicts, update record
        # If path not in path_dicts, add record
        data_paths = []
        for dirpath, _, filenames in os.walk(dirpath):
            filenames = [f for f in filenames if f == "index.json"]
            for filename in filenames:
                try:
                    filepath = os.path.join(dirpath, filename)
                    # read index.json
                    with open(filepath, "r") as f:
                        index = json.load(f)
                        is_confirm = index.get("is_confirm", True)
                    # Skip unconfirmed labs
                    if not is_confirm:
                        print(
                            f"[yellow]➜ SKIPPED[/yellow]: {filepath} because of unconfirmed"
                        )
                        continue
                    data = self.__parse_json(filepath, skills_dicts)
                    # Validate index.json
                    s = self.schema.validate(json_file=filepath)
                    if s:
                        data["JSON_SCHEMA"] = "🟢 VALID"
                    else:
                        data["JSON_SCHEMA"] = "🔴 INVALID"
                    # Add lab id
                    if is_sync_lab_id:
                        lab_id = labs_id_dict.get(data["PATH"])
                        if lab_id != None:
                            data["LAB_ID"] = lab_id
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
                            print(
                                f"[yellow]➜ SKIPPED[/yellow]: {data_path} because of skip=True"
                            )
                            continue
                        else:
                            if full:
                                # Update record with full=True
                                record_id = path_dicts[data_path]["record_id"]
                                r = self.feishu.update_bitable_record(
                                    self.app_token,
                                    self.lab_table_id,
                                    record_id,
                                    payloads,
                                )
                                print(
                                    f"[green]↑ UPDATED[/green]: {data_path} {r['msg'].upper()}"
                                )
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
                                list_fields = ["SKILLS_ID", "CONTRIBUTORS"]
                                num_fields = ["STEPS", "SCRIPTS", "DESC_WORDS", "TIME"]
                                # Add LAB_ID field if is_sync_lab_id
                                if is_sync_lab_id:
                                    str_fields.append("LAB_ID")
                                # Compare the fields, if any change, update
                                if (
                                    any(
                                        feishu_fields_data.get(field)
                                        != new_data.get(field)
                                        for field in str_fields
                                    )
                                    or any(
                                        sorted(feishu_fields_data.get(field, []))
                                        != sorted(new_data.get(field))
                                        for field in list_fields
                                    )
                                    or any(
                                        int(feishu_fields_data.get(field))
                                        != int(new_data.get(field))
                                        for field in num_fields
                                    )
                                ):
                                    # Update record
                                    record_id = path_dicts[data_path]["record_id"]
                                    r = self.feishu.update_bitable_record(
                                        self.app_token,
                                        self.lab_table_id,
                                        record_id,
                                        payloads,
                                    )
                                    print(
                                        f"[green]↑ UPDATED[/green]: {data_path} {r['msg'].upper()}"
                                    )
                                else:
                                    print(
                                        f"[yellow]➜ SKIPPED[/yellow]: {data_path} because of no change"
                                    )
                    else:
                        # Add record
                        r = self.feishu.add_bitable_record(
                            self.app_token, self.lab_table_id, payloads
                        )
                        print(f"[green]↑ ADDED[/green]: {data_path} {r['msg'].upper()}")
                except Exception as e:
                    print(f"[red]× Error[/red]: {filepath} {e}")
        # Delete records not in this repo
        repo_path_dicts = [
            path for path in path_dicts if path_dicts[path]["repo_name"] == self.repo
        ]
        print(
            f"[green]✔ Found[/green]: {len(repo_path_dicts)} labs in this {self.repo}, checking if need delete..."
        )
        deleted = 0
        for path in repo_path_dicts:
            if path not in data_paths:
                record_id = path_dicts[path]["record_id"]
                r = self.feishu.delete_bitable_record(
                    self.app_token, self.lab_table_id, record_id
                )
                print(f"[red]× Deleting[/red]: {record_id}-{path} {r['msg'].upper()}")
                deleted += 1
        print(f"[green]✔ Deleted[/green] {deleted} labs in {self.repo}")
