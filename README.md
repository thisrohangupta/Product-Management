# Repository Tests

This repository contains infrastructure YAML examples. A lightweight Python test suite validates basic YAML/Kubernetes structure and achieves >90% coverage through utility functions.

## Running tests

```bash
python -m pip install -r requirements.txt
pytest
```

Coverage threshold is enforced at 90% via `pytest.ini`.
