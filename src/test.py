# Dada la siguiente tupla, crear una lista que sólo incluya los números menor que 5 utilizando un ciclo for:

tupla = (13, 1, 8, 3, 2, 5, 8)
lista = []
for item in tupla:
    if item < 5:
        lista.append(item)
print(lista)

def suma(*args):
    resultado = 0
    for item in args:
        if type(item) == int:
            resultado += item
        elif type(item) == float:
            resultado += round(item)
        print(type(item))
    return resultado
print(suma(3,5, '6?', 3.0, 3.5))

def multi(*args):
    resultado = 1
    for item in args:
        if type(item) == int:
            resultado *= item
        elif type(item) == float:
            resultado *= round(item)
        print(type(item))
    return resultado
print(multi(3,5, '6?', 3.0, 3.5))

def recursiva(numero):
    if numero >= 1:
        print(numero)
        recursiva(numero-1)

recursiva(5)