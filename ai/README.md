# AI requests for c:geo

This folder lets you ask an AI assistant (Claude Code or GitHub Copilot) to analyze a c:geo issue, review a c:geo pull request, or review one of your branches before you open a pull request.
You describe the job in a small text file called `request.yml` and push it to the branch `dev/ai-workflows`.
A few minutes later GitHub adds the AI's answer as `report.md` in the same folder.

The AI only reads. It cannot change code, post comments, or submit reviews.

## Contents

1. [Quick start](#quick-start)
2. [What you can ask for](#what-you-can-ask-for)
3. [Where the request goes](#where-the-request-goes)
4. [The request file](#the-request-file)
5. [What happens after the push](#what-happens-after-the-push)
6. [One-time setup](#one-time-setup)
7. [Troubleshooting](#troubleshooting)
8. [Glossary](#glossary)
9. [How it is kept safe](#how-it-is-kept-safe)
10. [Maintenance](#maintenance)

## Quick start

Example: let Claude analyze issue 17573.

1. Create the file `ai/requests/issue-17573/analysis-001/request.yml` with this content:

   ```yaml
   task: analyze-issue
   provider: claude
   issue: 17573
   ```

2. Commit and push it:

   ```bash
   git switch dev/ai-workflows
   git pull --rebase origin dev/ai-workflows
   git add ai/requests/issue-17573/analysis-001/request.yml
   git commit -m "Request Claude analysis for issue #17573"
   git push origin dev/ai-workflows
   ```

3. Open the **Actions** tab of the repository on GitHub and watch the run called **AI request**.
4. When the run is green, fetch the result:

   ```bash
   git pull --rebase origin dev/ai-workflows
   ```

   The answer is now in `ai/requests/issue-17573/analysis-001/report.md`.

Ready-made request files are in [`templates/`](templates/). They use the same folder layout as `ai/requests/`:

- Issue analysis: [`templates/issue-XXX/analysis-00X/`](templates/issue-XXX/analysis-00X/request.yml)
- Pull-request review: [`templates/pr-XXX/review-00X/`](templates/pr-XXX/review-00X/request.yml)
- Branch review: [`templates/branch-XXX/review-00X/`](templates/branch-XXX/review-00X/request.yml)
- Smoke test: [`templates/smoke-test/XXX/`](templates/smoke-test/XXX/request.yml)

Copy the folder you need to `ai/requests/` and replace `XXX` and `00X` in the folder names as described in [Where the request goes](#where-the-request-goes).

## What you can ask for

| Task | What it does | Claude | Copilot |
|---|---|---|---|
| `analyze-issue` | Reads the issue with all comments and the current c:geo source code, then explains the probable cause and a possible fix. | yes | yes |
| `review-pr` | Reads a pull request (description, changes, existing reviews and comments) and the exact code of the PR, then lists concrete problems. | yes | yes |
| `review-branch` | Reviews a branch of `murggel/cgeo` that has no pull request yet, against `master` or `release` of `cgeo/cgeo`. Same checks as `review-pr`, plus a draft PR description. | yes | yes |
| `smoke-test` | Sends a tiny "are you there?" prompt. Use it to check that the setup works. Can optionally copy an issue description into the report. | yes | yes |

## Where the request goes

Every request has its own folder with two levels below `ai/requests/`: first *what* it is about, then *which* request it is.

```text
ai/requests/
├── issue-17573-map-crash/          ← issue number, optional description
│   ├── analysis-001/               ← first analysis
│   │   ├── request.yml             ← written by you
│   │   └── report.md               ← written by the workflow
│   └── analysis-002-copilot/       ← second analysis, e.g. with the other provider
├── pr-11067/
│   └── review-001/
├── branch-map-npe/                 ← short description of the branch
│   └── review-001/
└── smoke-test/
    ├── copilot/
    └── claude-issue-18739/
```

Rules:

- Issue analysis: `ai/requests/issue-<number>[-description]/analysis-NNN[-description]/request.yml`
- Pull-request review: `ai/requests/pr-<number>[-description]/review-NNN[-description]/request.yml`
- Branch review: `ai/requests/branch-<description>/review-NNN[-description]/request.yml` (the description is free, the branch name itself goes into `request.yml`)
- Smoke test: `ai/requests/smoke-test/<name>/request.yml`
- `NNN` is a three-digit sequence number (`001`, `002`, …). Use a new number for every new request so old reports are never overwritten.
- The number in the folder name must be the same as the number in `request.yml`.
- Folder names may only contain letters `A–Z a–z`, digits `0–9`, `_` and `-`. No dots, no spaces.

## The request file

`request.yml` is a short [YAML](#glossary) file. It may contain comments starting with `#`.

| Key | Required for | Allowed values |
|---|---|---|
| `task` | always | `analyze-issue`, `review-pr`, `smoke-test` |
| `provider` | always | `claude` or `copilot` |
| `issue` | `analyze-issue`; optional for `smoke-test` | issue number, e.g. `17573` |
| `pr` | `review-pr` | pull-request number, e.g. `11067` |
| `repository` | optional, only for `smoke-test` together with `issue` | `cgeo/cgeo` (default) or `murggel/cgeo` |
| `branch` | `review-branch` | branch name in `murggel/cgeo`, e.g. `feature/issue-18886-fix-map` |
| `base` | `review-branch` | `master` or `release` (the branch of `cgeo/cgeo` the later PR would target) |
| `instructions` | optional, only for `analyze-issue`, `review-pr` and `review-branch` | free text, up to 4000 characters, see [Additional instructions](#additional-instructions) |

Issue analysis and PR review always use `cgeo/cgeo`. Only a smoke test may read an issue from `murggel/cgeo`.

Examples:

```yaml
# Analyze an issue with Copilot
task: analyze-issue
provider: copilot
issue: 17573
```

```yaml
# Review a pull request
task: review-pr
provider: claude
pr: 11067
```

```yaml
# Review a pull request with additional instructions
task: review-pr
provider: claude
pr: 11067
instructions: |
  Pay special attention to database migrations and thread safety.
  Ignore the changes in the translation files.
```

```yaml
# Review a branch before opening a pull request
task: review-branch
provider: claude
branch: feature/release-issue-18886-NPE-isMapReady
base: release
```

```yaml
# Smoke test without an issue
task: smoke-test
provider: copilot
```

```yaml
# Smoke test that also copies an issue description into the report
task: smoke-test
provider: claude
issue: 18739
repository: cgeo/cgeo
```

### Additional instructions

With `instructions` you can tell the AI more about this one request, for example what to focus on, what to ignore, background you already know, or that the answer should be in German.
The text is added to the end of the prompt in its own section, for Claude and Copilot alike.

- Write it as a YAML block after `instructions: |`, indented by two spaces. Line breaks are kept.
- The instructions can change focus, scope, depth and form of the answer, also the report structure.
  They cannot lift the safety rules: the AI stays read-only and keeps treating issue and PR text as untrusted.
- At most 4000 characters, no control characters, not empty. Smoke tests do not accept instructions.
- The instructions are not copied into the report; they stay in `request.yml` next to it. The report header says `instructions: yes` when there were any.

The file is checked strictly. It is rejected if it has unknown or duplicate keys, YAML anchors (`&name`, `*name`), is larger than 16 KiB, is a symbolic link, or if a number is not a whole number between 1 and 999999999.

## What happens after the push

1. **Validate.** The workflow looks for the one `request.yml` that was added or changed in your push and checks it. A push must contain exactly one such file. Moving or deleting request files does not start a new AI run.
2. **Prepare.** It downloads the current c:geo source code (`cgeo/cgeo`, branch `master`) and, for a review, the exact code of the pull request. It also downloads the issue or PR text and comments from GitHub.
   For a branch review it downloads the branch from `murggel/cgeo` and the chosen base from `cgeo/cgeo`, finds the commit where the branch started (merge base) and builds the diff and the list of commit messages with git.
3. **Ask the AI.** Claude or Copilot reads these files and writes its answer. It can only use read-only tools.
4. **Check the answer.** The answer must not be empty, not larger than 512 KiB and must not look like it contains a password or token. Otherwise the run fails and nothing is saved.
5. **Save.** A separate step commits the answer as `report.md` next to your `request.yml` and pushes it to `dev/ai-workflows`.

Good to know:

- Because the workflow pushes to the branch, always run `git pull --rebase origin dev/ai-workflows` before your next push.
- Pushing the same `request.yml` again without changes does not start a new run. Change something (for example a comment) or use **Re-run all jobs** on the run page.
- Several pushes in a row are processed one after the other.
- If saving fails, the report can still be downloaded for 3 days as the artifact `report` on the run page.
- The first line of every report is a hidden comment with the exact c:geo commit, the issue or PR number, the provider and the workflow commit. This tells you later exactly what was analyzed.

## One-time setup

You only need to do this once per fork.

### 1. Allow the workflow to run and to push

1. In the repository on GitHub open **Settings → Actions → General**.
2. Under **Actions permissions**, allow actions.
3. **Workflow permissions** can stay at *Read repository contents*: the workflow asks for write access itself, and only in the job that saves the report.
4. If `dev/ai-workflows` has branch protection or a ruleset, it must allow pushes by `github-actions[bot]`.

The workflow only reacts to pushes by the account `murggel`. To use it in another fork, change `github.actor == 'murggel'` in `.github/workflows/ai-assistant-murggel.yml`.

### 2. Claude: add `CLAUDE_CODE_OAUTH_TOKEN`

You need a Claude Pro or Max subscription and Claude Code installed on your computer.

1. Run `claude setup-token` in a terminal and log in when asked. It prints a long token that starts with `sk-ant-oat`.
2. On GitHub open **Settings → Secrets and variables → Actions → New repository secret**.
3. Name: `CLAUDE_CODE_OAUTH_TOKEN`. Value: the token. Save.

Usage counts against your Claude subscription. If the token stops working, create a new one the same way and replace the secret.

### 3. Copilot: add `COPILOT_GITHUB_TOKEN`

1. On GitHub open your profile picture → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. Repository access: **Public repositories**. Account permissions: **Copilot Requests**. Give it no repository write permissions.
3. Copy the token and save it as repository secret `COPILOT_GITHUB_TOKEN` (same place as above).

Usage is billed to the Copilot plan of the account that created the token. On Copilot Free every request counts as a premium request.

### 4. Test it

Push a smoke test for each provider you set up, e.g. `ai/requests/smoke-test/claude/request.yml`:

```yaml
task: smoke-test
provider: claude
```

When it is green and `report.md` contains "Status: successful", try a small `analyze-issue` request.

There is no automatic fallback from one provider to the other. You always choose explicitly, so costs stay predictable and setup errors are not hidden.

## Troubleshooting

| What you see | What to do |
|---|---|
| No run starts | The push must go to `dev/ai-workflows`, come from the account `murggel` and add or change a file `ai/requests/…/request.yml`. Check that Actions are enabled. |
| Run is shown as skipped | The push was not made by `murggel` or not to `dev/ai-workflows`. |
| Run is green but says *Nothing to do* | The push only moved or deleted requests. To run a request again, change it (e.g. a comment) or use **Re-run all jobs** on its original run. |
| *Expected exactly one added or modified request.yml … found 2* (or more) | Push each new or changed request separately. |
| *Invalid request: … must be stored as …* | The folder name does not match the rules in [Where the request goes](#where-the-request-goes). |
| *refers to issue … but the request specifies …* | The number in the folder name and in `request.yml` differ. |
| *wrong keys (missing=…, unexpected=…)* | A key is missing, misspelled or not allowed for this task (e.g. `repository` in `analyze-issue`, `instructions` in `smoke-test`). |
| *branch must be a branch name …* | Check the spelling of `branch`. Only letters, digits, `.`, `_`, `-` and `/` are allowed, and the name must start with a letter, a digit or `_`. |
| *Cannot fetch … refs/heads/…* (branch review) | The branch does not exist in `murggel/cgeo`. Push it first: `git push -u origin <branch>`. |
| *has no commits that are not in …* | The branch contains nothing new compared to the base. Check `base` and whether the latest commits are pushed. |
| *no common ancestor … within 600 commits* | The branch and the base are far apart. Usually the wrong `base` (e.g. `master` instead of `release`); otherwise rebase the branch. |
| *at most 250 can be reviewed* | The branch has too many commits for one review. Rebase or split it. |
| *instructions must be text* | Write the instructions as a block: `instructions: |` and the text indented on the following lines. |
| *Repository secret … is missing* | Add the secret, see [One-time setup](#one-time-setup). |
| Claude: *error_max_turns* | Claude was stopped at the turn limit (30 for analysis and review) before it finished. Narrow the request or raise `MAX_TURNS` in `scripts/prepare_task.py`. |
| Claude step shows *… after N turns, exceeding the configured maximum of M*, but the run is green | Claude finished, only needed more turns than allowed. The report is still saved; its header says `status: exceeded-max-turns (N of M)` and it starts with a note. Review it with extra care. |
| Claude: authentication error | The token has expired or was revoked. Create a new one with `claude setup-token`. |
| Copilot: model error in the smoke test | Change `SMOKE_TEST_MODEL` in the workflow, e.g. to `gpt-5-mini`. |
| *the report seems to contain a credential* | The answer contains something that looks like a token. Nothing was saved. Check the run log; if it is a false alarm (e.g. a token-like example in the issue), change the request. |
| *exceeds the 512 KiB limit* | The issue/PR or the answer is too large. Nothing is cut off silently; the run fails instead. |
| Saving fails with error 403 | Check branch protection and rulesets for `dev/ai-workflows` (setup step 1). The report is still available as the artifact `report`. |
| Report push fails after 3 attempts | Someone pushed at the same moment several times. Re-run the job or download the artifact. |

## Glossary

- **GitHub Actions / workflow**: GitHub's built-in automation. A *workflow* is a recipe file in `.github/workflows/`; GitHub runs it on its own computers when something happens, here: a push.
- **Run / job / step**: one execution of the workflow is a *run*. It consists of *jobs* (here: validate, one AI job, save), and each job consists of *steps*.
- **Runner**: the temporary computer on which a job runs. It is deleted afterwards.
- **Provider**: the AI service that does the work, Claude Code (Anthropic) or GitHub Copilot.
- **Upstream / fork**: `cgeo/cgeo` is the original project (*upstream*). `murggel/cgeo` is a personal copy (*fork*), where this workflow lives.
- **Branch**: a separate line of development. Requests only work on `dev/ai-workflows`.
- **Pull request (PR)**: a proposed code change in `cgeo/cgeo`.
- **YAML**: a simple text format of `key: value` lines.
- **Secret / token**: a password-like string that lets the workflow use Claude or Copilot. Stored encrypted in the repository settings and never shown in logs.
- **Artifact**: a file that a run keeps for a few days for download on the run page.
- **Smoke test**: a minimal test that only checks that everything is connected.
- **Symbolic link (symlink)**: a file that points to another file. Not allowed in requests, and removed from downloaded code, because it could point to secret files.
- **SHA / pinning**: every commit has a unique ID (SHA). *Pinning* means the workflow uses a helper action at one exact SHA, so nobody can swap its code unnoticed.
- **Prompt injection**: text in an issue or PR that tries to give the AI new orders ("ignore your instructions and …"). The AI is told to treat that text as data only, and it has no tools to do harm.

## How it is kept safe

- **Who can start it:** only pushes by `murggel` to `dev/ai-workflows`.
- **Least privilege:** the workflow starts with no permissions. Each job gets only what it needs. Only the final save job may write to the repository, and it does not run any AI.
- **Read-only AI:** Copilot may only use `view`, `grep` and `glob`; shell, write and web tools are denied. Claude may only use `Read`, `Glob` and `Grep`; reading `/proc` (where environment variables are visible) is blocked. Neither gets a GitHub token.
- **Request instructions:** only the trusted requester writes them. They are passed to the jobs as an environment variable, never pasted into a shell script, and added to the prompt in a clearly marked section that cannot override the read-only rules.
- **Untrusted input:** issue texts, PR texts, comments, PR code, and branch code and commit messages are treated as untrusted. They are marked as such for the AI. Symbolic links are deleted from the downloaded c:geo, PR and branch code before the AI starts.
- **No silent truncation:** issue and PR data are read completely (all pages) and limited to 512 KiB. Too much data makes the run fail instead of hiding parts.
- **Output check:** the answer is limited to 512 KiB and scanned for tokens (`sk-ant-…`, `ghp_…`, `github_pat_…` and others, plus the actual secret values). If anything matches, nothing is saved.
- **Safe saving:** the save job writes only into the validated request folder and refuses symbolic links on the way.
- **Pinned dependencies:** all GitHub actions are pinned to full commit SHAs, Copilot CLI to an exact version, Python packages to exact versions with hashes.
- **Reports are untrusted too:** a report is derived from third-party text. Read it critically and do not feed it into other automation unchecked.

Possible future hardening: if the workflow is ever opened to other users or triggers, move the secrets into a protected GitHub *environment*.

## Maintenance

### Files

| Path | Purpose |
|---|---|
| `.github/workflows/ai-assistant-murggel.yml` | The workflow: validate, one job per provider (`run-copilot`, `run-claude`), save. |
| `scripts/validate_request.py` | Checks `request.yml`. The **only** place that defines allowed tasks, providers, repositories and folder names. |
| `scripts/fetch_context.py` | Downloads issue or PR data from the GitHub API (with paging, error handling and size limit) and formats the branch-review context. |
| `scripts/prepare_task.py` | Prepares the workspace for a task, the same for every provider: c:geo checkout, PR checkout, issue/PR data, removal of symbolic links, and the final prompt (`prompts/<task>.md` plus the request's instructions). |
| `scripts/finalize_report.py` | Builds `report.md`: header line, Claude's final answer only, size limit, token scan. |
| `scripts/test_*.py` | Unit tests for the scripts. |
| `scripts/requirements.txt` | Python dependencies with hashes. |
| `prompts/`, `skills/` | Instructions for the AI, shared by both providers. |
| `templates/` | Example request files, in the same folder layout as `requests/`. |

### Adding a task or provider

The work is split in two independent halves: *what* to prepare depends only on the task, *how* to ask the AI depends only on the provider.

- **New task:** add the rule to `TASKS` in `scripts/validate_request.py`, the preparation to `scripts/prepare_task.py` (including `MAX_TURNS`), a prompt `prompts/<task>.md`, and tests. The workflow needs no change.
- **New provider:** add it to the `providers` of the tasks in `scripts/validate_request.py`, add a job `run-<provider>` to the workflow with `if: needs.validate.outputs.provider == '<provider>'` (copy one of the existing jobs), add it to `needs:` of `publish-report`, and extend `scripts/finalize_report.py` if its output format is new.
- Document the change in this README.

### Versions

- `COPILOT_CLI_VERSION` (top of the workflow): exact version of `@github/copilot`, currently `1.0.105`. The workflow fails if a different version gets installed. Update deliberately after reading the release notes, then run a Copilot smoke test.
- `SMOKE_TEST_MODEL`: `auto` lets Copilot pick a model with a 0x–1x multiplier; `gpt-5-mini` is a fixed model included in paid plans.
- GitHub actions: each `uses:` line has a full SHA and the matching release tag as a comment. To update, look up the SHA of the new release tag in the action's repository (e.g. `git ls-remote --tags https://github.com/actions/checkout.git`) and replace SHA and comment together.
- Runner image: all jobs use `ubuntu-24.04` instead of `ubuntu-latest`, so a new Ubuntu version cannot change the environment unnoticed. To move to a newer image, change `runs-on` in all jobs and run one smoke test per provider.
- Python dependencies: `scripts/requirements.txt` uses pip hash-checking. When updating, copy the SHA-256 hash of the new release file from PyPI and change version and hash in the same commit.

### Running the tests

From the repository root:

```bash
python -m pip install --require-hashes --requirement ai/scripts/requirements.txt
python -m unittest discover --start-directory ai/scripts --pattern 'test_*.py' --verbose
```

On Windows `cmd` use double quotes: `--pattern "test_*.py"`. Tests that need symbolic links are skipped where the system does not allow creating them; on GitHub they run. The workflow runs all tests before every request.
