"""Модуль анализа графа зависимостей (DFS)."""
from dataclasses import replace
from src.config import Config
from src.graph import DependencyGraph
from src.fetcher import get_direct_dependencies

MAX_DEPTH_DEFAULT = -1


def build_transitive_graph(config: Config) -> DependencyGraph:
    """Построение транзитивного графа зависимостей.

    Args:
        config: Объект конфигурации.

    Returns:
        Построенный граф.
    """
    graph = DependencyGraph()
    visited = set()
    _dfs_build(config.package, 0, config, graph, visited)
    return graph


def _dfs_build(
    package: str,
    current_depth: int,
    config: Config,
    graph: DependencyGraph,
    visited: set
) -> None:
    """Рекурсивный обход в глубину (DFS) для построения графа.

    Args:
        package: Текущий анализируемый пакет.
        current_depth: Текущая глубина.
        config: Объект конфигурации.
        graph: Граф зависимостей.
        visited: Множество уже посещенных пакетов.
    """
    if config.max_depth != MAX_DEPTH_DEFAULT:
        if current_depth > config.max_depth:
            return

    if package in visited:
        return

    visited.add(package)
    graph.graph.setdefault(package, [])

    current_config = replace(config, package=package)
    deps = get_direct_dependencies(current_config)

    for dep in deps:
        graph.add_edge(package, dep)
        _dfs_build(dep, current_depth + 1, config, graph, visited)


def print_ascii_tree(graph: DependencyGraph, start_pkg: str) -> None:
    """Вывод графа в виде текстового ASCII-дерева.

    Args:
        graph: Граф зависимостей.
        start_pkg: Корневой пакет.
    """
    print(f"[{start_pkg}]")
    _print_branches(graph, start_pkg, "", set())


def _print_branches(
    graph: DependencyGraph,
    pkg: str,
    prefix: str,
    visited: set
) -> None:
    """Рекурсивный вывод ветвей ASCII-дерева.

    Args:
        graph: Граф зависимостей.
        pkg: Текущий пакет.
        prefix: Строковый префикс для отступов.
        visited: Множество посещенных пакетов в текущей ветке.
    """
    deps = graph.get_dependencies(pkg)
    for index, dep in enumerate(deps):
        is_last = (index == len(deps) - 1)
        marker = "└── " if is_last else "├── "
        
        if dep in visited:
            print(f"{prefix}{marker}{dep} (cycle)")
            continue
            
        print(f"{prefix}{marker}{dep}")
        
        next_prefix = prefix + ("    " if is_last else "│   ")
        next_visited = visited | {pkg}
        _print_branches(graph, dep, next_prefix, next_visited)
