"""Тесты для проверки парсера и трансформера варианта 4."""
import pytest
from lark.exceptions import UnexpectedInput
from src.parser import config_parser
from src.transformer import ConfigTransformer

_VAL_TWO = 2.0
_VAL_THREE = 3.0
_VAL_FIVE = 5.0
_EXPECTED_SUM = 7.0
_EXPECTED_SUB = 3.0
_EXPECTED_MUL = 10.0
_EXPECTED_DIV = 2.5
_EXPECTED_POW = 8.0
_EXPECTED_LEN = 3.0


def parse_and_transform(text: str) -> dict:
    """Парсит текст и возвращает словарь для TOML."""
    tree = config_parser.parse(text)
    return ConfigTransformer().transform(tree)


def test_number():
    """Тест числового литерала."""
    result = parse_and_transform("var a := 42.5")
    assert result == {"a": 42.5}


def test_string():
    """Тест строкового литерала."""
    result = parse_and_transform("var s := q(hello world)")
    assert result == {"s": "hello world"}


def test_array():
    """Тест массива."""
    result = parse_and_transform("var arr := ({ 1.0, 2.0, q(three) })")
    assert result == {"arr": [1.0, _VAL_TWO, "three"]}


def test_multiline_comment():
    """Тест многострочного комментария."""
    text = "/+\ncomment\n+/\nvar a := 1.0"
    result = parse_and_transform(text)
    assert result == {"a": 1.0}


def test_add_expr():
    """Тест сложения."""
    text = "var a := 5.0\nvar b := ?[+ a 2.0]"
    result = parse_and_transform(text)
    assert result == {"a": _VAL_FIVE, "b": _EXPECTED_SUM}


def test_sub_expr():
    """Тест вычитания."""
    text = "var a := 5.0\nvar b := ?[- a 2.0]"
    result = parse_and_transform(text)
    assert result == {"a": _VAL_FIVE, "b": _EXPECTED_SUB}


def test_mul_expr():
    """Тест умножения."""
    text = "var a := 5.0\nvar b := ?[* a 2.0]"
    result = parse_and_transform(text)
    assert result == {"a": _VAL_FIVE, "b": _EXPECTED_MUL}


def test_div_expr():
    """Тест деления."""
    text = "var a := 5.0\nvar b := ?[/ a 2.0]"
    result = parse_and_transform(text)
    assert result == {"a": _VAL_FIVE, "b": _EXPECTED_DIV}


def test_len_expr():
    """Тест функции len()."""
    text = "var arr := ({ 1.0, 2.0, 3.0 })\nvar l := ?[len arr]"
    result = parse_and_transform(text)
    assert result == {"arr": [1.0, _VAL_TWO, _VAL_THREE], "l": _EXPECTED_LEN}


def test_pow_expr():
    """Тест функции pow()."""
    text = "var a := 2.0\nvar p := ?[pow a 3.0]"
    result = parse_and_transform(text)
    assert result == {"a": _VAL_TWO, "p": _EXPECTED_POW}


def test_nested_eval():
    """Тест вложенного вычисления."""
    text = "var a := 2.0\nvar b := ?[+ ?[* a 3.0] 1.0]"
    result = parse_and_transform(text)
    assert result == {"a": _VAL_TWO, "b": _EXPECTED_SUM}


def test_undefined_constant():
    """Тест неизвестной константы."""
    text = "var b := ?[+ unknown 1.0]"
    with pytest.raises(ValueError, match="Неизвестная константа: unknown"):
        parse_and_transform(text)


def test_syntax_error():
    """Тест синтаксической ошибки."""
    with pytest.raises(UnexpectedInput):
        config_parser.parse("var A := 1.0")
