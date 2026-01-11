import numpy as np
import random

# Sudoku de prueba
sudoku_inicial = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# TODO: implementar algoritmo genetico
print("Sudoku inicial cargado")

def mostrar_sudoku(tablero):
    # funcion para ver el sudoku mas bonito
    print("\n")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        linea = ""
        for j in range(9):
            if j % 3 == 0 and j != 0:
                linea += "| "
            if tablero[i][j] == 0:
                linea += ". "
            else:
                linea += str(tablero[i][j]) + " "
        print(linea)
    print("\n")

# probar la funcion
mostrar_sudoku(sudoku_inicial)