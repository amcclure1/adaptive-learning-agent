# Core Tests

The standard-library test suite covers strict pack validation, the exact eight-table SQLite schema, all ten JSON-compatible tools, AT-01 through AT-12, and the additional core security and retry cases in the implementation task.

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -v
```

Tests use temporary user-data directories and do not invoke Hermes, an LLM, or the network.
