# Minimal Two-Variable Optimization

This is the smallest ShinkaEvolve example in this repo. 

The example is split into:

- `initial.py`: the starting program Shinka will edit
- `evaluate.py`: the scorer and validator
- `prompt.txt`: the task prompt given to the LLM
- `shinka.yaml`: the run settings for the evolutionary algorithm.
- `run_evo.py`: a tiny launcher that glues those files together with ShinkaEvolve.

The fixed objective is:

```python
f(x, y) = sin(x) * cos(y) + sin(x * y) + (x**2 + y**2) / 20
```

The goal is to return `(x, y, value)` with the lowest possible `value`.

## Quick start

1. Move to the folder
```bash
cd Examples_Shinkaevolve/1a_minimal_example
```

2. Test that your evaluator works
```bash
python3 evaluate.py --program_path initial.py --results_dir smoke_test
```

3. Run the experiment
```bash
python3 run_evo.py
```


## Notes

- The example is intentionally simple rather than strong.
- `run_evo.py` just reads `prompt.txt` and `shinka.yaml`, then starts the run.
- The default launcher is Gemini-only so it works with `GEMINI_API_KEY`.
