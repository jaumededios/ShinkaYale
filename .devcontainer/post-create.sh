#!/usr/bin/env bash
# Runs once, when the container is first created.
#
# Critical path: build the Python env so `from shinka.core import ...` works.
# Everything else (system math tools, global npm CLIs) is best-effort: a
# failure in those steps must NOT prevent the Python env from being built,
# because that is the only hard requirement for the workshop.

set -uo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
cd "$repo_root"

log_step() { echo; echo "=== $* ==="; }

run_optional() {
  local label="$1"; shift
  if "$@"; then
    echo "[ok] $label"
  else
    echo "[warn] $label failed (continuing)"
  fi
}

apt_install() {
  if command -v sudo >/dev/null 2>&1; then
    sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y "$@"
  else
    env DEBIAN_FRONTEND=noninteractive apt-get install -y "$@"
  fi
}

# ---- 1. Python env (critical) ------------------------------------------------
log_step "Bootstrapping Python environment"
if ! bash "$script_dir/bootstrap-python-env.sh"; then
  echo "[fatal] Python env bootstrap failed. Re-run 'bash .devcontainer/bootstrap-python-env.sh' to retry." >&2
  exit 1
fi

# ---- 2. Shell auto-activation (cheap, must succeed) --------------------------
log_step "Wiring .venv auto-activate into ~/.bashrc"
BASHRC="$HOME/.bashrc"
if ! grep -q "AUTO_ACTIVATE_SHINKA_VENV" "$BASHRC" 2>/dev/null; then
  cat >> "$BASHRC" <<EOF

# AUTO_ACTIVATE_SHINKA_VENV
if [ -f "$repo_root/.venv/bin/activate" ]; then
  . "$repo_root/.venv/bin/activate"
fi
EOF
fi

# ---- 3. Optional: system math tools (best-effort) ----------------------------
log_step "Installing system math tools (best-effort)"
math_packages=(sagemath macaulay2 singular pari-gp)

if command -v sudo >/dev/null 2>&1; then
  run_optional "apt-get update" sudo apt-get update
else
  run_optional "apt-get update" apt-get update
fi

available_packages=()
missing_packages=()
for pkg in "${math_packages[@]}"; do
  if apt-cache show "$pkg" >/dev/null 2>&1; then
    available_packages+=("$pkg")
  else
    missing_packages+=("$pkg")
  fi
done

if [[ ${#available_packages[@]} -gt 0 ]]; then
  run_optional "apt install ${available_packages[*]}" apt_install "${available_packages[@]}"
fi
if [[ ${#missing_packages[@]} -gt 0 ]]; then
  echo "[info] Skipping unavailable system packages: ${missing_packages[*]}"
fi

# ---- 4. Global AI CLIs -------------------------------------------------------
# codex is a hard requirement: users log in from the CLI (`codex login`) because
# the VS Code extension login flow does not work reliably in Codespaces.
log_step "Installing codex CLI"
if ! npm install -g @openai/codex; then
  echo "[fatal] Failed to install @openai/codex. Retry with 'npm install -g @openai/codex'." >&2
  exit 1
fi

log_step "Installing claude-code CLI (best-effort)"
run_optional "npm i -g @anthropic-ai/claude-code" npm install -g @anthropic-ai/claude-code

# ShinkaEvolve agent skills (shinka-setup, shinka-convert, shinka-run,
# shinka-inspect) for Claude Code and Codex.
run_optional "shinka skills for claude/codex" \
  npx --yes skills add SakanaAI/ShinkaEvolve --skill '*' -a claude-code -a codex -y

echo
echo "Environment setup complete."
echo "Run 'bash scripts/doctor.sh' to verify the installed tools."
