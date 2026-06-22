# MALP research state report

## Scope

- problem_id: `malp`
- max tested union size: `5`
- tested instances: `350`
- total computed facets/inequalities: `7200`
- derived records: `6472`
- candidate records: `728`
- unresolved records: `0`
- stop status: `continue`

Computed facets are evidence. This report is not a complete convex-hull proof.

## Derived families currently recognized

| family | status | covered records | reason |
| --- | --- | ---: | --- |
| `variable_bounds` | `derived` | 3628 | binary domain |
| `activation_j1` | `derived` | 194 | original model constraint |
| `activation_j2` | `derived` | 194 | original model constraint |
| `single_activation_residual_j1` | `derived` | 1228 | residual from x(J1) >= b1 y1 |
| `single_activation_residual_j2` | `derived` | 1228 | residual from x(J2) >= b2 y2 |

## Candidate and unresolved status

- candidate facets: `728`
- unresolved facets: `0`

### Candidate facet examples

- `-i1 - i2 + y1 + y2 <= 0` from `O=0,I=2,K=0,b1=1,b2=2`; signature: `relation=identical;O=0,I=2,K=0;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 + y1 + y2 <= 0` from `O=0,I=2,K=0,b1=2,b2=1`; signature: `relation=identical;O=0,I=2,K=0;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 + y1 + y2 <= 0` from `O=0,I=2,K=1,b1=1,b2=2`; signature: `relation=nested;O=0,I=2,K=1;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 + y1 + y2 <= 0` from `O=0,I=2,K=1,b1=1,b2=3`; signature: `relation=nested;O=0,I=2,K=0;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 + y1 + y2 <= 0` from `O=0,I=2,K=1,b1=2,b2=1`; signature: `relation=nested;O=0,I=2,K=1;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 + y1 + y2 <= 0` from `O=0,I=2,K=1,b1=2,b2=2`; signature: `relation=nested;O=0,I=2,K=0;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 - k2 + y1 + y2 <= 0` from `O=0,I=2,K=2,b1=1,b2=2`; signature: `relation=nested;O=0,I=2,K=2;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 + y1 + y2 <= 0` from `O=0,I=2,K=2,b1=1,b2=3`; signature: `relation=nested;O=0,I=2,K=1;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 - k2 + y1 + 2 y2 <= 0` from `O=0,I=2,K=2,b1=1,b2=3`; signature: `relation=nested;O=0,I=2,K=2;x_unit_negative=True;y1=1,y2=2;rhs=0`
- `-i1 - i2 - k2 + y1 + y2 <= 0` from `O=0,I=2,K=2,b1=1,b2=3`; signature: `relation=nested;O=0,I=2,K=1;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 + y1 + y2 <= 0` from `O=0,I=2,K=2,b1=1,b2=4`; signature: `relation=nested;O=0,I=2,K=0;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 - k2 + y1 + y2 <= 0` from `O=0,I=2,K=2,b1=2,b2=1`; signature: `relation=nested;O=0,I=2,K=2;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 + y1 + y2 <= 0` from `O=0,I=2,K=2,b1=2,b2=2`; signature: `relation=nested;O=0,I=2,K=1;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k2 + y1 + y2 <= 0` from `O=0,I=2,K=2,b1=2,b2=2`; signature: `relation=nested;O=0,I=2,K=1;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 + y1 + y2 <= 0` from `O=0,I=2,K=2,b1=2,b2=3`; signature: `relation=nested;O=0,I=2,K=0;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 - k2 - k3 + y1 + y2 <= 0` from `O=0,I=2,K=3,b1=1,b2=2`; signature: `relation=nested;O=0,I=2,K=3;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 - k2 + y1 + y2 <= 0` from `O=0,I=2,K=3,b1=1,b2=3`; signature: `relation=nested;O=0,I=2,K=2;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 - k3 + y1 + y2 <= 0` from `O=0,I=2,K=3,b1=1,b2=3`; signature: `relation=nested;O=0,I=2,K=2;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k2 - k3 + y1 + y2 <= 0` from `O=0,I=2,K=3,b1=1,b2=3`; signature: `relation=nested;O=0,I=2,K=2;x_unit_negative=True;y1=1,y2=1;rhs=0`
- `-i1 - i2 - k1 - k2 - k3 + y1 + 2 y2 <= 0` from `O=0,I=2,K=3,b1=1,b2=3`; signature: `relation=nested;O=0,I=2,K=3;x_unit_negative=True;y1=1,y2=2;rhs=0`
- ... truncated 708 more candidate facets

## Facet signature groups

| count | signature | recommended action |
| ---: | --- | --- |
| 121 | `relation=nested;O=0,I=1,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 121 | `relation=nested;O=0,I=1,K=0;x_unit_negative=True;y2=1;rhs=0` | covered |
| 78 | `relation=nested;O=0,I=2,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 78 | `relation=nested;O=0,I=2,K=0;x_unit_negative=True;y2=1;rhs=0` | covered |
| 76 | `relation=nested;O=0,I=1,K=1;x_unit_negative=True;y2=1;rhs=0` | covered |
| 76 | `relation=nested;O=1,I=1,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 64 | `relation=identical;O=0,I=2,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 64 | `relation=identical;O=0,I=2,K=0;x_unit_negative=True;y2=1;rhs=0` | covered |
| 61 | `relation=nested;O=0,I=2,K=1;x_unit_negative=True;y2=2;rhs=0` | covered |
| 61 | `relation=nested;O=1,I=2,K=0;x_unit_negative=True;y1=2;rhs=0` | covered |
| 60 | `relation=nested;O=0,I=2,K=0;x_unit_negative=True;y1=1,y2=1;rhs=0` | derive or compress interaction family |
| 54 | `relation=identical;O=0,I=1,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 54 | `relation=identical;O=0,I=1,K=0;x_unit_negative=True;y2=1;rhs=0` | covered |
| 54 | `relation=overlap;O=0,I=1,K=1;x_unit_negative=True;y2=1;rhs=0` | covered |
| 54 | `relation=overlap;O=1,I=1,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 52 | `relation=identical;O=0,I=3,K=0;x_unit_negative=True;y1=2;rhs=0` | covered |
| 52 | `relation=identical;O=0,I=3,K=0;x_unit_negative=True;y2=2;rhs=0` | covered |
| 48 | `relation=overlap;O=0,I=1,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 48 | `relation=overlap;O=0,I=1,K=0;x_unit_negative=True;y2=1;rhs=0` | covered |
| 42 | `relation=nested;O=0,I=2,K=1;x_unit_negative=True;y1=1,y2=1;rhs=0` | derive or compress interaction family |
| 42 | `relation=nested;O=1,I=2,K=0;x_unit_negative=True;y1=1,y2=1;rhs=0` | derive or compress interaction family |
| 42 | `relation=overlap;O=0,I=0,K=1;x_unit_negative=True;y2=1;rhs=0` | covered |
| 42 | `relation=overlap;O=1,I=0,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 41 | `relation=nested;O=0,I=2,K=1;x_unit_negative=True;y2=1;rhs=0` | covered |
| 41 | `relation=nested;O=1,I=2,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 40 | `relation=identical;O=0,I=2,K=0;x_unit_negative=True;y1=1,y2=1;rhs=0` | derive or compress interaction family |
| 38 | `relation=identical;O=0,I=3,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |
| 38 | `relation=identical;O=0,I=3,K=0;x_unit_negative=True;y2=1;rhs=0` | covered |
| 35 | `relation=nested;O=0,I=0,K=1;x_unit_negative=True;y2=1;rhs=0` | covered |
| 35 | `relation=nested;O=1,I=0,K=0;x_unit_negative=True;y1=1;rhs=0` | covered |

## Proof obligations

- Candidate interaction facets remain. Run FamilyGuesser and DerivationProver on interaction signatures.

## Generated machine-readable artifacts

- `reports\malp_state.json`
- `tasks\TASK_POOL.json`
- `memory\facets\malp\facet_signatures.json`
- `memory\family\malp\family_memory.json`
