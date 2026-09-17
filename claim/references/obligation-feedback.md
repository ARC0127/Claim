# Feedback on a user's proof obligation

Use at S5a after reading the coaching protocol. The user attempts the bridge first. This reference supplies diagnostic questions for the tutor, not a list of answers to reveal. It also supports review when the user explicitly requests a completed analysis.

## Compare the needed result with the proposed result

Read the confirmed claim and assumptions, then the user's exact obligation. Compare their meanings, not their vocabulary. In coaching, inspect all relevant dimensions but discuss only the mismatch that most directly blocks the next inference.

| Dimension | What to inspect | Why a mismatch matters |
|---|---|---|
| Input | What is given: data, access, estimates, premises, resources | An oracle quantity is not automatically available to the proposed method |
| Output | The quantity or relation the result would establish | Bounding a surrogate does not establish the paper's outcome without a bridge |
| Domain | Which objects, actions, populations or distributions are covered | A result outside the declared domain cannot support the claim inside it |
| Quantifier | Fixed object, all objects at once, average, or high probability; order of choices | A guarantee for a fixed choice may not survive selection using the same data |
| Comparator | What baseline or ideal is being compared, under which budget | “Better” can change meaning when either comparator or budget changes |
| Error | Which discrepancy is controlled, in what units, and where it enters | Small error is useful only when connected to the required conclusion |
| Regime | Exact, oracle, asymptotic, or finite sample; randomness if any | A limit statement alone gives no bound for the experiment's finite data |

Do not demand a statistical rate for a deterministic exact statement. An error-free claim may need an exact relation; record “not applicable: exact statement,” not an arbitrary epsilon. A finite-sample obligation must actually concern finite observations. Definitions and premise dependencies must remain visible.

## Give feedback that teaches one judgment

Within the four coaching sections:

1. Identify the useful part of the user's attempt in neutral language.
2. Locate the single mismatch in the user's own words. Describe what their proposed result would establish, then the conclusion still unsupported. Do not add a complete corrected statement.
3. Explain the inferential consequence using the current objects. If an example helps, vary only the relevant feature and do not reveal a next-stage assumption or theory category.
4. Ask the user to revise that one component. Keep the original attempt and subsequent revision separately in the record.

Prefer “your bound concerns one choice fixed before observing data; your procedure chooses after observing data” over “quantifier wrong.” A syntactically complete statement can still be circular, unrelated to the target, or as hard as the original claim. Explain which one applies. Do not reject a useful intermediate bridge merely because further bridges remain; identify precisely the arrow it closes and the unresolved next arrow without completing it.

## Common mismatches — tutor-side diagnostic notes

These are not assumptions, theorem recommendations, or a menu to print before the user's attempt.

- **Average to every instance:** the proposed average can conceal failures on individual objects. Identify whether the paper actually claims individual or average performance.
- **Estimate to decision:** accurate estimation and the quality of a selected decision are different conclusions. Check the rule that turns estimates into a decision before asserting an implication.
- **Pointwise to selected:** identify when and from what data the object is selected. Do not silently replace pointwise control with uniform control; let the user identify the needed coverage.
- **Limit to fixed data:** ask what statement would address the stated finite data budget. Do not insert a rate.
- **Observed to intervention:** check whether the premise describes what was observed or what would happen after an intervention. Do not invent an identification assumption.
- **One-step to repeated use:** check whether errors or conditions remain controlled when the operation is repeated. Do not nominate stability conditions in advance.
- **Sufficient to necessary:** a construction that works under a condition need not show that no alternative works without it.

If several mismatches exist, choose the earliest one needed to interpret the bridge; keep the others for subsequent turns. A label is not a verdict and finding a standard theorem with similar terminology is not an applicability check.

## Support without taking authorship

If the user is stuck, first point to the missing relationship. After an unsuccessful attempt, a requested neutral analogy may illustrate the relationship without supplying the target statement. If the user asks the tutor to write the full obligation, explain the explicit switch to review; do not silently award an independently authored S5a pass. An AI-written statement later accepted by the user remains AI-authored. A user revision after scaffolding can satisfy the learning task, with support recorded.

Pass S5a when the user's input-output statement plausibly addresses the named arrow, the relevant quantifiers and regime are explicit, and no known mismatch is concealed. Record it as a **proof target**. This does not mean a proof has been found, the premises are true, or the full paper claim follows.
