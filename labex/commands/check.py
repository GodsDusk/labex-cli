import sys
import json
from pathlib import Path
from rich import print
from jsonschema import validate
import jsonschema

sys.tracebacklimit = 0


class Check:
    def __init__(self) -> None:
        pass

    def validate_json(self, schema_file: str, json_file: str) -> None:
        print(f"schema file: {schema_file}")
        print(f"instance file: {json_file}")
        with open(schema_file, "r") as s:
            schema = json.load(s)
        with open(json_file, "r") as j:
            instance = json.load(j)
        try:
            validate(
                instance=instance, schema=schema,
            )
        except jsonschema.exceptions.ValidationError as e:
            print("[bold red]✗ Validation failed[/bold red]")
            print(e)

        except jsonschema.exceptions.SchemaError as e:
            print("[bold red]✗ Schema error[/bold red]")
            print(e)

        else:
            print("[bold green]✓ Validation success[/bold green]")
        print("\n-----------------------\n")

    def validate_all_json(self, schema_file, base_dir: str) -> None:
        for path in Path(base_dir).rglob("index.json"):
            self.validate_json(schema_file, path)
