from __future__ import annotations

from collections.abc import Iterable

from psa.inequality import LinearInequality


def convex_hull_inequalities_from_points(
    points: Iterable[Iterable[int]],
) -> list[LinearInequality]:
    """Compute H-representation of conv(points) using pycddlib.

    Parameters
    ----------
    points:
        Affine points [x1, ..., xn].

    Returns
    -------
    list[LinearInequality]
        Inequalities in PSA convention: a x <= rhs.

    Notes
    -----
    pycddlib uses rows [b, a1, ..., an] to mean:

        0 <= b + a1*x1 + ... + an*xn

    PSA uses:

        a*x <= rhs

    Therefore [b, a] is converted to (-a)*x <= b.
    """
    try:
        import cdd
    except ImportError as exc:
        raise RuntimeError(
            "pycddlib is required for the cdd backend. "
            "Install it with: python -m pip install pycddlib"
        ) from exc

    point_list = [list(p) for p in points]
    if not point_list:
        raise ValueError("At least one point is required.")

    dimension = len(point_list[0])
    if dimension == 0:
        raise ValueError("Points must have positive dimension.")

    if any(len(p) != dimension for p in point_list):
        raise ValueError("All points must have the same dimension.")

    generator_rows = [[1] + p for p in point_list]

    mat = cdd.matrix_from_array(
        generator_rows,
        rep_type=cdd.RepType.GENERATOR,
    )
    poly = cdd.polyhedron_from_matrix(mat)
    hrep = cdd.copy_inequalities(poly)

    inequalities: list[LinearInequality] = []

    for row_index, row in enumerate(hrep.array):
        if row_index in hrep.lin_set:
            # For now, skip equations. Later we should represent them explicitly.
            continue

        values = [int(v) for v in row]
        constant = values[0]
        coeffs_ge = values[1:]

        # 0 <= constant + coeffs_ge * x
        # <=> (-coeffs_ge) * x <= constant
        coeffs_le = tuple(-a for a in coeffs_ge)

        inequalities.append(
            LinearInequality(coeffs_le, constant, "<=").normalized()
        )

    return inequalities