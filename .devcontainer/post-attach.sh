#!/usr/bin/env bash
# Runs every time a shell attaches to the container.
#
# Keep this FAST. Heavy lifting belongs in post-create.sh. The only job here
# is a safety-net: if the Python env is missing/broken (for example because
# post-create failed upstream), rebuild it so the workshop commands work.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
WELCOME_FLAG="$HOME/.cache/shinka-workshop-welcome"

if [[ ! -x "$repo_root/.venv/bin/python" ]] \
  || ! "$repo_root/.venv/bin/python" -c "import importlib.util; raise SystemExit(0 if importlib.util.find_spec('shinka') else 1)" >/dev/null 2>&1; then
  echo "Repo Python environment missing or incomplete. Rebuilding .venv..."
  bash "$script_dir/bootstrap-python-env.sh"
fi

mkdir -p "$(dirname "$WELCOME_FLAG")"
if [[ ! -f "$WELCOME_FLAG" ]]; then
  cat <<EOF

Shinka workshop environment ready.
- Repo root: $repo_root
- Start here: README.md
- Check setup: bash scripts/doctor.sh
- Start the WebUI: bash scripts/webui.sh &

EOF
  touch "$WELCOME_FLAG"
fi
