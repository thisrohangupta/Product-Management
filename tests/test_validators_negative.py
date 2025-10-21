import pytest

from infra_checks.k8s_validators import (
    is_valid_k8s_document,
    validate_deployment_has_selector,
    validate_service_ports,
)


def test_is_valid_k8s_document_false_on_missing_keys():
    assert is_valid_k8s_document({}) is False


@pytest.mark.parametrize(
    "doc",
    [
        {"kind": "Service"},  # wrong kind
        {"kind": "Deployment", "spec": None},  # spec not dict
        {"kind": "Deployment", "spec": {}},  # selector missing
        {"kind": "Deployment", "spec": {"selector": []}},  # selector not dict
    ],
)
def test_validate_deployment_has_selector_negative_cases(doc):
    assert validate_deployment_has_selector(doc) is False


@pytest.mark.parametrize(
    "doc",
    [
        {"kind": "Deployment"},  # wrong kind
        {"kind": "Service", "spec": None},  # spec not dict
        {"kind": "Service", "spec": {}},  # ports missing
        {"kind": "Service", "spec": {"ports": []}},  # empty ports list
        {"kind": "Service", "spec": {"ports": [{}]}},  # port missing in entry
    ],
)
def test_validate_service_ports_negative_cases(doc):
    assert validate_service_ports(doc) is False
