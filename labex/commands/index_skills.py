import json
import os

from rich import print

from .utils.feishu_api import Feishu
from .utils.skill_trees import ParseSkills


class AddSkills:
    def __init__(self) -> None:
        self.languages = {
            "python": ["py", "python", "bash", "shell"],
            "pandas": ["py", "python"],
            "numpy": ["py", "python"],
            "matplotlib": ["py", "python"],
            "sklearn": ["py", "python"],
            "ml": ["py", "python"],
            "opencv": ["py", "python"],
            "django": ["py", "python"],
            "pygame": ["py", "python"],
            "tkinter": ["py", "python"],
            "flask": ["py", "python"],
            "linux": ["bash", "shell"],
            "shell": ["bash", "shell"],
            "kubernetes": ["bash", "shell"],
            "docker": ["bash", "shell"],
            "git": ["bash", "shell"],
            "ansible": ["bash", "shell"],
            "jenkins": ["bash", "shell"],
            "html": ["html"],
            "css": ["css"],
            "javascript": ["js", "javascript"],
            "react": ["js", "javascript"],
            "jquery": ["js", "javascript"],
            "java": ["java"],
            "c": ["c"],
            "cpp": ["cpp"],
            "go": ["go"],
            "rust": ["rust"],
            "mysql": ["sql", "mysql", "bash", "shell"],
            "sql": ["sql", "mysql", "bash", "shell"],
        }
        self.parse_skills = ParseSkills()

    def __parse_code_block(self, step_content: str, language: str) -> list:
        # parse checker content begin ```checker
        code_blocks = step_content.split(f"```{language}")[1:]
        # parse checker content end ```
        code_block_content = [i.split("```")[0] for i in code_blocks]
        return code_block_content

    def add_skills(self, dir_path: str, skilltree: str) -> None:
        # read the index.json file
        index_path = os.path.join(dir_path, "index.json")
        with open(index_path, "r") as f:
            data = json.load(f)
        steps = data["details"]["steps"]
        task_type = "ADD"
        for step in steps:
            step_skills = set(step.get("skills", []))
            # step_skills = set()
            if skilltree is None:
                task_type = "SORT"
                continue
            solution_files = step.get("solutions")
            if solution_files:  # process challenge
                for file in solution_files:
                    with open(os.path.join(dir_path, "solutions", file), "r") as f:
                        solution_content = f.read()
                    if file.endswith(".md"):  # solution.md
                        for language in self.languages[skilltree]:
                            solution_code_block_content = (
                                self.__parse_code_block(
                                    solution_content, language
                                )
                            )
                            solution_code_block_content = "\n".join(solution_code_block_content)
                            skills = self.parse_skills.parse(
                                skilltree, solution_code_block_content
                            )
                            step_skills.update(skills)
                    else:  # solution with each program language files
                        skills = self.parse_skills.parse(
                            skilltree, solution_content
                        )
                        step_skills.update(skills)
            else:  # process lab
                step_file = step['text']
                with open(os.path.join(dir_path, step_file), "r") as f:
                    step_content = f.read()
                # parse the code block
                languages = self.languages[skilltree]
                for language in languages:
                    code_block_content = self.__parse_code_block(
                        step_content, language
                    )
                    code_block_content = "\n".join(code_block_content)
                    skills = self.parse_skills.parse(
                        skilltree, code_block_content
                    )
                    step_skills.update(skills)
            step["skills"] = sorted(step_skills)

        # update the index.json file
        with open(index_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        # run prettier
        os.system(f"prettier --log-level silent --write {index_path}")
        print(f"[green]→ {task_type} SKILLS:[/] {index_path}")


class RemoveSkills:
    def __init__(self) -> None:
        pass

    def remove_all_skills(
            self, dir_path: str, skilltree: str, remove_skill: str
    ) -> None:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith("index.json"):
                    index_path = os.path.join(root, file)
                    # read the index.json file
                    try:
                        with open(index_path, "r") as f:
                            data = json.load(f)
                        steps = data["details"]["steps"]
                        is_remove = False
                        for step in steps:
                            step_skills = step.get("skills", [])
                            skill_remove = [
                                skill
                                for skill in step_skills
                                if skill.startswith(f"{skilltree}/")
                                   or skill == remove_skill
                            ]
                            if skill_remove:
                                is_remove = True
                                for skill in skill_remove:
                                    step_skills.remove(skill)
                        # update the index.json file
                        if is_remove:
                            with open(index_path, "w") as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            # run prettier
                            os.system(
                                f"prettier --log-level silent --write {index_path}"
                            )
                            print(f"[green]→ REMOVE SKILLS:[/] {index_path}")
                    except Exception as e:
                        print(f"[red]→ ERROR:[/] {index_path}")
                        print(e)

    def remove_invalid_skills(
            self, app_id: str, app_secret: str, dir_path: str
    ) -> None:
        # 从 skill tree 获取完整的 skill ids
        feishu = Feishu(app_id, app_secret)
        app_token = "bascnNz4Nqjqgqm1Nm5AYke6xxb"
        skills_table_id = "tblV5pGIsGZMxmE9"
        records = feishu.get_bitable_records(app_token, skills_table_id, params="")
        skills = [r["fields"]["SKILL_ID"][0]["text"] for r in records]
        print(f"[green]✔ Get[/green]: {len(skills)} skills in Feishu.")
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith("index.json"):
                    index_path = os.path.join(root, file)
                    # read the index.json file
                    try:
                        with open(index_path, "r") as f:
                            data = json.load(f)
                        steps = data["details"]["steps"]
                        is_remove = False
                        remove_skills = []
                        for step in steps:
                            step_skills = step.get("skills", [])
                            for skill in step_skills:
                                if skill not in skills:
                                    step_skills.remove(skill)
                                    remove_skills.append(skill)
                                    is_remove = True
                        if is_remove:
                            # update the index.json file
                            with open(index_path, "w") as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            # run prettier
                            os.system(
                                f"prettier --log-level silent --write {index_path}"
                            )
                            print(
                                f"[green]→ REMOVE SKILLS:[/] {index_path} {remove_skills}"
                            )
                    except Exception as e:
                        print(f"[red]→ ERROR:[/] {index_path}")
                        print(e)
