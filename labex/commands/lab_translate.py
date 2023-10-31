import os
import click
import json
import openai
import tiktoken
from rich import print
from titlecase import titlecase
from rich.progress import track
from langchain.text_splitter import RecursiveCharacterTextSplitter


class Translator:
    def __init__(self, gpt_model: str):
        # split text into chunks
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.chunk_size = 4096
        # openai
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
        # gpt model
        if gpt_model == "35":
            self.engine = "gpt-35-turbo-16k"
        elif gpt_model == "4":
            self.engine = "gpt-4"
        # system prompts
        self.trans_prompts = "You are a translation engine, you can only translate chinese markdown text into english using formal language. You cannot interpret it, and do not explain."

    def __chat_gpt(self, system_prompts: str, user_prompts: str) -> str:
        """ChatGPT API

        Args:
            prompts (str): prompts

        Returns:
            str: response
        """
        openai.api_type = self.openai_type
        openai.api_key = self.openai_key
        openai.api_base = self.openai_base
        openai.api_version = self.openai_version
        response = openai.ChatCompletion.create(
            deployment_id=self.engine,
            model=self.engine,
            messages=[
                {
                    "role": "system",
                    "content": system_prompts,
                },
                {"role": "user", "content": user_prompts},
            ],
        )
        output_text = response["choices"][0]["message"]["content"]
        output_tokens = response["usage"]["total_tokens"]
        return output_text, output_tokens

    def __token_price(self, tokens: int) -> float:
        pricing = round(tokens / 1000 * 0.004, 2)
        return pricing

    def __tiktoken_len(self, text) -> int:
        """length function"""
        tokens = self.tokenizer.encode(text, disallowed_special=())
        return len(tokens)

    def __text_splitter(self, text: str) -> list:
        """Text Splitter

        Args:
            text (str): text

        Returns:
            chunks: chunks
        """
        tokens = self.tokenizer.encode(text, disallowed_special=())
        print(f"[yellow]➜ TOKENS:[/yellow] {len(tokens)}")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=5,
            length_function=self.__tiktoken_len,
        )
        chunks = text_splitter.split_text(text)
        return chunks

    def __translate_text(self, text: str) -> str:
        """Translate

        Args:
            text (str): text

        Returns:
            str: translated text
        """
        chunks = self.__text_splitter(text)
        tokens = self.__tiktoken_len(text)
        print(f"[yellow]➜ TOKENS:[/yellow] {tokens}, ${self.__token_price(tokens)}")
        print(f"[yellow]➜ CHUNKS:[/yellow] {len(chunks)}")
        text_translated = ""
        text_tokens = 0
        if click.confirm("Start translating?"):
            for chunk in track(chunks, description="➜ Translating"):
                output_text, output_tokens = self.__chat_gpt(self.trans_prompts, chunk)
                text_translated += output_text
                text_tokens += output_tokens
        return text_translated, text_tokens

    def __in_chinese(self, text: str) -> bool:
        """Check if the text is in Chinese

        Args:
            text (str): text

        Returns:
            bool: True or False
        """
        for ch in text:
            if "\u4e00" <= ch <= "\u9fff":
                return True
        return False

    def __title_slugify(self, title: str) -> str:
        """Slugify title

        Args:
            title (str): title

        Returns:
            str: slugified title
        """
        return (
            title.replace(" ", "-")
            .lower()
            .replace("/", "-")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
            .replace(".", "")
            .replace("?", "")
            .replace("!", "")
        )

    def translate_md(self, file_path: str) -> str:
        """Translate File

        Args:
            file_path (str): file_path

        Returns:
            str: translated text
        """
        print(f"[yellow]➜ FILE:[/yellow] {file_path}")
        # read text
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        text_translated, text_tokens = self.__translate_text(text)
        # save translated text
        file_name = os.path.basename(file_path)
        file_suffix = os.path.splitext(file_name)[-1]
        new_file_name = file_name.replace(file_suffix, f".en{file_suffix}")
        file_path_translated = os.path.join(os.path.dirname(file_path), new_file_name)
        with open(file_path_translated, "w", encoding="utf-8") as f:
            f.write(text_translated)
        print(
            f"[green]✔ DONE:[/green] {file_path_translated} (tokens: {text_tokens}, ${self.__token_price(text_tokens)})"
        )

    def translate_lab(self, lab_path: str) -> str:
        """Translate Lab Folder

        Args:
            lab_path (str): lab_path

        Returns:
            str: translated text
        """
        print(f"[yellow]➜ FOLDER:[/yellow] {lab_path}")
        # search index.json
        for root, dirs, files in os.walk(lab_path):
            for file in files:
                if file == "index.json":
                    index_path = os.path.join(root, file)
        if index_path is None:
            print("[red]✗ ERROR:[/red] index.json not found.")
            exit(1)
        print(f"[yellow]➜ INDEX:[/yellow] {index_path}")
        # read index.json
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
        # translate index.json
        title = index["title"]
        print(f"[yellow]➜ TITLE:[/yellow] {title}")
        # translate steps
        steps = index["details"]["steps"]
        print(f"[yellow]➜ STEPS:[/yellow] {len(steps)}")
        if not click.confirm("Start translating?"):
            return
        all_tokens = 0
        if self.__in_chinese(title):
            title, output_tokens = self.__chat_gpt(self.trans_prompts, title)
            all_tokens += output_tokens
            index["title"] = titlecase(title)
        for step in track(steps, description="➜ TRANSLATING STEPS"):
            # translate step text
            step_text_path = os.path.join(lab_path, step["text"])
            with open(step_text_path, "r", encoding="utf-8") as f:
                step_text = f.read()
            if self.__in_chinese(step_text):
                # translate step text
                step_text, output_tokens = self.__chat_gpt(
                    self.trans_prompts, step_text
                )
                all_tokens += output_tokens
                with open(step_text_path, "w", encoding="utf-8") as f:
                    f.write(step_text)
            # replace step title
            step_title = step_text.split("\n")[0].replace("# ", "").strip()
            step_title_titlecase = titlecase(step_title)
            # replace step title in step_text_path
            with open(step_text_path, "r", encoding="utf-8") as f:
                step_text = f.read()
            # delete the first line in step_text
            step_text = "\n".join(step_text.split("\n")[1:])
            # add step title in step_text
            step_text = f"# {step_title_titlecase}\n{step_text}"
            with open(step_text_path, "w", encoding="utf-8") as f:
                f.write(step_text)
            # replace step title in index.json
            step["title"] = step_title_titlecase
            # translate step verify
            step_verifies = step["verify"]
            for step_verify in step_verifies:
                verify_name = step_verify["name"]
                verify_hint = step_verify["hint"]
                if self.__in_chinese(verify_name):
                    # translate verify name
                    verify_name, output_tokens = self.__chat_gpt(
                        self.trans_prompts, verify_name
                    )
                    all_tokens += output_tokens
                    step_verify["name"] = titlecase(verify_name)
                if self.__in_chinese(verify_hint):
                    # translate verify hint
                    verify_hint, output_tokens = self.__chat_gpt(
                        self.trans_prompts, verify_hint
                    )
                    all_tokens += output_tokens
                    step_verify["hint"] = verify_hint
        # translate intro
        intro = index["details"]["intro"]
        intro_text_path = os.path.join(lab_path, intro["text"])
        print(f"[yellow]➜ INTRO:[/yellow] {intro_text_path}")
        with open(intro_text_path, "r", encoding="utf-8") as f:
            intro_text = f.read()
        if self.__in_chinese(intro_text):
            # translate intro text
            intro_text, output_tokens = self.__chat_gpt(self.trans_prompts, intro_text)
            all_tokens += output_tokens
            # delete the first line in intro_text
            intro_text = "\n".join(intro_text.split("\n")[1:])
            # add step title in intro_text
            intro_text = f"# Introduction\n{intro_text}"
            with open(intro_text_path, "w", encoding="utf-8") as f:
                f.write(intro_text)
        # summary into description
        description = index["description"]
        if not description.startswith(f"In this {index['type']}"):
            desc_prompts = f"You are an AI assistant. Rewrite the content into one sentence and start with 'In this {index['type']}'"
            description_en, output_tokens = self.__chat_gpt(desc_prompts, intro_text)
            all_tokens += output_tokens
            index["description"] = description_en
        # translate finish
        finish = index["details"]["finish"]
        finish_text_path = os.path.join(lab_path, finish["text"])
        print(f"[yellow]➜ FINISH:[/yellow] {finish_text_path}")
        with open(finish_text_path, "r", encoding="utf-8") as f:
            finish_text = f.read()
        if self.__in_chinese(finish_text):
            # translate finish text
            finish_text, output_tokens = self.__chat_gpt(
                self.trans_prompts, finish_text
            )
            all_tokens += output_tokens
            # delete the first line in finish_text
            finish_text = "\n".join(finish_text.split("\n")[1:])
            # add step title in finish_text
            finish_text = f"# Summary\n{finish_text}"
            with open(finish_text_path, "w", encoding="utf-8") as f:
                f.write(finish_text)
        # save index.json
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        print(
            f"[green]✔ DONE:[/green] {index_path} (tokens: {all_tokens}, ${self.__token_price(all_tokens)})"
        )
        # rename lab folder
        if not click.confirm("Rename lab folder?"):
            return
        if "/" in lab_path:
            lab_name = os.path.dirname(lab_path)
        else:
            lab_name = lab_path
        lab_name_en = f"{index['type']}-{self.__title_slugify(title)}"
        os.rename(lab_name, lab_name_en)
        print(f"[green]✔ DONE:[/green] {lab_name} → {lab_name_en}")
        # run prettier
        os.system(f"prettier --log-level silent --write {lab_name_en}")
        print(f"[green]✔ prettier done![/green]")

    def __parse_ipynb(self, ipynb_file: str) -> dict:
        """Parse ipynb file

        Args:
            ipynb_file (str): ipynb file

        Returns:
            dict: parsed ipynb
        """
        with open(ipynb_file, "r") as f:
            ipynb = json.load(f)
        return ipynb

    def __count_ipynb_tokens(self, ipynb_file: str) -> None:
        """Count tokens of ipynb file

        Args:
            ipynb_file (str): ipynb file

        Returns:
            tokens length: tokens of sentences in Chinese
            pricing: pricing
        """
        ipynb = self.__parse_ipynb(ipynb_file)
        all_content = ""
        cell_count = 0
        for cell in ipynb["cells"]:
            if cell["cell_type"] == "markdown" or cell["cell_type"] == "code":
                cell_source = cell["source"]
                for source in cell_source:
                    if self.__in_chinese(source):
                        all_content += source
                        cell_count += 1
        cell_tokens = self.tokenizer.encode(all_content, disallowed_special=())
        cell_length = len(cell_tokens)
        prompts_tokens = self.tokenizer.encode(
            self.trans_prompts, disallowed_special=()
        )
        prompts_length = len(prompts_tokens) * cell_count
        length = cell_length + prompts_length
        return length

    def translate_ipynb(self, ipynb_file: str) -> None:
        """Translate ipynb file

        Args:
            ipynb_file (str): ipynb file
        """
        tokens = self.__count_ipynb_tokens(ipynb_file)
        print(f"[yellow]➜ TOKENS:[/yellow] {tokens}, ${self.__token_price(tokens)}")
        if click.confirm(f"Translate {ipynb_file}?"):
            file_name = os.path.basename(ipynb_file)
            ipynb = self.__parse_ipynb(ipynb_file)
            all_tokens = 0
            for cell in track(
                ipynb["cells"], description=f"Translating {file_name}..."
            ):
                if cell["cell_type"] == "markdown" or cell["cell_type"] == "code":
                    cell_source = cell["source"]
                    source_translated = []
                    for source in cell_source:
                        if "base64" in source or len(source) > 4096:
                            print(
                                f"[yellow]→ SKIP:[/yellow] source too long or base64."
                            )
                            continue
                        if self.__in_chinese(source):
                            output_text, output_tokens = self.__chat_gpt(
                                self.trans_prompts, source
                            )
                            all_tokens += output_tokens
                            source_translated.append(output_text)
                        else:
                            source_translated.append(source)
                    cell["source"] = source_translated
            output_file = ipynb_file.replace(".ipynb", f"_en.ipynb")
            with open(output_file, "w") as f:
                json.dump(ipynb, f, indent=2, ensure_ascii=False)
            print(
                f"[green]✔ DONE:[/green] {output_file} (tokens: {all_tokens}, ${self.__token_price(all_tokens)})"
            )
