# Backend Notes

## Current backend: pycddlib

The project uses `pycddlib` as its computational backend. See `docs/cdd-notes.md` for representation conventions and conversion rules.

pycddlib provides Python bindings for cddlib, which implements the double description method for converting between V-representations and H-representations of convex polyhedra.

## Backend configuration

The backend is called through `src/psa/backends/`. The study adapter passes enumerated feasible 0-1 points as a V-representation to pycddlib and retrieves the H-representation (inequalities) of their convex hull.

## Historical note: PORTA

An earlier version of this project referenced PORTA as an external backend. PORTA support has been superseded by pycddlib. The original `docs/porta-notes.md` file is no longer maintained. If PORTA support is needed in the future, it should be implemented as a configurable alternative backend under `src/psa/backends/` with the same interface as the cddlib backend.

## Adding a new backend

If a new polyhedral backend is needed (e.g., PORTA, polymake, or a custom exact-arithmetic solver):

1. Create a new module under `src/psa/backends/`.
2. Expose a function that accepts a list of feasible points and returns a list of `LinearInequality` objects.
3. Ensure the output is normalized using `src/psa/normalize.py`.
4. Add tests under `tests/`.
5. Do not put problem-specific logic in the backend module.
