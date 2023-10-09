import os
import click
import openai
import tiktoken
from rich import print
from rich.progress import track
from langchain.text_splitter import RecursiveCharacterTextSplitter


class MDTranslator:
    def __init__(self):
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
                    "content": "You are a professional translator. You are helping an English speaker translate Chinese into English. Only translate text and cannot interpret it.",
                },
                {"role": "user", "content": prompts},
            ],
        )
        print(
            f"[green]✓ DONE:[/green] {response['model']}-{response['usage']['total_tokens']} tokens used."
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

    def __translate_text(self, text: str, gpt_model: str) -> str:
        """Translate

        Args:
            text (str): text
            gpt_model (str): gpt_model

        Returns:
            str: translated text
        """
        chunks = self.__text_splitter(text)
        print(f"[yellow]➜ CHUNKS:[/yellow] {len(chunks)}")
        text_translated = ""
        if click.confirm("Start translating?"):
            for chunk in track(chunks, description="➜ Translating"):
                text_translated += self.__chat_gpt(chunk, gpt_model)
        return text_translated

    def translate(self, file_path: str, gpt_model: str) -> str:
        """Translate File

        Args:
            file_path (str): file_path
            gpt_model (str): gpt_model

        Returns:
            str: translated text
        """
        print(f"[yellow]➜ FILE:[/yellow] {file_path}")
        # read text
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        text_translated = self.__translate_text(text, gpt_model)
        # save translated text
        file_name = os.path.basename(file_path)
        file_suffix = os.path.splitext(file_name)[-1]
        new_file_name = file_name.replace(file_suffix, f".en{file_suffix}")
        file_path_translated = os.path.join(os.path.dirname(file_path), new_file_name)
        with open(file_path_translated, "w", encoding="utf-8") as f:
            f.write(text_translated)
        print(f"[green]✓ DONE:[/green] {file_path_translated}")
