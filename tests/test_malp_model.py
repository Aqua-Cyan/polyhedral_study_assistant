from examples.malp.model import classify_facets, make_instance
from psa.inequality import LinearInequality


def test_malp_instance_regions_and_variable_order() -> None:
    instance = make_instance("demo", ["a", "b", "c"], ["b", "c", "d"], 2, 1)

    assert instance.ground == ("a", "b", "c", "d")
    assert instance.region_signature == (1, 2, 1)
    assert instance.variable_map.variable_names == ("x_a", "x_b", "x_c", "x_d", "y_1", "y_2")


def test_malp_feasibility_predicate() -> None:
    instance = make_instance("demo", ["a", "b"], ["b", "c"], 2, 1)
    mapping = instance.variable_map

    feasible = [1, 1, 0, 1, 0]
    infeasible = [1, 0, 0, 1, 1]

    assert instance.is_feasible_point(feasible)
    assert not instance.is_feasible_point(infeasible)
    assert mapping.y1_index == 3
    assert mapping.y2_index == 4


def test_classify_bounds_originals_and_nontrivial() -> None:
    instance = make_instance("demo", ["a", "b", "c"], ["b", "c", "d"], 2, 2)
    mapping = instance.variable_map

    bound = LinearInequality((1, 0, 0, 0, 0, 0), 1, "<=")
    original = instance.activation_rows()[0].inequality
    nontrivial = LinearInequality((-1, -1, 0, 0, 1, 1), 0, "<=")

    classified = classify_facets(instance, [bound, original, nontrivial])

    assert len(classified.bounds) == 1
    assert len(classified.original_constraints) == 1
    assert len(classified.nontrivial) == 1
    assert classified.nontrivial[0].y_coefficients == (1, 1)
    assert classified.nontrivial[0].support_signature.startswith("x[")
