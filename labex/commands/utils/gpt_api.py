import os
import json
import openai
import requests


class ChatGPT:
    def __init__(self, engine: str = "gpt-35-turbo") -> None:
        # openai
        self.openai_type = "azure"
        self.openai_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.openai_base = os.getenv("AZURE_OPENAI_API_BASE")
        self.deploy_name = os.getenv("AZURE_DEPLOYMENT_NAME")
        self.cf_ai_gateway = os.getenv("CLOUDFLARE_AI_GATEWAY")
        self.openai_version = "2023-07-01-preview"
        self.engine = engine

    def azure_open_ai(self, system_prompts: str, user_prompts: str) -> str:
        """ChatGPT API

        Args:
            prompts (str): prompts

        Returns:
            str: response
        """
        if self.cf_ai_gateway is None:
            openai.api_type = self.openai_type
            openai.api_key = self.openai_key
            openai.api_base = self.openai_base
            openai.api_version = self.openai_version
            response = openai.ChatCompletion.create(
                engine=self.engine,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompts,
                    },
                    {"role": "user", "content": user_prompts},
                ],
            )
        else:
            endpoint_url = f"{self.cf_ai_gateway}/{self.deploy_name}/{self.engine}/chat/completions?api-version={self.openai_version}"
            response = requests.post(
                url=endpoint_url,
                headers={
                    "Content-Type": "application/json",
                    "Api-Key": self.openai_key,
                },
                data=json.dumps(
                    {
                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompts,
                            },
                            {"role": "user", "content": user_prompts},
                        ]
                    }
                ),
            ).json()
        try:
            output_text = response["choices"][0]["message"]["content"]
            output_tokens = response["usage"]["total_tokens"]
            return output_text, output_tokens
        except Exception as e:
            print(response)

    def azure_open_ai_fc(self, user_prompts: str, function_json: dict) -> str:
        """ChatGPT Function Call API

        Args:
            user_prompts (str): user_prompts
            function_json (dict): function_json

        Returns:
            str: response
        """
        messages = [{"role": "user", "content": user_prompts}]
        functions = [
            function_json,
        ]
        openai.api_type = self.openai_type
        openai.api_key = self.openai_key
        openai.api_base = self.openai_base
        openai.api_version = self.openai_version
        response = openai.ChatCompletion.create(
            engine=self.engine,
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
