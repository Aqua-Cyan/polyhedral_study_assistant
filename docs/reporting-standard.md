# Reporting Standard

This document defines the required format for research reports produced by the polyhedral study assistant.

The main report must be organized by **symbolic inequality families**, not by individual computational instances.

Computed facets are evidence. They are not the final mathematical output.

A report is considered incomplete if it only lists cddlib/PORTA facets without attempting to:

1. identify source constraints;
2. derive concrete facets using documented c-MIR patterns;
3. generalize successful derivations into symbolic families;
4. validate candidate families by exact matching and finite feasible-point checks;
5. clearly separate derived families, candidate families, invalidated candidates, and unresolved facets.

---

## 1. Required report philosophy

The report must support the following discovery loop:

```text
computed cdd facets
  ↓
facet normalization
  ↓
source-constraint identification
  ↓
concrete c-MIR derivation attempts
  ↓
candidate family proposal
  ↓
Gate 1: instantiation matching
  ↓
Gate 2: finite validity check
  ↓
Gate 3: derivation certificate check
  ↓
family-first report
  ↓
refinement loop if unresolved or invalidated candidates remain
```

Do not write a report as if the first proposed symbolic family is correct.

A symbolic family must pass validation gates before it can be reported as derived or proved valid.

---

## 2. Required report sections

Use the following top-level sections unless the user explicitly requests another format.

```markdown
# <Model or Study Name> convex-hull study report

## Scope and limitations

## Model and assumptions

## Computational setup

## Derived or proved symbolic inequality families

## Candidate symbolic inequality families

## Invalidated candidate families

## Coverage of computed facets

## Derivation attempts for not-yet-covered facets

## Unresolved computed facets

## Proof obligations

## Next refinement loop

## Appendix: computational evidence
```

The appendix is optional. If included, it may contain raw instance-level output, but the main body must remain family-first.

---

## 3. Scope and limitations

The report must begin by stating what is and is not being claimed.

Include:

* computational backend used;
* instance range tested;
* whether equations returned by the backend are handled;
* whether all computed facets were covered;
* whether any candidate families remain unproved;
* whether a complete hull description is claimed.

Use language such as:

```markdown
This report uses computed small-instance facets as evidence for symbolic inequality families.

No complete convex-hull description is claimed unless a reverse-inclusion proof is provided.

A family is reported as derived/proved only if it has passed exact matching, finite validity checking, and derivation-certificate checking.
```

Never imply that small-instance coverage is a proof of the full convex hull.

---

## 4. Model and assumptions

State the model in the user's original notation.

Include:

* variables;
* domains;
* index sets;
* parameters;
* feasibility assumptions;
* whether index sets may overlap;
* any internal decompositions used for analysis.

If internal decompositions are introduced, such as

[
J_1\setminus J_2,\qquad J_2\setminus J_1,\qquad J_1\cap J_2,
]

make clear that they are analysis devices. Final families should also be expressible in the original notation.

---

## 5. Computational setup

Record enough information for reproducibility.

Include:

* backend, e.g. pycddlib;
* point-generation method;
* tested instance range;
* random seed, if used;
* command used to generate the report;
* generated artifacts;
* limitations.

Example:

```markdown
The study enumerates feasible 0-1 points and computes the H-representation of their convex hull using pycddlib.

The tested instances include all admissible parameter choices with \(|J_1\cup J_2|\le 5\), plus selected boundary cases.

The backend currently reports inequalities. If equations occur, they must be recorded or reported as a limitation.
```

---

## 6. Derived or proved symbolic inequality families

Only include a family in this section if it has passed all three gates:

1. exact instantiation matching when claiming coverage;
2. finite validity check on enumerated feasible integer points;
3. derivation certificate using documented patterns.

For each derived family, include the following subsections.

```markdown
### Family name

#### Symbolic statement

#### Parameter conditions

#### Derivation certificate

#### Gate status

#### Covered computed facets

#### Validity, facetness, and completeness status

#### Notes
```

### 6.1 Symbolic statement

State the family in general notation.

Example:

[
x(D)\ge (b-|J\setminus D|)y,
\qquad
D\subseteq J,\quad b-|J\setminus D|>0.
]

### 6.2 Parameter conditions

State all required conditions.

Examples:

* (D\subseteq J);
* (b-|J\setminus D|>0);
* (1\le b\le |J|);
* (J_1\subseteq J_2);
* (D) must satisfy a minimality condition.

### 6.3 Derivation certificate

Give an explicit derivation.

The certificate must identify:

* source constraints;
* bounds used;
* aggregation multipliers;
* c-MIR or MIR step, if any;
* coefficient tightening step, if any;
* mixed-MIR data, if any;
* final symbolic inequality.

For residual inequalities, record:

```markdown
Source:
\[
x(J)\ge by.
\]

Let \(E=J\setminus D\). Since \(x(E)\le |E|\),

\[
x(D)+x(E)\ge by
\]

implies

\[
x(D)\ge (b-|E|)y.
\]
```

For mixed MIR, record:

* base inequalities (f^i(x)+Bg^i(x)\ge \pi_i);
* (f^i(x)\ge0);
* (g^i(x)\in\mathbb Z);
* (B,\pi_i,\tau_i,\gamma_i);
* ordering by (\gamma_i);
* common (\bar f);
* unsimplified mixed-MIR inequality;
* final simplified inequality.

Do not call ordinary addition of constraints mixed MIR.

### 6.4 Gate status

Report the three gates explicitly:

```markdown
- Gate 1, exact matching: passed / failed / not applicable
- Gate 2, finite validity: passed / failed / not checked
- Gate 3, derivation certificate: passed / incomplete / missing
```

A derived family must not have Gate 3 marked missing.

### 6.5 Covered computed facets

Only list a computed facet as covered if exact instantiation matching has been performed.

Coverage must be based on:

```text
symbolic family + concrete parameters
→ instantiated inequality
→ normalized inequality
→ exact equality with normalized cdd facet
```

Do not list a facet as covered based on visual similarity.

Each coverage item should include:

* source instance or instance class;
* family parameter values;
* instantiated inequality;
* normalized cdd facet;
* equality check result.

---

## 7. Candidate symbolic inequality families

Use this section for promising families that are not yet proved or derived.

A family belongs here if:

* it matches some computed facets but lacks a derivation certificate;
* it is valid on tested points but lacks a proof;
* it is a broad conjecture that still needs refinement;
* it is suggested by repeated facet patterns but is not yet certified.

For each candidate family, include:

```markdown
### Candidate family name

#### Candidate statement

#### Why it is plausible

#### Gate status

#### Evidence

#### Why it is not derived yet

#### Next actions
```

The candidate status must clearly say one of:

* `finite-valid but underived`;
* `partially matched`;
* `matched on some instances only`;
* `awaiting c-MIR derivation`;
* `needs refined parameter conditions`.

A candidate family must not be described as valid unless it has a proof.

---

## 8. Invalidated candidate families

Use this section for families rejected by finite feasible-point checking or exact matching failure.

Invalidated candidates are valuable. They show which guessed conditions were too broad.

For each invalidated family, include:

```markdown
### Invalidated family name

#### Invalidated statement

#### Reason for invalidation

#### Counterexample

#### Suggested refinement direction
```

Each counterexample must include:

* tested instance;
* family parameters;
* instantiated inequality;
* feasible point;
* violation value or violated side.

Example:

```markdown
Candidate:
\[
x(S)\ge r_1(S)y_1+r_2(S)y_2.
\]

Counterexample:
- instance: ...
- parameter: \(S=...\)
- inequality: ...
- feasible point: ...
- violation: ...
```

Do not delete invalidated candidates from the report. Use them to guide the next refinement loop.

---

## 9. Coverage of computed facets

This section should be compact and machine-checkable.

Use a table such as:

```markdown
| family | status | covered facets | tested instances | exact matching | notes |
| --- | --- | ---: | --- | --- | --- |
| residual family | derived | 245 | all small instances | passed | ... |
| interaction candidate | candidate | 12 | nested cases | partial | derivation missing |
```

Coverage counts must be generated from exact normalized matching, not from prose.

If any facet is counted as covered, the family instantiation that produced it must be recoverable.

---

## 10. Derivation attempts for not-yet-covered facets

Before a facet can be unresolved, the report must show attempted derivations.

For each target facet, include:

```markdown
### Target facet

- normalized facet:
- original notation:
- source constraints considered:
- support overlap:
- attempted patterns:
  - residual:
  - coefficient tightening:
  - aggregation + c-MIR:
  - mixed MIR:
  - MIR after MIR:
- result:
- next action:
```

The report must not simply say “unmatched” without documenting what was tried.

---

## 11. Unresolved computed facets

A facet may appear here only after documented derivation attempts fail.

For each unresolved facet, include:

* normalized inequality;
* source instance;
* support pattern;
* attempted derivation patterns;
* failure reason;
* next proposed attempt.

If many unresolved facets share the same pattern, group them by signature.

---

## 12. Proof obligations

The report must separate:

* validity proof;
* facetness proof;
* completeness proof;
* reverse inclusion proof;
* parameter-regime classification;
* unresolved candidate refinements.

Example proof obligations:

```markdown
1. Prove validity of each derived family for all admissible parameters.
2. For each candidate family, either derive it using c-MIR patterns or invalidate/refine it.
3. Characterize when each valid family is facet-defining.
4. Prove that all computed facets are covered in the tested range.
5. Prove reverse inclusion before claiming a complete hull description.
```

---

## 13. Next refinement loop

Every report must end with concrete next actions unless the complete hull is proved.

Examples:

```markdown
Next loop:

1. Take each unresolved mixed facet.
2. Identify source constraints.
3. Try residual, coefficient tightening, aggregation+c-MIR, mixed MIR, and MIR-after-MIR.
4. Generate candidate symbolic families.
5. Run exact matching and finite validity gates.
6. Promote, invalidate, or refine each candidate.
```

A report should not stop at “more work is needed.” It should say exactly what the next loop should do.

---

## 14. Status labels

Use these labels consistently.

### Family-level labels

* `derived/proved valid`
* `candidate`
* `invalidated`
* `experimentally supported`
* `facetness unproved`
* `complete hull not claimed`

### Facet-level labels

* `raw cddlib facet`
* `normalized`
* `variable bound`
* `original constraint`
* `covered by derived family`
* `covered by candidate family`
* `unresolved`
* `invalidated candidate evidence`

### Gate labels

* `Gate 1 passed`
* `Gate 1 failed`
* `Gate 2 passed`
* `Gate 2 failed`
* `Gate 3 passed`
* `Gate 3 missing`
* `Gate 3 incomplete`

Do not conflate these labels.

In particular:

* exact matching does not imply validity;
* finite validity does not imply a proof;
* validity does not imply facetness;
* facet coverage does not imply complete hull;
* candidate does not mean proved valid.

## Family compression requirement

Before producing the final report, the assistant must perform a family-compression pass.

If many similar candidate families appear, the report must not simply list them one by one. Instead, it must attempt to identify a common parameterized family.

The report should include a subsection:

## Family compression pass

### Candidate groups considered

### Proposed generalizations

### Validation results for generalizations

### Narrow families retained and why

For every proposed generalization, report:

which narrower families it subsumes;
exact matching results;
finite validity results;
derivation certificate status;
counterexamples if invalid.

If a generalization fails, keep the narrower families only if they are individually valid or useful as local candidates.

A report is incomplete if it contains many similar local candidate families but no compression attempt.

## Local candidate warning

A candidate family that covers only one instance or one facet must be labeled `local candidate`.

A local candidate may not be promoted to derived/proved status unless it has a derivation certificate.

If multiple local candidates share the same form, attempt to merge them into a general family before finalizing the report.