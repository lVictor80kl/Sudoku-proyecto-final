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
