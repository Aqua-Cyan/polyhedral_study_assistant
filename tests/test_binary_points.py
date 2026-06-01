from psa.binary_points import enumerate_binary_points


def test_enumerate_all_binary_points() -> None:
    points = enumerate_binary_points(2)
    assert set(points) == {
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    }


def test_enumerate_binary_points_with_predicate() -> None:
    points = enumerate_binary_points(3, lambda p: sum(p) >= 2)
    assert set(points) == {
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
    }