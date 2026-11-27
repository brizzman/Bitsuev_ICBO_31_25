"""Точка входа в приложение."""
import sys
from src.config import load_config, Config
from src.analyzer import (
    build_transitive_graph,
    print_ascii_tree,
    get_reverse_dependencies,
)


def print_config(config: Config) -> None:
    """Вывод конфигурации в формате ключ-значение."""
    print(f"package={config.package}")
    print(f"source={config.source}")
    print(f"test_mode={config.test_mode}")
    print(f"version={config.version}")
    print(f"output={config.output}")
    print(f"ascii_mode={config.ascii_mode}")
    print(f"max_depth={config.max_depth}")
    print(f"reverse={config.reverse}")


def main() -> None:
    """Главная функция приложения."""
    if len(sys.argv) < 2:
        print("Usage: ./run.sh <config.xml>", file=sys.stderr)
        sys.exit(1)

    config_path = sys.argv[1]
    try:
        config = load_config(config_path)
        print_config(config)

        print("\nBuilding dependency graph...")
        graph = build_transitive_graph(config)

        if config.reverse:
            print(f"\nReverse dependencies for {config.package}:")
            rev_deps = get_reverse_dependencies(config.package, graph)
            if not rev_deps:
                print("(none found)")
            for dep in rev_deps:
                print(f"- {dep}")
        elif config.ascii_mode:
            print("\nDependency Tree (ASCII):")
            print_ascii_tree(graph, config.package)
        else:
            print("\nGraph edges:")
            if not graph.graph:
                print("(empty)")
            for pkg, deps in graph.graph.items():
                if not deps:
                    print(f"{pkg} -> (no dependencies)")
                for dep in deps:
                    print(f"{pkg} -> {dep}")

    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
