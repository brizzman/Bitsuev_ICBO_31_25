"""Тесты модуля сбора зависимостей."""
import json
import pytest
from src.fetcher import _get_deps_from_test_file, _parse_requires_dist


def test_get_deps_from_test_file(tmp_path) -> None:
    """Тест чтения зависимостей из валидного JSON."""
    test_file = tmp_path / "data.json"
    test_file.write_text(json.dumps({"A": ["B", "C"]}))
    
    deps = _get_deps_from_test_file(str(test_file), "A")
    assert deps == ["B", "C"]


def test_get_deps_from_test_file_missing(tmp_path) -> None:
    """Тест чтения из несуществующего файла."""
    deps = _get_deps_from_test_file("nonexistent.json", "A")
    assert deps == []


def test_parse_requires_dist() -> None:
    """Тест парсинга сырых метаданных PyPI."""
    reqs = ["requests (>=2.0)", "numpy ; extra == 'test'"]
    deps = _parse_requires_dist(reqs)
    assert "requests" in deps
    assert "numpy" in deps
