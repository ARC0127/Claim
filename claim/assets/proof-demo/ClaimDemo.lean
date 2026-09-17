import Init

/- An elementary arithmetic example, independent of any research project.
left and right are natural numbers. leftWitness and rightWitness are their
half-values. left_even and right_even assert the corresponding equalities.
The existential witness halfSum certifies that the sum is also even.
-/
theorem ClaimDemo.even_add_even
    (left right leftWitness rightWitness : Nat)
    (left_even : left = 2 * leftWitness)
    (right_even : right = 2 * rightWitness) :
    ∃ halfSum : Nat, left + right = 2 * halfSum := by
  refine ⟨leftWitness + rightWitness, ?_⟩
  rw [left_even, right_even, Nat.mul_add]

#print ClaimDemo.even_add_even
#print axioms ClaimDemo.even_add_even
