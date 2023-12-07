import os
import sys
import json
from pathlib import Path
from rich import print
from jsonschema import validate
import jsonschema

sys.tracebacklimit = 0


class CheckIndexValidation:
    def __init__(self) -> None:
        self.lab_schema = os.path.join(
            os.path.dirname(__file__), "utils/lab_schema.json"
        )

    def validate_json(self, json_file: str) -> None:
        with open(self.lab_schema, "r") as s:
            schema = json.load(s)
        with open(json_file, "r") as j:
            instance = json.load(j)
        try:
            validate(
                instance=instance,
                schema=schema,
            )
        except jsonschema.exceptions.ValidationError as e:
            print(f"instance file: {json_file}")
            print(f"schema file: {self.lab_schema}")
            print("[bold red]✗ Validation failed[/bold red]")
            print(e)
            print("\n-----------------------\n")
            return 1

        except jsonschema.exceptions.SchemaError as e:
            print("[bold red]✗ Schema error[/bold red]")
            print(e)
            return 1
        else:
            return 0

    def validate_all_json(self, base_dir: str) -> None:
        error_counts = 0
        i = 0
        for path in Path(base_dir).rglob("index.json"):
            count = self.validate_json(self.lab_schema, path)
            error_counts += count
            i += 1
        print(
            f"Total files validated: {i}, passed: [green]{i - error_counts}[/green], failed: [red]{error_counts}[/red]"
        )


class CheckIndexNoSkills:
    def __init__(self) -> None:
        pass

    def check_skills(self, base_dir: str, filter_skill: str) -> None:
        i = 0
        for path in Path(base_dir).rglob("index.json"):
            skilltree = str(path).split("/")[1]
            if skilltree == "javascript":
                skilltree = "js"
            is_valid = False
            with open(path, "r") as j:
                data = json.load(j)
            steps = data["details"]["steps"]
            for step in steps:
                step_skills = step["skills"]
                for skill in step_skills:
                    if skill.startswith(f"{skilltree}/"):
                        is_valid = True
            if not is_valid:
                if filter_skill == None:
                    print(f"[red]No {skilltree} in:[/red] {path}")
                    i += 1
                else:
                    if filter_skill == skilltree:
                        print(f"[red]No {skilltree} in:[/red] {path}")
                        i += 1
        print(f"Total files: {i}")

class CheckLabDictinary:
    def __init__(self) -> None:
        pass

    def check_lab_dir(self, base_dir: str) -> None:
        i = 0
        for path in Path(base_dir).rglob("index.json"):
            with open(path, "r") as j:
                data = json.load(j)
            lab_skills = []
            for step in data["details"]["steps"]:
                lab_skills.extend(step["skills"])
            lab_skill_trees = [skill.split("/")[0] for skill in lab_skills]
            lab_skill_trees = list(set(lab_skill_trees))
            # replace js with javascript
            if "js" in lab_skill_trees:
                lab_skill_trees.remove("js")
                lab_skill_trees.append("javascript")
            check_status = False
            for lab_skill_tree in lab_skill_trees:
                path_skill_tree = str(path).split("/")
                if lab_skill_tree in path_skill_tree:
                    check_status = True
            if not check_status:
                print(f"[red]Wrong Dir:[/red] {path}")
                i += 1
