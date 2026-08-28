import os
import sys
import time
import zipfile

import numpy as np

from src.carga_dataset import cargar, RUTA_DATASET
from src.k2tree import K2Tree
from src.csr import CSR

RUTA_DATASETS = os.path.join(os.path.dirname(__file__), "datasets")
RUTA_ZIP = os.path.join(RUTA_DATASETS, "datasets.zip")
ARCHIVOS_DATASET = ["dataset_minimo.txt", "web-Google.txt", "web-Stanford.txt"]


print("inicia main.py \n")


# uso: python main.py [nombre_dataset.txt]
if len(sys.argv) > 1:
    nombre_dataset = sys.argv[1]
    ruta_dataset = os.path.join(RUTA_DATASETS, nombre_dataset)

    if not os.path.exists(ruta_dataset):
        raise FileNotFoundError(f"no existe el dataset: {ruta_dataset}")
else:
    ruta_dataset = RUTA_DATASET

# carga el dataset
filas, columnas, n = cargar(ruta_dataset)

# instancia CSR
inicio_csr = time.perf_counter()
csr = CSR(filas, columnas, n)
tiempo_construir_csr = time.perf_counter() - inicio_csr

inicio = time.perf_counter()
csr.existe_arista_lineal(1, 17793)
fin = time.perf_counter()
print("\ntiempo existe_arista_lineal:", (fin - inicio))

inicio = time.perf_counter()
csr.existe_arista_binaria(1, 17793)
fin = time.perf_counter()
print("tiempo existe_arista_binaria:", (fin - inicio))

print("\nbits_numpy():", csr.bits_numpy())
print("bits_numpy() / m:", csr.bits_numpy() / len(csr.indices))
print("bits_estructura():", csr.bits_estructura())
print("bits_estructura() / m:", csr.bits_estructura() / len(csr.indices))

# instancia K2Tree
inicio_k2tree = time.perf_counter()
arbol = K2Tree(filas, columnas, n, 2)
tiempo_construir_k2tree = time.perf_counter() - inicio_k2tree

print("\nIMPORTANTE 1: tiempos de construccion")
print("csr:", tiempo_construir_csr, "s")
print("k2tree:", tiempo_construir_k2tree, "s")

print("\nadj")

print("adj(0, 4):", arbol.adj(0, 4))  # true
print("adj(0, 2):", arbol.adj(0, 2))  # false

print("\nrank")

print("rank(4):", arbol.rank(4))  # da 3
print("rank(16):", arbol.rank(16))  # da 9


# miden muchas muestras si existen

rng = np.random.default_rng(42)
cant_muestras = 10_000

# aristas que existen
cant_existen = min(cant_muestras // 2, len(filas))
cant_random = cant_muestras - cant_existen

idx_existen = rng.choice(len(filas), size=cant_existen, replace=False)
pares_existen = np.column_stack([filas[idx_existen], columnas[idx_existen]])
pares_random = rng.integers(0, n, size=(cant_random, 2))
muestra = np.concatenate([pares_existen, pares_random])

inicio = time.perf_counter()
for p, q in muestra:
    arbol.adj(p, q)
tiempo_k2tree = time.perf_counter() - inicio

inicio = time.perf_counter()
for p, q in muestra:
    csr.existe_arista_binaria(p, q)
tiempo_csr = time.perf_counter() - inicio

print("\nIMPORTANTE 2: tiempos de verifica si existe arista")
print(f"muestras: {cant_muestras}. {cant_existen} aristas reales y {cant_random} random)")
print(f"csr: {tiempo_csr:.4f}s total, {tiempo_csr / cant_muestras * 1e6:.2f}us/query")
print(f"k2-tree: {tiempo_k2tree:.4f}s total, {tiempo_k2tree / cant_muestras * 1e6:.2f}us/query")


print("\n\nfin desde main.py \n")
