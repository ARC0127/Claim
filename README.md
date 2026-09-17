# Claim

<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

![Claim — Identify what your research claim actually requires you to prove](docs/assets/claim-cover.svg)

## AI has written the complete answer. You may not have understood it at all.

Give an idea to AI, and it can propose assumptions, suggest theorems, and produce something that looks like a complete proof. The argument sounds plausible. The discussion moves forward. Then someone asks why an assumption is necessary, whether a different quantifier changes the result, or what counterexample would defeat it. You realize you accepted the answer without developing the judgment behind it.

**Research should involve more than AI doing the reasoning and you approving the result.** This matters especially in theoretical work. If AI chooses the claim, assumptions, and proof target, the text can become increasingly polished while your understanding stands still.

Claim keeps those decisions in the conversation for you to make. AI can explain concepts, search the literature, construct counterexamples, and check reasoning. You first state what you want to establish, decide which conditions to accept, and attempt a **proof obligation**: the precise result still needed to make the argument work. Claim is a skill for research conversations, designed to make AI assistance support understanding as well as produce answers.

When you want a direct review or a formal proof, you can explicitly choose that route. Delivered work and independent practice are recorded separately.

**0.3.0 · internal** · General CLI, Claude Code, and Codex · Python 3.10+

[Quick start](#quick-start) · [Installation](#installation) · [Coaching](#how-coaching-works) · [Example](#a-concrete-feedback-example) · [Formal proofs](#continuing-to-a-formal-proof) · [FAQ](#faq)

## What Claim helps you work through

**The premise holds, but the conclusion does not follow yet.** A statement that holds separately at each point may not hold uniformly across a domain. Claim examines the missing inference and the quantifiers the conclusion actually requires.

**A counterexample leads to more and more assumptions.** An added condition may exclude the cases you care about most. You try to propose a minimal condition first. Claim then checks what it rules out, what scope it costs, and whether it merely restates the desired conclusion.

**You know a theorem's name, but not the result you need.** “Use a concentration inequality” is not yet a proof obligation. Claim checks your proposed inputs, outputs, quantifiers, and error control before searching for applicable theory.

**You have a proof, but may have proved a different claim.** Claim checks the formal statement, premises, dependencies, and application conditions. A mathematical theorem and an implementation satisfying its premises are different conclusions.

Choose Coaching to practice your judgment, or Review to receive a direct assessment. Having enough context is not permission to silently replace coaching with a complete theory written for you.

## Quick start

Download [Claim-0.3.0.zip](dist/Claim-0.3.0.zip) and keep the extracted `claim/` folder intact. Run the commands below from the repository root or the extracted directory containing that folder.

With Claude Code installed:

```bash
python claim/scripts/claim.py run --client claude --request "Coach me through my research claim one step at a time. Do not complete the theory for me."
```

With Codex CLI:

```bash
python claim/scripts/claim.py run --client codex --request "Guide me through analyzing my research claim."
```

On Windows, use `py -3` if `python` is unavailable. On macOS / Linux, `python3` is also suitable. The selected client must be installed and discoverable on PATH; it manages its own account and authentication.

Once the conversation starts, explain in your own words what you want readers to believe. You do not need to know a theorem's name or prepare a complete theoretical framework first.

## Installation

### Option 1: Run the CLI directly

No personal skill installation is required. Keep the extracted folder and run:

```bash
python claim/scripts/claim.py --version
python claim/scripts/claim.py doctor
python claim/scripts/claim.py run --client claude --mode coach --request "My claim is..."
```

The launcher uses your selected client's model, account, and interactive permissions. It does not choose a model or bypass permission prompts. Each `run` starts a new session; continue the conversation in that session.

### Option 2: Install as a client skill

| Client | Personal location | Project location | Invoke |
|---|---|---|---|
| Claude Code | `~/.claude/skills/claim/` | `.claude/skills/claim/` | `/claim` |
| Codex | `$CODEX_HOME/skills/claim/`; default `~/.codex/skills/claim/` | Follow the client's configuration | `$claim` |
| Other assistants | A location where the assistant can read the complete folder | Follow the assistant's file interface | Explicitly request `claim/SKILL.md` |

First-time Claude Code installation in Windows PowerShell:

```powershell
$claimSkillsRoot = Join-Path $env:USERPROFILE ".claude\skills"
Expand-Archive -LiteralPath ".\Claim-0.3.0.zip" -DestinationPath $claimSkillsRoot
```

First-time Codex installation in Windows PowerShell:

```powershell
$claimSkillsRoot = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME "skills"
} else {
    Join-Path $env:USERPROFILE ".codex\skills"
}
Expand-Archive -LiteralPath ".\Claim-0.3.0.zip" -DestinationPath $claimSkillsRoot
```

macOS / Linux:

```bash
# Claude Code
mkdir -p "$HOME/.claude/skills"
unzip Claim-0.3.0.zip -d "$HOME/.claude/skills"

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
unzip Claim-0.3.0.zip -d "${CODEX_HOME:-$HOME/.codex}/skills"
```

These commands assume the downloaded ZIP is in your current directory. When installing from the repository, use `dist/Claim-0.3.0.zip`. You can also copy the complete `claim/` folder directly.

For an existing installation, inspect personal changes and back up the old directory outside the client's skills directory. Replace the complete folder rather than mixing versions. Start a new session and reload the entrypoint afterward.

### Option 3: Export context for another assistant

```bash
python claim/scripts/claim.py prompt --mode coach --request "My research claim is..." --output claim-context.md
```

The UTF-8 export includes the entrypoint and the selected mode's main protocols. It refuses to overwrite an existing file. Give the assistant access to the complete `claim/` folder for references needed later.

Exporting text does not add search or execution tools to an assistant. Scientific source verification needs live web search; formal proof checking needs a working Lean environment.

## CLI reference

| Command or option | Purpose |
|---|---|
| `--version` | Show the packaged version |
| `doctor` | Inspect client paths and local Lean/Lake availability; no login or network calls |
| `run --client claude\|codex` | Launch the explicitly selected native client |
| `--mode coach` | Default: step-by-step coaching |
| `--mode review` | Direct claim and argument review |
| `--mode proof` | An explicitly requested formal proof task |
| `--request "..."` | Required request for launch or export |
| `--dry-run` | Print launch arguments without starting a conversation |
| `prompt --output filename` | Create a context file; omit output to print to the terminal |

For example:

```bash
python claim/scripts/claim.py run --client claude --mode review --request "Review the claim and proof in this directory."
python claim/scripts/claim.py run --client codex --mode proof --request "Read my confirmed obligation and check the formal statement first."
python claim/scripts/claim.py run --client claude --request "Coach me step by step." --dry-run
```

Archiving and deep explanations are requests inside the conversation, not additional CLI modes. The launcher does not infer missing user confirmations from old files.

## How coaching works

Each turn advances one decision. You retain ownership of the claim, exclusions, assumptions, and failure rule. You also attempt the required conclusion before AI writes it for you.

| Stage | Your judgment | Claim's help |
|---|---|---|
| S1 — Claim | What should the reader believe, and about which objects and domain? | Separate objects, conditions, comparator, and conclusion without adding a method |
| S2 — Formalization | Does the mathematical statement still mean what you intended? | Make quantifiers and symbols explicit, then wait for confirmation |
| S3 — Counterexample | Is it in scope, and would you exclude it? | Check premises and construct a counterexample without immediately repairing the claim |
| S4 — Assumptions | Try a minimal condition; accept, reject, or leave it unknown | Check whether it blocks the counterexample, is circular, or narrows scope |
| S5a — Proof obligation | Attempt the needed inputs, outputs, quantifiers, and error statement | Explain the single mismatch that most directly blocks the next inference |
| S5b — Theory type | Explain why the inference fails, then try to classify it | Allow multiple categories, other, or unknown; then search for applicable tools |
| S6 — Failure condition | What result would make you abandon this version of the claim? | Check that the proposed falsification matches the scope and quantifiers |
| S7 — Archive | Explicitly request an export after the earlier decisions are confirmed | Export the confirmed version, preserving unproved obligations and unknowns |

Do not invent a condition just to complete a stage. A pure mathematical statement may have no method comparator. A deterministic claim may involve no probability. If no counterexample is found, record the search scope and let the researcher decide whether to continue conditionally.

### Fixed format and state

Stages S1–S6 use four fixed headings. The state block follows the first heading. An ordinary coaching turn looks like this:

```text
1. **你刚才表达了什么**

`阶段 S1 · GATE OPEN`
`模式：STANDARD`
`检索：NO_NEW_SCIENTIFIC_CONTENT`

2. **我如何形式化**

3. **当前最大歧义**

4. **一个需要你亲自回答的问题**
```

The headings mean: what you expressed; how it is formalized; the main ambiguity; and one question for you to answer. `OPEN` means the current decision is unresolved. Passing requires your explicit answer to meet the stage's conditions; “continue” does not supply a missing decision.

Both READMEs describe the same protocol. Its fixed coaching headings, state prefixes, and formula-symbol explanations currently use Chinese. An English README does not turn the execution protocol into an English-only one. Maintenance requests, such as editing files or checking versions, do not use this teaching template.

### When you get stuck

- **“Explain this concept in depth, without advancing.”** `DEEP_DIVE` allows a fuller explanation of the current concept while leaving the stage unchanged.
- **“I cannot work out how to restrict this counterexample.”** Hints first identify the freedom the counterexample exploits, then use a neutral example from an unrelated domain. A candidate condition comes only if you still cannot formulate one.
- **“Check my proof target without giving me the answer.”** Claim explains what your target already covers and the missing component for you to revise.
- **“This time, give me a direct review.”** Explicitly switch to Review. An AI-written answer is not recorded as your independent completion.

A brief learning reflection can identify the judgment you just practiced and why it determines the kind of result needed next.

## A concrete feedback example

> **Learner:** “The function values tend to zero at every point, so eventually the error can be arbitrarily small everywhere at once.”
>
> **Claim:** “Each point having its own sufficiently late starting index does not establish one index that works for all points. You still need uniform error control over the interval.”
>
> **Question for the learner:** “How does the result you need for all points at once differ from the pointwise result you already have?”

This classical real-analysis problem develops quantifier order, counterexamples that change with the index, supremum versus maximum, the cost of restricting a domain, and the formulation of a uniform error obligation.

The [full advanced example](docs/examples.md) includes a mathematical check to open after answering and a transfer exercise on limits and differentiation. All examples are independent of specific research projects. Transfer answers are not given in advance or mixed into the original claim's archive.

## Literature, objections, and formulas

### Search again after each substantive change

A new or revised claim, assumption, quantifier, definition, piece of evidence, or proof step requires a new web search focused on that change. Previous references become candidates; reopen them and check applicability before reusing them. The bibliography may stay the same, but the fresh check cannot be skipped.

Confirming already displayed content, adjusting formatting, or exporting unchanged text is not new scientific content. If search fails, record what remains unverified instead of presenting model memory as a completed source check.

### Ground objections in evidence

When an idea appears to conflict materially with established results, Claim searches before objecting. It identifies the conflicting inference, the source statement, its conditions and domain, and a direct reference. References should give authors or issuing body, title, year, venue, DOI or stable link, and the precise proposition they support.

The objection concerns an inspectable argument, not the researcher. Contrary evidence does not authorize AI to select a replacement claim or accept an assumption on your behalf.

### Explain every symbol

A formula needs nearby explanations of its variables, functions, sets, indices, quantifiers, and probability objects, including domains, units, and dependencies. Expand unfamiliar English abbreviations at first use. Missing definitions stay unknown; unexplained labels are not an adequate explanation.

## Revision, archiving, and transfer

You may revise any previously confirmed claim. Claim preserves the old text, reason for revision, and scope cost, then reopens affected downstream stages. A counterexample should not disappear through an undocumented change of statement.

Your exact words from the current conversation can be reused. Recovery across conversations requires a verbatim user statement, labeled `UNCONFIRMED_PRIOR_USER_CLAIM` and shown for reconfirmation. An AI summary can help locate it but cannot replace that confirmation.

After S1–S6, explicitly request a Theory Specification, argument dependency diagram, or proof-obligation list. The archive preserves confirmed decisions. An unproved target stays unproved, and formatting does not turn `UNKNOWN` into a fact.

Transfer practice is separate: for a nearby but different claim, independently identify its objects, quantifiers, and first unsupported inference. Record whether hints were needed. Completing one claim together is not evidence of mastering the method.

## Continuing to a formal proof

Once the obligation is explicit, you can ask:

```text
Formalize the confirmed obligation in Lean.
First compare the informal and formal statements, then split the lemmas
and inspect the actual compiler results.
```

The workflow is:

```text
Confirmed claim
  → Precise proof obligation
  → Informal argument and supporting lemmas
  → Lean formalization in a pinned environment
  → Compilation, exact statement, and transitive axiom check
  → Optional Prove2Me targets, dependencies, and submission status
  → Check that the application satisfies the theorem's premises
```

Lean checks formal proofs. Prove2Me can organize targets, decompose obligations, and verify submissions. A dependency diagram should distinguish compiler-extracted logical dependencies, unproved decompositions, and implementation or experimental support.

A successful build is not the entire check: inspect whether the statement was weakened or relies on an unproved target or placeholder axiom. Waiting, accepted decomposition, and accepted proof are distinct platform states. Each applies only to the target actually checked.

The bundled [ClaimDemo.lean](claim/assets/proof-demo/ClaimDemo.lean) proves that adding two even natural numbers produces an even number. It is a minimal compilation check. Run it inside an existing Lean project environment:

```bash
lake env lean /path/to/claim/assets/proof-demo/ClaimDemo.lean
```

The file prints the exact theorem and its axiom dependencies. Pin toolchain and dependency versions for actual research. The real-analysis teaching example has not been formalized in Lean; the arithmetic smoke test does not establish it. [Detailed proof workflow](docs/proof-workflow.md)

## What has been checked

| Layer | Recorded results |
|---|---|
| Files and release | UTF-8, fixed Chinese template, manifest, links, checksums, exact ZIP contents, and deterministic rebuilding pass |
| Program regressions | 22 tests cover release and CLI behavior; mocked invocation is not a live model conversation |
| Local installations | Codex and Claude Code copies checked for exact file sets and bytes |
| Windows text | PowerShell 5.1 default and explicit reads compared, with incorrect decoding as a negative control |
| Minimal formal proof | Compiled with Lean 4.33.1; the even-addition theorem has no axiom dependencies |
| Model and learning outcomes | No live coaching-adherence evaluation or human learning study has been completed |

This update retains version 0.3.0 and rebuilds the ZIP. Verify downloads against the [current SHA-256 checksums](dist/SHA256SUMS.txt). See the [validation record](docs/validation.md) for commands and scope.

## FAQ

**Do I need Codex?** No. Use Claude Code, the CLI, or another assistant that can read the protocol files. The host supplies the model, search, and execution tools; Claim supplies the conversation protocol.

**Why does the ZIP not include the test suite?** The ZIP contains the installable `claim/` skill. The repository contains the full validation tools, tests, and documentation. Running the skill does not require the whole repository.

**Why is the skill missing or still using an old format?** Check that the path is exactly `skills/claim/SKILL.md`, without an extra nested folder. After updating, start a new session and explicitly reload the entrypoint.

**What should I do about garbled Chinese text?** Do not copy damaged headings from old messages. Read the file explicitly as UTF-8. The coaching reference carries a Windows-compatible BOM; Python can read it with `utf-8-sig`. Updating files cannot repair text already generated in historical messages.

```powershell
Get-Content -LiteralPath "actual/path/claim/SKILL.md" -Encoding UTF8
```

**What if search or Lean is unavailable?** Without search, scientific sources remain unverified. Without Lean, the assistant may prepare a formal target and run instructions, but must not claim compilation succeeded.

**Can I ask AI to write the answer directly?** Yes: explicitly request Review or formal proof work. That delivery will not count as your independent completion of a coaching stage.

## Repository and maintenance

```text
README.md / README.zh-CN.md  Complete English and Chinese entrypoints
claim/                      Independently installable skill
  SKILL.md                  Mode routing and shared rules
  references/               Coaching, review, archive, and proof protocols
  scripts/claim.py           CLI
  assets/proof-demo/         Minimal Lean example
docs/                       Focused guides and validation records
tools/                      Validation and packaging
tests/                      Regressions and Windows encoding checks
dist/                       Installable ZIPs and checksums
```

Run maintenance checks from the repository root:

```bash
python -B tools/validate.py
python -B -m unittest discover -s tests -v
python -B tools/package.py --check
python -B tools/validate.py --installed /path/to/skills/claim
```

Rebuild with `python -B tools/package.py --write`. Check sources first, then compare the ZIP and installed copies; a file's existence is not a completed verification.

The focused guides below are currently in Chinese; both READMEs contain the complete getting-started instructions.

[User guide](docs/guide.md) · [CLI details](docs/cli.md) · [Advanced example](docs/examples.md) · [Proof workflow](docs/proof-workflow.md) · [Design references](docs/design-notes.md) · [Validation](docs/validation.md) · [Changelog](docs/changelog.md)
