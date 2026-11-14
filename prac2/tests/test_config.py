"""Тесты модуля конфигурации."""
import pytest
from src.config import _parse_bool, _build_config


def test_parse_bool() -> None:
    """Тест парсинга булевых значений."""
    assert _parse_bool("true") is True
    assert _parse_bool("False") is False
    assert _parse_bool(" 1 ") is True
    assert _parse_bool("0") is False


def test_build_config_success() -> None:
    """Тест успешного создания конфигурации."""
    data = {
        "package": "flask",
        "source": "pypi",
        "version": "latest",
        "output": "out.png",
        "max_depth": "2",
    }
    config = _build_config(data)
    assert config.package == "flask"
    assert config.max_depth == 2
    assert config.test_mode is False
    assert config.ascii_mode is False


def test_build_config_missing_field() -> None:
    """Тест отсутствия обязательного поля."""
    data = {"package": "flask"}
    with pytest.raises(ValueError, match="Missing required parameter"):
        _build_config(data)


def test_build_config_invalid_depth() -> None:
    """Тест некорректной глубины (не число)."""
    data = {
        "package": "a", "source": "b",
        "version": "c", "output": "d", "max_depth": "abc",
    }
    with pytest.raises(ValueError, match="must be an integer"):
        _build_config(data)


def test_build_config_negative_depth() -> None:
    """Тест отрицательной глубины."""
    data = {
        "package": "a", "source": "b",
        "version": "c", "output": "d", "max_depth": "-5",
    }
    with pytest.raises(ValueError, match="must be >= -1"):
        _build_config(data)
