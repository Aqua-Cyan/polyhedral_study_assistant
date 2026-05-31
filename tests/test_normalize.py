from polyhedral_study_assistant.normalize import normalize_inequality


def test_gcd_normalization() -> None:
    inequality = normalize_inequality([2, 4, -2], 6)
    assert inequality.coefficients == (1, 2, -1)
    assert inequality.rhs == 3
    assert inequality.sense == "<="


def test_greater_equal_is_converted_to_less_equal() -> None:
    inequality = normalize_inequality([1, -2, 3], 5, ">=")
    assert inequality.coefficients == (-1, 2, -3)
    assert inequality.rhs == -5
    assert inequality.sense == "<="


def test_support() -> None:
    inequality = normalize_inequality([0, 3, 0, -6], 9)
    assert inequality.coefficients == (0, 1, 0, -2)
    assert inequality.rhs == 3
    assert inequality.support == (1, 3)