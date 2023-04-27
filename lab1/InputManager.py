import numpy as np


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
        if InputManager._check_number(num):
            return float(num.replace(',', '.'))
        return None

    @staticmethod
    def float_input(message=""):
        while True:
            buf = InputManager.string_input(message)
            if InputManager._check_number(buf):
                return InputManager._convert_to_number(buf)

    @staticmethod
    def int_input(message=""):
        return int(InputManager.float_input(message))

    @staticmethod
    def yes_or_no_input(message=""):
        answer = "0"
        while answer[0].lower() not in ["y", "n"]:
            answer = InputManager.string_input(message)
        return answer[0].lower() == "y"

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
