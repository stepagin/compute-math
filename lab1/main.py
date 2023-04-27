from MartixManager import MatrixContainer
from InputManager import InputManager
import numpy as np
import os, sys

if __name__ == "__main__":
    print("Добро пожаловать в решатель СЛАУ методом Гаусса-Зейделя!\n")

    matrix_container = MatrixContainer()

    if InputManager.yes_or_no_input("Хотите считать матрицу из csv-файла? [yes/no]: "):
        filename = InputManager.string_input('Введите название файла без ".csv": ')
        try:
            m = np.genfromtxt(filename + '.csv', delimiter=',')
        except ValueError:
            print("Матрица некорректна.")
            os.system("pause")
            sys.exit()
        except OSError:
            print("Файл не найден.")
            os.system("pause")
            sys.exit()

    else:
        m = InputManager.matrix_input()

    matrix_container.set_matrix(m)

    print("Хотите ввести точность? По умолчанию epsilon равно 10^-8.")
    if InputManager.yes_or_no_input("Ввести epsilon? [yes/no]: "):
        matrix_container.set_epsilon(InputManager.float_input("epsilon="))

    if matrix_container.find_determinant() == 0:
        print("Нахождение корней невозможно: определитель матрицы равен нулю")
    else:
        matrix_container.solve()

    os.system("pause")
