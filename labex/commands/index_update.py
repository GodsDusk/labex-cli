import os
import json
from rich import print
from .utils.titlecase import titlecase


class UpdateIndexJSON:
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
            step_files = [
                {"name": f, "step": int(f[4:-3])}
                for f in files
                if "step" in f and ".md" in f
            ]
            step_files_sorted = sorted(step_files, key=lambda d: d["step"])
            for step_file_ in step_files_sorted:
                step_file = step_file_["name"]
                with open(os.path.join(root, step_file), "r") as f:
                    lines = f.readlines()
                first_line = lines[0]
                if first_line.startswith("#"):
                    # remove # and replace ` with ', convert to title case
                    title = titlecase(first_line[2:].strip().replace("`", ""))
                    md_step_titles.append(title)
                    # Update title in md file
                    lines[0] = f"# {title}\n"
                    with open(os.path.join(root, step_file), "w") as f:
                        f.writelines(lines)
                        print(
                            f"{step_file}: [blue]{first_line[:-1]}[/blue] -> [green]{lines[0][:-1]}[/green]"
                        )
        # get steps from index.json
        with open(os.path.join(path, "index.json"), "r") as f:
            index_cofig = json.load(f)
            steps_cofig = index_cofig["details"]["steps"]
            in_step_titles = [step["title"] for step in steps_cofig]
            if len(in_step_titles) != len(md_step_titles):
                print("Error: md step titles and index.json steps do not match")
                return
            else:
                for i, step in enumerate(steps_cofig):
                    step["title"] = md_step_titles[i]
        # write to index.json
        with open(os.path.join(path, "index.json"), "w") as f:
            json.dump(index_cofig, f, indent=2)

