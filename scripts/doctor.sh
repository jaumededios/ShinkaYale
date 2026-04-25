#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

if [[ -f "$repo_root/.venv/bin/activate" ]]; then
  source "$repo_root/.venv/bin/activate"
fi

if [[ -f "$repo_root/.env.local" ]]; then
  source "$repo_root/.env.local"
fi

print_version() {
  local label="$1"
  shift

  if command -v "$1" >/dev/null 2>&1; then
    echo "$label: $("$@" 2>/dev/null)"
  else
    echo "$label: missing"
  fi
}

print_present() {
  local label="$1"
  local cmd="$2"

  if command -v "$cmd" >/dev/null 2>&1; then
    echo "$label: present"
  else
    echo "$label: missing"
  fi
}

print_version "Python" python3 --version
print_version "Node  " node --version
print_version "npm   " npm --version
print_version "uv    " uv --version

if command -v python3 >/dev/null 2>&1; then
  shinka_version="$(python3 -c 'import importlib.metadata as m; print(m.version("shinka-evolve"))' 2>/dev/null || true)"
  echo "Shinka: ${shinka_version:-missing}"
else
  echo "Shinka: missing"
fi

echo
echo "CLIs:"
print_version "codex " codex --version
print_version "claude" claude --version

echo
echo "Math tools:"
print_present "sage   " sage
print_present "M2     " M2
print_present "Singular" Singular
print_present "gp     " gp

echo
echo "Keys present:"
[ -n "${OPENAI_API_KEY:-}" ] && echo "OPENAI_API_KEY=present" || echo "OPENAI_API_KEY=missing"
[ -n "${ANTHROPIC_API_KEY:-}" ] && echo "ANTHROPIC_API_KEY=present" || echo "ANTHROPIC_API_KEY=missing"
[ -n "${GEMINI_API_KEY:-}" ] && echo "GEMINI_API_KEY=present" || echo "GEMINI_API_KEY=missing"
[ -n "${OPENROUTER_API_KEY:-}" ] && echo "OPENROUTER_API_KEY=present" || echo "OPENROUTER_API_KEY=missing"
