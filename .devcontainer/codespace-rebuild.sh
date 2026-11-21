#!/usr/bin/env bash
# Prepares and triggers a rebuild of this Codespace.
#
# - warns about uncommitted changes and offers to stash them
# - remembers the current branch so post-create.sh can switch back to it
# - switches to the branch that holds the devcontainer configuration
# - asks before triggering the rebuild
#
# Installed to ~/.local/bin/codespace-rebuild by post-create.sh.
set -euo pipefail

CONFIG_BRANCH="dev/codespace"

ask() {
    # ask "question" -> returns 0 for yes, 1 otherwise
    local answer
    read -r -p "$1 [j/N] " answer
    [[ "$answer" =~ ^[jJyY]$ ]]
}

repo_dir="${CODESPACE_VSCODE_FOLDER:-$PWD}"
if ! repo_root="$(git -C "$repo_dir" rev-parse --show-toplevel 2>/dev/null)"; then
    echo "Fehler: $repo_dir ist kein Git-Repository." >&2
    exit 1
fi
cd "$repo_root"
state_file="$(git rev-parse --absolute-git-dir)/codespace-rebuild-branch"

# Remember the current branch (or commit when detached).
current="$(git symbolic-ref --short -q HEAD || git rev-parse HEAD)"
echo "Aktueller Branch: $current"

# Uncommitted changes (including untracked files)?
if [[ -n "$(git status --porcelain)" ]]; then
    echo
    echo "Warnung: Es gibt uncommittete Änderungen:"
    git status --short
    echo
    if ask "Änderungen per 'git stash' sichern?"; then
        git stash push --include-untracked -m "codespace-rebuild: $current"
        echo "Gestasht. Später wiederherstellen mit: git stash pop"
    else
        echo "Abgebrochen. Bitte Änderungen committen oder stashen."
        exit 1
    fi
fi

# Switch to the configuration branch.
if [[ "$current" != "$CONFIG_BRANCH" ]]; then
    git switch "$CONFIG_BRANCH"
fi

# Inform if the local configuration branch is behind origin.
if git fetch -q origin "$CONFIG_BRANCH" 2>/dev/null; then
    behind="$(git rev-list --count "HEAD..FETCH_HEAD")"
    if [[ "$behind" -gt 0 ]]; then
        echo "$CONFIG_BRANCH ist $behind Commit(s) hinter origin."
        if ask "Mit origin/$CONFIG_BRANCH aktualisieren (fast-forward)?"; then
            git merge --ff-only FETCH_HEAD
        fi
    fi
fi

restore_branch() {
    rm -f "$state_file"
    if [[ "$current" != "$CONFIG_BRANCH" ]]; then
        git switch "$current" 2>/dev/null || git switch --detach "$current"
    fi
}

echo
if ! ask "Rebuild jetzt starten?"; then
    restore_branch
    echo "Kein Rebuild. Zurück auf $current."
    exit 0
fi

full_flag=()
if ask "Full Rebuild (Docker-Cache verwerfen)?"; then
    full_flag=(--full)
fi

# post-create.sh reads this file and switches back to the remembered branch.
printf '%s\n' "$current" > "$state_file"

if [[ -n "${CODESPACE_NAME:-}" ]] && gh codespace rebuild -c "$CODESPACE_NAME" "${full_flag[@]}"; then
    echo "Rebuild ausgelöst. Der Codespace startet neu."
else
    echo
    echo "Rebuild konnte nicht per gh ausgelöst werden."
    echo "Bitte in VS Code starten: F1 -> 'Codespaces: $([[ ${#full_flag[@]} -gt 0 ]] && echo 'Full ')Rebuild Container'"
    echo "Der Branch $current ist gemerkt und wird nach dem Rebuild wieder ausgecheckt."
fi
