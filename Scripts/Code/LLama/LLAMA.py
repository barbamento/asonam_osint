import requests
import json
from datetime import datetime
import pandas as pd
import os
import base64

from Code.Misc.Errors import ModelError


def image_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def image_to_base64_2(file_path: str) -> str:
    with open(file_path, "rb") as img_file:
        base64_data = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{base64_data}"


class API:
    url = "http://aime1:11434/api"
    available_models = ["llama3:70b-instruct", "llava:34b-v1.6", "mixtral:latest"]

    def __init__(self, model):
        if model in self.available_models:
            self.model = model
        else:
            raise ModelError(
                f"model {model} is not supported. Use one between {self.available_models}"
            )

    def call_image(self, prompt: str, image_path: str, seed: int = 42) -> str:
        base_request = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_to_base64(image_path)],
            "temperature": 1,
            "seed": seed,
            "stream": False,
        }
        # [
        #    print(
        #        [i, base_request[i]]
        #        if i != "images"
        #        else base_request["images"][0][:30]
        #    )
        #    for i in base_request
        # ]
        response = requests.post(f"{self.url}/generate", json=base_request)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            return json_data["response"]
        else:
            print(response.__dict__)

    def call_chat(self, prompt: str, seed: int = 42):
        data = {
            "model": "llama3:70b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "seed": seed,
            "stream": False,
        }

        response = requests.post(f"{self.url}/chat", json=data)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            return json_data["message"]["content"]
        else:
            print(response.__dict__)
