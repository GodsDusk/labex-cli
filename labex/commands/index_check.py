import sys
import json
from pathlib import Path
from rich import print
from jsonschema import validate
import jsonschema
import urllib.request

sys.tracebacklimit = 0


class CheckIndexValidation:
    def __init__(self) -> None:
        pass

    def __download_schema(self) -> None:
        # Download schema from github
        print(
            "[bold yellow]⚠️ Schema file not found, downloading it from LabEx...[/bold yellow]"
        )
        urllib.request.urlretrieve(
            "https://cdn.jsdelivr.net/gh/labex-labs/common-scripts/schema.json",
            "schema.json",
        )

    def validate_json(self, schema_file: str, json_file: str) -> None:
        try:
            with open(schema_file, "r") as s:
                schema = json.load(s)
        except FileNotFoundError:
            self.__download_schema()
            with open("./schema.json", "r") as s:
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
            print(f"schema file: {schema_file}")
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

    def validate_all_json(self, schema_file, base_dir: str) -> None:
        error_counts = 0
        i = 0
        for path in Path(base_dir).rglob("index.json"):
            count = self.validate_json(schema_file, path)
            error_counts += count
            i += 1
        print(f"Total files validated: {i}, passed: [green]{i - error_counts}[/green], failed: [red]{error_counts}[/red]")
