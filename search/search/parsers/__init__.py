import re
from abc import ABC
from functools import reduce
from operator import __and__, __or__

from pyparsing import (
    Forward,
    Group,
    Literal,
    ParseException,
    Word,
    alphanums,
    alphas,
    delimitedList,
)


class Converter:
    @classmethod
    def convert(cls, value, add_quote=True):
        if type(value) is str:
            value = cls.convert_string(value, add_quote)
        elif type(value) is list:
            value = (cls.convert(v) for v in value)
        else:
            raise NotImplementedError

        return value

    @staticmethod
    def convert_string(value, add_quote):
        is_digit = value.replace(".", "", 1).isdigit()
        if is_digit and "." in value:
            value = float(value)
        elif is_digit:
            value = int(value)
        elif add_quote:
            value = f"'{value}'"

        return value


class BaseParser(ABC):
    AND = Literal("and").setParseAction(lambda: "AND")
    OR = Literal("or").setParseAction(lambda: "OR")

    EQ = Literal("eq").setParseAction(lambda: "=")
    NE = Literal("ne").setParseAction(lambda: "!=")
    GT = Literal("gt").setParseAction(lambda: ">")
    LT = Literal("lt").setParseAction(lambda: "<")
    IN = Literal("in").setParseAction(lambda: "in")

    FN = EQ | NE | GT | LT | IN

    OB = Literal("(").suppress()
    CB = Literal(")").suppress()
    CM = Literal(",").suppress()

    NAME = Word(alphas + "_.", alphanums + "_.")
    _QUOTE = Literal('"').suppress()
    _cyrillicalphas = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    _WORD = Word(alphanums + " " + _cyrillicalphas + _cyrillicalphas.upper())
    _VALUE = _QUOTE + _WORD + _QUOTE
    VALUE = _WORD | _VALUE

    ARRAY = OB + delimitedList(VALUE, ",") + CB
    ARRAY = ARRAY.setParseAction(lambda s, loc, toks: [toks])

    SIMPLE_COND = FN + OB + NAME + CM + (VALUE | ARRAY) + CB

    NESTED_CONDS = Forward()
    AGGREGATE = (AND | OR) + OB + delimitedList(NESTED_CONDS, ",") + CB
    COND = Group(SIMPLE_COND) | Group(AGGREGATE)
    NESTED_CONDS << COND

    QUERY = NESTED_CONDS

    def __init__(self, rql_string):
        self.rql = rql_string
        self.parsed = self._parse_rql()

    def _parse_rql(self):
        parse_results = self.QUERY.parseString(self.rql)
        return parse_results.asList()

    def make_query(self, data=None):
        join_conditions = False
        if data is None:
            join_conditions = True
            data = self.parsed

        conditions = (self.get_condition(fn) for fn in data)
        if join_conditions:
            conditions = "".join(conditions)

        return conditions

    def get_condition(self, fn):
        raise NotImplementedError


class RQL2SQLParser(BaseParser):
    def __init__(self, rql_string):
        self.EQ.setParseAction(lambda: "=")
        self.NE.setParseAction(lambda: "<>")
        super().__init__(rql_string)

    def get_condition(self, fn):
        operator = fn[0].lower()
        if operator in (self.AND, self.OR):
            result = self.make_query(fn[1:])
            condition = f" {operator} ".join(result)
            condition = f"({condition})"
        elif operator == self.IN:
            values = ",".join(str(v) for v in Converter.convert(fn[2]))
            condition = f"{operator}({fn[1]},{values})"
        else:
            value = Converter.convert(fn[2])
            condition = f"{fn[1]} {operator} {value}"

        return condition


class RQL2SphinxQLParser(BaseParser):
    def __init__(self, rql_string):
        self.EQ.setParseAction(lambda: " ")
        self.NE.setParseAction(lambda: " !")
        super().__init__(rql_string)

    def get_condition(self, fn):
        operator = fn[0].lower()
        if operator in (self.AND, self.OR):
            condition = self.get_boolean(operator, fn[1:])
        else:
            value = Converter.convert(fn[2], add_quote=False)
            condition = f"(@{fn[1]}{operator}{value})"

        return condition

    def get_boolean(self, operator, operands):
        if operator == self.AND:
            joiner = " "
        elif operator == self.OR:
            joiner = " | "
        else:
            raise NotImplementedError

        result = self.make_query(operands)
        condition = joiner.join(result)
        return f"({condition})"
