# Resolución Inteligente de Sudoku mediante Algoritmos Genéticos 🧩

Este proyecto aplica principios de computación Emergente para resolver tableros de Sudoku. Utiliza un enfoque evolutivo donde una población de soluciones candidatas compite y se reproduce, mejorando automáticamente hasta encontrar una configuración válida sin conflictos.

# 📋 Descripción del Modelo

El sistema ha sido modelado siguiendo la arquitectura de un Algoritmo Genético (AG), diseñado para optimizar la disposición de los números del 1 al 9 respetando las reglas clásicas del juego.

# 1. Representación del Individuo
Un "individuo" representa un tablero completo. Para maximizar la eficiencia del modelado, se utiliza una codificación basada en permutaciones por fila:
Cada fila se inicializa con los números faltantes (1-9) de forma aleatoria.
Esto garantiza que nunca existan conflictos en las filas, reduciendo drásticamente el espacio de búsqueda y permitiendo que el algoritmo se concentre en columnas y bloques.

# 2. Función Fitness (Aptitud)
La función de aptitud mide la calidad de una solución contando los errores. El objetivo es minimizar este valor hasta llegar a 0:
Conflictos en Columnas: Penaliza repeticiones en las 9 columnas verticales.
Conflictos en Bloques: Penaliza repeticiones dentro de cada subcuadrícula de $3 \times 3$.

# 🧬 Operadores Genéticos

Se implementaron los siguientes operadores para guiar la evolución:
Selección por Torneo: Se seleccionan candidatos al azar y el más apto gana el derecho a reproducirse. Esto asegura que los mejores genes se transmitan con mayor probabilidad.
Cruce (Crossover) por Punto de Corte: Se combinan las filas de dos padres para crear un hijo, preservando bloques de información exitosos.
Mutación: Intercambia aleatoriamente dos números (no fijos) dentro de una fila. Este operador es vital para introducir diversidad y escapar de óptimos locales.
Elitismo: El mejor 10% de la población pasa directamente a la siguiente generación para garantizar que no se pierdan los mejores avances.

## 🚫 Restricciones del Problema

El algoritmo respeta estrictamente las condiciones del proyecto:
1.  Inmutabilidad de Fijos: Los números iniciales del tablero base permanecen intactos durante todo el proceso.
2.  No Repetición: El fitness garantiza el cumplimiento de la regla de oro del Sudoku (no repetir números en filas, columnas y subcuadrículas). 
📊 Visualización de la Evolución

El sistema utiliza `matplotlib` para generar una gráfica del progreso generacional. En ella se observa cómo el **fitness (número de conflictos)** decrece a medida que avanzan las generaciones, cumpliendo con el requisito de explicar y demostrar visualmente la mejora del sistema.

🛠️ Requisitos e Instalación

**Lenguaje:** Python 3.x
**Librerías:** `matplotlib` (para visualización)

Para instalar las dependencias, ejecuta:
```bash
pip install matplotlib

## Optimización de Horarios: Configuración de Incomodidad ⏰

Este repositorio también incluye un optimizador de horarios en [horario_optimizado.py](horario_optimizado.py), que evita choques de aula y profesor y penaliza horarios incómodos.

### Bloques horarios
- Se definen 6 bloques de 45 minutos empezando a las 07:00:
	- 07:00, 07:45, 08:30, 09:15, 10:00, 10:45
- Internamente se trabaja por índice de bloque: 0..5 mapeado al listado anterior.

### Incomodidad general (bloques)
- Función: `evaluar_comodidad_difusa(bloque)` en [horario_optimizado.py](horario_optimizado.py).
- Modelo difuso: `fuzz.trapmf(x, [a, b, c, d])` donde `x = range(0, N)` siendo `N` la cantidad de bloques.
	- 0 hasta `a`: pertenencia 0 (sin incomodidad)
	- `a`→`b`: sube linealmente a 1
	- `b`→`c`: se mantiene en 1 (máxima incomodidad)
	- `c`→`d`: baja linealmente a 0
- Valor por defecto: `[3, 4, ultimo, ultimo]`. Esto hace que la incomodidad sea alta a partir de los bloques tardíos (≥ índice 4).
- Cómo ajustar: cambia esos 4 números para desplazar/franja donde el sistema considere incómodo.

### Incomodidad por profesor
- Ubicación: en `__init__` dentro de [horario_optimizado.py](horario_optimizado.py), diccionario `self.incomodidad_profesor`.
- Cada profesor tiene su perfil definido sobre los índices 0..5 usando `fuzz.trapmf`:
```python
self.incomodidad_profesor = {
		# Dr. Gomez: incomodidad en tarde
		"Dr. Gomez": fuzz.trapmf(x, [3, 4, ultimo, ultimo]),
		# Ing. Perez: incomodidad en muy temprano
		"Ing. Perez": fuzz.trapmf(x, [0, 0, 1, 2]),
		# Lic. Luis: incomodidad centrada en medias
		"Lic. Luis": fuzz.trapmf(x, [1, 2, 3, 4]),
}
```
- Cómo asignar o modificar incomodidad:
	- Edita los 4 valores `[a, b, c, d]` de cada profesor para mover la franja incómoda.
	- Ejemplos:
		- Prefiere muy temprano (penaliza tarde): `[3, 4, ultimo, ultimo]`.
		- Prefiere tarde (penaliza temprano): `[0, 0, 1, 2]`.
		- Evita centro (penaliza 08:30–10:00): `[1, 2, 4, 5]`.
- Evaluación: `evaluar_incomodidad_profesor(profesor, bloque)` convierte la hora "HH:MM" al índice y devuelve el valor del perfil en ese punto.

### Cómo influye en el Fitness
- Choques (aula/profesor en el mismo día y bloque) se penalizan muy fuertemente.
- Por cada bloque ocupado de una clase, se suma una penalización blanda: `incomodidad_profesor * factor`.
- El `factor` actual es `0.1`. Si deseas darle más peso a la preferencia de profesor, aumenta este factor en la suma dentro de `calcular_fitness()`.

### Ejecución rápida
```bash
env/bin/python horario_optimizado.py
```
o
```bash
python3 horario_optimizado.py
```

### Consejos de configuración
- Si agregas más bloques (p. ej. 7 u 8), actualiza `cantidad` y vuelve a definir los perfiles `trapmf` para abarcar el nuevo rango 0..N-1.
- Mantén los nombres de profesores en `self.profesores` sincronizados con las claves de `self.incomodidad_profesor`.
- Para depurar, puedes imprimir el valor de incomodidad por fila en `imprimir_resultado()`.
