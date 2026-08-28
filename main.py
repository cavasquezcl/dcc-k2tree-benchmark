import os
import sys
import time
import zipfile

import numpy as np

from src.carga_dataset import cargar, RUTA_DATASET
from src.k2tree import K2Tree
from src.csr import CSR

RUTA_DATASETS = os.path.join(os.path.dirname(__file__), "datasets")


print("inicia main.py \n")


# uso: python main.py [nombre_dataset.txt]
if len(sys.argv) > 1:
    ruta_dataset = os.path.join(RUTA_DATASETS, sys.argv[1])
else:
    ruta_dataset = RUTA_DATASET

# carga el dataset
filas, columnas, n = cargar(ruta_dataset)

# instancia CSR
inicio_csr = time.perf_counter()
csr = CSR(filas, columnas, n)
tiempo_construir_csr = time.perf_counter() - inicio_csr

# esto sirve para el dataset de 50M de aristas, recalcular luego para uno mas grande
k_por_nivel_base = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

inicio_k2tree = time.perf_counter()
arbol = K2Tree(filas, columnas, n, k_por_nivel_base)
tiempo_construir_k2tree = time.perf_counter() - inicio_k2tree

print("\nIMPORTANTE 1: tiempos de construccion")
print("csr:", tiempo_construir_csr, "s")
print("k2tree:", tiempo_construir_k2tree, "s")


# miden muchas muestras si existen

rng = np.random.default_rng(42)
cant_muestras = 1_000

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


# se miden neigh (vecinos) con nodos que tienen al menos una arista

nodos_con_aristas = np.unique(filas)
cant_muestras_nodos = min(cant_muestras, len(nodos_con_aristas))
muestra_nodos = rng.choice(nodos_con_aristas, size=cant_muestras_nodos, replace=False)

inicio = time.perf_counter()
for nodo in muestra_nodos:
    arbol.neigh(int(nodo))
tiempo_neigh = time.perf_counter() - inicio

inicio = time.perf_counter()
for nodo in muestra_nodos:
    csr.vecinos(int(nodo))
tiempo_vecinos = time.perf_counter() - inicio

print("\nIMPORTANTE 3: tiempos de listar vecinos")
print(f"muestras: {cant_muestras_nodos} nodos con al menos una arista")
print(f"csr vecinos: {tiempo_vecinos:.4f}s total, {tiempo_vecinos / cant_muestras_nodos * 1e6:.2f}us/query")
print(f"k2tree neigh: {tiempo_neigh:.4f}s total, {tiempo_neigh / cant_muestras_nodos * 1e6:.2f}us/query")


m = len(filas)  # cantidad de aristas

print("\nIMPORTANTE 4: espacio ocupado")
print(f"csr bits_estructura(): {csr.bits_estructura()} ({csr.bits_estructura() / m:.2f} bits/arista)")
print(f"k2tree bits_estructura(): {arbol.bits_estructura()} ({arbol.bits_estructura() / m:.2f} bits/arista)")


# comparacion con distintos k por nivel, se compara espacio total y tiempo de adj y neigh

print("\nIMPORTANTE 5: distintos k por nivel")

# esto sirve para el dataset de 50M de aristas, recalcular luego para uno mas grande
candidatos = {
    "solo_2":   [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    "solo_4":   [4, 4, 4, 4, 4, 4, 4, 4],
    "grande_arriba": [4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    "chico_arriba":  [2, 2, 2, 4, 4, 4, 4, 4, 4],
}

for nombre, k_por_nivel in candidatos.items():
    arbol_candidato = K2Tree(filas, columnas, n, k_por_nivel)

    inicio = time.perf_counter()
    for p, q in muestra:
        arbol_candidato.adj(p, q)
    tiempo_adj_candidato = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for nodo in muestra_nodos:
        arbol_candidato.neigh(int(nodo))
    tiempo_neigh_candidato = time.perf_counter() - inicio

    print(f"\n\n{nombre}: k_por_nivel={k_por_nivel}")
    print("------------------------------------------------")
    print(f"- bits_estructura(): {arbol_candidato.bits_estructura()}")
    print(f"- tiempo adj: {tiempo_adj_candidato:.4f}s total, {tiempo_adj_candidato / cant_muestras * 1e6:.2f}us/query")
    print(f"- tiempo neigh: {tiempo_neigh_candidato:.4f}s total, {tiempo_neigh_candidato / cant_muestras_nodos * 1e6:.2f}us/query")


print("┌─────────────────┐")
print("│                 │")
print("│     F I N       │")
print("│                 │")
print("└─────────────────┘")
