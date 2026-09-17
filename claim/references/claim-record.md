# A record for the current claim

Use for coaching recovery, explicit record requests and S7 export. This is a small record of one claim and its decisions, not a general task scheduler or a learning system. Keep it in the conversation until the user requests a file or the host's applicable archive rules authorize one. Follow those rules for the destination; do not invent a global store or alter skills.

## What to preserve

Keep only fields that affect the scientific statement or the user's learning. Each decision needs its exact wording, origin (user, AI proposal, or source), source turn or document locator, version and explicit confirmation if any. Use `UNKNOWN` for absent evidence of confirmation; a summary saying “confirmed” does not substitute for the underlying message.

| Record | Content |
|---|---|
| Current claim | Version and parent; verbatim user statement; object, conditions, comparator, conclusion |
| Formal statement | Quantifiers, domain, probability semantics and symbol explanations; user's S2 confirmation |
| Counterexample review | Candidate and premise check, result, user's scope/exclusion/cost judgments; or searched scope and conditional continuation when none was found |
| Assumptions | Original user attempt, later revisions, hint level, accepted/rejected/unknown status, necessity, removal failure and observability judgments |
| Proof obligation | User's first wording and current revision, input/output, domain/quantifier, error and regime or justified not-applicable field; remaining defect if any |
| Theory diagnosis | User's failure-mechanism explanation and category attempt, then inspected theorem applicability or unknown target |
| Failure rule | User's criterion and whether it concerns falsifying the claim or abandoning a research route |
| Sources | Exact new-content delta, queries/date/access, references and locators, applicability; added/revalidated/narrowed/dropped status |
| Gates | S1, S2, S3, S4, S5a, S5b, S6: current state plus actual user decision evidence, not just a Boolean |
| Revision history | Old text, changed fields, trigger/reason, scope cost and affected gates, including failed/downgraded versions |

The transfer exercise is a separate learning record: exercise, user's attempts, support used, T1–T3 outcome and overall transfer status. It never becomes evidence for the paper's claim.

## Recovery

Use current-conversation direct statements without making the user repeat them. Recovered prior-task user wording remains `UNCONFIRMED_PRIOR_USER_CLAIM` until shown verbatim and reconfirmed under S1. An AI summary or this table can locate evidence but cannot author a claim or supply missing confirmations.

Inspect the current claim version before continuing. If the user changes a field, apply the coaching protocol's invalidation matrix and retain the old version. Explicitly unchanged and independent decisions may remain; uncertainty about dependency reopens the affected gate. File timestamps, successful parsing and a full-looking record do not establish that gates passed.

## S7: export confirmed decisions

Export only after S1–S6 (including S5a/S5b) pass and the user requests the artifact. The first document line should identify the claim version and scope of the export. Use a format proportionate to the request:

1. **Statement:** the confirmed natural-language claim and mathematical formulation with symbol explanations.
2. **Conditions and limits:** confirmed premises/exclusions with their cost; explicitly unresolved items stay `UNKNOWN`.
3. **What must be proved:** the user's accepted obligations, their dependency order and the actual proof status. Use an implication graph or theorem ladder only if requested or materially clearer.
4. **Evidence and failure:** source-to-proposition mappings and the user's falsification/stopping rule.
5. **Revision provenance:** changed claims, reasons, invalidated decisions and source locators. Preserve failed/downgraded versions as history, never as current successes.

Render Markdown by default or LaTeX when requested. Check the exported statement back against the confirmed record, including quantifier order, comparator and accepted assumptions. Do not complete a missing proof, improve the claim, add a new theorem or introduce experiments during export. A missing necessary confirmed decision returns to its gate; other unresolved science is exported explicitly as unknown.

Report the learning status outside the scientific artifact: `CURRENT_CLAIM_COACHED` and the actual transfer status. One supported or independent exercise is not evidence of broad mastery. Successful export means a faithful record was created, not that the theorem is true.
