from pathlib import Path
import pytest

from infra_checks.loader import load_yaml_documents, is_templated_yaml, read_file_text
from infra_checks.exceptions import TemplatedYAMLError


def test_read_file_text_reads_content(tmp_path: Path):
    file_path = tmp_path / "sample.yaml"
    file_path.write_text("key: value\n")
    content = read_file_text(file_path)
    assert "key: value" in content


def test_is_templated_yaml_detects_helm_tokens():
    text = "name: {{ include \"chart.fullname\" . }}"
    assert is_templated_yaml(text) is True


def test_load_yaml_documents_parses_multi_doc_repo_file():
    repo_root = Path(__file__).resolve().parents[1]
    k8s_file = repo_root / "k8s" / "microservice-demo.yaml"
    docs = load_yaml_documents(k8s_file)
    # Expect multiple documents in this file
    assert len(docs) >= 5
    # All should be dicts
    assert all(isinstance(d, dict) for d in docs)


def test_load_yaml_documents_raises_on_templated_yaml():
    repo_root = Path(__file__).resolve().parents[1]
    templated_file = repo_root / "helm-cdng" / "mychart" / "templates" / "deployment.yaml"
    with pytest.raises(TemplatedYAMLError):
        _ = load_yaml_documents(templated_file)
