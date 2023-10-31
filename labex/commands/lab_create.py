import os
import json
import click
from rich import print
from rich.prompt import Prompt
from titlecase import titlecase
from .project_create import CreateProject


class CreateLab:
    """Create a new lab or challenge"""

    def __init__(self) -> None:
        pass

    def init_step(self, step_index: int, lab_type: str, lab_slug: str) -> dict:
        """Initialize a step

        Args:
            step_index (int): lab step index

        Returns:
            _type_: step config
        """
        if lab_type == "lab":
            # step index.json config template
            step_config = {
                "title": "Please replace this text with the title of the step",
                "text": f"step{step_index}.md",
                "verify": [
                    {
                        "name": "The Target of the verify script",
                        "file": f"verify{step_index}.sh",
                        "hint": "Custom error message.",
                        "timeout": 0,
                        "showstderr": True,
                    }
                ],
                "skills": ["Please copy the skill ID from the official skill tree"],
            }
            # create step file
            step_file = open(f"{lab_slug}/step{step_index}.md", "w")
            step_file.write(f"# Step {step_index} Title\n")
            # create verify file
            verify_file = open(f"{lab_slug}/verify{step_index}.sh", "w")
            verify_file.write("#!/bin/zsh")
        else:
            # step index.json config template
            step_config = {
                "title": "Please replace this text with the title of the step",
                "text": f"step{step_index}.md",
                "verify": [
                    {
                        "name": "The Target of the verify script",
                        "file": f"verify{step_index}.sh",
                        "hint": "Custom error message.",
                        "timeout": 0,
                        "showstderr": False,
                    }
                ],
                "skills": ["Please copy the skill ID from the official skill tree"],
                "solutions": [f"step{step_index}-solution.md"],
            }
            # create step file
            step_file = open(f"{lab_slug}/step{step_index}.md", "w")
            step_file.write(f"# Step {step_index} Title\n")
            # create verify file
            verify_file = open(f"{lab_slug}/verify{step_index}.sh", "w")
            verify_file.write("#!/bin/zsh")
            # create solution file
            solution_folder = f"{lab_slug}/solutions"
            if not os.path.exists(solution_folder):
                os.mkdir(solution_folder)
            solution_file = open(
                f"{lab_slug}/solutions/step{step_index}-solution.md", "w"
            )
            solution_file.write(f"# Solution\n")
        return step_config

    def check_if_exists(self, lab_slug: str) -> None:
        if os.path.exists(lab_slug):
            print("[red]Lab Title already exists, please choose another one.[/red]")
            exit(1)
        else:
            os.mkdir(lab_slug)

    def init_base(self):
        lab_type = Prompt.ask(
            "Select Lab Type", choices=["lab", "challenge"], default="lab"
        )
        lab_title = titlecase(Prompt.ask("Enter Lab Title (e.g. Hello World)"))
        lab_slug = f'{lab_type}-{lab_title.lower().replace(" ", "-")}'
        lab_diff = Prompt.ask(
            "Select Lab Difficulty",
            choices=["Beginner", "Intermediate", "Advanced"],
            default="Beginner",
        )
        lab_time = Prompt.ask("Enter Lab Time (minutes)", default="5")
        lab_steps = int(Prompt.ask("Enter Number of Steps", default="3"))
        lab_image_id = Prompt.ask(
            "Select Image ID",
            choices=[
                "vnc-ubuntu:2204",
                "webide-ubuntu:2204",
                "vnc-instance-ubuntu:2204",
                "webide-instance-ubuntu:2204",
            ],
            default="vnc-ubuntu:2204",
        )
        self.if_assets = Prompt.ask(
            "Does it contain pictures or other attachments?",
            choices=["yes", "no"],
            default="yes",
        )

        # create folder
        self.check_if_exists(lab_slug)
        # create basic files
        intro_file = open(f"{lab_slug}/intro.md", "w")
        intro_file.write(f"# {lab_title}\n")
        finish_file = open(f"{lab_slug}/finish.md", "w")
        finish_file.write(f"# Summary\n")
        setup_file = open(f"{lab_slug}/setup.sh", "w")
        setup_file.write("#!/bin/zsh")
        # base index.json config template
        base_config = {
            "type": lab_type,
            "title": lab_title,
            "description": "",
            "difficulty": lab_diff,
            "time": int(lab_time),
            "fee_type": "pro",
            "hidden": False,
            "details": {
                "steps": [],
                "intro": {"text": "intro.md", "background": "setup.sh"},
                "finish": {"text": "finish.md"},
            },
            "backend": {"imageid": lab_image_id},
        }
        # add steps config
        for step_index in range(1, lab_steps + 1):
            base_config["details"]["steps"].append(
                self.init_step(step_index, lab_type, lab_slug)
            )
        # if assets, create assets folder
        if self.if_assets == "yes":
            assets_folder = f"{lab_slug}/assets"
            os.mkdir(assets_folder)
            base_config["details"]["assets"] = {
                "host01": [{"file": "", "target": "/tmp"}]
            }
        # write index.json
        base_file = open(f"{lab_slug}/index.json", "w")
        base_file.write(json.dumps(base_config, indent=2, ensure_ascii=False))

    def init_notebook(self, path: str) -> None:
        """Initialize a notebook lab"""
        with open(path, "r") as f:
            notebook = json.load(f)
        notebook_title = titlecase(
            notebook["cells"][0]["source"][0]
            .replace("### ", "")
            .replace("## ", "")
            .replace("# ", "")
            .strip()
        )
        lab_type = "lab"
        lab_title = Prompt.ask("Enter Lab Title", default=notebook_title)
        lab_slug = f'{lab_type}-{lab_title.lower().replace(" ", "-")}'
        # create folder
        self.check_if_exists(lab_slug)
        # create basic files
        intro_file = open(f"{lab_slug}/intro.md", "w")
        intro_file.write(f"# Introduction\n")
        finish_file = open(f"{lab_slug}/finish.md", "w")
        finish_file.write(
            f"# Summary\n\nCongratulations! You have completed the {lab_title}. You can practice more labs in LabEx to improve your skills."
        )
        setup_file = open(f"{lab_slug}/setup.sh", "w")
        setup_file.write("#!/bin/zsh")
        # base index.json config template
        base_config = {
            "type": lab_type,
            "title": lab_title,
            "description": "In this lab,",
            "difficulty": "Beginner",
            "time": 5,
            "fee_type": "pro",
            "hidden": False,
            "details": {
                "steps": [],
                "intro": {"text": "intro.md", "background": "setup.sh"},
                "finish": {"text": "finish.md"},
            },
            "backend": {"imageid": "webide-ubuntu:2204"},
        }
        # add steps config
        base_config["details"]["steps"].append(self.init_step(1, lab_type, lab_slug))
        # revise step1.md
        step_file = open(f"{lab_slug}/step1.md", "w")
        step_file.write(
            f"# {lab_title}\n\nYou can open the `notebook.ipynb` in WebIDE to start the exercises. Learn how to use [Jupyter Notebooks in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).\n\nWe can not verify your answers automatically in this lab."
        )
        # revise step1 json
        base_config["details"]["steps"][0]["title"] = lab_title
        base_config["details"]["steps"][0]["verify"][0][
            "name"
        ] = "Test the completion of step 1"
        base_config["details"]["steps"][0]["verify"][0][
            "hint"
        ] = "You need to practice coding in notebook.ipynb"
        base_config["details"]["steps"][0]["skills"] = []
        # if assets, create assets folder
        assets_folder = f"{lab_slug}/assets"
        os.mkdir(assets_folder)
        # copy path to assets folder
        os.system(f"cp {path} {assets_folder}/notebook.ipynb")
        base_config["details"]["assets"] = {
            "host01": [
                {"file": "notebook.ipynb", "target": "~/project", "chmod": "ugo+rwx"}
            ]
        }
        # write index.json
        base_file = open(f"{lab_slug}/index.json", "w")
        base_file.write(json.dumps(base_config, indent=2, ensure_ascii=False))
        # prettify lab folder
        os.system(f"prettier --log-level silent --write {lab_slug}/* ")
        print(f"[green]✔[/green] {lab_slug} is created.")
        if click.confirm("Do you want to revise the Introduction?"):
            # get the first 10 cells
            cells = notebook["cells"][:10]
            # append the cells to markdown
            lines = [line for cell in cells for line in cell["source"]]
            lines = "\n".join(lines)
            intro = CreateProject().chat_gpt(
                prompts=f"{lines}\n\n---\n\nPlease write a one-sentence introduction based on the programming experiment abstract above. Start with 'In this lab,'"
            )
            intro = intro.strip().replace("\n", " ")
            intro_file = open(f"{lab_slug}/intro.md", "w")
            intro_file.write(f"# Introduction\n\n{intro}")
            print(f"[green]✔[/green] Introduction is revised.")
            base_config["description"] = intro
            base_file = open(f"{lab_slug}/index.json", "w")
            base_file.write(json.dumps(base_config, indent=2, ensure_ascii=False))
            os.system(f"prettier --log-level silent --write {lab_slug}/* ")
        if click.confirm(f"Delete {path}"):
            os.remove(path)
            print(f"[green]✔[/green] {path} is deleted.")
