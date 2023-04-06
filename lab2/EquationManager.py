import re

import numpy as np
from math import sin, cos, asin, acos, tan, atan, log2, log10
from numpy import log as ln, log10 as lg
from numpy import log10 as log_10
from numpy import log2 as log_2
from numpy.lib.scimath import logn
from numpy.lib.scimath import logn as log_n

from Exceptions import InvalidVectorException
from InputManager import InputManager


class Equation:
    equation = ""
    raw_equation = ""
    var_names = []
    var_values = dict([("pi", np.pi), ("e", np.e)])
    _valid_vars_template = re.compile(r"[a-zA-Z_]+[0-9]*")
    _valid_functions_template = re.compile(r"a?sin|lg|a?cos|a?tan|log_?(?:2|10)?|logn|pi|e")

    # _valid_vars_template = re.compile(r"[a-zA-Z](?:_[0-9]*)?") # другой вариант выделений переменных

    def __init__(self, line):
        self.equation = line
        self.raw_equation = line
        self.var_names = self.find_vars()
        # print(self.var_names)

    def find_vars(self):
        vars = []
        for i in self._valid_vars_template.findall(self.equation):
            if self._valid_functions_template.fullmatch(i) is None and i not in vars:
                vars.append(i)
        return vars

    def set_valid_vars_template(self, template):
        self._valid_vars_template = template
        self.var_names = self._valid_vars_template.findall(self.raw_equation)

    def get_var_list(self):
        return self.var_names.copy()

    def _get_variable_value_with_match(self, match, x_vector_dict):
        name = match.group(0)
        value = x_vector_dict.get(name, None)
        if value is None:
            return name
        return f'({value})'

    def calculate(self, x_vector_dict={}):
        expression = self.equation

        expression = re.sub(self._valid_vars_template, lambda m: self._get_variable_value_with_match(m, x_vector_dict),
                            expression)
        expression = re.sub(r"\d+(?:\.\d+)?", lambda x: f'({x.group(0)})', expression)
        expression = expression.replace(")(", ")*(")
        # print(expression)
        return eval(expression)



