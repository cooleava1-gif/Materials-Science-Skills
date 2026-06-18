# Git History Slimming Plan

This plan is for a future coordinated rewrite of Git history to remove old
large generated figure exports from historical commits. The current repository
state already removes those files from `main`, but the old blobs still exist in
history until a filter-rewrite is performed.

Do not execute this plan casually. It rewrites commit IDs on `main` and requires
coordination with every clone and every audit branch.

## Goals

- Remove historical generated figure exports from repository history.
- Keep source-only figure package examples.
- Keep `showcase-proof` product screenshots.
- Preserve the current `main` content and release behavior.
- Give other agents a clean resync procedure after the rewrite.

## Non-Goals

- Do not delete source data, plot scripts, package manifests, README files,
  storyboards, caption boundaries, QA reports, or contracts.
- Do not remove `plugins/materials-skills/skills/materials-figure/assets/showcase-proof/*.png`.
- Do not change release gates during the history rewrite unless verification
  finds a mismatch.
- Do not rewrite history while other agents are actively committing to `main`.

## Target Paths

The primary historical targets are generated exports under the plugin package
example packages:

```text
plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.svg
plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.png
plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.pdf
plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.tif
plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.tiff
```

Add more paths only after `git filter-repo --analyze` proves they are generated
or duplicated assets and a maintainer approves the expanded list.

## Preconditions

1. Announce a freeze window for `main`.
2. Confirm all active agents have stopped committing.
3. Confirm `origin/main` contains the latest verified slimming commit.
4. Confirm the local worktree is clean:

```powershell
git status --short --branch
```

5. Create and push a backup ref:

```powershell
git branch backup/pre-history-slimming-2026-06-16 main
git push origin backup/pre-history-slimming-2026-06-16
```

Use the actual execution date in the backup branch name.

## Analysis

Run the rewrite in a fresh clone or disposable worktree, not in the daily
working directory.

```powershell
git clone https://github.com/cooleava1-gif/Materials-Science-Skills.git Materials-Science-Skills-slimming
cd Materials-Science-Skills-slimming
git checkout main
git count-objects -vH
git filter-repo --analyze
```

Inspect `.git/filter-repo/analysis/` and confirm that the largest blobs match
the target generated export paths. If unrelated files appear in the largest
blob list, stop and decide whether they belong in a separate plan.

## Rewrite Command

Requires `git-filter-repo`.

```powershell
git filter-repo --force `
  --path-glob 'plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.svg' `
  --path-glob 'plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.png' `
  --path-glob 'plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.pdf' `
  --path-glob 'plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.tif' `
  --path-glob 'plugins/materials-skills/skills/materials-figure/examples/figure-packages/*/figure.tiff' `
  --invert-paths
```

PowerShell backticks are line continuations. If running in another shell,
translate the command syntax carefully.

## Post-Rewrite Verification

Run these checks before force-pushing:

```powershell
git status --short --branch
git ls-files '*figure.tiff'
git ls-files 'plugins/materials-skills/skills/materials-figure/examples/figure-packages/**/figure.*'
git count-objects -vH
python -m unittest tests.test_figure_asset_slimming -v
python scripts\check_skill_architecture.py --json
python scripts\run_release_checks.py --json
```

Expected:

- `git status` is clean.
- The two `git ls-files` commands return no tracked generated package exports.
- `showcase-proof` PNG files remain tracked.
- Architecture and release gates pass.
- Repository object size is lower than the pre-rewrite baseline.

## Push Procedure

Only push after verification and human approval:

```powershell
git push --force-with-lease origin main
```

Do not force-push audit branches unless a maintainer decides to recreate them.
Prefer recreating `gemini` and `mimo` from the new `origin/main` if their old
history is no longer needed.

## Resync Procedure For Agents

After the force-push, every agent or local clone must resync:

```powershell
git fetch origin --prune
git checkout main
git reset --hard origin/main
```

If a clone has local work, save it as patches before the reset:

```powershell
git diff > local-work-before-history-slimming.patch
git diff --staged > local-staged-work-before-history-slimming.patch
```

Then reapply only the intended changes on top of the rewritten `main`.

## Rollback

If the rewrite is pushed and a critical problem is found, restore from the
backup ref:

```powershell
git push --force-with-lease origin backup/pre-history-slimming-2026-06-16:main
```

After rollback, rerun release checks and tell every agent to resync again.

## Acceptance Criteria

- `origin/main` has rewritten history with generated package export blobs
  removed.
- `python scripts\run_release_checks.py --json` returns `status: pass`.
- `git ls-files '*figure.tiff'` returns empty.
- `git ls-files` does not list `examples/figure-packages/**/figure.svg`,
  `figure.png`, `figure.pdf`, `figure.tif`, or `figure.tiff`.
- `showcase-proof` assets remain tracked and plugin metadata still points to
  them.
- All active agents confirm they have reset or recloned from the rewritten
  `origin/main`.
