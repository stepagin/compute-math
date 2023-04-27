class Integrate:

    @staticmethod
    def left_rectangle(integral, left, right, n):
        result = 0
        step = abs(left - right) / n
        i = left
        while i < right:
            result += integral.calculate(i)
            i += step
        return result * step

    @staticmethod
    def center_rectangle(integral, left, right, n):
        result = 0
        step = abs(left - right) / n
        i = left + step / 2
        while i < right:
            result += integral.calculate(i)
            i += step
        return result * step

    @staticmethod
    def right_rectangle(integral, left, right, n):
        result = 0
        step = abs(left - right) / n
        i = left + step
        while i <= right:
            result += integral.calculate(i)
            i += step
        return result * step

    @staticmethod
    def trapezoid_method(integral, left, right, n):
        result = 0
        step = abs(left - right) / n
        i = left + step
        while i < right:
            result += integral.calculate(i)
            i += step
        result += (integral.calculate(left) + integral.calculate(right)) / 2
        return result * step

    @staticmethod
    def simpson_method(integral, left, right, n):
        result = 0
        step = abs(left - right) / n
        for i in range(1, n):
            if i % 2:
                result += 2 * integral.calculate(left + step * i)
            else:
                result += 4 * integral.calculate(left + step * i)
        result += integral.calculate(left) + integral.calculate(right)
        return result * step / 3
