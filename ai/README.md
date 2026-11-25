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
11. [Issue snapshot](#issue-snapshot)
12. [Issue cleanup](#issue-cleanup)
13. [Settings and schedule](#settings-and-schedule)
14. [Skills for interactive sessions](#skills-for-interactive-sessions)

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
- Issue verification: [`templates/issue-XXX/verify-00X/`](templates/issue-XXX/verify-00X/request.yml)
- Issue cleanup: [`templates/cleanup/XXX/`](templates/cleanup/XXX/request.yml)
- Issue snapshot: [`templates/issue-snapshot/XXX/`](templates/issue-snapshot/XXX/request.yml)

Copy the folder you need to `ai/requests/` and replace `XXX` and `00X` in the folder names as described in [Where the request goes](#where-the-request-goes).

## What you can ask for

| Task | What it does | Claude | Copilot |
|---|---|---|---|
| `analyze-issue` | Reads the issue with all comments and the current c:geo source code, then explains the probable cause and a possible fix. Also lists other open issues that make sense to handle in the same change (from the [issue snapshot](#issue-snapshot)). | yes | yes |
| `review-pr` | Reads a pull request (description, changes, existing reviews and comments) and the exact code of the PR, then lists concrete problems and the open issues the PR fixes (referenced ones and further ones from the [issue snapshot](#issue-snapshot)). | yes | yes |
| `review-branch` | Reviews a branch of `murggel/cgeo` that has no pull request yet, against `master` or `release` of `cgeo/cgeo`. Same checks as `review-pr`, including fixed issues, plus a draft PR description with `fixes #` lines. | yes | yes |
| `verify-issues` | Checks candidate issues of an earlier report (or a list of issues) against their full, current text and the code. See [Verifying candidate issues](#verifying-candidate-issues). | yes | yes |
| `cleanup-issues` | Checks open `cgeo/cgeo` issues from the [issue snapshot](#issue-snapshot) and recommends which ones can be closed, grouped by reason, with closing comments in English. See [Issue cleanup](#issue-cleanup). | yes | yes |
| `refresh-issues` | Creates the [issue snapshot](#issue-snapshot) of all open `cgeo/cgeo` issues from scratch. Runs no AI and needs no provider. Started automatically every two weeks. | – | – |
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
- Issue verification: `ai/requests/<issue-, pr- or branch-folder>/verify-NNN[-description]/request.yml`
- Issue snapshot: `ai/requests/issue-snapshot/<name>/request.yml`, for example the date `2026-11-15`
- Issue cleanup: `ai/requests/cleanup/<name>/request.yml`, for example the date `2026-11-15`
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
| `previous` | optional, only for `analyze-issue`, `review-pr` and `review-branch` | folder name of an earlier request in the same directory, e.g. `review-001`, see [Building on an earlier report](#building-on-an-earlier-report) |

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

### Building on an earlier report

With `previous` a new request builds on the report of an earlier request. Name the folder of that request; it must be in the same directory as the new one:

```yaml
# ai/requests/branch-map-npe/review-002/request.yml
task: review-branch
provider: claude
branch: feature/release-issue-18886-NPE-isMapReady
base: release
previous: review-001
```

- The AI checks every point of the earlier report against the current code and starts its answer with a section "Status of the previous report": fixed, still open or wrong. The rest of the new report is complete on its own: it describes every open point in full, also unchanged ones, and marks what is new or different. You do not need to keep the earlier report at hand.
- The earlier report must already be in the commit you push. Wait until its run is finished and run `git pull --rebase origin dev/ai-workflows` first. Otherwise the request is rejected.
- Only the report is passed on, not the `instructions` of the earlier request. Repeat them if they still matter.
- The provider may differ from the earlier one. The report header says `previous: <folder>`.
- Smoke tests do not accept `previous`.

### Preselecting candidate issues

Analyses and reviews find related or fixed issues by searching the [issue snapshot](#issue-snapshot), which only has short summaries. With `preselect` the run also downloads the full text of the best matches before the AI starts:

```yaml
task: analyze-issue
provider: claude
issue: 18829
preselect: true          # 5 issues; or a number from 1 to 10
```

- Off by default. `preselect: false` is the same as leaving it out.
- The matches are found by rules, not by AI: terms from the issue, PR or branch (title, class names, exceptions, backticked terms, known c:geo terms) are compared with the snapshot. Rare terms count more, and an issue needs at least two matching terms. The analyzed issue itself is left out.
- The full texts land in `ai-context/candidates/issue-<number>.md`. The AI judges them with their full text and marks them `verified (full text)`; issues it finds by searching the snapshot itself stay `to be verified`.
- Costs more input for the AI (a few thousand tokens per issue) and gives one more agent turn per downloaded issue. The report header says `preselected: <n>`.
- Available for `analyze-issue`, `review-pr` and `review-branch`.

### Verifying candidate issues

Candidates marked `to be verified` were judged from their summary only. The task `verify-issues` checks them against their full, current text and the code, without repeating the analysis or review:

```yaml
# ai/requests/issue-18829/verify-001/request.yml
task: verify-issues
provider: claude
issue: 18829             # the target: issue, pr, or branch with base
report: analysis-001     # the request whose report proposed the issues
issues: unverified       # or all, or a list: [18830, 18841]
```

- Store it in the folder of the issue, PR or branch, with the folder name `verify-NNN[-description]`. The target must match the folder (`issue-<n>` with `issue`, `pr-<n>` with `pr`, `branch-…` with `branch` and `base`).
- `unverified` takes the issues on lines marked `to be verified` in the report, `all` every issue the report links. Both need `report`. A list names the issues yourself and works without a report, for example "does PR 18854 fix #18830?".
- At most 10 issues. The target issue or PR is left out. With `unverified` or `all` and more matches, the first 10 are used and the run shows a warning.
- The run prepares the same code and context as an analysis or review of the target and downloads each issue with description, all comments, state and labels. An issue that cannot be downloaded gets a short note instead.
- The report contains one verdict per issue (current state, confirmed or rejected with reasons from the issue text and the code), the updated recommendation (for PRs and branches the final `fixes #` list) and a list of issues that could be closed (already fixed, duplicate, no longer applicable, waiting for information), as a recommendation only.
- The age of an issue (creation date, last activity, version) is taken into account as a hint, also when candidates are searched in the snapshot.
- `instructions` are allowed. The run gets one more agent turn per issue. The report header says `verify: <n> issues` and `report: <folder>`.

## What happens after the push

1. **Validate.** The workflow looks for the one `request.yml` that was added or changed in your push and checks it. A push must contain exactly one such file. Moving or deleting request files does not start a new AI run.
2. **Prepare.** It downloads the current c:geo source code (`cgeo/cgeo`, branch `master`) and, for a review, the exact code of the pull request. It also downloads the issue or PR text and comments from GitHub.
   The [issue snapshot](#issue-snapshot) in `ai/issues/` is part of the checkout; it is not updated here.
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

Usage is billed to the Copilot plan of the account that created the token. It is billed in GitHub AI Credits by the tokens used.

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
| *… report.md does not exist in this commit* | The report named by `previous` is missing from your push. Check the folder name, wait for that run to finish, run `git pull --rebase origin dev/ai-workflows` and change the request again so that a new push starts a run. |
| *previous must be the folder name …* | Write only the folder name of the earlier request, e.g. `previous: review-001`, without a path. |
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
- **Safe saving:** the save job writes only into the validated request folder and refuses symbolic links on the way. The `refresh-issues` job, which runs no AI, additionally writes only `ai/issues/issues.md` and `ai/issues/snapshot.json`.
- **Issue snapshot:** the summaries are untrusted like all other issue data, and the AI is told so. The AI gets no network access to read issues itself.
- **Pinned dependencies:** all GitHub actions are pinned to full commit SHAs, Copilot CLI to an exact version, Python packages to exact versions with hashes.
- **Reports are untrusted too:** a report is derived from third-party text. Read it critically and do not feed it into other automation unchecked. A report named by `previous` is only passed as a file that the AI is told to treat as untrusted data and to verify against the code.

Possible future hardening: if the workflow is ever opened to other users or triggers, move the secrets into a protected GitHub *environment*.

## Maintenance

### Files

| Path | Purpose |
|---|---|
| `.github/workflows/ai-assistant-murggel.yml` | The workflow: validate, one job per provider (`run-copilot`, `run-claude`), save. |
| `scripts/validate_request.py` | Checks `request.yml`. The **only** place that defines allowed tasks, providers, repositories and folder names. |
| `scripts/fetch_context.py` | Downloads issue or PR data from the GitHub API (with paging, error handling and size limit) and formats the branch-review context. |
| `scripts/issue_cleanup.py` | Selects the issues for `cleanup-issues`, records their results in `issues/cleanup.json` and writes the overview `issues/cleanup.md`. |
| `scripts/fix_history.py` | Finds the pull requests of the issues that `cleanup-issues` considers fixed and lists them in the report. |
| `scripts/issue_snapshot.py` | Creates the search snapshot of all open upstream issues in `issues/` (task `refresh-issues`) and preselects matching issues for `preselect`. |
| `issues/` | The issue snapshot, written by the workflow. Do not edit by hand. |
| `scripts/prepare_task.py` | Prepares the workspace for a task, the same for every provider: c:geo checkout, PR checkout, issue/PR data, removal of symbolic links, and the final prompt (`prompts/<task>.md` plus the request's instructions). |
| `scripts/finalize_report.py` | Builds `report.md`: header line, Claude's final answer only, size limit, token scan. |
| `scripts/test_*.py` | Unit tests for the scripts. |
| `scripts/requirements.txt` | Python dependencies with hashes. |
| `prompts/`, `skills/` | Instructions for the AI, shared by both providers. |
| `skills/cgeo-ai-request/` | Not used by the workflow: a skill for interactive Claude sessions that writes, validates and pushes a `request.yml`, follows the run and summarizes the report. See [Skills for interactive sessions](#skills-for-interactive-sessions). |
| `skills/cgeo-support-ticket/` | Not used by the workflow: a skill for interactive Claude sessions that analyzes a ticket of the c:geo support system (with logcat attachments) and writes a reply to the user and a developer analysis. See [Skills for interactive sessions](#skills-for-interactive-sessions). |
| `skills/interactive-skills.txt`, `skills/install-skills.ps1` | The list of skills for interactive sessions and the Windows script that links them into `~/.claude/skills/`. |
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

## Issue snapshot

The AI has no network access, so it cannot search GitHub itself. To still find related issues, `ai/issues/` holds a search snapshot of all open issues of `cgeo/cgeo`:

| File | Content |
|---|---|
| `cleanup.json` | Results of earlier [cleanup runs](#issue-cleanup): category and date per issue. |
| `cleanup.md` | Overview of the cleanup runs: first the issues that can probably be closed, by category, then all reports with provider, number of checked issues and counts per category. Written by the workflow after every cleanup run and issue snapshot. The reports themselves are in the request folders. |
| `issues.md` | One line per open issue: number, labels, c:geo version, creation date, last update, number of comments, assignees, title, keywords and a short summary. The AI searches it with `Grep`; every hit returns the whole entry. |
| `snapshot.json` | Repository, creation time and number of issues. |

How the summary is built (by rules in `scripts/issue_snapshot.py`, without AI):

- Only title, labels and description are used, no comments. The whole snapshot therefore needs only one API request per 100 issues and takes a few seconds.
- Removed: issue-form headings, `_No response_`, HTML comments, code blocks, log and stack-trace lines, the sections *System information*, *Reproducible* and *c:geo Version*, images and URLs.
- Kept: the c:geo version (from the form, else a version number in the title or the text), the creation date and the first 400 characters of the remaining text. Quote marks (`>`) are removed, the quoted text stays.
- Keywords: class names from `cgeo.geocaching…` paths, exceptions, CamelCase names, terms in backticks and known c:geo terms, some of them in German (for example *live map*, *offline log*, *GPX*, *opencaching*, *Karte*). At most 25 per issue.

How the AI uses it:

- `analyze-issue` lists open issues that make sense to handle together, `review-pr` and `review-branch` list the issues the change fixes. `review-branch` also puts `fixes #` lines into the draft PR description.
- The AI only sees the summary. Each listed issue is marked *to be verified*, with a link. Check the full issue on GitHub, [preselect](#preselecting-candidate-issues) the best matches in full text, or let a [`verify-issues`](#verifying-candidate-issues) request check them.
- These tasks get 10 more agent turns for the search. The report header names the snapshot date, or `outdated` if it is older than 14 days, or `missing`.

How it stays current:

- The snapshot is never updated during an analysis or review.
- The task `refresh-issues` creates it from scratch. A scheduled Claude Code task pushes such a request on the days set in [`ai/settings.yml`](#settings-and-schedule) (1st and 15th), at 3:00 Berlin time. You can also push one yourself at any time:

  ```bash
  mkdir -p ai/requests/issue-snapshot/$(date +%F)
  printf 'task: refresh-issues\n' > ai/requests/issue-snapshot/$(date +%F)/request.yml
  git add ai/requests/issue-snapshot
  git commit -m "Request issue snapshot"
  git push origin dev/ai-workflows
  ```

- The job replaces `ai/issues/issues.md` and `ai/issues/snapshot.json` and writes a one-line `report.md` in the request folder. Cleanup results and reports stay.
- Entries of issues checked by a cleanup run show its result, for example `cleanup: probably fixed (2026-11-15)`. An `updated` date after that means the issue has changed since.
- Locally the script works too: `GH_API_TOKEN=<token> python ai/scripts/issue_snapshot.py` (without a token GitHub allows 60 requests per hour, which is enough as well).

## Issue cleanup

`cleanup-issues` finds open issues that can probably be closed. It uses the [issue snapshot](#issue-snapshot) as input, and its results flow back into the next snapshot.

```yaml
# ai/requests/cleanup/2026-11-15/request.yml
task: cleanup-issues
provider: copilot
count: 20                  # optional, 1 to 30, default from ai/settings.yml
# labels: [Bug, Unverified] # optional: only issues with one of these labels
```

How it works:

1. **Selection (by rules, without AI):** from `ai/issues/issues.md`, the issues with the oldest last activity first, optionally only those with one of the `labels`. Issues checked by a cleanup run in the last `skip_days` (default 183) are skipped, unless they have had activity since.
2. **Download:** each selected issue with description, all comments, state and labels.
3. **Check (AI):** against the full text, the current `cgeo/cgeo` code and the snapshot (for duplicates). Categories:
   - *Probably fixed:* the problem no longer exists in the code, or the feature exists.
   - *Duplicates:* another issue covers the same, which one is named.
   - *No longer applicable:* feature, connector, service or code path was removed or reworked.
   - *Waiting for information:* the last substantive comment asks the reporter for something, the reporter has not answered, and that comment is at least `waiting_months` (default 6) old. The label *Feedback required* means feedback from other developers and is no reason on its own.
   - *Keep open:* everything else and every case of doubt. Age alone and unimplemented feature requests are no reason to close.
4. **Report:** `ai/requests/cleanup/<name>/report.md` next to the request, grouped by category, with reason, confidence and a closing comment in English for each issue you could close. Issues to keep open are only listed by number. The AI closes nothing.
5. **Fixing pull requests (by rules, without AI):** for each *probably fixed* issue the AI names a file and a short piece of code that only the fix introduced. `scripts/fix_history.py` searches the full history of `cgeo/cgeo` for the first commit that added this code (`git log --follow -S`) and looks up its pull request (GitHub API, otherwise the `(#<number>)` at the end of a squash commit). The report gets a section with pull request, commit and date per issue. The result is a hint: the first commit with the code is not always the fix, and a commit older than the issue is marked as probably not the fix. The closing comments therefore do not name the pull request; check it first and add it yourself if it fits.
   The same script adds the GitHub assignees from the snapshot to each issue you could close: "— assigned: @login" or "— unassigned" at the end of its entry.
6. **Results:** a machine-readable block at the end of the report (`#<number> <category>`) is recorded in `ai/issues/cleanup.json`. Only issues the run actually checked are accepted. If the block is missing, the report is still saved and a warning is shown.

Costs: since June 2026 Copilot bills by tokens in GitHub AI Credits, so the cost grows with the text the model reads and writes. Cleanup runs with Copilot use the cheaper model `copilot.cleanup_model` (default `claude-haiku-5.5`). Above about 25 to 30 issues per run the checks get less thorough. The header of every Copilot report (the HTML comment in its first line) shows the AI Credits used this month before the run, e.g. `AI credits before run: 950 of 1500 used, 250 available beyond the reserve`. The difference between two consecutive nights, divided by the batches, is the real cost per batch; adjust `copilot.cost_per_batch` to it.

With `provider: auto` the workflow chooses provider, number of issues and number of batches from [`ai/settings.yml`](#settings-and-schedule) and the Copilot AI Credits. Several batches give one report each in the same request folder: `report.md`, `report-2.md`, ...

Overview: after every cleanup run and every issue snapshot the workflow rewrites [`ai/issues/cleanup.md`](issues/cleanup.md) from all reports under `ai/requests/cleanup/`:

- **Issues that can probably be closed**, one table per category (probably fixed, duplicates, no longer applicable, waiting for information) with issue, title from the snapshot and a link to the report. Only the latest result per issue counts: a later run that keeps an issue open removes it here. Issues that are no longer open in the issue snapshot are left out, so closed issues disappear with the next snapshot.
- **Reports**, newest first: provider, number of checked issues, counts per category and the issues that can probably be closed.

## Settings and schedule

[`settings.yml`](settings.yml) holds everything you may want to adjust; `scripts/settings.py` reads and checks it. A mistake makes the next run fail with an explanation.

| Setting | Meaning |
|---|---|
| `timezone` | Time zone for days and weekdays (`Europe/Berlin`). |
| `snapshot.days` | Days of the month on which the scheduled task renews the snapshot. |
| `cleanup.count`, `skip_days`, `waiting_months` | Default issues per cleanup run, pause for checked issues, minimum age of an unanswered question. |
| `cleanup.auto` | Plan for `provider: auto`: rules with `days`, `weekdays`, `provider`, `count` and `max_batches` (Copilot only). The first rule that matches the night is used. |
| `copilot.monthly_credits`, `cost_per_batch`, `reserve` | GitHub AI Credits per month (1500), estimated credits per cleanup batch, credits that must stay free for your own work. |
| `copilot.cleanup_model` | Copilot model for `cleanup-issues` (`claude-haiku-5.5`; empty: Copilot's default). |

The default plan:

- Days 1–20: Claude on Fridays (the Claude weekly limit resets on Friday at 5:00), Copilot on Tuesdays, one run of 20 issues each.
- Days 21–31: Copilot every night, up to 5 batches, as far as the AI Credits allow. Unused AI Credits expire at the end of the month, so they are used for the cleanup.

How a night runs:

1. A scheduled Claude Code task wakes up every night at 3:00 in a session with this repository and runs `python3 ai/scripts/settings.py tonight`. It pushes a `refresh-issues` request on snapshot days and, after the new snapshot, a `cleanup-issues` request with `provider: auto` if a rule matches. Otherwise it pushes nothing.
2. The workflow resolves `provider: auto` with `settings.py resolve`: it picks the rule of the night and, for Copilot, reads the AI Credits used this month from the GitHub billing API (entries with `sku` "Copilot AI Credits" and `unitType` "ai-credits", summed over `grossQuantity` of all models). Available = `monthly_credits` − `reserve` − used; the number of batches is limited by available ÷ `cost_per_batch` and by `max_batches`. If not enough is available, or the billing API fails or returns no AI Credits entries, the Copilot run is skipped. That costs no AI credits, only the request commit; the reason is shown in the run summary.
3. Claude's quota cannot be read, so Claude rules run as planned. Keep them sparse if you get close to your weekly limit.

The nightly session itself uses a little of your Claude quota, even when it pushes nothing.

### Copilot quota token

The AI Credits check needs the repository secret `COPILOT_BILLING_TOKEN`: a fine-grained personal access token of the account that owns the Copilot subscription.

1. GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**.
2. Name it, for example *cgeo AI workflow quota*. Choose an expiration date and note it.
3. **Repository access:** *Public repositories* (the token needs no repository).
4. **Permissions** → **Account permissions** → **Plan**: *Read-only*. Nothing else.
5. Generate the token and copy it.
6. In `murggel/cgeo`: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**, name `COPILOT_BILLING_TOKEN`, paste the token.

The workflow uses it only in the step that resolves the provider, for `GET /users/<owner>/settings/billing/ai_credit/usage`. Without the secret, Copilot rules of `provider: auto` are skipped, and other Copilot reports show `AI credits before run: unknown`. If the check reports HTTP 403 or 404 although the secret is set, the account may not support this endpoint with fine-grained tokens; then try a classic token with the `user` scope.

## Skills for interactive sessions

Some skills in `skills/` are not used by the workflow but by interactive Claude Code sessions: `cgeo-ai-request` and `cgeo-support-ticket`. `skills/interactive-skills.txt` lists them. This branch is the only place where they are maintained, so every change is a commit here. Do not keep copies as account skills in claude.ai: a second version with the same name gets out of date.

Claude Code loads personal skills from `~/.claude/skills/` (Windows: `%USERPROFILE%\.claude\skills`) in every session, whatever branch is checked out. Both ways below put the listed skills there.

### Local sessions on Windows (desktop app, CLI)

The skills are linked from a separate git worktree that keeps `dev/ai-workflows` checked out for good. That worktree is also the place where you work on this branch: write requests, change skills, commit and push there. Changes to a skill take effect in the next session, even before you push.

**Once**, in a PowerShell in your existing clone of `murggel/cgeo`. `<worktree>` is any folder on a local NTFS drive, e.g. `D:\dev\cgeo-ai`; avoid network drives and folders synced by OneDrive, Dropbox and the like.

```powershell
git fetch origin dev/ai-workflows
git worktree add <worktree> dev/ai-workflows
git -C <worktree> pull --rebase origin dev/ai-workflows
powershell -ExecutionPolicy Bypass -File <worktree>\ai\skills\install-skills.ps1
```

- **The `pull` is needed** if a local branch `dev/ai-workflows` already existed: `git worktree add` checks out that local branch, which can be older than `origin`.
- **`origin` must be `murggel/cgeo`.** If your clone calls the fork differently (`git remote -v`), use that name instead.
- **Already checked out elsewhere:** git allows a branch in only one worktree at a time, so `git worktree add` refuses if `dev/ai-workflows` is checked out in the clone or another worktree. Switch that one to another branch first. From then on you cannot check out `dev/ai-workflows` anywhere else; use the new worktree for it.
- **No clone yet:** clone only this branch instead of adding a worktree, then run the script from there:
  `git clone --branch dev/ai-workflows --single-branch --filter=blob:none https://github.com/murggel/cgeo.git <worktree>`

The script prints `Linked <skill> -> <path>` per skill and creates a directory junction for each (no administrator rights needed). Check the result with:

```powershell
Get-ChildItem $env:USERPROFILE\.claude\skills | Select-Object Name, LinkType, Target
```

Every skill of `interactive-skills.txt` should show `Junction` and a target in the worktree. Then start a new session with the environment *This computer* and type `/`.

**From then on:**

- **Changes to a skill:** `git -C <worktree> pull --rebase` and start a new session.
- **New skill:** add its folder to `interactive-skills.txt`, pull, and run the script again.
- **Moving the worktree:** do not move it in Explorer. Use `git worktree move <old> <new>` and run the script again from the new place; it replaces the old junctions. The links point to the old path until then.
- **Existing folder of the same name** in `~/.claude/skills/`: the script skips it with a warning; `-Force` renames it to `<name>.bak` and links the skill.
- **Older copies of a skill** elsewhere (an account skill or plugin in claude.ai, or an old personal skill folder) show up as a second entry in the `/` menu, e.g. `cgeo-support-ticket:cgeo-support-ticket`. Remove them.

### Cloud sessions (claude.ai, app)

The setup script of the cloud environment `cgeo` (personal environment for `murggel/cgeo`; choose it instead of *Default* when starting a session) fetches this branch when a session starts and copies the listed skills into `/root/.claude/skills/`:

```bash
# Install the interactive c:geo skills from murggel/cgeo:dev/ai-workflows (ai/skills/).
if [ -d cgeo/.git ]; then
  if git -C cgeo fetch -q --depth 1 origin dev/ai-workflows; then
    rm -rf /root/.claude/cgeo-skills
    mkdir -p /root/.claude/cgeo-skills /root/.claude/skills
    git -C cgeo archive FETCH_HEAD ai/skills | tar -x -C /root/.claude/cgeo-skills
    src=/root/.claude/cgeo-skills/ai/skills
    for s in $(grep -v '^#' "$src/interactive-skills.txt" | tr -d '\r'); do
      if [ -f "$src/$s/SKILL.md" ]; then
        rm -rf "/root/.claude/skills/$s"
        cp -r "$src/$s" "/root/.claude/skills/$s"
      fi
    done
  else
    echo "cgeo skills: could not fetch dev/ai-workflows, skipped"
  fi
fi
```

A session picks up changes when its container is built fresh; a resumed session keeps the version it started with. `cgeo-support-ticket` needs a logged-in browser for the support system and therefore works fully only in local sessions.
