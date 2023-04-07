from InputManager import InputManager
from IntegralManager import Integral
from IntegralSolver import Integrate

if __name__ == "__main__":
    variants = ["x^3 - 3x^2 + 7x - 10",
                "2x^3 - 5x^2 - 3x + 21",
                "7x^3 - 2x^2 - 9x + 36"]
    values = [Integral(lambda x: x ** 3 - 3 * x ** 2 + 7 * x - 10),
              Integral(lambda x: 2 * x ** 3 - 5 * x ** 2 - 3 * x + 21),
              Integral(lambda x: 7 * x ** 3 - 2 * x ** 2 - 9 * x + 36)]
    integral = InputManager.multiple_choice_input(variants, values, "Выберите функцию для интегрирования:")

    variants = ["Метод прямоугольника - левый", "Метод прямоугольника - центр", "Метод прямоугольника - правый",
                "Метод трапеций", "Метод Симпсона"]
    values = [Integrate.left_rectangle, Integrate.center_rectangle, Integrate.right_rectangle,
              Integrate.trapezoid_method, Integrate.simpson_method]
    method = InputManager.multiple_choice_input(variants, values, "Выберите метод интегрирования:")

    left = InputManager.float_input("Введите левый предел интегрирования: ")
    right = InputManager.float_input("Введите правый предел интегрирования: ")
    while not left < right:
        print("Левый предел должен быть меньше правого.")
        left = InputManager.float_input("Введите левый предел интегрирования: ")
        right = InputManager.float_input("Введите правый предел интегрирования: ")

    result = integral.solve(left, right, method)

    print("------------РЕШЕНИЕ------------")
    print("Результат вычисления:", result)
    print("Число разбиений:", integral.steps)
    if InputManager.yes_or_no_input("Нарисовать график функции?"):
        integral.draw_func(left, right)
