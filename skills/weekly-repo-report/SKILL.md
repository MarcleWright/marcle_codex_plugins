---
name: weekly-repo-report
description: Generate a concise Chinese weekly product report from a repository's Git commit history, with PM-friendly task summaries and business value.
---

# Weekly Repo Report

Use this skill when the user asks for a weekly report, last-week summary, or product-oriented summary of repository work based on Git history.

## Source and period

- Inspect the repository's Git history with read-only commands such as `git log`.
- If the user does not provide a period, use the previous natural calendar week, Monday through Sunday, based on the current date.
- Report the period as `YYYY-MM-DD to YYYY-MM-DD`. Use ASCII `to`; do not use Chinese date words or an em dash.
- Treat commit messages and diffs as evidence. Group related commits into product-level workstreams rather than listing commits one by one.
- Derive the repository name from the repository context or remote name when available. Prefer the project name over a local worktree folder name.

## Writing requirements

- Write in clear, natural Chinese from a product manager's perspective.
- Target about 250 Chinese characters unless the user requests another length.
- Explain both what was delivered and why it matters: user experience, efficiency, reliability, capability expansion, reuse, or future scalability.
- Technical terms are allowed when they clarify the product change, but avoid implementation-heavy wording.
- Do not invent impact metrics, user outcomes, roadmap commitments, or unverified functionality. Use qualitative value statements when metrics are unavailable.
- Combine overlapping work and prioritize user-facing capabilities, then reliability and foundational work.

## Required output format

Return only the report unless the user asks for explanation:

```md
YYYY-MM-DD to YYYY-MM-DD

### repo-name

总结：本周用一句话概括主要方向、产品收益和基础价值。

- 任务与价值。
- 任务与价值。
- 任务与价值。
```

The `总结` line is正文 and must not have a bullet marker. Use 3–6 bullets after it. Each bullet should follow “完成什么 + 带来什么价值”. Keep the heading and labels in the demonstrated form, use ASCII punctuation where practical, and preserve product names or technical terms when they are useful for accuracy.
