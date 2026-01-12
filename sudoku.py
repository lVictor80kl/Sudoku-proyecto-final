import numpy as np
import random
import matplotlib.pyplot as plt

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
print("="*50)
print("PROYECTO: SUDOKU CON ALGORITMOS GENÉTICOS")
print("="*50)
print("\nSudoku inicial cargado correctamente")
print(f"Celdas vacías: {sum(row.count(0) for row in sudoku_inicial)}")

def mostrar_sudoku(tablero, titulo="Sudoku"):
    """Muestra el sudoku de forma visual con separadores"""
    print(f"\n{titulo}")
    print("-" * 25)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 25)
        linea = ""
        for j in range(9):
            if j % 3 == 0 and j != 0:
                linea += "| "
            if tablero[i][j] == 0:
                linea += ". "
            else:
                linea += str(tablero[i][j]) + " "
        print(linea)
    print("-" * 25)

# Probar visualización
mostrar_sudoku(sudoku_inicial, "SUDOKU INICIAL")
print(f"\nCeldas vacías: {sum(row.count(0) for row in sudoku_inicial)}")

def obtener_posiciones_fijas(tablero):
    """
    Identifica qué celdas tienen valores fijos (no pueden cambiar)
    Retorna una matriz booleana del mismo tamaño
    """
    fijas = []
    for i in range(9):
        fila_fijas = []
        for j in range(9):
            # Si la celda tiene un número (no es 0), es fija
            fila_fijas.append(tablero[i][j] != 0)
        fijas.append(fila_fijas)
    return fijas

def estadisticas_tablero(tablero, fijas):
    """Muestra estadísticas del tablero"""
    total_celdas = 81
    celdas_fijas = sum(sum(fila) for fila in fijas)
    celdas_vacias = total_celdas - celdas_fijas
    
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"  Total de celdas: {total_celdas}")
    print(f"  Celdas fijas: {celdas_fijas}")
    print(f"  Celdas a llenar: {celdas_vacias}")
    print(f"  Porcentaje completo: {(celdas_fijas/total_celdas)*100:.1f}%")

# Probar
posiciones_fijas = obtener_posiciones_fijas(sudoku_inicial)
estadisticas_tablero(sudoku_inicial, posiciones_fijas)

def crear_individuo(tablero_original, fijas):
    """
    Crea un individuo (tablero completo de sudoku)
    
    ESTRATEGIA:
    - Cada fila debe tener números del 1 al 9 sin repetir
    - Respeta los números fijos del sudoku original
    - Llena las celdas vacías con números aleatorios disponibles
    
    Esto garantiza que no haya conflictos en las filas
    """
    nuevo_tablero = []
    
    for i in range(9):
        fila = list(tablero_original[i])
        
        # Obtener números que ya están fijos en esta fila
        numeros_fijos = [fila[j] for j in range(9) if fijas[i][j]]
        
        # Números disponibles: los que no están fijos en la fila
        disponibles = [n for n in range(1, 10) if n not in numeros_fijos]
        random.shuffle(disponibles)
        
        # Llenar las celdas vacías con números disponibles
        indice = 0
        for j in range(9):
            if not fijas[i][j]:  # Si la celda no es fija
                fila[j] = disponibles[indice]
                indice += 1
        
        nuevo_tablero.append(fila)
    
    return nuevo_tablero

# Probar creación de individuo
print("\n" + "="*50)
print("CREACIÓN DE INDIVIDUO")
print("="*50)

individuo_test = crear_individuo(sudoku_inicial, posiciones_fijas)
mostrar_sudoku(individuo_test, "INDIVIDUO GENERADO (tablero completo)")

# Verificar que no hay repeticiones en filas
print("\n✓ Verificando que no haya repeticiones en filas...")
for i, fila in enumerate(individuo_test):
    if len(set(fila)) != 9:
        print(f"  ⚠ Error en fila {i+1}")
    else:
        print(f"  ✓ Fila {i+1}: OK")
print("✓ Todas las filas tienen números del 1-9 sin repetir")

def crear_poblacion(tablero_original, fijas, tamaño=100):
    """
    Crea la población inicial de individuos
    
    Args:
        tablero_original: Sudoku inicial con celdas vacías
        fijas: Matriz de posiciones fijas
        tamaño: Número de individuos en la población
    
    Returns:
        Lista de individuos (tableros completos)
    """
    poblacion = []
    print(f"\n🧬 Generando población de {tamaño} individuos...")
    
    for i in range(tamaño):
        individuo = crear_individuo(tablero_original, fijas)
        poblacion.append(individuo)
        
        # Mostrar progreso cada 20 individuos
        if (i + 1) % 20 == 0:
            print(f"  Generados: {i+1}/{tamaño}")
    
    print(f"✓ Población inicial creada: {len(poblacion)} individuos")
    return poblacion

def mostrar_muestra_poblacion(poblacion, n=3):
    """Muestra una muestra de individuos de la población"""
    print(f"\n📋 MUESTRA DE LA POBLACIÓN (primeros {n} individuos):")
    for i in range(min(n, len(poblacion))):
        mostrar_sudoku(poblacion[i], f"Individuo #{i+1}")

# Crear población inicial
TAMAÑO_POBLACION = 50  # Empezamos con 50 para pruebas
poblacion = crear_poblacion(sudoku_inicial, posiciones_fijas, TAMAÑO_POBLACION)

# Mostrar muestra
mostrar_muestra_poblacion(poblacion, 2)

print("\n" + "="*50)
print("PARTE 1 COMPLETADA: Representación del individuo ✓")
print("="*50)

# PARTE 2: ALGORITMO GENÉTICO

def calcular_fitness(tablero):
    """
    Calcula el fitness de un tablero de Sudoku.
    Fitness = número de conflictos (duplicados en columnas y cajas 3x3)
    Menor fitness es mejor (0 = solución perfecta)
    """
    fitness = 0
    
    # Verificar columnas
    for j in range(9):
        columna = [tablero[i][j] for i in range(9)]
        fitness += 9 - len(set(columna))  # Número de duplicados
    
    # Verificar cajas 3x3
    for caja_i in range(0, 9, 3):
        for caja_j in range(0, 9, 3):
            caja = []
            for i in range(3):
                for j in range(3):
                    caja.append(tablero[caja_i + i][caja_j + j])
            fitness += 9 - len(set(caja))  # Número de duplicados
    
    return fitness
