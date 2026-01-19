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
        # Bloques horarios: 6 slots de 45 minutos empezando a las 07:00
        inicio_min = 7 * 60  # 07:00 en minutos
        paso = 45            # duración de cada bloque en minutos
        cantidad = 6         # total de bloques
        self.bloques = [
            f"{(inicio_min + i * paso) // 60:02d}:{(inicio_min + i * paso) % 60:02d}"
            for i in range(cantidad)
        ]
        # Incomodidad por profesor (difusa), definida por índice de bloque
        x = np.arange(0, cantidad, 1)
        ultimo = cantidad - 1
        self.incomodidad_profesor = {
            # Prefiere temprano, le incomoda tarde
            "Dr. Gomez": fuzz.trapmf(x, [3, 4, ultimo, ultimo]),
            # Le incomoda muy temprano, prefiere más tarde
            "Ing. Perez": fuzz.trapmf(x, [0, 0, 1, 2]),
            # Prefiere evitar el medio, incomodidad centrada en horas intermedias
            "Lic. Luis": fuzz.trapmf(x, [1, 2, 3, 4]),
        }

    def evaluar_comodidad_difusa(self, bloque):
        """Evalúa incomodidad difusa en función del índice del bloque horario.
        Soporta bloque como índice anterior (1..5) o etiqueta de hora ("HH:MM").
        """
        x = np.arange(0, len(self.bloques), 1)
        # Determinar índice del bloque
        if isinstance(bloque, (int, np.integer)):
            # Compatibilidad: si viniera en 1..N, convertir a índice 0..N-1
            idx = max(0, min(len(self.bloques) - 1, int(bloque) - 1))
        else:
            idx = self.bloques.index(bloque)

        # Incomodidad alta en los últimos bloques, creciente desde el medio
        ultimo = len(self.bloques) - 1
        incomodo = fuzz.trapmf(x, [3, 4, ultimo, ultimo])
        return float(fuzz.interp_membership(x, incomodo, idx))

    def evaluar_incomodidad_profesor(self, profesor, bloque):
        """Devuelve incomodidad específica del profesor para el bloque indicado.
        Acepta bloque como índice 1..N o como etiqueta "HH:MM".
        """
        # Resolver índice del bloque
        if isinstance(bloque, (int, np.integer)):
            idx = max(0, min(len(self.bloques) - 1, int(bloque) - 1))
        else:
            idx = self.bloques.index(bloque)
        # Obtener incomodidad del profesor en ese índice
        perfil = self.incomodidad_profesor.get(profesor)
        if perfil is None:
            # Si no hay perfil, usar incomodidad global como fallback
            return self.evaluar_comodidad_difusa(bloque)
        return float(perfil[idx])

    def crear_individuo(self):
        individuos = []
        for m in self.materias:
            dur = random.choice([1, 2])
            start_idx = random.randint(0, len(self.bloques) - dur)
            bloques_sel = [self.bloques[start_idx + i] for i in range(dur)]
            individuos.append({
                'materia': m,
                'profesor': random.choice(self.profesores),
                'aula': random.choice(self.aulas),
                'dia': random.choice(self.dias),
                'bloque': bloques_sel
            })
        return individuos

    def analizar_individuo(self, individuo):
        """Detecta qué filas específicas tienen conflicto."""
        conflictos = [False] * len(individuo)
        usos_aula = {}
        usos_prof = {}
        
        for i, c in enumerate(individuo):
            # Asegurar lista de bloques
            bloques = c['bloque'] if isinstance(c['bloque'], list) else [c['bloque']]
            for b in bloques:
                a_key = (c['aula'], c['dia'], b)
                p_key = (c['profesor'], c['dia'], b)
                if a_key in usos_aula:
                    conflictos[i] = True
                    conflictos[usos_aula[a_key]] = True
                else:
                    usos_aula[a_key] = i
                if p_key in usos_prof:
                    conflictos[i] = True
                    conflictos[usos_prof[p_key]] = True
                else:
                    usos_prof[p_key] = i
        return conflictos

    def calcular_fitness(self, individuo):
        choques = 0
        penalizacion_blanda = 0
        usos_aula = set()
        usos_prof = set()
        
        for c in individuo:
            bloques = c['bloque'] if isinstance(c['bloque'], list) else [c['bloque']]
            for b in bloques:
                a = (c['aula'], c['dia'], b)
                p = (c['profesor'], c['dia'], b)
                if a in usos_aula:
                    choques += 1
                else:
                    usos_aula.add(a)
                if p in usos_prof:
                    choques += 1
                else:
                    usos_prof.add(p)
                # Penalización blanda específica del profesor
                penalizacion_blanda += self.evaluar_incomodidad_profesor(c['profesor'], b) * 0.1

        return 1 / (1 + (choques * 5000) + penalizacion_blanda)

    def imprimir_resultado(self, individuo, titulo):
        print(f"\n{'='*30} {titulo} {'='*30}")
        conflictos = self.analizar_individuo(individuo)
        
        # Encabezado con separadores y anchos fijos
        header = f"{'ESTADO':<8} | {'MATERIA':<12} | {'PROFESOR':<15} | {'AULA':<10} | {'DÍA':<10} | {'HORA'}"
        print(header)
        print("-" * len(header))
        
        # Ordenar los datos para la visualización
        datos_ordenados = sorted(
            individuo,
            key=lambda x: (
                x['dia'],
                self.bloques.index(x['bloque'][0] if isinstance(x['bloque'], list) else x['bloque'])
            )
        )
        
        conflictos_ordenados = self.analizar_individuo(datos_ordenados)

        for i, c in enumerate(datos_ordenados):
            mark = "[!] " if conflictos_ordenados[i] else "OK  "
            
            # Formatear bloques: lista a cadena amigable
            bloques = c['bloque'] if isinstance(c['bloque'], list) else [c['bloque']]
            bloque_str = ", ".join(bloques)
            fila = (f"{mark:<8} | {c['materia']:<12} | {c['profesor']:<15} | "
                    f"{c['aula']:<10} | {c['dia']:<10} | {bloque_str}")
            print(fila)
            
        print("-" * len(header))
        print(f"Fitness Resultante: {self.calcular_fitness(individuo):.8f}\n")

    def ejecutar(self):

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
                    # Reasignar 1 o 2 bloques consecutivos
                    dur = random.choice([1, 2])
                    start_idx = random.randint(0, len(self.bloques) - dur)
                    m['bloque'] = [self.bloques[start_idx + i] for i in range(dur)]
                    m['aula'] = random.choice(self.aulas)
                
                nueva_gen.append(hijo)
            poblacion = nueva_gen

        self.imprimir_resultado(poblacion[0], "HORARIO FINAL OPTIMIZADO")

if __name__ == "__main__":
    motor = OptimizadorMaestro()
    motor.ejecutar()
