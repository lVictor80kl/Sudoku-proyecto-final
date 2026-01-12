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

