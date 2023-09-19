import os
import json
import click
import openai
from rich import print
from titlecase import titlecase


class CreateProject:
    def __init__(self):
        self.openai_type = "azure"
        self.openai_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.openai_base = os.getenv("AZURE_OPENAI_API_BASE")
        self.openai_version = "2023-07-01-preview"
        if self.openai_key is None:
            print(
                "[red]✗ ERROR:[/red] AZURE_OPENAI_API_KEY environment variable not set."
            )
            exit(1)
        if self.openai_base is None:
            print(
                "[red]✗ ERROR:[/red] AZURE_OPENAI_API_BASE environment variable not set."
            )
            exit(1)

    def __chat_gpt(self, prompts: str, gpt_model: str) -> str:
        """ChatGPT API

        Args:
            prompts (str): prompts
            gpt_model (str): gpt_model

        Returns:
            str: response
        """
        openai.api_type = self.openai_type
        openai.api_key = self.openai_key
        openai.api_base = self.openai_base
        openai.api_version = self.openai_version
        if gpt_model == "35":
            engine = "gpt-35-turbo-16k"
        elif gpt_model == "4":
            engine = "gpt-4"
        print(f"[yellow]➜ ENGINE:[/yellow] {engine}")
        response = openai.ChatCompletion.create(
            deployment_id=engine,
            model=engine,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps people find information.",
                },
                {"role": "user", "content": prompts},
            ],
        )
        print(
            f"[green]✓ DONE:[/green] {response['model']}-{response['usage']['total_tokens']} tokens used."
        )
        return response["choices"][0]["message"]["content"]

    def __chat_gpt_fc(self, prompts: str, gpt_model: str, techstack: str) -> str:
        """ChatGPT Function Call API

        Args:
            prompts (str): prompts
            gpt_model (str): gpt_model
            techstack (str): techstack for prompts

        Returns:
            str: response
        """
        messages = [{"role": "user", "content": prompts}]
        functions = [
            {
                "name": "develop_a_project",
                "description": f"Develop a project using {techstack}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Project Title",
                            "minLength": 5,
                            "maxLength": 50,
                        },
                        "code_file_name": {
                            "type": "string",
                            "description": "The code file name of the project.",
                        },
                        "full_codes": {
                            "type": "string",
                            "description": "The full codes of the project. The project code must be ensured to be executable.",
                        },
                    },
                    "required": ["title", "code_file_name", "full_codes"],
                },
            }
        ]
        openai.api_type = self.openai_type
        openai.api_key = self.openai_key
        openai.api_base = self.openai_base
        openai.api_version = self.openai_version
        if gpt_model == "35":
            engine = "gpt-35-turbo-16k"
        elif gpt_model == "4":
            engine = "gpt-4"
        print(f"[yellow]➜ ENGINE:[/yellow] {engine}")
        response = openai.ChatCompletion.create(
            engine=engine,
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            function_args = json.loads(response_message["function_call"]["arguments"])
            return function_args
        else:
            return None

    def __parse_md(self, md: str) -> tuple:
        """Parse Lab MD File

        Args:
            md (str): md file

        Returns:
            str: lab_title, lab_intro, lab_steps, lab_summary
        """
        # read the md file
        with open(md, "r") as f:
            md_content = f.read()
        # Title begins with markdown first level header
        lab_title = titlecase(md_content.split("\n")[0].replace("# ", "").strip())
        # remove begin and end spaces
        lab_title = lab_title.strip()
        # Introduction begins with "## Introduction"
        lab_intro = md_content.split("## Introduction")[1].split("## Steps")[0].strip()
        # Steps begins with "## Steps"
        lab_steps_raw = md_content.split("## Steps")[1].split("## Summary")[0].strip()
        # Split the steps into a list
        lab_steps = lab_steps_raw.split("### Step")[1:]
        # Summary begins with "## Summary"
        try:
            lab_summary = md_content.split("## Summary")[1].strip()
        except:
            lab_summary = f"# Summary\n\nCongratulations! You have completed the {lab_title} lab. You can practice more labs in LabEx to improve your skills.\n"
        return lab_title, lab_intro, lab_steps, lab_summary

    def __new_lab(
        self,
        path: str,
        lab_title: str,
        lab_intro: str,
        lab_steps: str,
        lab_summary: str,
    ) -> None:
        """Create a new lab

        Args:
            path (str): path to save the lab
            lab_title (str): lab title
            lab_intro (str): lab introduction
            lab_steps (str): lab steps
            lab_summary (str): lab summary
        """
        # create assets folder
        assets_folder = os.path.join(path, "assets")
        if not os.path.exists(assets_folder):
            os.makedirs(assets_folder)
        # move all existing files to assets folder
        for file in os.listdir(path):
            if file != "assets":
                os.rename(os.path.join(path, file), os.path.join(assets_folder, file))
        # create intro.md
        intro_path = os.path.join(path, "intro.md")
        intro_file = open(intro_path, "w")
        intro_file.write(f"# Introduction\n\n{lab_intro}\n")
        # create finish.md
        finish_path = os.path.join(path, "finish.md")
        finish_file = open(finish_path, "w")
        finish_file.write(f"# Summary\n\n{lab_summary}\n")
        # create setup.sh
        setup_path = os.path.join(path, "setup.sh")
        setup_file = open(setup_path, "w")
        setup_file.write("#!/bin/zsh\n")
        # create solutions folder
        solutions_folder = os.path.join(path, "solutions")
        if not os.path.exists(solutions_folder):
            os.makedirs(solutions_folder)
        # create stepx.md from lab_steps list
        steps_config = []
        step_count = 0
        for i, step_content in enumerate(lab_steps):
            # create stepx.md for each step
            step_path = os.path.join(path, f"step{i+1}.md")
            step_file = open(step_path, "w")
            step_file.write(f"# {step_content[4:]}\n")
            # create verifyx.sh for each step
            verify_path = os.path.join(path, f"verify{i+1}.sh")
            verify_file = open(verify_path, "w")
            verify_file.write(f"#!/bin/zsh\n")
            # step title
            step_title = step_content.split("\n\n")[0].strip()[3:]
            # step index.json config
            step_config = {
                "title": f"{step_title}",
                "text": f"step{i+1}.md",
                "verify": [
                    {
                        "name": f"Test the completion of step {i+1}",
                        "file": f"verify{i+1}.sh",
                        "hint": f"You need to practice coding in LabEx VM.",
                        "timeout": 0,
                        "showstderr": False,
                    }
                ],
                "skills": [],
            }
            steps_config.append(step_config)
            step_count += 1
        # create index.json
        index_path = os.path.join(path, "index.json")
        index_file = open(index_path, "w")
        # index.json config template
        index_config = {
            "type": "lab",
            "title": lab_title,
            "description": lab_intro,
            "difficulty": "Beginner",
            "time": step_count * 5,
            "hidden": False,
            "fee_type": "pro",
            "details": {
                "steps": steps_config,
                "intro": {"text": "intro.md", "background": "setup.sh"},
                "finish": {"text": "finish.md"},
                "assets": {
                    "host01": [
                        {
                            "file": "",
                            "target": "~/project",
                            "chmod": "ugo+rwx",
                        }
                    ]
                },
            },
            "backend": {
                "imageid": "webide-vnc-ubuntu:2204",
            },
            "contributors": [],
        }
        index_file.write(json.dumps(index_config, indent=2, ensure_ascii=False))
        print(f"[green]✓ DONE:[/green] {lab_title} created successfully.")

    def __parse_json_content(self, json_path: str) -> str:
        """Parse JSON Content from data.json

        Args:
            json_path (str): json file path

        Returns:
            str: lab_content_prompt
        """
        with open(json_path, "r") as f:
            content = json.load(f)
        title = content["title"]
        code_file_name = content["code_file_name"]
        # read the code file
        with open(f"{os.path.dirname(json_path)}/{code_file_name}", "r") as f:
            full_codes = f.read()
        lab_content_prompt = f"# {title}\n\nIn this tutorial, you need to create a file named {code_file_name} and write the following code in it:\n\n```\n{full_codes}\n```"
        return lab_content_prompt

    def create_project_code(
        self,
        path: str,
        project_name: str,
        project_description: str,
        gpt_model: str,
        techstack: str,
        mode: str,
    ) -> None:
        """STEP1: Create Project Code

        Args:
            path (str): save path
            project_name (str): project name
            project_description (str): project description
            gpt_model (str): gpt_model
            techstack (str): techstack
            mode (str): mode
        """
        lab_name_lower = (
            project_name.lower().replace(" ", "-").replace("/", "-").replace(":", "-")
        )
        path_name = f"{os.path.join(path, lab_name_lower)}-using-{techstack.lower().replace(' ', '-')}"
        if os.path.exists(path_name):
            print(f"[red]✗ ERROR:[/red] {path_name} already exists.")
            return
        else:
            try:
                print(f"[yellow]➜ PROJECT:[/yellow] {project_name}")
                lab_content_prompt = f"Please help me to develop a project named {project_name} using {techstack}: {project_description} It should contain the file name and full codes. The project code must be ensured to be executable. The user interface is beautiful and modern."
                print(f"[yellow]➜ PROMPTS:[/yellow] {lab_content_prompt}")
                if mode == "fc":
                    print(f"[yellow]➜ MODE:[/yellow] Function Call")
                    lab_content = self.__chat_gpt_fc(
                        lab_content_prompt, gpt_model=gpt_model, techstack=techstack
                    )
                    if lab_content is not None:
                        # create the folder
                        os.mkdir(path_name)
                        # save the json
                        with open(f"{path_name}/data.json", "w") as f:
                            json.dump(lab_content, f, indent=2, ensure_ascii=False)
                        code_file_name = lab_content["code_file_name"]
                        full_codes = lab_content["full_codes"]
                        # create code file
                        with open(f"{path_name}/{code_file_name}", "w") as f:
                            f.write(full_codes)
                        print(f"[green]✓ SAVE:[/green] {path_name}")
                    else:
                        print(f"[red]➜ MODE:[/red] Change to markdown mode.")
                        lab_content = self.__chat_gpt(
                            lab_content_prompt, gpt_model=gpt_model
                        )
                        if lab_content is not None:
                            # create the folder
                            os.mkdir(path_name)
                            # save the json
                            with open(f"{path_name}/data.md", "w") as f:
                                f.write(lab_content)
                            print(f"[green]✓ SAVE:[/green] {path_name}")
                elif mode == "md":
                    print(f"[yellow]➜ MODE:[/yellow] Markdown")
                    lab_content = self.__chat_gpt(
                        lab_content_prompt, gpt_model=gpt_model
                    )
                    if lab_content is not None:
                        # create the folder
                        os.mkdir(path_name)
                        # save the json
                        with open(f"{path_name}/data.md", "w") as f:
                            f.write(lab_content)
                        print(f"[green]✓ SAVE:[/green] {path_name}")
            except Exception as e:
                print(f"[red]✗ ERROR:[/red] {project_name} failed, {e}")
                pass

    def create_project_md(self, path: str, gpt_model: str) -> None:
        """STEP2: Create Project MD

        Args:
            path (str): data.md or data.json path
            gpt_model (str): gpt_model
        """
        json_path = os.path.join(path, "data.json")
        md_path = os.path.join(path, "data.md")
        if os.path.exists(json_path):
            print(f"[yellow]➜ FOUND:[/yellow] {json_path}")
            lab_content = self.__parse_json_content(json_path)
        elif os.path.exists(md_path):
            print(f"[yellow]➜ FOUND:[/yellow] {md_path}")
            with open(md_path, "r") as f:
                lab_content = f.read()
        else:
            print(f"[red]✗[/red] data.json or data.md not found.")
            exit(1)
        lab_content_prompt = f'Please revise the following content to a step-by-step tutorial as required. The tutorial only contains the Title, Introduction, Steps, and Summary. The title should begin with "# <Title>", and use Title Case. Introduction, Steps, Summary should begin with "## Introduction", "## Steps", and "## Summary". The complete code needs to be split into multiple steps. Each step should begin with "### Step X: <Step Title>", and the step title should be concise and clear. Each step should contain code blocks, and the code blocks must have code comments and language identifier. Ensure the code is correct and can be executed. Each step should be explained in detail. The first step is to create the project files. The final step is how to run this project. Ensure the authenticity of the content and avoid fabrication. Be sure to include any necessary background information and avoid using technical jargon. Use markdown syntax to output the modified content. This tutorial needs to be completed so that students can complete it step by step.\n\n---\n\n{lab_content}'
        print(f"[yellow]➜ PROMPTS:[/yellow] {lab_content_prompt}")
        step_raw_path = os.path.join(path, "step_raw.md")
        lab_content = self.__chat_gpt(lab_content_prompt, gpt_model)
        with open(step_raw_path, "w") as f:
            f.write(lab_content)
            print(f"[green]✓ SAVE:[/green] {step_raw_path}")

    def create_project_lab(self, path: str) -> None:
        """STEP3: Create Project Lab

        Args:
            path (str): step_raw.md path
        """
        step_raw_path = os.path.join(path, "step_raw.md")
        if os.path.exists(step_raw_path):
            lab_title, lab_intro, lab_steps, lab_summary = self.__parse_md(
                step_raw_path
            )
            print(f"[yellow]➜ TITLE:[/yellow] {lab_title}")
            print(f"[yellow]➜ INTRO:[/yellow] {lab_intro}")
            print(f"[yellow]➜ STEPS:[/yellow] {len(lab_steps)} steps")
            print(f"[yellow]➜ SUMMA:[/yellow] {lab_summary}")
            if click.confirm(f"➜ Create this lab?"):
                self.__new_lab(path, lab_title, lab_intro, lab_steps, lab_summary)
                lab_title_lower = (
                    lab_title.lower()
                    .replace(" ", "-")
                    .replace("/", "-")
                    .replace(":", "-")
                )
                # rename folder to lab_title_lower
                os.rename(path, lab_title_lower)
        else:
            print(f"[red]✗ ERROR:[/red] {step_raw_path} not found.")
