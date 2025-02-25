```console
    __                               __  
   / /_  ___  __  ______  ____  ____/ /  
  / __ \/ _ \/ / / / __ \/ __ \/ __  /   
 / /_/ /  __/ /_/ / /_/ / / / / /_/ /    
/_.___/\___/\__, /\____/__ /_/\__,_/     
  _____/ /_  ___/ _/ /_/ /_(_)___  ____ _
 / ___/ __ \/ __ `/ __/ __/ / __ \/ __ `/
/ /__/ / / / /_/ / /_/ /_/ / / / / /_/ / 
\___/_/ /_/\__,_/\__/\__/_/_/ /_/\__, /  
                                /____/   
```

<h1>Getting Serious with Large Language Models:</br>A Practical Introduction</h1>


* [x] 🕹️ playful and explorative learning 
* [x] 🪜 step by step
* [x] ⏱️ short and simple
* [x] 🦆 no coding skills required to get started
* [x] 🛤️ putting you on track to use AI like a pro
* [x] 🏡 all-local AI 
* [x] ❤️ open source models and software


## Lessons


* **Lesson 01**: ⛓️ Chains and 💬 Chats with 🫥 Placeholders [[notebook]](./lessons/lesson01.ipynb)
* **Lesson 02** (planned): Devise and Control Sophisticated Workflows (If-Then-Conditions, Branches, Iterations, etc.)
* **Lesson 03** (planned): Connecting LLM-Workflows To Your Data
* **Lesson 04** (possible): Understanding and Exploiting Decoding Techniques
* **Lesson 05** (possible): Structured and Constrained Output
* **Lesson 06** (possible): Integrating Tools
* **Lesson 07** (possible): Multi-Agent Workflows 
* **Lesson 08** (planned): Unravelling Beyond-Chatting, and Preparing You for the Real Stuff 


<!--
1. Texte generieren (pipeline, Modell laden, tokenizer, greedy, sampling, beam search)
2. Große Modelle aus der Cloud (openai, HuggingFace)
3. Promptschablonen (LangChain)
4. Einfache Arbeitsabläufe (LangChain)
5. Datenverarbeitung (pandas, LangChain)
6. Entscheidungen treffen (multiple choice via constrained generation)
7. Komplexe Arbeitsabläufe (LangChain)
8. Bonus: Magische Textgenerierung (Guidance, SGLang)
9. Bonus: RAG
-->

## Installation (might take 1h+)

> 💡 INFO
>
> If you're unsure with any of the following, don't hesitate to head over to huggingface.co/chat and talk this through with a strong LLM. If you still don't feel confident enough to move ahead: team up with friends, or ask a colleague for
 help. 

Required or recommended:

* A local LLM inference server
* Git
* Python
* VS Code
* VS Code Python Extension

Beyond-chatting assumes that you're running a LLM on your own computer. To do so, install

* [LM Studio](https://lmstudio.ai/)
* [Jan.ai](https://jan.ai/)
* [llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/docs/install.md)
* or any alternative inference server app;

download, as described in your LLM App's documentation, a local model; and start an OpenAI-compatible inference server. *Note*: I've been testing the course with 🦙 **meta-llama/llama-3.2-3b-instruct**. 

In your `> Terminal` app: set up git, which you'll need to download the beyond-chatting course, as [pointed out here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

To set up python, I suggest you install `uv` as described [here](https://docs.astral.sh/uv/getting-started/installation/), and then install the latest python version following [these instructions](https://docs.astral.sh/uv/guides/install-python/). 

To set up VS Code, [download](https://code.visualstudio.com/) and install the code editor.

To set up the VS Code Python Extension, follow the instructions [here](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (some more [background](https://code.visualstudio.com/docs/python/python-quick-start)).

For a pleasant and less intimidating look, you might consider to install the [catppuccin theme](https://marketplace.visualstudio.com/items?itemName=AlexDauenhauer.catppuccin-noctis) and the corresponding [icon set](https://marketplace.visualstudio.com/items?itemName=AlexDauenhauer.catppuccin-noctis-icons). 

Now, to finally get beyond-chatting, in your `> Terminal` app `cd` into the folder where you plan to store the beyond-chatting course and clone the repo with `git`:

```shell
cd my-projects
git clone https://github.com/debatelab/beyond-chatting.git
```

This downloads the course in a newly created beyond-chatting folder.

Next:

```shell
cd beyond-chatting
uv venv  # install packages for beyond chatting
```

Then start VS Code and [open the beyond-chatting folder as a workspace](https://code.visualstudio.com/docs/editor/workspaces/workspaces#_how-do-i-open-a-vs-code-workspace).

🎉 Congrats. You're now ready to start.


## Other Learning Resources

* 😎 https://github.com/mlabonne/llm-course
* 🤗 https://huggingface.co/learn
* 🦜 https://python.langchain.com/docs/tutorials/
* 📄 https://dottxt-ai.github.io/outlines/latest/cookbook/

## About

This is currently a side project of mine. In case the course is picked up and considered useful, I'm happy to  expand the tutorials.

Please **⭐️ star this repo** in case you think its useful.

Feel free to suggest topics that should be covered via Github issues.