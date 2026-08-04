---
name: claim
description: One entry point for research-claim coaching, complete theory audits, evidence alignment, proof checks, formalization, contribution refinement, and overclaim-safe writing. Use when the user invokes $claim or asks to analyze a claim. Coaching includes gated decisions, learning reviews, progressive hints, deep dives, transfer checks, prior-claim recovery, a fresh web literature pass for every substantive new user contribution, and web-backed counterpositions whenever an idea materially conflicts with verifiable theory, standards, or empirical evidence.
---

# Claim

Use this skill as the single user-facing entry point. Route by the decision the user wants, not by isolated keywords.

## Route

| User intent | Route |
|---|---|
| Learn or practice how to derive needed theory from a user-owned claim | Internal coaching protocol in `references/theory-coach.md` |
| Request a detailed explanation of a concept at the current coaching gate | Internal `DEEP_DIVE` mode; keep the gate unchanged |
| A user idea appears materially wrong or conflicts with established knowledge | Internal `EVIDENCE_CHALLENGE`; browse the web and provide detailed references before objecting |
| Receive a complete theoretical claim audit, implication DAG, theorem ladder, or verdict | `theory-claim-audit` |
| Map claims to evidence and expose unsupported claims | `zyr-s203-claim-evidence-matrix` |
| Refine a contribution claim or positioning | `zyr-s207-contribution-claim-refinement` |
| Check contradictions, missing premises, circularity, or scope drift | `zyr-s226-logic-consistency-audit` |
| Normalize theorem quantifiers, notation, or hidden assumptions | `zyr-s237-theorem-assumption-normalizer` |
| Check proof-idea viability or find the first proof gap | `zyr-s230-proof-idea-check` or `zyr-s235-proof-gap-finder` |
| Verify a proof | `zyr-s240-pessimistic-proof-verification`; use `zyr-s241-progressive-proof-verification` for materially long proofs |
| Produce a theorem-prover scaffold after natural-language audit | `zyr-s433-formal-proof-adapter` |
| Audit sentence-level overclaim risk | `zyr-s527-claim-language-risk-linter` |

## Coaching versus audit

- Route pedagogical intent such as “教我”, “引导我”, “逐轮”, “训练判断”, or “不要替我做完” to the internal coaching protocol.
- Route deliverable intent such as “完整审计”, “替我检查”, “生成 Theory Specification”, “给出 DAG/定理路线”, or “一次性完成” to `theory-claim-audit`.
- During coaching, route explicit requests such as “详细解释这个概念”, “展开讲一下”, or “为什么” to `DEEP_DIVE`, not audit.
- When a user statement appears materially inconsistent with known theory, standards, or evidence, treat internal knowledge only as a search trigger. Enter `EVIDENCE_CHALLENGE` only after mandatory web verification.
- When the user asks to continue or recover a claim from another task, use the coaching protocol's `UNCONFIRMED_PRIOR_USER_CLAIM` procedure; do not silently activate a historical claim.
- If “帮我分析理论 claim” remains ambiguous, ask exactly one question: “你要我完成审计，还是逐轮训练你自己判断？” Do not start either mode until answered.
- Never switch from coaching to audit because context appears sufficient. Switch only when the user explicitly exits coaching or passes its archival gate.
- Treat completion of the current claim and evidence of learned transfer as different statuses. Archival may proceed with `TRANSFER_UNTESTED`, but never call the coaching successful without the required transfer evidence.

For coaching, read `references/theory-coach.md` completely before responding and let it control every turn. Treat its canonical four-heading template, status-line grammar, and precedence rules as literal output requirements. Do not attach a secondary skill during coaching stages S1-S6.

## Global formula clarity contract

Apply this contract to every formula produced through this skill, including coaching, audit, proof review, `DEEP_DIVE`, `EVIDENCE_CHALLENGE`, transfer exercises, and archival documents. Enforce it on downstream-skill output before sending the response. Brevity limits never justify leaving notation unexplained.

For every displayed formula and every nontrivial inline formula:

1. Introduce in Chinese what the formula represents and why it is needed at the current step.
2. Immediately after the formula, provide a symbol table with these fields: `符号`, `中文含义`, `类型或取值域`, `形状/维度/单位`, and `角色与依赖关系`.
3. Define every variable, index, set, function, parameter, estimator, random variable, decision variable, constant, nonstandard operator, subscript, superscript, conditioning expression, norm or metric, quantifier, and probability or expectation measure that appears.
4. At first use, expand every English acronym and technical English phrase and explain its Chinese meaning. Do not paste English labels as if they were self-explanatory.
5. After the symbol table, give a plain-Chinese reading of the formula: identify its inputs, operation or comparison, output or conclusion, and relevance to the current claim.
6. If a symbol's meaning, domain, unit, dependency, or status is unavailable, mark that field `UNKNOWN`; do not guess.
7. When quoting or adapting a formula from a source, preserve the source notation, cite the source when required, and explicitly map each source symbol to the user's scientific objects.
8. A symbol may be defined once per response or tightly scoped section only while its meaning and scope remain unchanged. Redefine it whenever either changes.

Ordinary arithmetic symbols need no separate row unless overloaded, but “familiar to experts” is not a reason to omit a definition. Do not use a dense equation as a substitute for reasoning. Before sending any formula-bearing response, check that no symbol or English acronym remains undefined.

## Global fresh-literature contract

Treat every user turn as a possible change to the active scientific object. When the user adds or changes substantive scientific content, run a new `FRESH_LITERATURE_PASS` with live web search before relying on literature in the response. Apply this rule in coaching, audit, proof review, `DEEP_DIVE`, `EVIDENCE_CHALLENGE`, transfer exercises, and archival work, including after a downstream skill drafts its output.

Substantive new content includes a new or changed claim, object, domain, comparator, quantifier, definition, assumption, mechanism, implication, theorem obligation, proof step, metric, dataset, empirical result, cited work, scope exclusion, or failure rule. A purely conversational acknowledgement or formatting request that changes no scientific meaning may be marked `NO_NEW_SCIENTIFIC_CONTENT`; when uncertain, treat the turn as substantive.

For each `FRESH_LITERATURE_PASS`:

1. State the exact new-content delta and rethink what literature is relevant to that delta instead of copying the previous query frame.
2. Search the current web. When feasible, use at least two conceptually distinct query angles: one directly matching the new content and one seeking a counterexample, alternative explanation, canonical theorem, or competing formulation.
3. Downgrade all previously used references to `PRIOR_SOURCE_CANDIDATE` for the new delta. Reopen and reinspect a prior source in the current turn before calling it `REVALIDATED_PRIOR_SOURCE`. The bibliography may remain the same only after this fresh applicability check; source novelty is not required, but fresh search and reasoning are.
4. Open direct source pages rather than relying on snippets. Prefer original papers, official proceedings, formal standards, official documentation, original datasets, and canonical theorem sources. Verify publication metadata, version, corrections, retractions, and current access when relevant.
5. Search for evidence both supporting and challenging the new content. Do not use the search only to confirm the active idea.
6. For every retained source, explain its exact connection to the new delta and check its objects, assumptions, domain, comparator, quantifiers, outcome, and limitations. Drop or narrow a source whose applicability no longer matches.
7. Give detailed references: title, authors or issuing body, year, venue or publisher, DOI or stable identifier when available, direct link, source type, precise supported proposition, applicability, and limitation.
8. Report the search date and one status: `FRESH_SEARCH_COMPLETE`, `SEARCH_BLOCKED`, or `LITERATURE_NOT_FOUND`. Also identify material sources added, revalidated, narrowed, or dropped. Under the latter two statuses, preserve `UNKNOWN` and do not silently fall back to the old bibliography.
9. Keep the search within the current coaching gate. Before S5b, literature may clarify concepts, test factual premises, or support counterexamples, but it must not choose an assumption, write the user's theorem obligation, name the final theory category, or select a theorem family.

An `EVIDENCE_CHALLENGE` search satisfies the fresh-literature requirement for the same user-content delta when it follows the stricter challenge protocol. Never perform a second redundant search merely to produce both labels.

## General execution rules

1. Select one primary route. Add at most one secondary route only when the requested outcome truly spans two non-coaching contracts.
2. State the route briefly. If its output contract is exact, place the marker inside the first permitted section or in commentary; do not add an extra section.
3. Read the selected downstream skill's `SKILL.md` completely and follow its required inputs, workflow, hard failures, and output contract.
4. Preserve `UNKNOWN`; never invent assumptions, evidence, citations, theorem validity, or experimental results.
5. Keep scientific claims, mathematical validity, implementation binding, empirical evidence, and publication wording distinct.
6. Never present a factual or literature-based objection without current web search, direct source links, and an applicability analysis.
7. Use formal-proof adaptation only after the natural-language claim and proof obligations are stable.
8. Do not create a multi-skill pipeline unless the user asks for one.
9. Apply the global formula clarity contract after every primary or downstream route; a formula with undefined notation is a hard output failure.
10. Apply the global fresh-literature contract after every substantive user contribution; automatic inheritance of the previous bibliography is a hard output failure.
11. During S1-S6 coaching, do not paraphrase the canonical headings or status block, and do not use legacy `Stage Sx` or `GATE UNCHANGED` markers.

## Examples

- “Use `$claim` to teach me how to decide what theorem I need.” -> internal coaching.
- “Use `$claim` to explain IPM versus reachable-set guarantees in detail without advancing.” -> `DEEP_DIVE` at the current gate.
- “Use `$claim` to continue the claim I stated in another task.” -> retrieve verbatim user text, label it unconfirmed, and request reconfirmation.
- “This mechanism must always improve return.” -> if materially doubtful, pause the gate, browse primary sources, and present the strongest sourced counterposition.
- “I now want the guarantee to hold uniformly rather than on average.” -> identify the quantifier delta, run a fresh web search, and revalidate rather than inherit the earlier sources.
- “Use `$claim` to produce a complete audit of this theory claim.” -> `theory-claim-audit`.
- “Use `$claim` on these claims and Tables 1-2.” -> `zyr-s203-claim-evidence-matrix`.
- “Use `$claim` to inspect this theorem and proof.” -> theorem normalization, then proof verification if no blocking ambiguity remains.
- “Use `$claim` to make this abstract sentence safer.” -> claim-language risk linter.
