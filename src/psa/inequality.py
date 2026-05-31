from dataclasses import dataclass
from math import gcd
from functools import reduce


@dataclass(frozen=True)
class LinearInequality:
    coefficients: tuple[int, ...]
    rhs: int
    sense: str = "<="

    def __post_init__(self) -> None:
        if self.sense not in {"<=", ">=", "="}:
            raise ValueError(f"Unsupported inequality sense: {self.sense}")
        if len(self.coefficients) == 0:
            raise ValueError("An inequality must have at least one coefficient.")

    @property
    def support(self) -> tuple[int, ...]:
        return tuple(i for i, a in enumerate(self.coefficients) if a != 0)

    def normalized(self) -> "LinearInequality":
        coeffs = list(self.coefficients)
        rhs = self.rhs
        sense = self.sense

        if sense == ">=":
            coeffs = [-a for a in coeffs]
            rhs = -rhs
            sense = "<="

        values = [abs(a) for a in coeffs if a != 0]
        if rhs != 0:
            values.append(abs(rhs))

        if values:
            g = reduce(gcd, values)
            coeffs = [a // g for a in coeffs]
            rhs = rhs // g

        return LinearInequality(tuple(coeffs), rhs, sense)

    def as_dict(self) -> dict:
        return {
            "coefficients": list(self.coefficients),
            "rhs": self.rhs,
            "sense": self.sense,
            "support": list(self.support),
        }