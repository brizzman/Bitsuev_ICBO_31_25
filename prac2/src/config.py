"""Модуль конфигурации CLI-приложения (XML)."""
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict

MAX_DEPTH_DEFAULT = -1
REQUIRED_FIELDS = ["package", "source", "version", "output"]


@dataclass
class Config:
    """Класс для хранения конфигурации."""
    package: str
    source: str
    test_mode: bool
    version: str
    output: str
    ascii_mode: bool
    max_depth: int


def _parse_bool(value: str) -> bool:
    """Парсинг булевого значения из строки.

    Args:
        value: Строковое значение.

    Returns:
        Булево значение.
    """
    return value.strip().lower() in ("true", "1", "yes")


def _read_xml(filepath: str) -> Dict[str, str]:
    """Чтение XML файла и преобразование в словарь.

    Args:
        filepath: Путь к XML файлу.

    Returns:
        Словарь с параметрами.

    Raises:
        ValueError: Если файл не найден или поврежден.
    """
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        data = {}
        for child in root:
            if child.text:
                data[child.tag] = child.text
        return data
    except Exception as error:
        raise ValueError(f"Failed to read XML config: {error}")


def _build_config(data: Dict[str, str]) -> Config:
    """Валидация данных и создание объекта конфигурации.

    Args:
        data: Словарь с параметрами.

    Returns:
        Объект конфигурации.

    Raises:
        ValueError: При некорректных параметрах.
    """
    for req in REQUIRED_FIELDS:
        if not data.get(req):
            raise ValueError(f"Missing required parameter: {req}")

    try:
        max_depth = int(data.get("max_depth", str(MAX_DEPTH_DEFAULT)))
    except ValueError:
        raise ValueError("max_depth must be an integer")

    if max_depth < MAX_DEPTH_DEFAULT:
        raise ValueError("max_depth must be >= -1")

    return Config(
        package=data["package"],
        source=data["source"],
        test_mode=_parse_bool(data.get("test_mode", "false")),
        version=data["version"],
        output=data["output"],
        ascii_mode=_parse_bool(data.get("ascii_mode", "false")),
        max_depth=max_depth,
    )


def load_config(filepath: str) -> Config:
    """Загрузка и валидация конфигурации.

    Args:
        filepath: Путь к XML файлу.

    Returns:
        Готовая конфигурация.
    """
    data = _read_xml(filepath)
    return _build_config(data)
