import os
import json
import click


class StandardName:
    """Standardize the name of the index.json file and the step file."""

    def __init__(self, path: str):
        self.path = path

    def check_step_and_verify(self, index_json_path: str):
        """Check if the step and verify are matched."""
        with open(index_json_path, "r") as f:
            data = json.load(f)
        steps = data["details"]["steps"]
        for step in steps:
            step_file = step["text"]
            step_num = step_file.replace("step", "").replace(".md", "")
            step_verify = step.get("verify", [])
            if len(step_verify) == 0:
                print(f"Error: {index_json_path}")
                print(f"Step {step_num} has no verify")
                return False
            else:
                for v in step_verify:
                    v_file = v["file"]
                    if int(step_num) >= 10:
                        v_num = v_file.replace("verify", "")[:2]
                    else:
                        v_num = v_file.replace("verify", "")[0]
                    if step_num != v_num:
                        print(f"Error: {index_json_path}")
                        print(f"step: {step_num}, verify: {v_num}")
                        return False

    def update_steps(self, index_json_path: str):
        """Update the step and verify name.

        Args:
            index_json_path (str): _description_
        """
        update = False
        # read json file
        with open(index_json_path, "r") as f:
            data = json.load(f)
        steps = data["details"]["steps"]
        for i, step in enumerate(steps):
            # original file name
            step_file = step["text"]
            step_file_path = index_json_path.replace("index.json", step_file)
            # rename file by step number
            new_step_file = f"new-step{i+1}.md"
            new_step_file_path = index_json_path.replace("index.json", new_step_file)
            if f"new-{step_file}" != new_step_file:
                # rename file
                os.rename(step_file_path, new_step_file_path)
                # update json file
                step["text"] = new_step_file
                update = True
            # verify name
            try:
                step_verify = step.get("verify", [])
                if len(step_verify) == 0:
                    new_v_file = f"verify{i+1}.sh"
                    new_v_file_path = index_json_path.replace("index.json", new_v_file)
                    verify_json = {
                        "name": f"Check the step {i+1}",
                        "file": new_v_file,
                        "hint": "Please follow the instructions to complete the step.",
                        "timeout": 0,
                        "showstderr": true,
                    }
                    # create new verify file
                    with open(new_v_file_path, "w") as f:
                        f.write("#!/bin/bash")
                    # add verify to json file
                    step["verify"] = [verify_json]
                    update = True
                elif len(step_verify) == 1:
                    v = step_verify[0]
                    v_file = v["file"]
                    v_file_path = index_json_path.replace("index.json", v_file)
                    new_v_file = f"new-verify{i+1}.sh"
                    new_v_file_path = index_json_path.replace("index.json", new_v_file)
                    if f"new-{v_file}" != new_v_file:
                        os.rename(v_file_path, new_v_file_path)
                        v["file"] = new_v_file
                        update = True
                elif len(step_verify) > 1:
                    for j, v in enumerate(step_verify):
                        v_file = v["file"]
                        v_file_path = index_json_path.replace("index.json", v_file)
                        new_v_file = f"new-verify{i+1}-{j+1}.sh"
                        new_v_file_path = index_json_path.replace(
                            "index.json", new_v_file
                        )
                        if f"new-{v_file}" != new_v_file:
                            os.rename(v_file_path, new_v_file_path)
                            v["file"] = new_v_file
                            update = True
            except Exception as e:
                print(f"Error: {e}, {index_json_path}")
        if update:
            # write json file
            with open(index_json_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def remove_new_prefix(self, index_json_path: str):
        """Remove the new prefix of the step and verify name.

        Args:
            index_json_path (str): _description_
        """
        update = False
        # read json file
        with open(index_json_path, "r") as f:
            data = json.load(f)
        steps = data["details"]["steps"]
        for step in steps:
            # original file name
            step_file = step["text"]
            step_file_path = index_json_path.replace("index.json", step_file)
            if step_file.startswith("new-"):
                new_step_file = step_file.replace("new-", "")
                new_step_file_path = index_json_path.replace(
                    "index.json", new_step_file
                )
                # rename file
                os.rename(step_file_path, new_step_file_path)
                # update json file
                step["text"] = new_step_file
                update = True
            # verify name
            step_verify = step["verify"]
            for v in step_verify:
                v_file = v["file"]
                v_file_path = index_json_path.replace("index.json", v_file)
                if v_file.startswith("new-"):
                    new_v_file = v_file.replace("new-", "")
                    new_v_file_path = index_json_path.replace("index.json", new_v_file)
                    os.rename(v_file_path, new_v_file_path)
                    v["file"] = new_v_file
                    update = True
        if update:
            # write json file
            with open(index_json_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def main(self, mode: str):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.startswith("index.json"):
                    index_json_path = os.path.join(root, file)
                    if mode == "check":
                        self.check_step_and_verify(index_json_path)
                    elif mode == "update":
                        self.update_steps(index_json_path)
                        self.remove_new_prefix(index_json_path)
        # run prettier shell command
        if click.confirm("→ If you want to run prettier, press y"):
            os.system(f"prettier --write {self.path}/**/*.json")
