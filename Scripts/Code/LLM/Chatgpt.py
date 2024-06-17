import requests
import json
from datetime import datetime
import pandas as pd
import os
import base64

from openai import AzureOpenAI

from Code.Misc.Errors import ModelError
from Code.Misc.Utils import *


class API:
    model = "gpt-4o"
    cost = {"gpt-4o": {"input": 0.005 / 1000, "output": 0.015 / 1000}}

    def __init__(self, secrets: dict):
        self.client = AzureOpenAI(
            api_key=secrets["api_key"],
            api_version=secrets["api_version"],
            azure_endpoint=secrets["azure_endpoint"],
        )

    def call_image(self, prompt: str, image_path: str, seed: int = 42) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_to_base64_2(image_path)},
                        },
                    ],
                }
            ],
            max_tokens=512,
            stream=False,
        )
        output_cost = response.usage.completion_tokens * self.cost[self.model]["output"]
        prompt_cost = response.usage.prompt_tokens * self.cost[self.model]["input"]
        print(
            f"this call costed {prompt_cost} € in prompt and {output_cost} € in output\n"
            f"for a total of {prompt_cost+output_cost} € and {response.usage.total_tokens} tokens"
        )
        return response.choices[0].message.content
