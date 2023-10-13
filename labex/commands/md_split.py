import os
import json
import yaml
import click
from titlecase import titlecase
from rich import print


class MDSplitter:
    def __init__(self) -> None:
        pass

    def __parse_md(self, md_path: str) -> tuple:
        """parse md file to title, intro, steps, summary

        Args:
            md (str): md file path

        Returns:
            tuple: title, intro, steps, summary
        """
        # read the md file
        with open(md_path, "r") as f:
            md_content = f.read()
        print(f"[yellow]➜ FILE:[/yellow] {md_path}")
        # Title begins with markdown first level header
        lab_title = titlecase(md_content.split("\n")[0].replace("# ", "").strip())
        # remove begin and end spaces
        lab_title = lab_title.strip()
        print(f"➜ TITLE: {lab_title}")
        # Introduction between Title and firt ## second level header
        lab_intro = md_content.split("\n## ")[1]
        print(f"➜ INTRO: {len(lab_intro)} chars")
        # each step begins with ## second level header
        lab_steps = md_content.split("\n## ")[2:]
        print(f"➜ STEPS: {len(lab_steps)} steps")
        lab_summary = lab_steps[-1]
        print(f"➜ SUMMARY: {len(lab_summary)} chars")
        return lab_title, lab_intro, lab_steps, lab_summary

    def __parse_checker(self, step_index: int, step_content: str) -> list:
        """parse checker content from step content

        Args:
            step_index (int): step index
            step_content (str): step content

        Returns:
            list: checker content
        """
        # parse checker content begin ```checker
        checker = step_content.split("```checker")[1:]
        # parse checker content end ```
        checker_content = [c.split("```")[0] for c in checker]
        # parse checker content from yaml to dict
        checker_content = [
            yaml.load(c, Loader=yaml.FullLoader) for c in checker_content
        ]
        # merge checker content into one dict
        checker_content = [d for c in checker_content for d in c]
        print(f"➜ CHECKERS: {len(checker_content)} checkers in step {step_index+1}")
        return checker_content

    def __delete_checker(self, step_content: str) -> str:
        """delete checker content from step content

        Args:
            step_content (str): step content

        Returns:
            str: step content without checker content
        """
        # parse checker content begin ```checker
        checker = step_content.split("```checker")[1:]
        # parse checker content end ```
        checker_content = [i.split("```")[0] for i in checker]
        # delete checker content
        step_content = step_content.replace(
            "```checker" + checker_content[0] + "```", ""
        )
        return step_content

    def new_lab(self, md_path: str) -> None:
        """create new lab folder"""
        # parse md file
        lab_title, lab_intro, lab_steps, lab_summary = self.__parse_md(md_path)
        if not click.confirm("Start creating lab?"):
            return
        # create lab slug
        lab_slug = f"lab-{lab_title.lower().replace(' ', '-')}"
        if os.path.exists(lab_slug):
            print(f"[red]✘ {lab_slug} already exists![/red]")
            return
        # create folder
        os.mkdir(lab_slug)
        print(f"[green]✔ {lab_slug} created![/green]")
        # create intro.md
        intro_file = open(f"{lab_slug}/intro.md", "w")
        intro_file.write(f"# {lab_intro.strip()}")
        # create finish.md
        finish_file = open(f"{lab_slug}/finish.md", "w")
        finish_file.write(f"# {lab_summary.strip()}")
        # create setup.sh
        setup_file = open(f"{lab_slug}/setup.sh", "w")
        setup_file.write("#!/bin/zsh\n")
        # create stepx.md from lab_steps list
        steps_config = []
        step_count = 0
        lab_steps = lab_steps[:-1]
        for step_index, step_content in enumerate(lab_steps):
            step_title = step_content.split("\n\n")[0].strip()
            if "```checker" in step_content:
                checkers = self.__parse_checker(step_index, step_content)
                verifys = []
                for checker_index, checker in enumerate(checkers):
                    checker_name = checker.get(
                        "name", "Check the completion of the step"
                    )
                    checker_script = checker.get("script", "#!/bin/bash\n")
                    checker_error = checker.get(
                        "error", "Please check the step carefully."
                    )
                    checker_script_file = f"verify{step_index+1}-{checker_index+1}.sh"
                    with open(f"{lab_slug}/{checker_script_file}", "w") as f:
                        f.write(checker_script)
                    verify_json = {
                        "name": checker_name.strip(),
                        "file": checker_script_file,
                        "hint": checker_error.strip(),
                        "timeout": 0,
                        "showstderr": False,
                    }
                    verifys.append(verify_json)
                step_config = {
                    "title": step_title.strip(),
                    "text": f"step{step_index+1}.md",
                    "verify": verifys,
                    "skills": [],
                    "solutions": [],
                }
                steps_config.append(step_config)
                # delete checker content
                step_content = self.__delete_checker(step_content)
            else:
                # create verifyx.sh for each step
                verify_file = open(f"{lab_slug}/verify{step_index+1}.sh", "w")
                verify_file.write(f"#!/bin/zsh\n")
                # step index.json config
                step_config = {
                    "title": step_title.strip(),
                    "text": f"step{step_index+1}.md",
                    "verify": [
                        {
                            "name": f"Test the completion of step {step_index+1}",
                            "file": f"verify{step_index+1}.sh",
                            "hint": f"Please check the step {step_index+1} carefully.",
                            "timeout": 0,
                            "showstderr": False,
                        }
                    ],
                    "skills": [],
                    "solutions": [],
                }
                steps_config.append(step_config)
            step_file = open(f"{lab_slug}/step{step_index+1}.md", "w")
            step_file.write(f"# {step_content}\n")
        # create assets folder
        assets_folder = f"{lab_slug}/assets"
        os.mkdir(assets_folder)
        # create solutions folder
        solution_folder = f"{lab_slug}/solutions"
        os.mkdir(solution_folder)
        # convert lab_intro to one line string and select first sentence as description
        lab_description = lab_intro.replace("\n", " ").split(".")[0]
        # create index.json
        base_file = open(f"{lab_slug}/index.json", "w")
        # index.json config template
        base_config = {
            "type": "lab",
            "title": lab_title,
            "description": lab_description,
            "difficulty": "Beginner",
            "time": step_count * 5,
            "hidden": False,
            "fee_type": "pro",
            "details": {
                "steps": steps_config,
                "intro": {"text": "intro.md", "background": "setup.sh"},
                "finish": {"text": "finish.md"},
                "assets": {"host01": [{"file": "", "target": "/tmp"}]},
            },
            "backend": {
                "imageid": "webide-ubuntu:2204",
            },
        }
        base_file.write(json.dumps(base_config, indent=2, ensure_ascii=False))
        print(f"[green]✔ {lab_slug}/index.json created![/green]")
        # run prettier
        os.system(f"prettier --log-level silent --write {lab_slug}")
        print(f"[green]✔ prettier done![/green]")