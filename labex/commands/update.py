import os
import json
import click
from rich import print
from .utils.titlecase import titlecase


class Update:
    def __init__(self) -> None:
        pass

    def title(self, path: str) -> str:
        """Update lab title from md files

        Returns:
            str: _description_
        """
        # get step title from steps md files
        md_step_titles = []
        for root, dirs, files in os.walk(path):
            step_files = [f for f in files if "step" in f and ".md" in f]
            for step_file in sorted(step_files):
                with open(os.path.join(root, step_file), "r") as f:
                    first_line = f.readline()
                    if first_line.startswith("#"):
                        # remove # and replace ` with ', convert to title case
                        title = titlecase(first_line[2:].strip().replace("`", ""))
                        md_step_titles.append(title)
        # get steps from index.json
        with open(os.path.join(path, "index.json"), "r") as f:
            index_cofig = json.load(f)
            steps_cofig = index_cofig["details"]["steps"]
            in_step_titles = [step["title"] for step in steps_cofig]
            if len(in_step_titles) != len(md_step_titles):
                print("Error: md step titles and index.json steps do not match")
                return
            else:
                # print index steps titles and md step titles
                for in_step_title, md_step_title in zip(in_step_titles, md_step_titles):
                    print(
                        f"[blue]{in_step_title}[/blue] -> [green]{md_step_title}[/green]"
                    )
                if click.confirm("Update index.json steps titles?"):
                    for i, step in enumerate(steps_cofig):
                        step["title"] = md_step_titles[i]
        # write to index.json
        with open(os.path.join(path, "index.json"), "w") as f:
            json.dump(index_cofig, f, indent=2)

