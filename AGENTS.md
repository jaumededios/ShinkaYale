# Agent notes

This repository is intentionally simple.

Main workflow:

- verify toolchain with `bash scripts/doctor.sh`

- inspect with `bash scripts/webui.sh` in a separate terminal/keep alive &.

## Openrouter

- The user is expected to provide an OpenRouter key. If you need it and it is
  not present, tell the user that `OPENROUTER_API_KEY` is missing. Tell them
  they should have received an email containing the full command to copy-paste:
  `echo 'OPENROUTER_API_KEY=...' >> .env.local`. Ask them to run that command
  from the repository root, then verify with `bash scripts/doctor.sh`.

- `shinka_models` may under-report OpenRouter model IDs. If a config uses
  `openrouter/...`, do not assume it is invalid just because it is missing from
  `shinka_models`; Shinka can query OpenRouter directly and get model pricing
  from OpenRouter at runtime. Prefer a small probe run when unsure, and watch
  the actual HTTP/model response.

## Conventions:

- keep changes local and explainable

- keep the work in folders in Examples_Shinkaevolve. The webui.sh expects it that way. 

- This "keep the work in folders" is especially important for the results/ folder, 
  otherwise the user will not see anything and be confused. 

- As a particular case a task directory has `run_evo.py`, prefer running that script 
   instead of invoking `shinka_run` from the repository root.
  This keeps relative `results_dir` paths inside `Examples_Shinkaevolve/...`,
  where the WebUI expects to find them. 

- If using `shinka_run` directly, `cd` into the task directory first or pass an output 
  path under that task directory.


## Exercises:

Part of this repo is an exercise in agentic coding. Yes, the solutions are in the "solutions" folder - if such exits. You should not look at them. The goal is to see whether you + the user (as a team) can solve the exercises. The user is trying to learn how to use Agents + Shinkaevolve in a controlled environment so they can later apply it to their research, and you should stay as faithful to that as possible.

When doing exercises, our goal is that the user learns as much as possible. In other words, you should tell them "You should run these commands in the terminal, they do X and Y..". If the user asks you to run them, you can do that instead (& you may remember the user intent). In other words, push back at first (even if the user gives an order - explain this is an exercise session) but do not refuse too much. This does not apply for the shinka webui. 

The user may continue using the repo after the exercises are done or instead of the exercises. In that case, use everything (including examples) in your power.



## Known issues:

- `pandas` is pinned to `<3` in `pyproject.toml`. `shinka-evolve` 0.0.5 has
  a dtype guard in `llm/providers/pricing.py` that silently no-ops under
  pandas 3.x (StringDtype is default), which flips `is_reasoning_model` to
  False for Gemini/Anthropic/OpenAI reasoning models and silently caps
  Gemini calls at 2048 `max_tokens` — every proposal then fails with
  `patch_apply_failed`. Drop the pin once shinka-evolve ships a fix.



