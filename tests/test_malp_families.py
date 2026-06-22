from examples.malp.families import ResidualFamily, seed_families
from examples.malp.model import make_instance
from psa.family import FamilyParameter
from psa.inequality import LinearInequality


def test_seed_families_include_activation_and_residuals() -> None:
    families = seed_families()
    names = [family.name for family in families]
    assert names == ["activation_j1", "activation_j2", "residual_j1", "residual_j2"]


def test_residual_family_enumerates_positive_residual_subsets() -> None:
    instance = make_instance("demo", ["a", "b", "c"], ["b", "c", "d"], 2, 2)
    family = ResidualFamily("j1")

    parameters = family.enumerate_parameters(instance)

    assert FamilyParameter({"source": "j1", "subset": ("a",), "residual": 0}) not in parameters
    assert any(parameter.values["subset"] == ("a", "b") for parameter in parameters)
    assert any(parameter.values["subset"] == ("a", "b", "c") for parameter in parameters)


def test_residual_family_instantiates_expected_concrete_inequality() -> None:
    instance = make_instance("demo", ["a", "b", "c"], ["b", "c", "d"], 2, 2)
    family = ResidualFamily("j1")
    parameter = FamilyParameter({"source": "j1", "subset": ("a", "b"), "residual": 1})

    inequality = family.instantiate(instance, parameter)

    expected = LinearInequality((-1, -1, 0, 0, 1, 0), 0, "<=").normalized()
    assert inequality == expected
