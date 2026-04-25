# Codespaces

You made it into Github Codespaces! This is a remote machine provided by Github, with all of the material we will need for today installed. 

It's essentially a copy of the VScode editor, with all dependencies/etc frozen to make sure we have a reproducible experience. This machine already has the following installed:


* **ShinkaEvolve** (Follow [these instructions](#) to install it locally, if you want to follow this tutorial in your machine)
* A Python 3.11 environment with the usual suspects (`numpy`, `scipy`, `matplotlib`, `jax`, `optax`, `sympy`...) plus larger system math tools installed by the devcontainer bootstrap (`sagemath`, `macaulay2`, `singular`, `pari-gp`).
* The basic CLIs & plug-ins for your favorite LLM Agents. If you are used to using Codex/Claude Code/... you can just log-in and use them. They come with pre-installed *agent skills* to help you run your experiments.
* A bunch of Skills/Instruction manuals, both for you (called `README.md`) and for LLM agents (called `AGENTS.md`, `CLAUDE.md` and `GEMINI.md`)


# Shinka Evolve


In today's exercises we will use [`shinka`](https://sakana.ai/shinka-evolve/) by [Sakana AI]((https://sakana.ai) ) is a framework that combines Large Language Models (LLMs) with evolutionary algorithms to drive scientific discovery. By leveraging the creative capabilities of LLMs and the optimization power of evolutionary search, `shinka` enables automated exploration and improvement of scientific code. The system is inspired by the [AI Scientist](https://sakana.ai/ai-scientist/), [AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) and the [Darwin Goedel Machine](https://sakana.ai/dgm/): It maintains a population of programs that evolve over generations, with an ensemble of LLMs acting as intelligent mutation operators that suggest code improvements.

Other useful resources are

* Their [documentation website](https://sakanaai.github.io/ShinkaEvolve/) with guides for getting started, configuration, async evolution, local models, WebUI usage, and agentic workflows.
* The [github repo](https://github.com/SakanaAI/ShinkaEvolve) with the code.



# Getting started

## This repo

In this repo you will find the following subfolders. You can see those on your left.

* `Examples_Shinkaevolve/` Contains a series of examples and exercises, that we will use to work on during the *guided* part of the exercise session.

* `scripts/` contains small helper scripts such as `scripts/doctor.sh` for checking the environment and `scripts/webui.sh` for launching the Shinka WebUI.


## Setting up Codex, Claude Code / Gemini CLI

The most comon LLM agent systems (Claude/Codex/Gemini) are installed on the systems. If you have purchased any of them, you can log in into them from Github Codespaces. They will make your life a lot easier. Here are the options

## Claude

Click on the claude icon, **DO NOT** go to the link that will automatically want to open. Instead, copy the link that will appear later. Paste it on your browser, log in, and paste the  code back. 

## Codex

DO NOT click on the codex icon. Instead, on the terminal, type `codex`. It will ask you to sign in, use option 2 `Sign in with Device Code` and follow the instructions. 

If you have trouble logging in, go to https://chatgpt.com/#settings/Security and toggle the `Enable device code authorization for Codex` option. 

Then you can click on the Codex button. If it asks you to log in again, press `cmd+shift+p` and type `Developer: Reload Window`, then press enter.

## Starting with ShinkaEvolve

If you want to confirm that the prebuilt environment is ready, run

```bash
bash scripts/doctor.sh
```

## Starting upp the WebUI

*This is a one-off task, at the begining of the day.*

Shinka comes with a WebUI. Either ask your agent to start it, or run the command 

```
bash scripts/webui.sh &
```
on the terminal, (and open a new terminal). 

This will start the WebUI for you (when prompted, click on the link to open the WebUI). 

## Using OpenRouter

We are using OpenRouter for the examples. OpenRouter is an agregator of models from multiple companies. You can search online for which models it supports in case you want to try other models (it essentially supports all models, but has some issues with some thinking models.).

# Next steps

Select 
`Examples_Shinkaevolve/1a_minimal_example`

it contains a `README.md` with information to continue.
