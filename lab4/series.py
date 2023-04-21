from InputManager import InputManager


class SeriesManager():
    def __init__(self):
        self.n = 0
        self.X = []
        self.Y = []

    def drop_context(self):
        self.n = 0
        self.X = []
        self.Y = []

    def enter_points(self):
        self.drop_context()
        while True:
            if InputManager.yes_or_no_input("Хотите считать точки из файла?"):
                filename = InputManager.string_input("Введите имя файла: ")
                try:
                    self._enter_points_from_file(filename)
                    break
                except FileNotFoundError:
                    print("Файл не найден.")
                except Exception:
                    print("Произошла ошибка во время считывания. Проверьте содержание файла.")
            else:
                self._enter_points_from_console()
                break

    def _enter_points_from_file(self, filename):
        file = open(filename, "r")
        self.n = int(file.readline())
        if self.n < 5 or self.n > 12:
            print("Необходимо ввести не менее 8 и не более 12 точек.")
            raise ValueError
        for i in range(self.n):
            x, y = map(float, file.readline().split())
            self.X.append(x)
            self.Y.append(y)
        file.close()

    def _enter_points_from_console(self):
        self.n = InputManager.int_input_with_borders(8, 12, "Введите число точек от 8 до 12: ")
        print("Теперь введите x y координаты точек через пробел.")
        for i in range(self.n):
            x, y = InputManager.point_input(f"Координаты точки {i + 1}: ")
            self.X.append(x)
            self.Y.append(y)

    def set_n(self, n):
        self.n = n

    def set_x(self, x):
        self.X = x
        self.n = min(len(x), self.n)

    def set_y(self, y):
        self.Y = y
        self.n = min(len(y), self.n)

    def set_xy(self, x, y):
        self.set_n(min(len(x), len(y)))
        self.set_x(x)
        self.set_y(y)

    def print_points(self):
        print("Исходные точки: ", end="")
        print(*[f"({self.X[i]}, {self.Y[i]})" for i in range(self.n)], sep=", ")

    def copy(self):
        sm = SeriesManager()
        sm.set_n(self.n)
        sm.set_x(self.X)
        sm.set_y(self.Y)
        return sm
