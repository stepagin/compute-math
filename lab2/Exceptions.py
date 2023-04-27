class InvalidVectorException(ValueError):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class InvalidAlgebraicEquationException(ValueError):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
