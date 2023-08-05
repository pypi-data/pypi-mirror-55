class SyntaxIPError(Exception):
    def __init__(self):
        self.message = "La sintaxis de la IP es incorrecta."

    def __str__(self):
        return self.message
