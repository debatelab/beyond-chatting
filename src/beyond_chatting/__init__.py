import rich

import beyond_chatting.__about__
import beyond_chatting.inputs
from beyond_chatting.llm import LLM

__all__ = ["LLM"]

inputs = beyond_chatting.inputs.Inputs()  # factory for creating Pipables

def hello():
    welcome = "👋 Hello from beyond-chatting!\n"
    welcome += f"Version: {beyond_chatting.__about__.__version__}\n\n"
    welcome += beyond_chatting.__about__.logo
    rich.print(welcome)

hello()
