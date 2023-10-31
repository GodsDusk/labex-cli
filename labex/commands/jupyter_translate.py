import os
import click
import json
import openai
import tiktoken
from rich import print
from rich.progress import track


class IpynbTranslator:
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
        total_tokens = response["usage"]["total_tokens"]
        return output_text, total_tokens

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

    def __count_tokens(self, ipynb_file: str) -> None:
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
        # pricing
        pricing = round(length / 1000 * 0.004, 2)
        return length, pricing

    def translate_ipynb(self, ipynb_file: str) -> None:
        """Translate ipynb file

        Args:
            ipynb_file (str): ipynb file
        """
        length, pricing = self.__count_tokens(ipynb_file)
        if click.confirm(f"Translate {ipynb_file} ({length} tokens, ${pricing})?"):
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
                            output_text, total_tokens = self.__chat_gpt(
                                self.trans_prompts, source
                            )
                            source_translated.append(output_text)
                            all_tokens += total_tokens
                        else:
                            source_translated.append(source)
                    cell["source"] = source_translated
            output_file = ipynb_file.replace(".ipynb", f"_en.ipynb")
            with open(output_file, "w") as f:
                json.dump(ipynb, f, indent=2, ensure_ascii=False)
            print(f"[green]✓ SUCCESS:[/green] {output_file}, used {all_tokens} tokens.")
