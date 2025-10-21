from __future__ import annotations

from typing import Any, Dict

from .yaml_utils import ensure_required_keys


def is_valid_k8s_document(doc: Dict[str, Any]) -> bool:
    try:
        ensure_required_keys(doc, ("apiVersion", "kind", "metadata"))
    except KeyError:
        return False
    return isinstance(doc.get("metadata"), dict)


def validate_deployment_has_selector(doc: Dict[str, Any]) -> bool:
    if doc.get("kind") != "Deployment":
        return False
    spec = doc.get("spec")
    if not isinstance(spec, dict):
        return False
    selector = spec.get("selector")
    if not isinstance(selector, dict):
        return False
    match_labels = selector.get("matchLabels")
    return isinstance(match_labels, dict) and len(match_labels) > 0


def validate_service_ports(doc: Dict[str, Any]) -> bool:
    if doc.get("kind") != "Service":
        return False
    spec = doc.get("spec")
    if not isinstance(spec, dict):
        return False
    ports = spec.get("ports")
    if not isinstance(ports, list) or len(ports) == 0:
        return False
    # Each port spec should have 'port'
    return all(isinstance(p, dict) and "port" in p for p in ports)
