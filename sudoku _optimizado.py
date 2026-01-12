import random
import matplotlib.pyplot as plt

# ---------------- SUDOKU BASE ----------------
SUDOKU = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

# ---------------- UTILIDAD ----------------
def mostrar(tablero, titulo="Sudoku"):
    print("\n" + titulo)
    for i in range(9):
        if i % 3 == 0:
            print("-"*21)
        for j in range(9):
            if j % 3 == 0:
                print("|", end=" ")
            print(tablero[i][j], end=" ")
        print("|")
    print("-"*21)

# ---------------- INDIVIDUO ----------------
def crear_individuo(tablero):
    """Crea individuo con filas válidas (1-9 sin repetir)"""
    ind = []
    for fila in tablero:
        fijos = [n for n in fila if n != 0]
        libres = [n for n in range(1,10) if n not in fijos]
        random.shuffle(libres)
        ind.append([n if n != 0 else libres.pop() for n in fila])
    return ind

# ---------------- FITNESS ----------------
def fitness(tablero):
    """Cuenta conflictos en columnas y bloques 3x3"""
    f = 0
    # Columnas
    for i in range(9):
        f += 9 - len(set(tablero[j][i] for j in range(9)))
    # Bloques 3x3
    for x in range(0,9,3):
        for y in range(0,9,3):
            f += 9 - len({tablero[x+i][y+j] for i in range(3) for j in range(3)})
    return f

# ---------------- SELECCIÓN ----------------
def seleccionar(pob):
    """Selección por torneo de 3 individuos"""
    candidatos = random.sample(pob, 3)
    return min(candidatos, key=fitness)

# ---------------- REPRODUCCIÓN (CORREGIDO) ----------------
def reproducir(p1, p2, base, mut=0.3):
    """
    Cruce + mutación respetando filas válidas
    - Cruce por punto de corte (filas completas)
    - Mutación intercambia dentro de filas
    """
    hijo = []
    corte = random.randint(1, 8)
    
    # Cruce: primera parte de p1, segunda de p2
    for i in range(9):
        if i < corte:
            hijo.append(list(p1[i]))
        else:
            hijo.append(list(p2[i]))
    
    # Mutación: intercambiar valores no fijos en varias filas
    num_mutaciones = random.randint(1, 3)
    for _ in range(num_mutaciones):
        i = random.randint(0, 8)
        libres = [j for j in range(9) if base[i][j] == 0]
        if len(libres) >= 2:
            a, b = random.sample(libres, 2)
            hijo[i][a], hijo[i][b] = hijo[i][b], hijo[i][a]
    
    return hijo

# ---------------- ALGORITMO GENÉTICO ----------------
def algoritmo_genetico(tablero, poblacion=100, generaciones=1000):
    """Algoritmo genético con elitismo"""
    print("🧬 Iniciando algoritmo genético...")
    print(f"Población: {poblacion} | Generaciones: {generaciones}")
    
    # Población inicial
    pob = [crear_individuo(tablero) for _ in range(poblacion)]
    hist = []
    
    for g in range(generaciones):
        # Ordenar por fitness (menor = mejor)
        pob = sorted(pob, key=fitness)
        best = fitness(pob[0])
        hist.append(best)
        
        # Verificar solución
        if best == 0:
            print(f"\n🎉 ¡Solución encontrada en generación {g}!")
            return pob[0], hist
        
        # Elitismo: mantener top 10%
        elite = pob[:poblacion//10]
        nueva = elite[:]
        
        # Crear nueva generación
        while len(nueva) < poblacion:
            p1 = seleccionar(pob)
            p2 = seleccionar(pob)
            nueva.append(reproducir(p1, p2, tablero))
        
        pob = nueva
        
        # Progreso
        if g % 50 == 0:
            print(f"Gen {g:4d} | Mejor fitness: {best:3d}")
    
    print(f"\n⚠️ No se encontró solución perfecta en {generaciones} generaciones")
    return pob[0], hist

# ---------------- EJECUCIÓN ----------------
print("="*50)
print("PROYECTO: SUDOKU CON ALGORITMOS GENÉTICOS")
print("="*50)

mostrar(SUDOKU, "SUDOKU INICIAL")

# Ejecutar algoritmo
solucion, historial = algoritmo_genetico(SUDOKU)

# Resultados
mostrar(solucion, "MEJOR SOLUCIÓN ENCONTRADA")
print(f"\n📊 Fitness final: {fitness(solucion)}")

if fitness(solucion) == 0:
    print("✅ Sudoku resuelto correctamente")
else:
    print(f"⚠️ Quedan {fitness(solucion)} conflictos")

# ---------------- GRÁFICA ----------------
plt.figure(figsize=(10, 6))
plt.plot(historial, linewidth=2, color='blue')
plt.xlabel("Generación", fontsize=12)
plt.ylabel("Fitness (conflictos)", fontsize=12)
plt.title("Evolución del Fitness - Algoritmo Genético", fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()