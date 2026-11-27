"""Модуль трансформации AST в словарь Python для сериализации в TOML."""
from lark import Transformer, v_args


class ConfigTransformer(Transformer):
    """Преобразует дерево разбора Lark в словарь Python."""

    def __init__(self):
        """Инициализирует словарь констант."""
        super().__init__()
        self.constants = {}

    def start(self, items):
        """Собирает все объявления переменных в итоговый словарь."""
        result = {}
        for item in items:
            if isinstance(item, tuple):
                key, value = item
                result[key] = value
        return result

    @v_args(inline=True)
    def var_decl(self, name_token, value):
        """Объявляет переменную var имя := значение."""
        name = str(name_token)
        self.constants[name] = value
        return (name, value)

    @v_args(inline=True)
    def var_ref(self, name_token):
        """Возвращает значение константы, когда к ней обращаются."""
        name = str(name_token)
        if name not in self.constants:
            raise ValueError(f"Неизвестная константа: {name}")
        return self.constants[name]

    @v_args(inline=True)
    def number(self, token):
        """Обрабатывает числовые литералы."""
        return float(token)

    @v_args(inline=True)
    def string(self, token=None):
        """Обрабатывает строковые литералы q(...)."""
        if token is None:
            return ""
        return str(token)

    def array(self, items):
        """Обрабатывает массивы ({ ... })."""
        return list(items)

    @v_args(inline=True)
    def eval_expr(self, inner):
        """Возвращает вычисленное значение выражения."""
        return inner

    @v_args(inline=True)
    def add_expr(self, left, right):
        """Сложение."""
        return left + right

    @v_args(inline=True)
    def sub_expr(self, left, right):
        """Вычитание."""
        return left - right

    @v_args(inline=True)
    def mul_expr(self, left, right):
        """Умножение."""
        return left * right

    @v_args(inline=True)
    def div_expr(self, left, right):
        """Деление."""
        return left / right

    @v_args(inline=True)
    def len_expr(self, operand):
        """Вычисление длины len()."""
        return float(len(operand))

    @v_args(inline=True)
    def pow_expr(self, base, exp):
        """Возведение в степень pow()."""
        return float(pow(base, exp))
