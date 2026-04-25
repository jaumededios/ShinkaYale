#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

if [[ -f "$repo_root/.venv/bin/activate" ]]; then
  source "$repo_root/.venv/bin/activate"
fi

# Serve from the Examples_Shinkaevolve tree. Each example's
# <name>/results/programs.sqlite shows up in the UI labelled with <name>
# (the library uses the first path segment under this root as the task name).
cd "$repo_root/Examples_Shinkaevolve"

echo "Starting Shinka WebUI in $PWD"
echo "Visit http://127.0.0.1:8888"

shinka_visualize --port 8888 "$@"
