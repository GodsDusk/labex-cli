import os
import click
import json
import openai
import tiktoken
from rich import print
from rich.progress import track
from langchain.text_splitter import RecursiveCharacterTextSplitter


class MDTranslator:
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
        self.trans_prompts = "You are a professional translator. You are helping an English speaker translate Chinese into English. Only translate text and cannot interpret it."
        self.desc_prompts = "You are an AI assistant. Rewrite the content into one sentence and start with 'In this lab'"

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
        print(
            f"[green]✓ {response['model'].upper()}:[/green] {response['usage']['total_tokens']} TOKENS."
        )
        return response["choices"][0]["message"]["content"]

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
        print(f"[yellow]➜ CHUNKS:[/yellow] {len(chunks)}")
        text_translated = ""
        if click.confirm("Start translating?"):
            for chunk in track(chunks, description="➜ Translating"):
                text_translated += self.__chat_gpt(self.trans_prompts, chunk)
        return text_translated

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
        text_translated = self.__translate_text(text)
        # save translated text
        file_name = os.path.basename(file_path)
        file_suffix = os.path.splitext(file_name)[-1]
        new_file_name = file_name.replace(file_suffix, f".en{file_suffix}")
        file_path_translated = os.path.join(os.path.dirname(file_path), new_file_name)
        with open(file_path_translated, "w", encoding="utf-8") as f:
            f.write(text_translated)
        print(f"[green]✓ DONE:[/green] {file_path_translated}")

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
        if self.__in_chinese(title):
            title = self.__chat_gpt(self.trans_prompts, title)
            index["title"] = title
        for step in track(steps, description="➜ Translating"):
            # translate step text
            step_text_path = os.path.join(lab_path, step["text"])
            with open(step_text_path, "r", encoding="utf-8") as f:
                step_text = f.read()
            if self.__in_chinese(step_text):
                # translate step text
                step_text = self.__chat_gpt(self.trans_prompts, step_text)
                with open(step_text_path, "w", encoding="utf-8") as f:
                    f.write(step_text)
            # replace step title
            step_title = step_text.split("\n")[0].replace("# ", "").strip()
            step["title"] = step_title
            # translate step verify
            step_verifies = step["verify"]
            for step_verify in step_verifies:
                verify_name = step_verify["name"]
                verify_hint = step_verify["hint"]
                if self.__in_chinese(verify_name):
                    # translate verify name
                    verify_name = self.__chat_gpt(self.trans_prompts, verify_name)
                    step_verify["name"] = verify_name
                if self.__in_chinese(verify_hint):
                    # translate verify hint
                    verify_hint = self.__chat_gpt(self.trans_prompts, verify_hint)
                    step_verify["hint"] = verify_hint
        # translate intro
        intro = index["details"]["intro"]
        intro_text_path = os.path.join(lab_path, intro["text"])
        print(f"[yellow]➜ INTRO:[/yellow] {intro_text_path}")
        with open(intro_text_path, "r", encoding="utf-8") as f:
            intro_text = f.read()
        if self.__in_chinese(intro_text):
            # translate intro text
            intro_text = self.__chat_gpt(self.trans_prompts, intro_text)
            with open(intro_text_path, "w", encoding="utf-8") as f:
                f.write(intro_text)
        # summary into description
        description = index["description"]
        if not description.startswith("In this lab"):
            description_en = self.__chat_gpt(self.desc_prompts, intro_text)
            index["description"] = description_en
        # translate finish
        finish = index["details"]["finish"]
        finish_text_path = os.path.join(lab_path, finish["text"])
        print(f"[yellow]➜ FINISH:[/yellow] {finish_text_path}")
        with open(finish_text_path, "r", encoding="utf-8") as f:
            finish_text = f.read()
        if self.__in_chinese(finish_text):
            # translate finish text
            finish_text = self.__chat_gpt(self.trans_prompts, finish_text)
            with open(finish_text_path, "w", encoding="utf-8") as f:
                f.write(finish_text)
        # save index.json
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        print(f"[green]✓ DONE:[/green] {index_path}")
        # rename lab folder
        if not click.confirm("Rename lab folder?"):
            return
        lab_name = os.path.dirname(lab_path)
        lab_name_en = f"{index['type']}-{self.__title_slugify(title)}"
        os.rename(lab_name, lab_name_en)
        print(f"[green]✓ DONE:[/green] {lab_name} → {lab_name_en}")
