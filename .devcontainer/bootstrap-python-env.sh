#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
cd "$repo_root"

ensure_uv() {
  if command -v uv >/dev/null 2>&1; then
    return
  fi

  echo "Installing uv..."
  python3 -m pip install --upgrade pip
  python3 -m pip install uv
}

venv_is_ready() {
  [[ -x "$repo_root/.venv/bin/python" ]] || return 1
  "$repo_root/.venv/bin/python" -c "import importlib.util; raise SystemExit(0 if importlib.util.find_spec('shinka') else 1)" >/dev/null 2>&1 || return 1
}

if venv_is_ready; then
  echo "Python environment already available at $repo_root/.venv"
  exit 0
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to bootstrap the repo environment." >&2
  exit 1
fi

ensure_uv

echo "Creating repo virtual environment in $repo_root/.venv..."
uv sync --frozen --python 3.11

source "$repo_root/.venv/bin/activate"

jupyter kernelspec uninstall -f scevo >/dev/null 2>&1 || true
python -m ipykernel install --user --name scevo --display-name scevo
python -c "from shinka.core import EvolutionConfig, ShinkaEvolveRunner" >/dev/null

echo "Python environment ready."
