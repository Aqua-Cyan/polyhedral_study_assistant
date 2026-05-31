# polyhedral_study_assistant

`polyhedral_study_assistant` is a research harness for studying convex hull descriptions of integer linear sets.

The goal is not to automatically solve arbitrary convex hull problems. Instead, this project helps researchers:

- generate and manage small integer programming instances;
- compute small-instance convex hulls using external tools such as PORTA;
- normalize and classify facet-defining inequalities;
- match PORTA-generated facets against candidate inequality families;
- record c-MIR derivation certificates;
- track proof obligations for proposed convex hull descriptions.

## Intended users

This project is intended for researchers in integer programming, polyhedral combinatorics, and combinatorial optimization.

## Current status

Early development. The initial focus is on:

1. inequality representation and normalization;
2. small-instance workflows;
3. PORTA output organization;
4. candidate facet matching;
5. research documentation templates.

## Philosophy

A candidate inequality system should not be called a complete convex hull description unless:

- every inequality family has a validity proof;
- tested PORTA facets are covered or exceptions are explained;
- the reverse inclusion has been proved;
- all assumptions and parameter ranges are explicit.