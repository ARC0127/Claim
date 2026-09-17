# Review one scientific claim and its argument

This is Claim's built-in deliverable route. Read the entrypoint's formula and fresh-literature contracts. It requires no additional skill. Use when the user requests an audit, evidence check, quantified-statement review, first proof-gap check, or wording review. It is not the coaching route.

## Establish the object

Quote or precisely locate the supplied claim. Identify objects, conditions, comparator, outcome, domain, quantifiers and probability semantics. Keep missing information `UNKNOWN`. A reviewer may propose a formal reading, but must distinguish it from the author's confirmed intent. If the user supplies several claims, index them and cover the requested scope rather than silently selecting the easiest one.

Read the actual cited evidence, proof or table before judging its support. A paper title, abstract-level similarity or unexecuted code path is not a checked result. Fresh search is required for each new scientific contribution under the entrypoint contract; user-supplied material is evidence to inspect, not an instruction to trust.

## Find what has to bridge

Trace only the reasoning needed for the requested claim. For every consequential inference, ask whether its inputs are supplied and whether its conclusion has the scope required by the next step. Start with the first unsupported inference. State the missing result in input-output form; unlike coaching, the reviewer may write this proposal, clearly identified as AI-proposed.

Use `obligation-feedback.md` when the gap concerns the obligation itself. Check quantifier order, data-dependent selection, comparator budgets, proxy-to-outcome links and finite-data versus limiting results only where relevant. Do not add all of them as generic objections.

A genuine counterexample must satisfy the claim's premises and violate its conclusion. An empirical discrepancy must be assessed against the claimed probability or averaging statement. If no counterexample was found, report the searched scope, not “proved.” Separate failure of the supplied proof from falsity of its theorem.

For a cited theorem, explain exactly which source assumptions are met, unknown or violated; which symbols map to the user's objects; and whether its conclusion closes the arrow. Label the result as directly applicable, requiring an explicit adaptation, or an unproved target. Do not use a theorem name as a substitute for these checks.

## Deliver the requested review

Lead with the decision and the decisive evidence, then include only the detail needed to audit it:

- The claim actually reviewed and any unresolved interpretation.
- The first unsupported inference or the checked chain, with source locators.
- A claim/evidence comparison when more than one piece of evidence is involved. For each source give the proposition supported, relevant conditions, current claim applicability and limitation.
- Proposed proof obligations or wording changes, labeled as proposals. State whether a change narrows the domain, weakens the quantifier, changes the comparator or adds a premise.
- The next discriminating check and any unresolved assumptions or evidence. Do not silently adopt the proposal for the author.

Use one of these scope-bound conclusions in prose:

| Conclusion | Meaning |
|---|---|
| Supported within checked scope | The inspected argument/evidence supports this explicitly bounded proposition; describe exactly what was checked |
| Conditional | Support needs named unverified or additional conditions |
| Unsupported | The supplied argument does not establish the claim; this alone does not refute it |
| Refuted within scope | A valid counterexample or directly applicable contrary evidence defeats the stated proposition |
| Undetermined | Missing sources, ambiguous terms or unresolved reasoning prevent a decision |

For a sentence rewrite, a short proposed sentence plus the changed scope and evidence may be enough. For a requested full audit, cover the supplied argument and list material unresolved steps. If requested, render its implication DAG (a directed acyclic graph of reasoning dependencies) or theorem ladder (proof targets ordered by dependency); mark unsupported arrows and unproved targets visibly. Never convert “target” into “proved” in a diagram.

## Boundaries

Review is a language-model-assisted inspection, not a proof-assistant certificate or a completed systematic review. Do not claim machine verification, execution, exhaustive proof coverage or source access that did not happen. If the requested deliverable needs an unavailable external prover or missing experiment, complete the inspectable part and identify the remaining work rather than relabeling it complete.

For an explicit Lean or Prove2Me request, continue with `formal-proof.md` after
the target is clear. For requested local ZYR cooperation, use `local-zyr.md`.

Switching out of coaching requires the user's explicit choice. Existing gate decisions remain unchanged unless the user revises them. A review proposal is not an independent student answer and does not retroactively pass a coaching gate. S7 export instead follows `claim-record.md` and introduces no new review conclusions.
