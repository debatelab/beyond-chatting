from abc import ABC, abstractmethod
from enum import Enum
from getpass import getpass
import os
import socket

from huggingface_hub import HfApi
from openai import OpenAI
import rich
from rich.progress import Progress

from beyond_chatting.utils import in_notebook


class Provider(Enum):
    HUGGINGFACE = "huggingface"
    LOCAL = "local"


class Client(ABC):

    @abstractmethod
    def __init__(self, model_id: str | None = None, model_kwargs: dict = {}, gen_kwargs: dict = {}):
        pass

    @abstractmethod
    def create(self, messages: list[dict], *args, **kwargs):
        pass


class LocalOpenAIClient(Client):
    _default_model_kwargs = {
        "base_url": "http://localhost:8080/v1/",
        "api_key": "empty",
    }

    _default_models = [
        "meta-llama/Llama-3.2-3B-Instruct",
        "meta-llama/Llama-3.2-1B-Instruct",
        "Qwen/Qwen2.5-0.5B-Instruct",
    ]


    def __init__(self, model_id: str | None, model_kwargs: dict = {}, gen_kwargs: dict = {}):
        self.model_kwargs = {**self._default_model_kwargs, **model_kwargs}
        self.gen_kwargs = gen_kwargs

        try:
            self.client = OpenAI(**self.model_kwargs)
            self.client.models.list()
        except Exception:
            client = next(self.search_inference_server(), None)
            if client is None:
                rich.print("🚨🚨🚨 No local inference server found. Please start one and try again. 🚨🚨🚨")
                if in_notebook():
                    rich.print(
                        "👉 Set up a local inference server (like llama.cpp) and re-run the entire notebook. "
                        "Do [bold]not[/bold] proceed with executing the next cells, as this might throw errors."
                    )
                    return
                exit(1)
            self.client = client

        served_models = [model.id for model in self.client.models.list().data]
        if not served_models:
            rich.print(f"🚨🚨🚨 No models are currently available on the local inference server running at {self.client.base_url}. 🚨🚨🚨")
            if in_notebook():
                return
            exit(1)
        model_id = next((m for m in self._default_models if m in served_models), None)
        if model_id is None:
            model_id = served_models[0]
        self.model_id = model_id

        self.model_kwargs["base_url"] = self.client.base_url
        rich.print(f"🤖 Found local model {self.model_id} at {self.client.base_url}")

    def create(self, messages: list[dict], *args, **kwargs):
        gen_kwargs = {**self.gen_kwargs, **kwargs}
        chat_completion = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,  # type: ignore
            **gen_kwargs,
        )
        return chat_completion.choices[0].message.content
    
    def search_inference_server(self):
        ports = list(range(1000, 9000))

        with Progress() as progress:
            task_scan = progress.add_task("[cyan]Scanning local ports...", total=len(ports))

            for port in ports:
                progress.update(task_scan, advance=1)

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if sock.connect_ex(("localhost", port)) != 0:
                    continue

                url = f"http://localhost:{port}/v1/"
                try:
                    client = OpenAI(base_url=url, api_key="empty")
                    client.models.list()
                    progress.update(task_scan, completed=len(ports), refresh=True)

                    yield client
                except Exception:
                    continue

            progress.update(task_scan, completed=len(ports), refresh=True)


class HuggingFaceInferenceApiClient(Client):

    _default_models = [
        "meta-llama/Llama-3.2-3B-Instruct",
        "meta-llama/Llama-3.1-8B-Instruct",
        "meta-llama/Llama-3.2-1B-Instruct",
    ]

    def __init__(self, model_id: str | None, model_kwargs: dict = {}, gen_kwargs: dict = {}):
        hf_api = HfApi()
        hf_avail_models = [
            m.id for m 
            in hf_api.list_models(pipeline_tag="text-generation", inference="warm")
        ]
        if model_id is not None and model_id not in hf_avail_models:
            rich.print(f"ℹ️ Model {model_id} is currently not available via HF Inference Api. Trying to load a default model instead...")
        if model_id not in hf_avail_models:
            model_id = next((m for m in self._default_models if m in hf_avail_models), None)
            if model_id is None:
                rich.print("ℹ️ None of the default models is available via HF Inference Api.")
                rich.print("   Please choose a model from here: https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads&inference=warm")
                exit(1)
        if "api_key" not in model_kwargs:
            if "HF_TOKEN" not in os.environ:
                os.environ["HF_TOKEN"] = getpass("Enter your HF access token:")
            model_kwargs["api_key"] = os.getenv("HF_TOKEN")
        if "base_url" not in model_kwargs:
            model_kwargs["base_url"] = "https://api-inference.huggingface.co/v1/"
        self.model_id = model_id
        self.model_kwargs = model_kwargs
        self.gen_kwargs = gen_kwargs
        self.client = OpenAI(**model_kwargs)

    def create(self, messages: list[dict], *args, **kwargs):
        gen_kwargs = {**self.gen_kwargs, **kwargs}
        chat_completion = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,  # type: ignore
            **gen_kwargs,
        )
        return chat_completion.choices[0].message.content

