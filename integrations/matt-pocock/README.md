# Matt Pocock skills in Wingman

The 27 published engineering/productivity skills are pinned to Matt Pocock's
[upstream collection](https://github.com/mattpocock/skills) at
`abeeaf95660ba9e8b7c753eb38f441ca707a8823`. `upstream.tar` is a regular-file
`git archive` of those skill directories and the upstream MIT license. The
manifest records every input hash, original path and per-skill routing purpose.
The generated top-level skills keep every upstream file and invocation policy, adding only an
early persistence override to `SKILL.md`. The archive is maintenance input, not
another discoverable skill tree. The repository root contains the distributable overlay,
so relative adapter links work both in source and when installed side by side.
The shared [adapter](../../wingman-matt-adapter/SKILL.md) is maintained at the
repository root. Upstream copyright/license remain in the archive and
[LICENSE.upstream](LICENSE.upstream).

In a Wingman channel, invoke the same skills as before. `to-spec` writes one
canonical channel Doc and links its execution task; `to-tickets` creates channel
tasks with native parent/blocker links; `research` revises channel Docs;
`grill-with-docs` retains the interview and saves domain decisions there.
Outside Wingman the original configured tracker/files remain available. The
adapter does not grant deployment, restart, delegation or publishing authority.

## Validate and install locally

From this repository:

```sh
python3 scripts/matt-overlay.py check
python3 -m unittest discover -s scripts -p 'test_matt_overlay.py'
uv run --with pyyaml python scripts/check-matt-skills.py
python3 scripts/matt-overlay.py install --target "$HOME/.agents/skills" \
  --alias "$HOME/.codex/skills" --alias "$HOME/.claude/skills"
python3 scripts/matt-overlay.py check-installed --target "$HOME/.agents/skills" \
  --alias "$HOME/.codex/skills" --alias "$HOME/.claude/skills"
```

Install requires the existing `flight-deck-workflow`, `ambulando-artefacts`,
`wingman-sessions` and `artifacts` dependencies. Install those through their
maintained sources first. The installer checks all 28 canonical skill trees and
all requested aliases before changing any. It accepts pristine pinned upstream,
the current generated output, or an exact previously managed receipt; it refuses
local modifications, symlinks inside canonical trees and unmanaged alias
collisions. Reconcile conflicts explicitly, preserving local work. The receipt
is `.wingman-matt-install.json` in the canonical root. Updates recheck after
staging and immediately before each swap, then replace individual directories
with rollback on a failed rename and verification of the renamed previous tree.
Previous trees are retained under `.wingman-matt-backups/<run-id>/` beside the
canonical root, including after success, for explicit review/cleanup. They are
never removed by temporary staging cleanup; this preserves old-inode writes.
The batch is not a filesystem-wide transaction. After an interrupted install,
inspect each tree and receipt before retrying. Existing sessions may retain an
older discovery snapshot; installation is not a remote/fresh-client claim.

The general root `sync-skills.py` also discovers the top-level Matt skills.
Use the overlay installer for this collection's conflict/provenance checks;
use `--skill` selections when syncing unrelated Wingman skills.

## Review an upstream update

1. Fetch an upstream checkout and explicitly choose/review the new commit.
   Compare all 27 skill trees, supporting templates and invocation policies;
   account for additions/removals and every persistence instruction in the
   manifest's routing inventory. Re-read `ask-matt` and the adapter together.
2. Use `git archive --format=tar <commit> LICENSE <the manifest skill paths>`
   to replace `upstream.tar`. Update the manifest commit, archive digest and
   per-file hashes from that same checkout. This is an explicit reviewed repin,
   not an automatic pull or fuzzy patch.
3. Run `python3 scripts/matt-overlay.py render`; inspect the full diff. An
   input hash/archive mismatch or unknown generated-source edit stops rendering.
   `generated-lock.json` records the previous rendered trees for this check.
   File inventory removals require
   explicit reconciliation; render never silently deletes a generated file.
4. Run `check`, behavioral installer tests, frontmatter/link/dependency checks
   and review generated saving instructions. Commit the compatible tested source
   on the repository's chosen branch. Install only explicitly intended targets,
   then run `check-installed` and actual supported harness discovery.

Never edit installed copies as the only source. Changes to a managed installed
tree block the next rollout until reconciled; a receipt is not permission to
replace arbitrary content. Preserve user-invoked frontmatter and OpenAI policy
files exactly, including explicit-only skills. No update runs upstream hooks.

## Remote rollout

Autopilot's `docs/skill-catalogue.md` describes immutable source imports and
exact-revision project deployment plans. Import/activate is separate from project
application and agent discovery. The root skills are
regular-file importable source; the archive is not traversed. Dependencies must
also be present on each target. Resolve exact authorized agents, connection,
project and revision before mutation. Existing unmanaged content must remain a
conflict. This repository contains no remote-host allowlist or credentials and
does not imply that a local install reached any remote machine.
