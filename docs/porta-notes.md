# PORTA Notes

PORTA is treated as an external dependency.

This repository does not vendor or redistribute PORTA binaries.

The harness should call PORTA through configurable executable paths, for example:

- `traf`
- `valid`
- other PORTA executables as needed

On Windows, using PORTA through WSL is recommended if native compilation is inconvenient.

The initial harness should separate:

1. writing PORTA input files;
2. calling PORTA executables;
3. parsing PORTA output files;
4. normalizing resulting inequalities.