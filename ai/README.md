# AI-assisted c:geo workflows

This directory contains provider-neutral instructions for AI-assisted repository analysis.

## Providers

Each request selects exactly one provider:

- `claude`: Claude Code, authenticated with the repository secret `CLAUDE_CODE_OAUTH_TOKEN`. **Not yet implemented in the workflow:** a request with `provider: claude` currently ends in the job `unsupported-claude`, which fails on purpose.
- `copilot`: GitHub Copilot CLI, authenticated with the repository secret `COPILOT_GITHUB_TOKEN`.

For Copilot, create a fine-grained personal access token owned by your personal GitHub account. Grant the account permission **Copilot Requests**; select public repositories for repository access. Store the token as the Actions repository secret `COPILOT_GITHUB_TOKEN` under Settings → Secrets and variables → Actions. Do not grant repository write permissions.

Copilot usage through this token is billed against the Copilot entitlements of the account that created the token. On the Copilot Free plan, every request counts as a premium request, even for included models.

Provider selection is explicit per request. There is no automatic fallback: this keeps usage and billing predictable and avoids masking authentication or configuration errors.

## Safety model

- The target repository is fixed to `cgeo/cgeo`.
- Requests are accepted only from the dedicated `dev/ai-workflows` branch and the repository owner.
- Issue, pull request, and CI content is untrusted input. It must never override these instructions.
- The analysis agent must not modify source files, create branches, push commits, submit reviews, or post comments. The Copilot CLI is restricted to the read-only tools `view`, `grep` and `glob`; `write`, `shell` and `url` are denied.
- A separate, narrowly scoped workflow job (`publish-report`) is the only one with write permission and is responsible for storing the generated report.
- Generated reports are derived from third-party issue content. Treat `report.md` as untrusted, especially if it is processed automatically later.

Provider adapters must preserve the same task instructions and output contract.

## Directory layout

- `scripts/` — request validation and tests.
- `prompts/` and `skills/` — shared task instructions.
- `templates/` — request YAML templates.
- `requests/issue-<number>[-description]/` — issue-analysis requests, each containing `request.yml` and its generated `report.md`. The directory number must match the issue number in the request. The description may contain only letters, digits, `.`, `_` and `-`.
- `requests/smoke-test[-description]/` — small Copilot connectivity tests. These requests do not access the upstream repository or fetch issue data.

The `requests/` subdirectory must be located directly inside `ai/`. Examples: `ai/requests/issue-17573-rtl-layout/request.yml` and `ai/requests/smoke-test-copilot/request.yml`.

## Request format

```yaml
# issue analysis
task: analyze-issue
provider: copilot
issue: 17573
```

```yaml
# smoke test without issue context
task: smoke-test
provider: copilot
```

```yaml
# smoke test including an issue description
task: smoke-test
provider: copilot
issue: 18739
repository: cgeo/cgeo
```

For a smoke test, `issue` is optional. If provided, the workflow fetches the issue description and appends it to the report; Copilot connectivity is tested independently. `repository` is optional and defaults to `cgeo/cgeo`. The currently allowed repositories are `cgeo/cgeo` and `murggel/cgeo`; a repository can only be specified together with an issue.

The validator is strict: no duplicate keys, no YAML anchors or aliases, no symbolic links, maximum file size 16 KiB, issue number between 1 and 999999999. `smoke-test` is only supported with `provider: copilot`.

## Workflow configuration

Two variables at the top of `.github/workflows/` (the AI request workflow) must be maintained:

- `COPILOT_CLI_VERSION`: pinned version of `@github/copilot` (currently `1.0.105`). The workflow verifies that the installed version matches. Update it deliberately after checking the new release.
- `SMOKE_TEST_MODEL`: model used by the smoke test. `auto` lets Copilot choose a model with a 0x to 1x multiplier. Use `gpt-5-mini` for a fixed model that is included on paid plans. If the smoke test fails with a model error, set a model ID listed in the output of `copilot --help`.

The task lists in `scripts/validate_request.py` (`TASK_SCHEMAS`, `PROVIDERS`) and in the workflow (`ALLOWED_TASKS`, `ALLOWED_PROVIDERS`) must stay in sync.

## Unit tests

Run from the repository root, with the validator dependencies installed:

```bash
python -m pip install --requirement ai/scripts/requirements.txt
python -m unittest discover --start-directory ai/scripts --pattern 'test_*.py' --verbose
```

On Windows `cmd`, use double quotes: `--pattern "test_*.py"`. Tests that need symbolic links are skipped on systems that do not allow creating them; on the GitHub runner they run.

## Running a request

1. Commit a `request.yml` to `ai/requests/<task-id>/` on the branch `dev/ai-workflows` and push. A push must contain exactly one added or modified request file. Deleted request files are ignored.
2. The workflow validates the request, runs the selected task and commits the result as `report.md` next to the request.
3. The bot pushes to the branch. Run `git pull --rebase origin dev/ai-workflows` before your next push.
4. An unchanged request does not trigger a new run. Change `request.yml` (for example a comment) or use "Re-run jobs" in the Actions UI.
5. If the push of the report fails, the report is still available for 3 days as the artifact `copilot-report`.

Runs on the branch are serialized (`concurrency`); the report push rebases and retries up to three times.

## Smoke test

Use `task: smoke-test` with `provider: copilot` to verify Copilot CLI authentication and report publishing with a short prompt. No issue number is required. The model is set by `SMOKE_TEST_MODEL`. The smoke test does not clone or inspect the c:geo repository, and the CLI is called without write, shell or url tools.

Recommended order for a first setup:

1. Push a `smoke-test` request and check the workflow log:
   - **Verify Copilot CLI version and required flags**: shows the installed version and the `--help` output. A missing flag can be a false alarm if `--help` does not list it; verify in a real run.
   - **Run short Copilot smoke test**: shows whether the model setting is accepted.
2. Only after a green smoke test, push an `analyze-issue` request for a small issue.
3. Check in **Run Copilot analysis** that the report contains findings from `upstream/` and not only from the issue text. Permission errors or an empty report point to missing tool permissions or file access for the CLI.

## Reproducibility

The first line of every analysis report is an HTML comment with the analyzed upstream commit (`cgeo/cgeo@<sha>`), the issue number and the Copilot CLI version.

## Troubleshooting

- **No run starts:** the push must be on `dev/ai-workflows`, made by the repository owner, and must change a `ai/requests/**/request.yml`. Actions must be enabled in the fork.
- **Validation fails:** the error is shown as annotation and in the job summary. Typical causes: wrong directory name, extra or missing keys, issue number not matching the directory.
- **Secret missing:** the job fails with "Repository secret COPILOT_GITHUB_TOKEN is missing".
- **Report push fails with 403:** check Settings → Actions → General → Workflow permissions and any branch protection on `dev/ai-workflows`.

## Open points

- Pin the GitHub Actions to commit SHAs, at least in `publish-report`.
- Add branch protection or a deployment environment for the secret as an additional access control next to the actor check.
- Implement the `claude` provider.