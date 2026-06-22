from examples.malp.derive import MalpAttemptContext, MalpDerivationEngine, make_candidate_record
from examples.malp.model import MalpFacetRecord, make_instance
from psa.inequality import LinearInequality


def test_derivation_engine_derives_residual_and_adds_row() -> None:
    instance = make_instance("demo", ["a", "b", "c"], ["b", "c", "d"], 2, 2)
    context = MalpAttemptContext(instance=instance, original_rows=instance.activation_rows(), derived_rows=[])
    facet = MalpFacetRecord(
        instance_name=instance.name,
        inequality=LinearInequality((-1, -1, 0, 0, 1, 0), 0, "<=").normalized(),
        classification="nontrivial",
        rendered=instance.inequality_to_string(LinearInequality((-1, -1, 0, 0, 1, 0), 0, "<=")),
        x_support_names=("a", "b"),
        y_coefficients=(1, 0),
        support_signature="x[2,0,0]|y[1,0]|rhs=0",
    )

    bundle = MalpDerivationEngine().derive_facet(instance, facet, context)

    assert bundle.status == "derived_concrete"
    assert bundle.derived_rows
    assert context.derived_rows
    assert any(attempt.pattern == "residual" and attempt.equality_passed for attempt in bundle.attempts)


def test_derivation_engine_proposes_candidate_for_unresolved_overlap() -> None:
    instance = make_instance("demo", ["a", "b", "c"], ["b", "c", "d"], 2, 2)
    context = MalpAttemptContext(instance=instance, original_rows=instance.activation_rows(), derived_rows=[])
    target = LinearInequality((-1, -1, 0, 0, 1, 1), 0, "<=").normalized()
    facet = MalpFacetRecord(
        instance_name=instance.name,
        inequality=target,
        classification="nontrivial",
        rendered=instance.inequality_to_string(target),
        x_support_names=("a", "b"),
        y_coefficients=(1, 1),
        support_signature="x[1,1,0]|y[1,1]|rhs=0",
    )

    bundle = MalpDerivationEngine().derive_facet(instance, facet, context)
    candidate = make_candidate_record(bundle)

    assert bundle.candidate_family is not None
    assert candidate is not None
    assert "derivation certificate" in candidate.reason_not_derived
