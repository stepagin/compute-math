import numpy as np

from Exceptions import InvalidAlgebraicEquationException


class InputManager:
    @staticmethod
    def string_input(message=""):
        buf = ""
        while buf == "":
            buf = input(message).strip()
        return buf

    @staticmethod
    def _check_number(buf):
        try:
            float(buf.replace(',', '.'))
            return True
        except ValueError:
            return False

    @staticmethod
    def _convert_to_number(num):
        try:
            return float(num.replace(',', '.'))
        except ValueError:
            return None

    @staticmethod
    def float_input(message=""):
        number = None
        while number is None:
            number = InputManager._convert_to_number(InputManager.string_input(message))
        return number

    @staticmethod
    def int_input(message=""):
        return int(InputManager.float_input(message))

    @staticmethod
    def yes_or_no_input(message=""):
        answer = "0"
        while answer[0].lower() not in ["y", "n", "д", "н"]:
            answer = InputManager.string_input(message + " [y/n]: ")
        return answer[0].lower() in ["y", "д"]

    @staticmethod
    def matrix_input():
        lines_number = InputManager.int_input("Введите количество строк матрицы: ")
        print("Введите матрицу вида\n"
              "a_11, a_12, ..., a_1n, b_1\n"
              "...\n"
              "a_n1, a_n2, ..., a_nn, b_n\n")
        matrix = [[0] * (lines_number + 1) for _ in range(lines_number)]
        for i in range(lines_number):
            line = InputManager.string_input().split()
            while len(line) != lines_number + 1 or not all([InputManager._check_number(t) for t in line]):
                print("Некорректный ввод строки")
                line = InputManager.string_input().split()
            for j in range(lines_number + 1):
                matrix[i][j] = InputManager._convert_to_number(line[j])
        print()
        return np.array(matrix)

    """
    x => x = 0
    ln(x) => ln(x) = 0
    log_2(x)
    sin(x)
    x^2 - x
    cos(x)^2 + sin(x)^2 - 1
    cos(x)^2+sin(x)^2-1
    cos(x_1)^2)+sin(x_2)^2 = 0
    
    нижний индекс поддерживается только у:
        логарифма
        икса (сначала идёт индекс, потом степень - x_1^2
    
    
    """

    @staticmethod
    def algebraic_expression_input(message=""):
        line = InputManager.string_input(message)
        line = line.replace(" ", "")
        line = line.replace(",", ".")
        line = line.replace("^", "**")
        if line.__contains__('='):
            raise InvalidAlgebraicEquationException
        return line

        pass

    @staticmethod
    def vector_dict_input(var_names, message=""):
        if message != "":
            print(message)
        result = dict()
        for name in var_names:
            result[name] = InputManager.float_input(f"\tВведите {name}: ")
        return result

    @staticmethod
    def enum_input(variants_list, message):
        buf = ""
        while buf not in variants_list:
            buf = InputManager.string_input(message)
        return buf

    @staticmethod
    def multiple_choice_input(variant_list, values_list, message=""):
        n = len(variant_list)
        if n == 0 or len(variant_list) != len(values_list):
            raise ValueError

        if message != "":
            print(message)

        for i in range(n):
            s = f"{i + 1}."
            lines = variant_list[i].split('\n')
            print('\t' + s, lines[0])
            for line in lines[1:]:
                print("\t" + ' ' * len(s), line)

        i = int(InputManager.enum_input([str(i) for i in range(1, n + 1)], f"Введите число от 1 до {n}: ")) - 1
        return values_list[i]

