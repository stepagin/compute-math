from InputManager import InputManager
from series import SeriesManager
from OLS import *

output_result = ""


def my_print(*args):
    global output_result
    print(*args)
    for i in args:
        output_result += str(i) + " "
    output_result += '\n'


if __name__ == '__main__':

    seriesManager = SeriesManager()
    # ввод исходных данных
    seriesManager.enter_points()
    seriesManager.print_points()

    # выбор функции и решение

    variants = ["Линейная функция", "Полиномиальная функция 2-й степени", "Полиномиальная 3-й степени",
                "Экспоненциальная фунция", "Логарифмическая функция", "Степенная функция"]
    values = [LinearFunction, PolynomialFunction2ndDegree, PolynomialFunction3rdDegree,
              ExponentialFunction, LogarithmicFunction, PowerFunction]
    results = []

    best_approximation = None
    for i in range(6):
        my_print(variants[i] + ":")
        function = values[i](seriesManager)
        if function.broken_flag:
            my_print("В аппроксимации учтены не все точки. Решение учитываться не будет.")
            my_print()
        else:
            result = function.solve()
            if function.mse is not None:
                if best_approximation is None:
                    best_approximation = function
                elif best_approximation.mse > function.mse:
                    best_approximation = function
            my_print(result)
            if InputManager.yes_or_no_input("Нарисовать график функции?"):
                function.draw_graphic(seriesManager)
            print()

    if best_approximation is not None:
        my_print("Наилучшее приближение:", best_approximation.method_name)
        my_print("СКО:", round(best_approximation.mse, 4))
    else:
        my_print("Наилучшего приближения не существует.")

    if InputManager.yes_or_no_input("Сохранить результаты в файл?"):
        try:
            filename = InputManager.string_input("Введите имя файла: ")
            with open(filename, "w") as f:
                f.write(output_result)
                f.flush()
        except Exception:
            print("Не удалось сохранить результаты в файл.")

