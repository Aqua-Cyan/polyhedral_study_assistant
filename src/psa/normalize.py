from .inequality import LinearInequality


def normalize_inequality(
    coefficients: list[int] | tuple[int, ...],
    rhs: int,
    sense: str = "<=",
) -> LinearInequality:
    inequality = LinearInequality(tuple(coefficients), rhs, sense)
    return inequality.normalized()