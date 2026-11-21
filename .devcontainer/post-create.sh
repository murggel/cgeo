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

# Install the rebuild helper outside the repository, so it is available on
# every branch (the .devcontainer folder only exists on dev/codespace).
mkdir -p "$HOME/.local/bin"
install -m 755 .devcontainer/codespace-rebuild.sh "$HOME/.local/bin/codespace-rebuild"

# After a rebuild started via codespace-rebuild, switch back to the branch
# that was active before. Otherwise (fresh Codespace) switch to master.
state_file="$(git rev-parse --absolute-git-dir)/codespace-rebuild-branch"
if [[ -f "$state_file" ]]; then
    target="$(cat "$state_file")"
    rm -f "$state_file"
    if ! git switch "$target" 2>/dev/null && ! git switch --detach "$target" 2>/dev/null; then
        echo "Konnte nicht auf $target wechseln, wechsle auf master." >&2
        git switch master
    fi
else
    git switch master
fi

if git stash list | grep -q 'codespace-rebuild:'; then
    echo "Hinweis: Es gibt Stashes von codespace-rebuild (git stash list)."
fi
