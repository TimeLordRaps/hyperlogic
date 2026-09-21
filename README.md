# Hyperlogic

A **self-grounded triangle** of shape, matter and reading, derived from one
primitive operation. Foundational rather than grounded: the name carries no
`grounded-` prefix because nothing outside this repository supplies its ground,
and — as the argument below shows — nothing outside it *could*.

Where [hypermath](https://github.com/TimeLordRaps/hypermath) derives a formal
universe from `□` under application and
[hyperethics](https://github.com/TimeLordRaps/hyperethics) derives normative
structure from `create` under immanence, hyperlogic derives a derivation
structure from `turn` under circuit closure.

One layer is implemented: **L0 triangle**. One of its five graduation criteria is
discharged.

> **This is not a logic, and this package does not claim to be one.** There is no
> connective, no quantifier, no inference rule and no proof object anywhere in
> it. What is established is narrower and worth stating exactly: a cycle of three
> registers with a distinguished fixed point, whose three structural predicates
> are closed in the same file that declares them.

## Why this field exists

Not as a taxonomy exercise. The derivation relation — what it means for one thing
to follow from another — is currently written out **three separate times** in
this family, because there was no field to cite:

| Where | What |
|---|---|
| [`hypermath/L0_ground.hm`](https://github.com/TimeLordRaps/hypermath) §VIII | seven executive opaques: syntax, substance, semantics, derives, discharge, definition, form-closure |
| `metamathethicology/src/metamathethicology/spaces.py:283` | `Domain.METALOGIC`, the `derivable-in` relation emitted by `reflect()` |
| `grounded-hypercalculi/src/grounded_hypercalculi/language_calculus.py:151` | `MetamathDatabase`, with `verify_proof`, `_modus_ponens`, `is_derivable` |

Three independent instances of one concept is the Rule of Three threshold, and
the same knowledge living in three places is the thing DRY is actually about.
That is the case for a field. It is not yet a case that the field is
*independent*, which is GC-2 below and is open.

## Why there is no `grounded-hyperlogic`

The dependency would be a cycle, and the argument is structural rather than
stylistic. It is stated in full as `nd-import-hypermath` in
[`L0_triangle.hm`](L0_triangle.hm):

1. hypermath `L0_ground.hm` Sections I–VII are written in a metalanguage —
   `derive`, `close`, `axiom`, `discharge`, `graduation`.
2. hypermath's own Section VIII header states that those words "appear
   constantly but were never defined as formal L0 objects", and Section VIII
   exists to define them.
3. So the metalanguage is needed by hypermath *in order to state hypermath*.
4. If this package imported hypermath, the dependency would run
   hyperlogic → hypermath → hyperlogic.

Under the acyclic dependency constraint the family already follows — foundations
import nothing, grounded packages import inward — there is no
`grounded-hyperlogic`. Either this is a foundation with its own ground, or the
material stays inside hypermath. This repository takes the first option.

**Nothing has moved out of hypermath, and nothing will yet.** `nd-the-gate`
holds that hypermath Section VIII stays exactly where it is, unmodified, until
GC-4 is discharged. A foundation that removed another foundation's metalanguage
before it could supply a replacement would break the base field of the family to
make a point about layering.

## The ground

The irreducible is **`closure`**: the sign whose shape, matter and reading
coincide. The sole operation is **`turn`**, which advances a sign one edge around
the circuit

```
shape  ->  matter  ->  reading  ->  shape
```

and the self-grounding axiom is `ax-triangle`: **three turns are a circuit**. A
cycle needs no exterior. That is the whole of the ground, and it is the one
structural place this layer differs from hypermath, whose `ax-box` closes an
orbit at **two** steps. The difference is not cosmetic — a structure satisfying
all four axioms here fails a two-step return, and that failure is checkable.

Four axioms, three of them universally quantified and one naming the irreducible:

| Axiom | Content |
|---|---|
| `ax-advance` | turning moves a sign past where it was |
| `ax-stay` | turning stays inside what is derivable from the closure |
| `ax-triangle` | **the self-grounding axiom.** three turns return |
| `ax-closure-self` | the closure already returns after one turn |

## What is actually established

**Conclusively** — one countermodel settles a universal claim, and no number of
confirming models settles one:

- **Axiom independence.** Four finite structures, each satisfying exactly three
  axioms and failing the fourth.
- **Three refutations.** That every sign returns after one turn (false: the
  closure's privilege is not general); that two turns suffice for a circuit
  (false: the period is three); and that plurality follows from the axioms alone
  (false: the collapsed one-sign structure models every axiom).
- **One declared strictness, witnessed.** Section V declares that
  `same-conclusion` does not imply `interderivable`. In the minimal circuit the
  two relations have the same extension, so a fourth structure exists purely to
  witness the strictness. A declared property with no structure exhibiting it is
  a claim, not a check.

**Checked, not proved** — everything shown as `HOLDS_IN_MODEL` was checked
against finite structures and is not thereby valid. There is no proof-assistant
theorem and no adequacy proof for this layer.

The third refutation is worth reading carefully, because it looks like a
contradiction and is not. `d-two-signs` is a `FORM` derive of Section IV, and it
rests on the **Section VI close** of `log-advances`, not on the axioms alone. The
collapsed structure satisfies every axiom and violates that close.
`nd-two-signs-from-axioms-alone` records this so that a reader who took the
derive as a consequence of Section III would be corrected by the file rather than
left wrong. hypermath's `two-members-in-class` has the same dependence on
`struct-distinct` closing to not-`==`.

## GC-1, and why it is stated first

> **GC-1:** this layer closes its own three opaque predicates, in this file,
> rather than deferring them. **DISCHARGED** — Section VI, three closes, all
> `FORM`.

This is the bar hypermath L0 meets at its Section VI and the bar hyperethics L0
does not: hyperethics deferred its three to L1, and `L1_will.hm` GC-3 records
that L1 closed none of them and added a fourth. GC-1 is stated first because it
is the criterion that decides whether this is a foundation or a layer of
something else.

The other four are open, and `python -m hyperlogic` prints them every run.

## Try it

```bash
python -m hyperlogic
```

```console
CONCLUSIVE REFUTATIONS -- one countermodel settles a universal claim
------------------------------------------------------------------------
  REFUTED: every sign returns after one turn is not a consequence of the L0 axioms.
  REFUTED: two turns suffice for a circuit is not a consequence of the L0 axioms.
  REFUTED: the carrier has at least two members, from the axioms alone ...
```

```python
from hyperlogic import minimal_model, shares_context, interderivable

model = minimal_model()
turned = model.turn("closure")

shares_context(model, turned, "closure")   # True
interderivable(model, turned, "closure")   # False
# That gap is where every nontrivial derivation lives.
```

## The epistemic contract

`Verdict` deliberately has **no truth value**. `if verdict:` raises, because the
interesting distinction is between *checked here* and *established*, and a
boolean erases exactly that distinction. A `FAILS_IN_MODEL` verdict is a
refutation only when the structure satisfies every axiom; `refuted_by` raises
`NotAModel` rather than returning a softer result when it does not.

## Open obligations

| | |
|---|---|
| **GC-2** independence from hypermath L0 | **OPEN.** That `Sign` and `Claim` are not `Form` and `Prop` respelled. No argument for it is offered anywhere in this repository. If the triangle turns out to need a `Form`-like carrier in order to be stated at all, this is hypermath Section VIII with new spelling, and this repository should be **archived with that result recorded** rather than kept. |
| **GC-3** three registers rather than four | NOT_ESTABLISHED. A fourth register would change the period without disturbing anything else here, which is itself a sign the number does no derivational work yet. |
| **GC-4** closing hypermath's seven executive opaques | NOT_ATTEMPTED. The eventual purpose of the field, deliberately not claimed at L0. The gate depends on it. |
| **GC-5** the declare-from / close-as fixed point | OPEN. Sections V and VI declare each relation from an opaque predicate and close that predicate as the relation. Inherited as a shared open problem with hypermath, which uses the same construction and does not settle it either. |

`nd-shape-is-not-content` records one more thing, in the file rather than only
here: the three-plus-one axiom shape, the five derives, the plurality result and
the opaque-then-close method are all shared with hypermath L0. That resemblance
is a **method being reused** and is not evidence that this layer says anything
new. Whether the content is independent is GC-2, and GC-2 is open.

## Preprint

There is none, and none is drafted. This is recorded rather than left to
inference: GC-2 is what a manuscript would have to settle, and if it
resolves against this layer the right outcome is an archived repository,
not a paper.

## License

Apache-2.0. See [LICENSE](LICENSE).
