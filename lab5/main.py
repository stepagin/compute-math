import numpy as np

from InputManager import InputManager
from solvers import Lagrange, Gaussian, StirlingAndBessel, PreparedFunctionSolver

working_flag = True
points = []


def stop_program():
    global working_flag
    working_flag = False

def sort_and_delete_dublicates(points):
    points.sort()
    i = 1
    while i < len(points):
        if points[i][0] == points[i - 1][0]:
            points[i - 1] = (points[i - 1][0], (points[i - 1][1] + points[i][1]) / 2)
            points.pop(i)
        else:
            i += 1
    return points

def enter_points():
    global points
    if InputManager.yes_or_no_input("Хотите считать точки из файла?"):
        while True:
            filename = InputManager.string_input("Введите название файла: ")
            try:
                file = open(filename, "r")
                n = int(file.readline())
                if n < 2:
                    print("Точек должно быть не менее двух!")
                    raise ValueError
                points = []
                for i in range(n):
                    x, y = map(float, file.readline().split())
                    points.append((x, y))
                file.close()
                break
            except FileNotFoundError:
                print("Не удалось найти указанный файл.")
            except ValueError:
                print("Не удалось считать данные из файла.")
    else:
        n = InputManager.int_input("Введите количество точек: ")
        while n < 2:
            print("Точек должно быть не менее двух!")
            n = InputManager.int_input("Введите количество точек: ")
        points = []
        print(f"Введите x y координаты {n} точек через пробел.")
        for i in range(n):
            x, y = InputManager.point_input(f"Координаты точки {i + 1}: ")
            points.append((x, y))

    points = sort_and_delete_dublicates(points)

    if len(points) < 2:
        print("Различных точек должно быть не менее двух!")
        return enter_points()
    print("Исходный набор точек:", points)
    return points


def save_points():
    global points
    filename = InputManager.string_input("Введите название файла: ")
    try:
        with open(filename, "w") as f:
            f.writelines(str(len(points)) + "\n")
            f.writelines([f"{x} {y}\n" for x, y in points])
    except Exception:
        print("Не удалось сохранить точки в указанный файл.")


def lagrange_solver():
    solver = Lagrange(points)
    solver.solve()


def gaussian_solver():
    solver = Gaussian(points)
    solver.solve()


def prepared_function_solver():
    global points
    variants = ["y = sin(x)",
                "y = x * e^(sin(3x/5)) - 3.44",
                "y = x^3 - 3x^2 + 2"]
    values = [PreparedFunctionSolver(lambda x: np.sin(x)),
              PreparedFunctionSolver(lambda x: x * np.exp(np.sin(3 / 5 * x)) - 3.44),
              PreparedFunctionSolver(lambda x: x ** 3 - 3 * x ** 2 + 2)]

    chosen_variant = InputManager.multiple_choice_input(variants, values, "Выберите функцию:")

    if InputManager.yes_or_no_input("Показать график выбранной функции?"):
        chosen_variant.draw_init_graphic()

    n = InputManager.int_input("Введите количество точек для интерполирования: ")
    while n < 2:
        print("Точек должно быть не менее двух!")
        n = InputManager.int_input("Введите количество точек для интерполирования: ")
    points_x = []
    points = []
    for i in range(n):
        x = InputManager.float_input(f"Введите x-координату точки {i + 1}: ")
        while x in points_x:
            print("Такая координата уже была.")
            x = InputManager.float_input(f"Введите x-координату точки {i + 1}: ")
        points.append((x, chosen_variant.f(x)))
        points_x.append(x)
    del points_x
    points = sort_and_delete_dublicates(points)
    solver = Lagrange(points)

    solver.solve(draw_graphic=False)

    chosen_variant.draw_two_graphics(solver.f, points)



def stirling_and_bessel_solver():
    solver = StirlingAndBessel(points)
    solver.solve()


if __name__ == '__main__':
    variants = ["Ввести точки", "Интерполировать функцию из предложенных"] + ["Выйти из программы"]
    values = [enter_points, prepared_function_solver] + [stop_program]

    chosen_variant = InputManager.multiple_choice_input(variants, values, "Выберите нужный вариант:")
    chosen_variant()

    variants = ["Ввести точки заново", "Сохранить введённый набор точек", "Решить методом Лагранжа",
                "Решить методом Гаусса", "Интерполировать функцию из предложенных",
                "Вычислить значение функции, используя схемы Стирлинга и Бесселя"] + ["Выйти из программы"]
    values = [enter_points, save_points, lagrange_solver, gaussian_solver, prepared_function_solver,
              stirling_and_bessel_solver] + [stop_program]

    while working_flag:
        chosen_variant = InputManager.multiple_choice_input(variants, values, "Выберите нужный вариант:")
        chosen_variant()
        print()
