---
name: review-gate
description: Review software task plans or coder changes when asked to review; explain evidence, responsibility, and the recommended next step.
---

# Review Gate

Use for software task or coder-implementation reviews. Review is read-only unless the user asks for changes. Respond in Chinese:

1. State **Approved** or **Changes Requested** and whether the next stage may proceed.
2. Explain the causal/ownership relationship and product impact briefly, with high logic and little code; avoid long tutorials.
3. For each P0/P1/P2 finding, preserve file/line evidence, task-versus-code comparison, actual test status, and a bounded correction suggestion.
4. In one brief paragraph, assess the overall cause: mainly **task design** (contradictory or missing boundary), mainly **coder execution** (explicit contract violated), **shared**, or **undetermined**. Distinguish missing tests from wrong design; this guides whether the task must change, not blame.
5. Recommend one overall path and why: **coder instruction only**, **small task correction then coder instruction**, or **revisit the whole task design**.

Stop at the recommendation. Do not edit, implement, or write the coder instruction in the review turn unless asked. On later confirmation, perform the recommended next step.
