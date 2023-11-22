import os
import json
from rich import print
from .utils.feishu_api import Feishu


class SyncCoursesToFeishu:
    def __init__(self, app_id: str, app_secret: str, repo: str) -> None:
        """Sync courses to feishu

        Args:
            app_id (str): feishu app id
            app_secret (str): feishu app secret
            repo (str): github repo like "labex-dev/devops-labs"
        """
        self.feishu = Feishu(app_id, app_secret)
        self.app_token = "bascnNz4Nqjqgqm1Nm5AYke6xxb"
        self.lab_table_id = "tblW2umsCYJWzzUX"
        self.course_table_id = "tblHpYvtI1OqDmwK"
        self.repo = repo

    def __parse_json(
        self, file_path: str, labs_dict: dict, is_upload_cover: bool = False
    ) -> dict:
        """Parse course.json file

        Args:
            file_path (str): course.json file path
            labs_dict (dict): feishu labs dict {lab_path: record_id}
            is_upload_cover (bool): upload cover to feishu, Defaults to False.

        Returns:
            dict: feishu record payload
        """
        with open(file_path, "r") as f:
            course = json.load(f)
        course_name = course.get("name", None)
        course_description = course.get("description", None)
        course_level = course.get("level", None)
        course_alias = course.get("alias", [])
        course_tags = course.get("tags", [])
        course_priority = course.get("priority", 0)
        course_type = course.get("type", None)
        course_fee_type = course.get("fee_type", "free")
        course_lab_coins = course.get("coins", 0)
        course_is_orderly = course.get("orderly", False)
        course_hidden = course.get("hidden", False)
        course_labs = course.get("labs", [])
        in_labs_dict = []
        not_in_labs_dict = []
        for lab in course_labs:
            lab_path = lab.get("path", None)
            lab_record_id = labs_dict.get(lab_path)
            if lab_record_id:
                in_labs_dict.append(lab_record_id)
            else:
                not_in_labs_dict.append(lab_path)
        data = {
            "NAME": course_name,
            "DESCRIPTION": course_description,
            "LEVEL": course_level,
            "ALIAS": course_alias,
            "TAGS": course_tags,
            "PRIORITY": course_priority,
            "TYPE": course_type,
            "FEE_TYPE": course_fee_type,
            "LAB_COINS": course_lab_coins,
            "ORDERLY": course_is_orderly,
            "HIDDEN": course_hidden,
            "REPO_NAME": self.repo,
            "LABS": list(set(in_labs_dict)),
            "LABS_ERROR": list(set(not_in_labs_dict)),
        }
        return data

    def __is_upload_cover(self, file_path: str, payloads: dict) -> bool:
        """Check if need upload cover to feishu

        Args:
            file_path (str): _description_
            payloads (dict): _description_

        Returns:
            bool: _description_
        """
        try:
            with open(file_path, "r") as f:
                course = json.load(f)
            course_cover = course.get("cover", None)
            cover_path = file_path.replace(
                "course.json", course_cover.replace("./", "")
            )
            print(f"[yellow]➜ TASK:[/yellow] Uploading cover {cover_path}")
            cover_record = self.feishu.upload_media(
                file_path=cover_path,
                parent_type="bitable_image",
                parent_node=self.app_token,
            )
            file_token = cover_record["data"]["file_token"]
            data = payloads["fields"]
            data["COVER"] = [{"file_token": file_token}]
            payloads["fields"] = data
            return payloads
        except:
            return payloads

    def sync_courses(self, skip: bool, full: bool, dirpath: str) -> None:
        """Sync courses from github to feishu

        Args:
            skip (bool): skip the courses that already in feishu
            full (bool): synchronize all courses without checking for changes in record fields.
            dirpath (str, optional): Defaults to ".".
        """
        print(f"[yellow]➜ TASK:[/yellow] Syncing {self.repo} to Feishu...")
        print(f"[yellow]➜ MODE:[/yellow] Skip: {skip}, Full: {full}")
        # Get all course from feishu
        records = self.feishu.get_bitable_records(
            self.app_token, self.course_table_id, params=""
        )
        print(f"[green]✔ Found:[/green] {len(records)} courses in Feishu.")
        # Drop Duplicate records
        records = list({v["fields"]["NAME"]: v for v in records}.values())
        print(
            f"[green]✔ Found:[/green] {len(records)} courses in Feishu after deduplication."
        )
        # Make a full dict of name and record_id and repo_name
        name_dicts = {
            r["fields"]["NAME"]: {
                "record_id": r["record_id"],
                "repo_name": r["fields"]["REPO_NAME"],
                "fields_data": r["fields"],
            }
            for r in records
        }
        # Get all labs from feishu
        labs = self.feishu.get_bitable_records(
            self.app_token, self.lab_table_id, params=""
        )
        # Make a dict of lab_path and record_id
        labs_dicts = {r["fields"]["LAB_PATH"][0]["text"]: r["record_id"] for r in labs}
        print(
            f"[green]✔ Found:[/green] {len(labs_dicts)} labs in Feishu, start syncing..."
        )
        # Walk through all index.json files
        # If course name in name_dicts, update record
        # If course name not in name_dicts, add record
        course_names = []
        for dirpath, dirnames, filenames in os.walk(dirpath):
            filenames = [f for f in filenames if f == "course.json"]
            for filename in filenames:
                try:
                    filepath = os.path.join(dirpath, filename)
                    data = self.__parse_json(filepath, labs_dicts)
                    # Make payloads
                    payloads = {"fields": data}
                    # Get data path like "Getting-Started"
                    course_name = data["NAME"]
                    # Add course name to list for deleting
                    course_names.append(course_name)
                    # Compare course name in feishu and in repo
                    if course_name in name_dicts:
                        if skip:
                            # Skip record
                            print(
                                f"[yellow]➜ SKIPPED:[/yellow] {course_name} because of skip=True"
                            )
                            continue
                        else:
                            if full:
                                # Update record with full=True
                                record_id = name_dicts[course_name]["record_id"]
                                # upload course cover
                                payloads = self.__is_upload_cover(filepath, payloads)
                                r = self.feishu.update_bitable_record(
                                    self.app_token,
                                    self.course_table_id,
                                    record_id,
                                    payloads,
                                )
                                print(
                                    f"[green]↑ UPDATED:[/green] {course_name} {r['msg'].upper()}"
                                )
                            else:
                                # Update record with full=False
                                # Compare JSON to determine whether to update
                                feishu_fields_data = name_dicts[course_name][
                                    "fields_data"
                                ]
                                new_data = data
                                # Only compare the required fields
                                str_fields = [
                                    "NAME",
                                    "DESCRIPTION",
                                    "LEVEL",
                                    "TYPE",
                                    "FEE_TYPE",
                                    "REPO_NAME",
                                ]
                                list_fields = ["ALIAS", "TAGS"]
                                num_fields = ["PRIORITY", "LAB_COINS"]
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
                                    record_id = name_dicts[course_name]["record_id"]
                                    r = self.feishu.update_bitable_record(
                                        self.app_token,
                                        self.course_table_id,
                                        record_id,
                                        payloads,
                                    )
                                    print(
                                        f"[green]↑ UPDATED:[/green] {course_name} {r['msg'].upper()}"
                                    )
                                else:
                                    print(
                                        f"[yellow]➜ SKIPPED:[/yellow] {course_name} because of no change"
                                    )
                    else:
                        # upload course cover
                        payloads = self.__is_upload_cover(filepath, payloads)
                        # Add record
                        r = self.feishu.add_bitable_record(
                            self.app_token, self.course_table_id, payloads
                        )
                        print(
                            f"[green]↑ ADDED:[/green] {course_name} {r['msg'].upper()}"
                        )
                except Exception as e:
                    print(f"× Error {filepath} {e}")
        # Delete records not in this repo
        repo_name_dicts = [
            name for name in name_dicts if name_dicts[name]["repo_name"] == self.repo
        ]
        print(
            f"[green]✔ Found:[/green] {len(repo_name_dicts)} courses in {self.repo}, checking if need delete..."
        )
        deleted = 0
        for name in repo_name_dicts:
            if name not in course_names:
                record_id = name_dicts[name]["record_id"]
                r = self.feishu.delete_bitable_record(
                    self.app_token, self.course_table_id, record_id
                )
                print(f"× Deleting {record_id}-{name} {r['msg'].upper()}")
                deleted += 1
        print(f"[green]✔ Deleted[/green] {deleted} courses in {self.repo}")
