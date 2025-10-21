from pathlib import Path

import pytest

from infra_checks.loader import load_yaml_documents
from infra_checks.yaml_utils import ensure_required_keys, collect_kinds, extract_image_references
from infra_checks.k8s_validators import (
    is_valid_k8s_document,
    validate_deployment_has_selector,
    validate_service_ports,
)


def test_ensure_required_keys_raises_on_missing():
    with pytest.raises(KeyError) as exc:
        ensure_required_keys({"a": 1}, ("a", "b"))
    assert "Missing required keys" in str(exc.value)


def test_collect_kinds_counts_documents(tmp_path: Path):
    docs = [
        {"apiVersion": "v1", "kind": "Service", "metadata": {}},
        {"apiVersion": "v1", "kind": "Service", "metadata": {}},
        {"apiVersion": "apps/v1", "kind": "Deployment", "metadata": {}},
        {},
        "not a dict",
    ]
    counts = collect_kinds(docs)  # type: ignore[arg-type]
    assert counts == {"Service": 2, "Deployment": 1}


def test_extract_image_references_from_deployment():
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": "x"},
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {"name": "a", "image": "nginx:1.25"},
                        {"name": "b", "image": "redis:7"},
                        {"name": "c"},
                    ]
                }
            }
        },
    }
    images = extract_image_references(deployment)
    assert images == ["nginx:1.25", "redis:7"]


def test_validators_on_repo_k8s_file():
    repo_root = Path(__file__).resolve().parents[1]
    k8s_file = repo_root / "k8s" / "microservice-demo.yaml"
    docs = load_yaml_documents(k8s_file)

    assert any(is_valid_k8s_document(doc) for doc in docs)

    # There should be at least one valid Deployment with a selector
    deployments = [d for d in docs if isinstance(d, dict) and d.get("kind") == "Deployment"]
    assert any(validate_deployment_has_selector(d) for d in deployments)

    # There should be at least one Service with ports defined
    services = [d for d in docs if isinstance(d, dict) and d.get("kind") == "Service"]
    assert any(validate_service_ports(svc) for svc in services)
