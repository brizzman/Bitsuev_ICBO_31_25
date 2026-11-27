"""Точка входа для CLI инструмента трансляции в TOML."""
import sys
import tomli_w
from lark.exceptions import UnexpectedInput
from src.parser import config_parser
from src.transformer import ConfigTransformer

_EXIT_ERROR = 1


def main():
    """Читает stdin, парсит, сохраняет TOML в stdout."""
    input_text = sys.stdin.read()

    try:
        tree = config_parser.parse(input_text)
        transformer = ConfigTransformer()
        result_dict = transformer.transform(tree)

        toml_string = tomli_w.dumps(result_dict)
        print(toml_string, end="")

    except UnexpectedInput as e:
        print(f"Синтаксическая ошибка:\n{e}", file=sys.stderr)
        sys.exit(_EXIT_ERROR)
    except ValueError as e:
        print(f"Ошибка трансляции:\n{e}", file=sys.stderr)
        sys.exit(_EXIT_ERROR)


if __name__ == "__main__":
    main()
