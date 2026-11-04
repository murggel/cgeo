#!/usr/bin/env bash
set -euo pipefail

# Install Claude Code for the vscode user. Authentication is completed
# interactively after the Codespace starts; no credentials are stored here.
if ! command -v claude >/dev/null 2>&1 && [[ ! -x "$HOME/.local/bin/claude" ]]; then
    curl -fsSL https://claude.ai/install.sh | bash
fi

# Ensure the native installer location is available in interactive Bash terminals.
if ! grep -Fq 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc"; then
    printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc"
fi

# Preserve the existing Codespace behavior.
git switch master
