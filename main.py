import os
import sys
import time
import numpy as np

from src.carga_dataset import cargar, RUTA_DATASET
from src.k2tree import K2Tree
from src.csr import CSR

RUTA_DATASETS = os.path.join(os.path.dirname(__file__), "datasets")

def armar_k_por_nivel(n, k_arriba, niveles_arriba, k_abajo):
    # primero mete los niveles_arriba
    k_por_nivel = [k_arriba] * niveles_arriba
    tamagno = k_arriba ** niveles_arriba

    # y despues rellena con k_abajo hasta el final
    while tamagno < n:
        k_por_nivel.append(k_abajo)
        tamagno *= k_abajo

    return k_por_nivel

print("┌─────────────────────┐")
print("│                     │")
print("│     I N I C I O     │")
print("│                     │")
print("└─────────────────────┘")


# uso: python main.py [nombre_dataset.txt]
if len(sys.argv) > 1:
    ruta_dataset = os.path.join(RUTA_DATASETS, sys.argv[1])
else:
    ruta_dataset = RUTA_DATASET

# carga el dataset
filas, columnas, n = cargar(ruta_dataset)
m = len(filas)  # cantidad de aristas

# muestras para medir tiempos de consulta, se reusan en cada experimento

rng = np.random.default_rng(42)
cant_muestras = 1_000

# mitad aristas que existen, mitad al azar
cant_existen = min(cant_muestras // 2, len(filas))
cant_random = cant_muestras - cant_existen

idx_existen = rng.choice(len(filas), size=cant_existen, replace=False)
pares_existen = np.column_stack([filas[idx_existen], columnas[idx_existen]])
pares_random = rng.integers(0, n, size=(cant_random, 2))
muestra = np.concatenate([pares_existen, pares_random])

nodos_con_aristas = np.unique(filas)
cant_muestras_nodos = min(cant_muestras, len(nodos_con_aristas))
muestra_nodos = rng.choice(nodos_con_aristas, size=cant_muestras_nodos, replace=False)


# datos del CSR (una sola vez, sirve de referencia para todos los experimentos)

inicio = time.perf_counter()
csr = CSR(filas, columnas, n)
tiempo_construir_csr = time.perf_counter() - inicio

inicio = time.perf_counter()
for p, q in muestra:
    csr.existe_arista_binaria(p, q)
tiempo_csr_adj = time.perf_counter() - inicio

inicio = time.perf_counter()
for nodo in muestra_nodos:
    csr.vecinos(int(nodo))
tiempo_csr_neigh = time.perf_counter() - inicio

print("\ndatos del CSR")
print("------------------------------------------------")
print(f"tiempo construccion: {tiempo_construir_csr:.4f}s")
print(f"bits_estructura(): {csr.bits_estructura()} ({csr.bits_estructura() / m:.2f} bits/arista)")
print(f"tiempo adj: {tiempo_csr_adj:.4f}s total, {tiempo_csr_adj / cant_muestras * 1e6:.2f}us/query")
print(f"tiempo neigh: {tiempo_csr_neigh:.4f}s total, {tiempo_csr_neigh / cant_muestras_nodos * 1e6:.2f}us/query")


# cada experimento: un K2Tree con un k distinto por nivel

candidatos = {
    "solo_2":        armar_k_por_nivel(n, 2, 0, 2),  # arma algo como [2, 2, 2, 2, 2, 2]
    "solo_4":        armar_k_por_nivel(n, 4, 0, 4),  # arma algo como [4, 4, 4, 4, 4, 4]
    "grande_arriba": armar_k_por_nivel(n, 4, 3, 2),  # arma algo como [4, 4, 4, 2, 2, 2]
    "chico_arriba":  armar_k_por_nivel(n, 2, 3, 4),  # arma algo como [2, 2, 2, 4, 4, 4]
}

for nombre, k_por_nivel in candidatos.items():
    inicio = time.perf_counter()
    arbol = K2Tree(filas, columnas, n, k_por_nivel)
    tiempo_construir = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for p, q in muestra:
        arbol.adj(p, q)
    tiempo_adj = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for nodo in muestra_nodos:
        arbol.neigh(int(nodo))
    tiempo_neigh = time.perf_counter() - inicio

    print(f"\n\n{nombre}: k_por_nivel={k_por_nivel}")
    print("------------------------------------------------")
    print(f"tiempo construccion: {tiempo_construir:.4f}s")
    print(f"bits_estructura(): {arbol.bits_estructura()} ({arbol.bits_estructura() / m:.2f} bits/arista)")
    print(f"tiempo adj: {tiempo_adj:.4f}s total, {tiempo_adj / cant_muestras * 1e6:.2f}us/query")
    print(f"tiempo neigh: {tiempo_neigh:.4f}s total, {tiempo_neigh / cant_muestras_nodos * 1e6:.2f}us/query")


print("┌─────────────────┐")
print("│                 │")
print("│     F I N       │")
print("│                 │")
print("└─────────────────┘")
