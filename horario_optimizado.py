import random
import numpy as np
import pandas as pd
import skfuzzy as fuzz
import copy

class OptimizadorMaestro:
    def __init__(self):
        self.materias = [f"Materia_{i}" for i in range(1, 21)]
        self.profesores = ["Dr. Gomez", "Ing. Perez", "Lic. Luis"]
        self.aulas = ["Aula_101", "Aula_102"]
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        self.bloques = list(range(1, 6))

    def evaluar_comodidad_difusa(self, bloque):
        x = np.arange(1, 6, 1)
        incomodo = fuzz.trapmf(x, [3, 4, 5, 5])
        return float(fuzz.interp_membership(x, incomodo, bloque))

    def crear_individuo(self):
        return [{
            'materia': m,
            'profesor': random.choice(self.profesores),
            'aula': random.choice(self.aulas),
            'dia': random.choice(self.dias),
            'bloque': random.choice(self.bloques)
        } for m in self.materias]

    def analizar_individuo(self, individuo):
        """Detecta qué filas específicas tienen conflicto."""
        conflictos = [False] * len(individuo)
        usos_aula = {}
        usos_prof = {}
        
        for i, c in enumerate(individuo):
            a_key = (c['aula'], c['dia'], c['bloque'])
            p_key = (c['profesor'], c['dia'], c['bloque'])
            
            if a_key in usos_aula:
                conflictos[i] = True
                conflictos[usos_aula[a_key]] = True
            else: usos_aula[a_key] = i
                
            if p_key in usos_prof:
                conflictos[i] = True
                conflictos[usos_prof[p_key]] = True
            else: usos_prof[p_key] = i
        return conflictos

    def calcular_fitness(self, individuo):
        choques = 0
        penalizacion_blanda = 0
        usos_aula = set()
        usos_prof = set()
        
        for c in individuo:
            a = (c['aula'], c['dia'], c['bloque'])
            p = (c['profesor'], c['dia'], c['bloque'])
            
            if a in usos_aula: choques += 1
            else: usos_aula.add(a)
            if p in usos_prof: choques += 1
            else: usos_prof.add(p)
            
            penalizacion_blanda += self.evaluar_comodidad_difusa(c['bloque']) * 0.1

        return 1 / (1 + (choques * 5000) + penalizacion_blanda)

    def imprimir_resultado(self, individuo, titulo):
        print(f"\n{'='*30} {titulo} {'='*30}")
        conflictos = self.analizar_individuo(individuo)
        
        # Encabezado con separadores y anchos fijos
        header = f"{'ESTADO':<8} | {'MATERIA':<12} | {'PROFESOR':<15} | {'AULA':<10} | {'DÍA':<10} | {'BLOQUE'}"
        print(header)
        print("-" * len(header))
        
        # Ordenar los datos para la visualización
        datos_ordenados = sorted(individuo, key=lambda x: (x['dia'], x['bloque']))
        
        # Para saber si la fila actual tiene conflicto (debemos re-analizar tras ordenar o usar índices)
        # Es más fácil re-analizar sobre la lista ordenada para que el [!] coincida visualmente
        conflictos_ordenados = self.analizar_individuo(datos_ordenados)

        for i, c in enumerate(datos_ordenados):
            mark = "[!] " if conflictos_ordenados[i] else "OK  "
            
            # Formateo de cada fila con el caracter |
            fila = (f"{mark:<8} | {c['materia']:<12} | {c['profesor']:<15} | "
                    f"{c['aula']:<10} | {c['dia']:<10} | {c['bloque']}")
            print(fila)
            
        print("-" * len(header))
        print(f"Fitness Resultante: {self.calcular_fitness(individuo):.8f}\n")

    def ejecutar(self):
        # 1. Población inicial
        poblacion = [self.crear_individuo() for _ in range(100)]
        horario_inicial = copy.deepcopy(poblacion[0])
        self.imprimir_resultado(horario_inicial, "HORARIO INICIAL")

        print("\nOptimización en progreso...")
        
        for gen in range(501): # Más generaciones para 20 materias
            poblacion = sorted(poblacion, key=lambda x: self.calcular_fitness(x), reverse=True)
            mejor_f = self.calcular_fitness(poblacion[0])
            
            if gen % 100 == 0:
                print(f"Gen {gen} | Fitness: {mejor_f:.6f}")

            if mejor_f > 0.99:
                print(f"¡Éxito en Gen {gen}!")
                break
            
            nueva_gen = [copy.deepcopy(poblacion[0])] # Elitismo
            
            while len(nueva_gen) < 100:
                # Selección
                p1, p2 = random.sample(poblacion[:20], 2)
                
                # Crossover
                punto = random.randint(1, len(p1)-1)
                hijo = copy.deepcopy(p1[:punto] + p2[punto:])
                
                # Mutación más variada
                if random.random() < 0.3:
                    m = random.choice(hijo)
                    m['dia'] = random.choice(self.dias)
                    m['bloque'] = random.randint(1, 5)
                    m['aula'] = random.choice(self.aulas)
                
                nueva_gen.append(hijo)
            poblacion = nueva_gen

        self.imprimir_resultado(poblacion[0], "HORARIO FINAL OPTIMIZADO")

if __name__ == "__main__":
    motor = OptimizadorMaestro()
    motor.ejecutar()
