from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping


def ensure_required_keys(mapping: Mapping[str, Any], required_keys: Iterable[str]) -> None:
    missing = [k for k in required_keys if k not in mapping]
    if missing:
        raise KeyError(f"Missing required keys: {', '.join(sorted(missing))}")


def collect_kinds(docs: List[dict]) -> dict[str, int]:
    kind_counts: dict[str, int] = {}
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        kind = doc.get("kind")
        if not kind:
            continue
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
    return kind_counts


def extract_image_references(doc: Dict[str, Any]) -> List[str]:
    images: List[str] = []

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            # Common container list path in k8s manifests
            if "containers" in node and isinstance(node["containers"], list):
                for container in node["containers"]:
                    if isinstance(container, dict):
                        image = container.get("image")
                        if isinstance(image, str):
                            images.append(image)
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for item in node:
                visit(item)
        else:
            return

    visit(doc)
    # Return stable order for deterministic tests
    return sorted(set(images))
