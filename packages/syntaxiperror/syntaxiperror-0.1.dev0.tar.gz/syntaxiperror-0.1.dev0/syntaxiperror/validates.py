import math

from syntaxiperror.error import SyntaxIPError


def SyntaxIP(val):
    ip = val.split(".")
    cont = 0
    veri = 0
    for celda in ip:
        octeto = int(celda)
        if octeto == 0:
            cont += 1
        else:
            try:
                if math.log(octeto, 2) + 1 < 9:
                    cont += 1
            except ValueError:
                print("Ingreso un numero negativo")
    if veri > 4:
        cont = 0
    return cont == 4


def validate_address(val):
    try:
        return isinstance(val, str)
    except ValueError:
        return False


def address(val):
    try:
        if validate_address(val) and SyntaxIP(val):
            print("La sintaxis de la IP es correcta.")
        else:
            raise SyntaxIPError()
    except SyntaxIPError as error:
        print(error)
        return False
    else:
        return True
