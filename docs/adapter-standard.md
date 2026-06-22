\# Problem Adapter Standard



A user defines a new parametric integer set by creating:



examples/<problem\_id>/README.md



The repository does not directly parse arbitrary mathematical Markdown into a complete study. Instead, an LLM-assisted coding step creates a thin problem-specific adapter.



The adapter must live under:



examples/<problem\_id>/



Required files:



\- model.py

\- families.py

\- derive.py

\- study.py



The adapter must expose:



def run(max\_union\_size: int = 5) -> dict:

&#x20;   ...



The adapter must output:



\- reports/<problem\_id>\_state.json

\- reports/<problem\_id>\_report.md

\- memory/facets/<problem\_id>/facet\_signatures.json

\- memory/family/<problem\_id>/family\_memory.json

\- tasks/TASK\_POOL.json



The adapter may define:



\- variables and canonical ordering;

\- feasible point enumeration;

\- source constraints;

\- instance generation;

\- problem-specific candidate families;

\- problem-specific derivation attempts.



The adapter must not reimplement:



\- inequality normalization;

\- finite validity checking;

\- exact matching;

\- cdd backend logic;

\- generic report rendering if reusable functions exist.



Problem-specific logic must remain under examples/<problem\_id>/ unless it becomes genuinely reusable.

