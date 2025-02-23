from typing_extensions import TypedDict

from contextlib import contextmanager
from multipledispatch import dispatch  # type: ignore
import rich
import textwrap

from beyond_chatting.client import (
    Client,
    HuggingFaceInferenceApiClient,
    LocalOpenAIClient,
    Provider,
)
from beyond_chatting.inputs import PipableStr


def has_placeholder_slots(prompt):
    return prompt.count("{") > prompt.count("\{")

def dedent_messages(messages):
    for message in messages:
        message["content"] = textwrap.dedent(message["content"]).strip("\n")
    return messages


class ChatMessage(TypedDict):
    role: str
    content: str


class Chat():
    def __init__(self, llm, quiet = False):
        self.llm = llm
        self._quiet = quiet
        self._chat_history: list[ChatMessage] = []

    def ask(self, prompt, *args, **kwargs):
        prompt = prompt.format(*args, **kwargs) if args or kwargs else prompt
        self._chat_history.append({"role": "user", "content": prompt})
        answer = self.llm(self.chat_history)
        self._chat_history.append({"role": "assistant", "content": answer})
        if not self._quiet:
            rich.print(f"[bold]👤 User:[/bold] {textwrap.shorten(prompt, 50)}")
            rich.print(f"[bold]🤖 Assistant:[/bold] {textwrap.shorten(answer, 50)}")
        return answer

    @property
    def chat_history(self):
        return self._chat_history



class LLM():

    def __init__(self,
        provider: Provider = Provider.LOCAL,
        model_id: str | None = None,
        model_kwargs: dict = {},
        gen_kwargs: dict = {}
    ):
        default_gen_kwargs = {
            "max_tokens": 256,
            "temperature": 0.7,
            "stream": False
        }
        gen_kwargs = {**default_gen_kwargs, **gen_kwargs}
        self._system_prompt = None
        self._inference_client: Client
        if provider == Provider.LOCAL:
            self._inference_client = LocalOpenAIClient(model_id, model_kwargs, gen_kwargs)
        if provider == Provider.HUGGINGFACE:
            self._inference_client = HuggingFaceInferenceApiClient(model_id, model_kwargs, gen_kwargs)

    @dispatch(str)
    def _generate(self, prompt: str):
        messages = []
        if self._system_prompt:
            messages.append({"role": "system", "content": self._system_prompt})
        messages.append({"role": "user", "content": prompt})
        messages = dedent_messages(messages)
        completion = self._inference_client.create(messages)
        return completion

    @dispatch(list)  # type: ignore
    def _generate(self, messages: list[ChatMessage | str]):
        if isinstance(messages[0], str):
            assert all(isinstance(message, str) for message in messages), "Messages must be of same type"
            for i, message in enumerate(messages):
                role = "assistant" if (i % 2) else "user"
                messages[i] = {"role": role, "content": message}
        if self._system_prompt:
            messages = [{"role": "system", "content": self._system_prompt}] + messages
        messages = dedent_messages(messages)
        completion = self._inference_client.create(messages)
        return completion

    def __call__(self, inputs, *args, **kwargs):
        if isinstance(inputs, list):
            return PipableStr(self._generate(inputs))
        if args or kwargs:
            inputs = inputs.format(*args, **kwargs)
        elif has_placeholder_slots(inputs):
            return lambda *arg, **kwargs: self._generate(inputs.format(*arg, **kwargs))
        completion = self._generate(inputs)
        return PipableStr(completion)

    def set_system_prompt(self, prompt):
        pass

    @contextmanager
    def session(self, quiet=False):
        chat = Chat(llm=self, quiet=quiet)
        try:
            if not quiet:
                rich.print("🏁 Staring new 💬 chat session:")
            yield chat
        finally:
            del chat

    def who_am_i(self):
        rich.print(
            f"I am [bold]{self._inference_client.model_id}[/bold], a large language model.\n"
            f"I am served at {self._inference_client.model_kwargs.get('base_url', 'UNKNOWN')}."
        )


