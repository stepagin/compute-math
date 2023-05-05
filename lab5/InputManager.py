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
    def enum_input(variants_list, message=""):
        variants_list = [str(i) for i in variants_list]
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

        i = int(InputManager.enum_input([*range(1, n + 1)], f"Введите число от 1 до {n}: "))
        return values_list[i - 1]

    @staticmethod
    def epsilon_input(message=""):
        e = InputManager.float_input(message)
        while not (0 < e and e <= 1):
            print("Эпсилон должно быть в промежутке от 0 до 1!")
            e = InputManager.float_input(message)
        return e

    @staticmethod
    def int_input_with_borders(left, right, message=""):
        if left >= right:
            raise ValueError
        if message != "":
            print(message)
        i = int(InputManager.enum_input([*range(left, right + 1)], f"Введите число от {left} до {right}: "))
        return i

    @staticmethod
    def point_input(message=""):
        x, y = None, None
        while x is None or y is None:
            line = InputManager.string_input(message).split()
            if len(line) != 2:
                continue
            x, y = InputManager._convert_to_number(line[0]), InputManager._convert_to_number(line[1])
        return x, y

    @staticmethod
    def float_input_with_borders(left, right, message=""):
        if not left < right:
            raise ValueError
        x = InputManager.float_input(message)
        while not (left < x < right):
            print(f"Значение должно быть от {left} до {right}!")
            x = InputManager.float_input(message)
        return x
