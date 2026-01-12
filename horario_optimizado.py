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

