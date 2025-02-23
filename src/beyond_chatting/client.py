from abc import ABC, abstractmethod
from enum import Enum
from getpass import getpass
import os

from huggingface_hub import HfApi
from openai import OpenAI
import rich


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

    def __init__(self, model_id: str | None, model_kwargs: dict = {}, gen_kwargs: dict = {}):
        self.model_kwargs = {**self._default_model_kwargs, **model_kwargs}
        self.gen_kwargs = gen_kwargs
        self.model_id = model_id if model_id else "local-default"
        self.client = OpenAI(**self.model_kwargs)

    def create(self, messages: list[dict], *args, **kwargs):
        gen_kwargs = {**self.gen_kwargs, **kwargs}
        chat_completion = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,  # type: ignore
            **gen_kwargs,
        )
        return chat_completion.choices[0].message.content
    

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

