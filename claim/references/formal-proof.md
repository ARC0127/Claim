# From an agreed obligation to a checked proof

Use for an explicit request to formalize or check a stable obligation. During
coaching, do not activate this route before the user's S5a/S5b attempts or silently
turn S7 export into a proof project. The user must request the separate proof work.
Apply the entrypoint's fresh-search and symbol-explanation rules.

## Keep the statement, proof and application connected

1. Record the user's current claim version and exact obligation. Map its objects,
   domains, quantifiers, comparison and assumptions into Lean definitions. Explain
   every symbol in the user's language. A formal statement is a translation to
   review, not permission to weaken the original goal.
2. Sketch the mathematical argument and isolate the first open lemma. Separate
   definitions, assumptions, proved lemmas, and open goals. Do not accept a premise
   that simply grants the desired result without saying what remains to prove.
3. Work in an explicitly pinned Lean/Mathlib environment, using small imports.
   Read its lean-toolchain, lakefile and dependency lock before proposing commands.
   Separate target sketches from submitted solutions so a solution cannot import
   its own unproved target. Keep source changes and the actual compiler output.
4. Compile the solution and inspect the exact theorem type and its transitive
   axioms with `#print axioms Qualified.theoremName`. Record the exit status,
   toolchain, source revision and output. A successful build alone is insufficient
   when the statement or dependencies contain placeholders or added axioms.
5. Review semantic correspondence again: did the formal theorem establish the
   requested statement, a finite restriction, or only an assumed bridge? Then map
   each mathematical premise to the actual algorithm or evidence if that is part
   of the user's request. Compilation does not test deployment conditions.

Lean's standard logical axioms are `propext`, `Classical.choice`, and `Quot.sound`.
Report the actual list. `sorryAx` means an incomplete proof; custom or native
evaluation axioms require explicit review, not automatic acceptance. Do not claim
adversarial proof validation merely from a local build and printed axioms; stronger
checking should follow the current Lean validation documentation.

## Lean 4 and Prove2Me have different jobs

Lean checks the formal terms. Prove2Me optionally organizes exact target statements,
child obligations, submissions and verification results. Use its current official
workspace/protocol rather than inventing API fields or copying a private adapter.

For a Prove2Me target, match its formal statement and environment, not just its
title. Keep the returned submission identifier and actual verdict. `PENDING`
means waiting; `SKETCH_ACCEPTED` is a reduction with open dependencies, not a
completed proof. Even `ACCEPTED` applies to the target checked by the platform,
not automatically to the original research claim or a working implementation.

For a dependency diagram, label provenance of each edge:

- compiler-extracted theorem/type dependencies;
- proposed mathematical decomposition not yet proved;
- implementation or empirical evidence links, which are not logical implications.

Display unresolved child goals and local/platform disagreement. A drawn arrow,
manually entered status or numerical test must not be presented as kernel evidence.
Keep natural-language explanation alongside formal code: state the proof idea,
why each lemma is needed, and what the final result does and does not cover.

Local formalization does not need a platform account. Only send sources to a hosted
service when the user authorizes that destination and content; adding this route
does not initiate uploads or read credentials. Use current service documentation
for submission, not a permanent hardcoded toolchain or endpoint assumption.

## Deliverable

Give the exact obligation and translation, Lean files, a scoped proof/dependency
map when useful, actual build/axiom output, and remaining application conditions.
Distinguish `FORMAL_TARGET`, `PROOF_INCOMPLETE`, `KERNEL_CHECKED_WITH_RECORDED_AXIOMS`,
and `IMPLEMENTATION_BINDING_UNCHECKED` as needed; these are separate axes, not a
single progress score. If Lean is unavailable, provide the target and runnable
check instructions but leave execution explicitly untested.

## Primary references

- Lean Team, *Validating a Lean Proof*, sections on printing axioms and rechecking:
  https://lean-lang.org/doc/reference/latest/ValidatingProofs/ (checked 2026-09-17).
- Lean Team, *Axioms*: https://lean-lang.org/doc/reference/latest/Axioms/
  (checked 2026-09-17).
- Prove2Me maintainers, *Prove: Submit Proofs, Disproofs, and Reductions*:
  https://github.com/prove2me/prove2me_workspace/blob/main/references/prove.md
  (checked 2026-09-17; verify current target environment and status semantics).
