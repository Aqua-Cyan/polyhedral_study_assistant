from __future__ import annotations

from pprint import pprint


def main() -> None:
    import cdd

    # Vertices of the unit square [0,1]^2.
    #
    # In cddlib generator representation:
    # [1, x1, x2] means a vertex.
    # [0, r1, r2] would mean a ray.
    points = [
        [1, 0, 0],
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 1],
    ]

    mat = cdd.matrix_from_array(points, rep_type=cdd.RepType.GENERATOR)
    poly = cdd.polyhedron_from_matrix(mat)
    inequalities = cdd.copy_inequalities(poly)

    print("Raw inequalities from cdd:")
    pprint(inequalities.array)

    print("Linear rows, if any:")
    pprint(inequalities.lin_set)


if __name__ == "__main__":
    main()