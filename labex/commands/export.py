import os
import csv
import glob
import json
from .utils.feishu import Feishu
from rich import print


class Export:
    def __init__(self, app_id, app_secret) -> None:
        feishu = Feishu(app_id, app_secret)
        app_token = "bascnNz4Nqjqgqm1Nm5AYke6xxb"
        table_id = "tblV5pGIsGZMxmE9"
        # Get all records from feishu
        records = feishu.get_bitable_records(app_token, table_id, params="")
        # Get all skill id
        self.skills_id = [r["fields"]["SKILL_ID"][0]["text"] for r in records]
        print(f"[green]Got {len(self.skills_id)} skills[/green]")

    def __parse_single_config(self, path: str) -> str:
        """Parse config from index.json"""
        configs = []
        with open(os.path.join(path, "index.json"), "r") as f:
            index_cofig = json.load(f)
            lab_title = index_cofig["title"]
            lab_type = index_cofig["type"]
            steps = index_cofig["details"]["steps"]
            step_index = 1
            for step in steps:
                step_title = step["title"]
                step_file = step["text"]
                step_skills = ",".join(step["skills"])
                error_skills = ",".join(set(step["skills"]) - set(self.skills_id))
                step_verify = len(step["verify"])
                configs.append(
                    {
                        "LAB_TITLE": f"{lab_type}-{lab_title}",
                        "STEP_TITLE": step_title,
                        "STEP_FILE": step_file,
                        "STEP_INDEX": step_index,
                        "STEP_SKILLS": step_skills,
                        "STEP_ERROR_SKILLS": error_skills,
                        "STEP_VERIFY": step_verify,
                    }
                )
                step_index += 1
        return configs

    def export_skills(self) -> None:
        """Export skills to csv"""
        configs = []
        for path in glob.glob(f"**/index.json", recursive=True):
            try:
                config = self.__parse_single_config(os.path.dirname(path))
            except:
                print(f"[red]Error:[/red] {path}")
                pass
            configs.extend(config)
        # Export to csv
        with open("lab-skills.csv", "w", newline="") as csvfile:
            fieldnames = [
                "LAB_TITLE",
                "STEP_TITLE",
                "STEP_FILE",
                "STEP_INDEX",
                "STEP_SKILLS",
                "STEP_ERROR_SKILLS",
                "STEP_VERIFY",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(configs)
        print("[green]Exported to lab-skills.csv[/green]")
