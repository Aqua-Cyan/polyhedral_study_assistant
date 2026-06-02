from __future__ import annotations
from dataclasses import dataclass, field
from typing import Sequence

@dataclass(frozen=True)
class SourceConstraint:
    name: str
    symbolic_form: str
    concrete_form: str

@dataclass(frozen=True)
class DerivationStep:
    method: str
    description: str
    expression: str | None = None

@dataclass(frozen=True)
class DerivationAttempt:
    concrete_facet: str
    source_constraints: tuple[SourceConstraint, ...]
    steps: tuple[DerivationStep, ...]
    symbolic_family: str | None
    parameter_conditions: tuple[str, ...] = ()
    status: str = "unresolved"
    failure_reason: str | None = None