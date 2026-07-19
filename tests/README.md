# Core and Adapter Tests

The standard-library test suite covers strict formats 0.1, 0.2, and 0.3; static PNG structure/CRC/limit/integrity validation; confined logical asset references; the exact eight-table SQLite schema; all ten JSON-compatible operations; AT-01 through AT-12; sourced provenance and pre-answer safety; restart/challenge/immutability behavior; approved E1A and pending E7B golden evidence; and direct non-LLM tests for every project-local Hermes adapter handler and fallback-first skill rule.

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -v
```

Automated tests use temporary user-data directories and do not invoke Hermes, an LLM, or the network. Real pinned-Hermes E7B acceptance is deliberately deferred until the exact candidate receives explicit human approval.
