"""Точка входа в приложение."""
import sys
from src.config import load_config, Config


def print_config(config: Config) -> None:
    """Вывод конфигурации в формате ключ-значение.

    Args:
        config: Объект конфигурации.
    """
    print(f"package={config.package}")
    print(f"source={config.source}")
    print(f"test_mode={config.test_mode}")
    print(f"version={config.version}")
    print(f"output={config.output}")
    print(f"ascii_mode={config.ascii_mode}")
    print(f"max_depth={config.max_depth}")


def main() -> None:
    """Главная функция приложения."""
    if len(sys.argv) < 2:
        print("Usage: .\run.bat <config.xml>", file=sys.stderr)
        sys.exit(1)

    config_path = sys.argv[1]
    try:
        config = load_config(config_path)
        print_config(config)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
