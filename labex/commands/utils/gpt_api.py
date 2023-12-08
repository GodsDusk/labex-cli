import os
import json
import openai
from openai import AzureOpenAI
import requests


class ChatGPT:
    def __init__(self, model: str = "gpt-35-turbo") -> None:
        # openai
        self.model = model
        self.resource_name = os.getenv("AZURE_OPENAI_RESOURCE_NAME")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.cf_ai_gateway = os.getenv("CLOUDFLARE_AI_GATEWAY")
        self.api_version = "2023-07-01-preview"
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )

    def azure_open_ai(self, system_prompts: str, user_prompts: str) -> str:
        """ChatGPT API

        Args:
            prompts (str): prompts

        Returns:
            str: response
        """
        if self.cf_ai_gateway is None:
            completions = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompts,
                    },
                    {"role": "user", "content": user_prompts},
                ],
            )
            response = json.loads(completions.model_dump_json())
        else:
            endpoint_url = f"{self.cf_ai_gateway}/{self.resource_name}/{self.model}/chat/completions?api-version={self.api_version}"
            response = requests.post(
                url=endpoint_url,
                headers={
                    "Content-Type": "application/json",
                    "Api-Key": self.api_key,
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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        function_args = json.loads(
            response.choices[0].message.model_dump_json(indent=2)
        )
        if function_args.get("function_call"):
            return function_args
        else:
            return None
