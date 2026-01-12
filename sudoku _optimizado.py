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
    ind = []
    for fila in tablero:
        fijos = [n for n in fila if n != 0]
        libres = [n for n in range(1,10) if n not in fijos]
        random.shuffle(libres)
        ind.append([n if n != 0 else libres.pop() for n in fila])
    return ind

# ---------------- FITNESS ----------------
def fitness(tablero):
    f = 0
    for i in range(9):
        f += 9 - len(set(tablero[j][i] for j in range(9)))
    for x in range(0,9,3):
        for y in range(0,9,3):
            f += 9 - len({tablero[x+i][y+j] for i in range(3) for j in range(3)})
    return f

# ---------------- REPRODUCCIÓN ----------------
def reproducir(p1, p2, base, mut=0.1):
    hijo = []
    for i in range(9):
        fila = list(p1[i] if random.random() < 0.5 else p2[i])
        # respetar celdas fijas
        for j in range(9):
            if base[i][j] != 0:
                fila[j] = base[i][j]
        # mutación
        if random.random() < mut:
            libres = [j for j in range(9) if base[i][j] == 0]
            if len(libres) >= 2:
                a,b = random.sample(libres,2)
                fila[a], fila[b] = fila[b], fila[a]
        hijo.append(fila)
    return hijo

# ---------------- ALGORITMO GENÉTICO ----------------
def algoritmo_genetico(tablero, poblacion=80, generaciones=1000):
    pob = [crear_individuo(tablero) for _ in range(poblacion)]
    hist = []

    for g in range(generaciones):
        pob = sorted(pob, key=fitness)
        best = fitness(pob[0])
        hist.append(best)

        if best == 0:
            print(f"\n🎉 Solución encontrada en generación {g}")
            return pob[0], hist

        elite = pob[:poblacion//10]
        nueva = elite[:]

        while len(nueva) < poblacion:
            p1, p2 = random.sample(pob[:20], 2)
            nueva.append(reproducir(p1, p2, tablero))

        pob = nueva

        if g % 50 == 0:
            print(f"Gen {g} | Mejor fitness: {best}")

    return pob[0], hist

# ---------------- EJECUCIÓN ----------------
solucion, historial = algoritmo_genetico(SUDOKU)

mostrar(SUDOKU, "Sudoku inicial")
mostrar(solucion, "Mejor solución encontrada")
print("Fitness final:", fitness(solucion))


# ---------------- GRÁFICA ----------------
plt.plot(historial)
plt.xlabel("Generación")
plt.ylabel("Fitness")
plt.title("Evolución del fitness")
plt.grid()
plt.show()

