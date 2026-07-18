# Core and Adapter Tests

The standard-library test suite covers strict pack validation, the exact eight-table SQLite schema, all ten JSON-compatible operations, AT-01 through AT-12, the additional core security/retry cases, and direct non-LLM tests for every project-local Hermes adapter handler.

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -v
```

Automated tests use temporary user-data directories and do not invoke Hermes, an LLM, or the network. Real pinned-Hermes acceptance evidence is recorded separately in `docs/handoffs/hermes-integration-0.1.md`.
