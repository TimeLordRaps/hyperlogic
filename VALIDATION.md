# Local validation receipt

Date: 2026-09-20. Status: the L0 triangle is validated for the bounded claims
below. One of the layer's five graduation criteria is discharged. The other four,
including the one on which the existence of this repository depends, are open and
are **not** validated by anything in this receipt.

This is the repository's first receipt.

## Coordinates

- Repository `hyperlogic`, branch `main`, private repository
  `TimeLordRaps/hyperlogic`. The validated bytes were committed and pushed
  unchanged. Publication records where they live; it is not an additional check.
- Python 3.12.8 on Windows, pytest 9.1.1, ruff 0.16.8, in a repository-local
  `.venv`. These are the same tool versions the `hyperethics` receipt of the
  same date records, so the two receipts are comparable.
- **No runtime dependencies.** The package imports only the standard library, so
  there are no dependency pins to record and no dependency source to trust. This
  is a design commitment stated in `DESIGN.md`, not an incidental fact.
- **No citation of another field is imported.** `L0_triangle.hm` cites hypermath
  by file, section and line in three places, and imports nothing from it. That
  asymmetry is deliberate and is argued in `nd-import-hypermath`: an import would
  make the dependency cyclic. **Nothing was read from, written to, or removed
  from the `hypermath` repository during this work.** `nd-the-gate` requires
  that, and it is recorded here because "we did not touch it" is a checkable
  claim about this session and "we will not touch it" is not.
- The implementation and tests are byte-bound in
  [`validation/source-manifest.json`](validation/source-manifest.json). The
  digest of its canonical `files` mapping is
  `79dc946b857d0095b818d7ce1998e1e5b8883c5563b442991f6be38615c24db4`.
  The manifest identifies tested bytes; it does not sign or certify them.

## Observed checks

```console
python -m pytest tests
python -m ruff check src tests
python -m hyperlogic
```

- **64 passed, zero skips, one run.** The package has no optional import and no
  conditional path, so there is no second configuration to report.
- Lint passed with no findings.
- The executable report exits zero and reports its open obligations as `OPEN`,
  `NOT_ESTABLISHED`, or `NOT_ATTEMPTED`. Tests assert that it never upgrades one
  of these, that it never asserts a checked claim was proved or is valid, and
  that it never claims this layer is a logic.
- **Axiom independence is established conclusively.** Four finite structures,
  each satisfying exactly three axioms and failing the fourth. One countermodel
  settles the independence of one axiom, so this result does not depend on the
  number of confirming models.
- **Three universal claims are refuted conclusively**, each by a structure
  satisfying all four axioms:
  1. that every sign returns after one turn — `minimal`, witness `matter`;
  2. that two turns suffice for a circuit — `minimal`, witness `closure`;
  3. that plurality follows from the axioms alone — `collapsed`, witness
     `closure`.
- **GC-1 is discharged.** All three opaque predicates of Section II are closed in
  Section VI of the same file, and each close is checked against every structure
  rather than asserted in prose.
- **One declared Section V property is witnessed by a structure built for it.**
  `separating` holds `same-conclusion` between `matter` and `echo` while they are
  not `interderivable`. The minimal circuit cannot witness this, because there
  the two relations have the same extension; a test records that limitation
  explicitly so it stays visible.

## What the checks do not establish

- **Nothing here is proved.** Every `HOLDS_IN_MODEL` outcome was checked against
  finite structures. Only the refutations and the independence result are
  conclusive, because a single countermodel settles a universal claim and no
  number of confirming models settles one. There is no proof-assistant theorem
  and no adequacy proof for this layer.
- **GC-2 is untouched by every check above.** No test, and nothing in the report,
  bears on whether `Sign` and `Claim` are independent of hypermath's `Form` and
  `Prop`. The package could pass all 64 tests and still be hypermath Section VIII
  with new spelling, in which case the correct outcome is to archive this
  repository with that result recorded. `nd-shape-is-not-content` states that the
  shared axiom shape, the five derives, the plurality result and the
  opaque-then-close method are a **method being reused** and are not evidence of
  independent content.
- **GC-3 is untouched.** No check bears on whether three registers are the right
  number. A fourth register would change `ax-triangle`'s period and disturb
  nothing else in the file.
- **GC-4 was not attempted.** hypermath's seven executive opaques — syntax,
  substance, semantics, derives, discharge, definition, form-closure — are not
  closed here and no attempt to close them exists.
- **GC-5 is not resolved.** Sections V and VI declare each relation from an
  opaque predicate and close that predicate as the relation. Read as a reduction
  this is circular; it is intended as a fixed point, and this receipt does not
  establish that the fixed point is well-founded. hypermath uses the same
  construction and does not settle it either, so this is a shared open problem
  rather than a defect introduced here.
- **The layer is not a logic and no check pretends otherwise.** There is no
  connective, no quantifier, no inference rule and no proof object in the
  package. "That this layer is a logic" is carried as a standing open obligation
  with status `NOT_ESTABLISHED`, and a test asserts it stays there.
- **The three-instance record is a citation, not a verification.** The file and
  line pointers in `L0_triangle.hm` to `hypermath`, `metamathethicology` and
  `grounded-hypercalculi` were read at the time of writing and are not
  cross-checked by any test in this repository, because doing so would require
  importing or vendoring those packages. If those files move, the pointers go
  stale silently. This is a known weakness of the record and is stated rather
  than mitigated.

## Exclusions

- No Lean 4 translation exists for this layer. The other packages in the family
  carry Track 2 as a standing obligation and this one joins them at the back of
  that queue, behind GC-2.
- No L1 exists. Filtration between the three relation strengths is L1 content and
  is not written.
- No performance, concurrency, or scale claim is made or checked. Every structure
  in the package has at most four elements.
- No packaging artifact was built or published. `pyproject.toml` is present and
  lint-clean; `python -m build` was not run and nothing was uploaded anywhere.

## Environment note

The checks were run on Windows with the repository-local `.venv`, which is
excluded from version control by `.gitignore`. A reader reproducing this receipt
should create a fresh environment from the `dev` extra rather than expect the
one used here to be present.
