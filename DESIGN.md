# Architecture and research ancestry

This document records why the package is shaped the way it is, including the
decisions that could have gone the other way and the one that the package is
betting on.

## Position in the stack

The family divides on a naming rule that is load-bearing rather than cosmetic:

- **No `grounded-` prefix** — the field is self-grounding. It states its own
  ground inside itself and imports nothing to do it. `hypermath`,
  `hyperphysics`, `hyperethics`, and now `hyperlogic`.
- **A `grounded-` prefix** — the field is grounded *in another*, and its ground
  arrives by import. `grounded-hyperset-theory`, `grounded-hypercalculi`.
  `ordinatics` belongs to this group by structure and not yet by name.

Dependencies run inward and never outward. A foundation imports nothing; a
grounded package imports foundations. This is the Acyclic Dependencies
Principle, and here it is not a style preference — it is what decides this
package's existence, because a `grounded-hyperlogic` is impossible under it.

```
hypermath          hyperphysics       hyperethics        hyperlogic
(self-grounding)   (mirror)           (shadow)           (this package)
      |                  |                  |
      +------------------+------------------+
                         |
        grounded-hyperset-theory, grounded-hypercalculi,
        ordinatics, metamathethicology
```

`hyperlogic` sits beside the other three foundations and under nothing. It has
no arrows out.

## Why the foundation carries no dependency

The package imports only the standard library. No proof assistant, no ordinal
notation, no sibling package. This is a design commitment rather than an
incidental fact: **a foundation that needs another package in order to state its
own ground is not a foundation.** The same commitment is stated in
`hyperethics/DESIGN.md` and holds here for the same reason.

It has a sharper consequence in this package than in the others. hyperlogic is
*about* the metalanguage that hypermath uses to state hypermath. If it imported
hypermath to say so, the dependency would run hyperlogic → hypermath →
hyperlogic, and the family's acyclic constraint would be violated at its base.
`nd-import-hypermath` sets the four steps out in full. The package therefore
**cites** hypermath — by file, section and line — and imports nothing from it.
Citation without import is what the three-instance record in `L0_triangle.hm`
does, and it is the only relationship to hypermath this package has.

## Why one operation

`turn` is the only primitive operation, and the circuit is its only structure.
Each additional primitive would be an additional thing to justify at the ground,
and a ground with four operations is four grounds. The three registers — shape,
matter, reading — are *positions* in the circuit rather than operations on it.
Whether three is the right number is GC-3 and is open; a fourth register would
change `ax-triangle`'s period without disturbing anything else here, which is
itself the evidence that the number is not yet doing derivational work.

## Why the period is three

This is the one structural place the layer differs from hypermath. hypermath's
`ax-box` closes an orbit at **two** steps: `□□x` relates back to `x`. Here
`ax-triangle` closes at **three**.

The difference is checkable rather than declared. `two_turn_return` fails in a
structure that satisfies all four axioms, so the two-step reading is refuted
outright rather than merely unsupported. That refutation is the executable
content of the claim that the triangle has three edges, and without it the
period would be decoration.

## Operation and ground

The ground is `ax-triangle`, and its content is that **a cycle needs no
exterior**. This is the self-grounding move, and it is the direct structural
analogue of what the other two foundations do:

| Field | Self-grounding move |
|---|---|
| hypermath | `ax-ground-self`: the ground operation applies to itself |
| hyperethics | `ax-archetype-self`: the creator is within what it creates |
| hyperlogic | `ax-triangle`: the circuit closes on itself |

`ax-closure-self` is deliberately **minimal** and is not a second ground. It says
the closure already returns after one turn. It does **not** say the closure made
itself, produced itself, or is prior to anything. The stronger reading is
available and is not taken, for the same reason hyperethics' `ax-archetype-self`
is kept minimal: a self-production claim would need a notion of production the
layer does not have.

`without_closure_self` shows the axiom is not redundant. The three-step circuit
still closes for every sign when the closure's one-turn return is removed,
because the other three axioms are universally quantified and say nothing that
singles out the irreducible.

## The epistemic contract, enforced by types

`Verdict` has no truth value. `__bool__` raises `TypeError`, so `if verdict:` is
a crash rather than a silent narrowing. This is enforced in the type because the
distinction it protects — *checked against one finite structure* versus
*established* — is exactly the distinction a boolean erases, and exactly the one
a reader of a foundations repository most needs kept.

Three consequences follow in the code:

- A `HOLDS_IN_MODEL` verdict may not name a witness. A success has no
  distinguished witness, and inventing one would overstate what was checked.
- A `FAILS_IN_MODEL` verdict must name one.
- `refuted_by` raises `NotAModel` when the structure fails an axiom. A failure
  inside a non-model shows nothing about the theory, and returning a softer
  result would let it look like it did.

## What is deliberately absent

**Any logic.** No connective, no quantifier, no inference rule, no proof object,
no consequence relation, no soundness or completeness statement. The package
name invites all of these and the package supplies none of them. `report.py`
carries "That this layer is a logic" as a standing open obligation with status
`NOT_ESTABLISHED`, and a test asserts it stays there.

**Filtration between the three relations.** Section V declares the relations in
strictly increasing strength and stops. How a claim moves between strengths is L1
content and is not in this layer.

**Anything carved out of hypermath.** See `nd-the-gate`. hypermath Section VIII
and `L1_relations.hm` Section IV are untouched, and this package is written
beside them rather than extracted from them.

## The principal open problem

**GC-2: that this layer is independent of hypermath L0.**

The honest statement of the risk: `Sign` may be `Form` with a different name and
`Claim` may be `Prop` with a different name. The three-plus-one axiom shape, the
five derives, the plurality result, and the opaque-then-close method are all
shared with hypermath L0, and `nd-shape-is-not-content` records that this
resemblance is a method being reused rather than a result.

No argument for independence is offered anywhere in this repository. If the
triangle turns out to need a `Form`-like carrier in order to be stated at all,
then this is hypermath Section VIII with new spelling, and the correct outcome is
to **archive this repository with that result recorded** rather than keep it. A
foundations repository that could not reach that verdict about itself would not
be worth trusting about anything else.

GC-5 is a second open problem and a shared one: Sections V and VI declare each
relation from an opaque predicate and then close that predicate as the relation.
Read as a reduction this is circular; it is intended as a fixed point, and
whether that fixed point is well-founded is not settled here or in hypermath.

## Next obligations, in order

1. **GC-2.** Attempt an independence argument, and be willing to reach the
   negative result. Everything else is contingent on this.
2. **GC-4.** Close hypermath's seven executive opaques — syntax, substance,
   semantics, derives, discharge, definition, form-closure — using the three
   relations. This is the eventual purpose of the field and the gate's condition.
3. **The gate.** Only once GC-1 and GC-4 are both discharged does anything move
   out of hypermath, and the move is then a deletion from hypermath paired with
   a citation, not a copy.
4. **L1.** Filtration between the three relation strengths.
5. **Lean 4.** A translation plus an audit that publishes its own open
   obligations, with admissions and assumptions counted rather than hidden, as
   the other packages in the family do.
