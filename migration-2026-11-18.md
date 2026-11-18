# Skill ownership migration — 2026-11-18

Source: `doc-system-governance` working tree at base `a4043105d126d1389d8adf9d01d3bf27b84efbad`, including its existing uncommitted source edits. Original source/release directories remain preserved; active maintenance moves here. New goal owns the loop semantics; renamed doc skill keeps generic rules and templates, with separate Reviewer conclusions and Planner dispositions.

Existing unrelated untracked `skills/hf-download/` is excluded from this migration commit. No old repository history or dirty work is reset. The nested installed weekly report adds a useful evidence-gated Skill-system paragraph; that content is retained in the single canonical skill. Existing weekly interface metadata remains unchanged.

Source file SHA256 before restructuring:

```json
{
  "SKILL.md": "ff5db8ee2a4fafbb92a46eff027f58edf5335ec97692537ebc9bf22f4a85d8a2",
  "references\\doc-system-rules.md": "124d8fe8db3554c825a6b81a12f20a8b22606f7fd07a3d583865dfa492ddd2e6",
  "references\\file-templates.md": "6ed5e62154f0b6c9d74ca292bb17d28cc6298f75c0037f9a29adb710f04826fa",
  "agents\\openai.yaml": "24899b15a3a97aae5973cb5f855e66723018a1db447bdea012b8724fc98d6c0e"
}
```

## Installation and retirement

On this workstation, `C:\Users\Freshman\.codex\skills\marcle-goal-excution`, `marcle-doc-governance` and `weekly-repo-report` are directory junctions to the matching canonical skill directories here. All installed files match source bytes; there is no independent maintained installed copy.

The former installed doc skill and the complete former weekly directory (including its nested duplicate) were moved to `C:\Users\Freshman\.codex\skill-backups\20261118-goal-doc-migration`, outside skill discovery. The old source repository has a `RETIRED.md` pointer; its previous dirty source and release copies remain intact. No old-repository commit or push was performed.

## Validation

- Official skill-creator `quick_validate.py` passed all three skills using `python -X utf8`. Initial default Windows GBK decoding failed; the files are UTF-8 and the validator was rerun in UTF-8 mode, without changing shared tooling.
- Relative Markdown links resolve; source/install bytes match. Filesystem discovery found exactly one entry for each new skill and weekly report, and zero entries named `doc-system-governance` under the Codex skill root. This verifies disk installation; the currently running chat's cached catalog is not claimed refreshed. Start a new Codex session to reload discovery.
- Independent read-only behavioral evaluation exercised analysis-only with existing project facts, a contested enterprise-platform P1, three consecutive P2 rounds with acceptance drift, deferred manual acceptance with commit-only authorization, and standalone documentation maintenance. No conflicting instructions were found. This is scenario reasoning, not an actual multi-day execution benchmark.
- The final independent review is in [review-2026-11-18.md](review-2026-11-18.md). Review conclusions and Planner acceptance remain separate.

## Planner disposition

Root accepts the independent review's Approved conclusion for skill content and verified local installation/retirement. No blocker remains in that scope; remote publication is verified separately at handoff.

The five scenario results match the agreed workflow. Existing user/project authorization and acceptance gates take precedence over defaults; the third-round rule requires design reassessment, not a fixed cap or automatic assignment of blame. No additional framework or automated scheduler is introduced.
