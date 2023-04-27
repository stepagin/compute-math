import numpy as np
from MatrixError import MatrixError


class MatrixContainer:
    def __init__(self):
        self.matrix = None
        self.constants = None
        self.lines_number = None
        self.determinant = None
        self.epsilon = None
        self._drop_context()

    def _drop_context(self):
        self.lines_number = 0
        self.constants = []  # b vector
        self.matrix = []  # coefficients matrix
        self.solutions = []  # x vector
        self.lines_swapped = 0
        self.iterations_count = 0
        self.epsilon = 0.00000001

    def set_matrix(self, matrix):
        self._drop_context()
        self.matrix = matrix[:, :-1]
        self.constants = matrix[:, -1]
        self.lines_number = matrix.shape[0]
        self.solutions = np.zeros(self.lines_number)

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def calculate_discrepancies(self):
        try:
            return max(abs(self.matrix.dot(self.solutions) - self.constants))
        except ValueError:
            return np.inf

    def _add_any_line(self, matrix, target_string, target_element):
        """
        Добавляет к строке target_string любую строку так,
        чтобы в позиции target_element не было нуля
        """
        if matrix[target_string][target_element] == 0:
            for i in range(self.lines_number):
                if matrix[target_string][target_element] + matrix[i][target_element] != 0:
                    matrix[target_string] += matrix[i]
                    break

        return matrix

    def find_determinant(self):
        if self.determinant is not None:
            return self.determinant
        self.determinant = round(np.linalg.det(self.matrix), 11)
        return self.determinant

    def _start_calculating(self):
        n = self.lines_number
        # Начальные значения вектора Х задаются нулями
        self.solutions = np.zeros(n)  # X vector

        coeffs_matrix = np.zeros((n, n))  # C's matrix
        # заполнение coeffs_matrix
        for i in range(n):
            if self.matrix[i][i] == 0:
                # эта функция заполняет нули на диагонали
                self._add_any_line(self.matrix, i, i)
            coeffs_matrix[i] = self.matrix[i] / self.matrix[i][i]
        np.fill_diagonal(coeffs_matrix, 0)  # заполнение диагонали coeffs_matrix нулями

        # на данный момент на диагонали matrix нет нулей
        free_members = self.constants / np.diag(self.matrix)  # D's vector

        # Начало решения
        k = self.iterations_count
        self.solutions = np.zeros(n)
        last_discrepancies = self.calculate_discrepancies()
        while last_discrepancies > self.epsilon and k < 99999:
            # Если бы мы использовали метод простой итерации:
            # self.solutions = free_members - coeffs_matrix.dot(self.solutions)

            # Метод Гаусса-Зейделя заключается в том, что элементы вектора иксов берутся из предыдущей итерации
            for i in range(n):
                self.solutions[i] = free_members[i] - sum(coeffs_matrix[i] * self.solutions)

            k += 1
            if last_discrepancies - self.calculate_discrepancies() < 0:
                raise MatrixError("Итерационный метод расходится.")
            last_discrepancies = self.calculate_discrepancies()

        self.iterations_count += k

        return True

    def solve(self):
        if self.matrix == [] or self.lines_number == 0:
            print("Матрица не задана.")
            return
        if self.find_determinant() == 0:
            print("Определитель матрицы равен нулю. Матрица имеет бесконечное число решений.")
            return
        try:
            self._start_calculating()
            print("______________РЕШЕНИЕ______________")
            print("Определитель:", self.determinant)
            print("Количество итераций:", self.iterations_count)
            print("Вектор решений:", self.solutions)
            print("Расхождение:", self.calculate_discrepancies())
            print("___________________________________")
        except MatrixError:
            print("У данной матрицы итерационный метод расходится. \n"
                  "Попробуйте поменять местами столбцы так, чтобы в каждой строке диагональные "
                  "элементы были больше суммы остальных.")
        except Exception:
            print("Не удалось найти решение для данной матрицы. Попробуйте другую")
        return
