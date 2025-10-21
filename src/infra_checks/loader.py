from __future__ import annotations

from pathlib import Path
from typing import Any, List

import yaml

from .exceptions import TemplatedYAMLError, YamlLoadingError


HELM_TEMPLATE_TOKENS = ("{{", "}}")


def read_file_text(file_path: str | Path, encoding: str = "utf-8") -> str:
    path = Path(file_path)
    try:
        return path.read_text(encoding=encoding)
    except Exception as exc:
        raise YamlLoadingError(f"Failed to read file: {path}") from exc


def is_templated_yaml(text: str) -> bool:
    return any(token in text for token in HELM_TEMPLATE_TOKENS)


def load_yaml_documents(file_path: str | Path, allow_templated: bool = False) -> List[Any]:
    """Load 1..N YAML documents from a file.

    When Helm/Go template tokens are detected, raise unless allow_templated=True.
    We do not attempt to render templates in this utility.
    """
    text = read_file_text(file_path)
    if is_templated_yaml(text) and not allow_templated:
        raise TemplatedYAMLError()
    try:
        docs = list(yaml.safe_load_all(text))
        # Filter out None documents from stray separators
        return [d for d in docs if d is not None]
    except yaml.YAMLError as exc:
        raise YamlLoadingError(f"Failed to parse YAML: {file_path}") from exc
