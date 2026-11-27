"""Модуль представления графа зависимостей."""
from typing import Dict, List


class DependencyGraph:
    """Класс для хранения графа зависимостей (список смежности)."""

    def __init__(self) -> None:
        """Инициализация пустого графа."""
        self.graph: Dict[str, List[str]] = {}

    def add_edge(self, source: str, target: str) -> None:
        """Добавление направленного ребра в граф.

        Args:
            source: Пакет, который зависит.
            target: Пакет-зависимость.
        """
        if source not in self.graph:
            self.graph[source] = []
        if target not in self.graph:
            self.graph[target] = []
        if target not in self.graph[source]:
            self.graph[source].append(target)

    def get_dependencies(self, package: str) -> List[str]:
        """Получение прямых зависимостей пакета.

        Args:
            package: Имя пакета.

        Returns:
            Список зависимостей.
        """
        return self.graph.get(package, [])
