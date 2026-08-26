import os
import time

import numpy as np

RUTA_DATASET = os.path.join(os.path.dirname(__file__), "../datasets/web-Stanford.txt")

data = np.loadtxt(RUTA_DATASET, dtype=np.int64)

origenes = data[:, 0]
destinos = data[:, 1]

cant_origenes = len(origenes)
cant_destinos = len(destinos)

print("origenes:", cant_origenes)
print("destinos:", cant_destinos)
print(origenes, destinos)

todos = np.concatenate([origenes, destinos])

# unicos: la lista ordenada
# todos_idx: posicion de "todos" en "únicos"
unicos, todos_idx = np.unique(todos, return_inverse=True)
print("\nunicos:")
print(unicos)

print("\ntodos_idx")
print(todos_idx)

origenes_idx = todos_idx[:len(origenes)]
destinos_idx = todos_idx[len(origenes):]
#print(todos_idx, origenes_idx, destinos_idx)

"""
Ej: origenes = [A, B], destinos = [C, A]

todos = [A, B, C, A]
unicos = [A, B, C] --> índices 0, 1, 2
todos_idx = [0, 1, 2, 0]
origenes_idx = todos_idx[:2] = [0, 1] --> índices densos de A y B
destinos_idx = todos_idx[2:] = [2, 0] --> índices densos de C y A
"""

n = len(unicos) # cantidad de nodos

filas = origenes_idx
columnas = destinos_idx

# verifica que no hayan self-loops ni arists repetidas (dataset ad-hoc)
pares = np.column_stack([filas, columnas])

# revisa que no hayan self-loops, debería dar 0
cant_self_loops = (pares[:, 0] == pares[:, 1]).sum()
print("\nself-loops:", cant_self_loops)

# revisa que no hayan repetidos, debería dar 0
cant_repetidos = len(pares) - len(np.unique(pares, axis=0))
print("\naristas repetidas:", cant_repetidos)

# arma el csr

orden = np.lexsort((columnas, filas))  # ordena por filas y, a empate, por columnas
filas = filas[orden]
columnas = columnas[orden]

grado = np.bincount(filas, minlength=n)  # cuenta apariciones
indptr = np.zeros(n + 1, dtype=np.int64)  # array lleno de 0s para contador
indptr[1:] = np.cumsum(grado)  # suma cuantas aristas tiene cada nodo

indices = columnas

print("\nn:", n)
print("\naristas csr:", len(indices))

def vecinos(nodo):
    return indices[indptr[nodo]:indptr[nodo + 1]]

print("\nvecinos(1):", vecinos(1))
print("vecinos(2):", vecinos(2))


def existe_arista(nodo_origen, nodo_destino):
    return nodo_destino in vecinos(nodo_origen)

print("\nexiste_arista(1, 17793):", existe_arista(1, 17793))
print("existe_arista(1, 0):", existe_arista(1, 0))
print("existe_arista(2, 74360):", existe_arista(2, 74360))
print("existe_arista(2, 0):", existe_arista(2, 0))


# prueba de tiempo

inicio = time.perf_counter()
vecinos(1)
fin = time.perf_counter()
print("\ntiempo vecinos:", (fin - inicio))

inicio = time.perf_counter()
existe_arista(1, 17793)
fin = time.perf_counter()
print("\ntiempo existe_arista:", (fin - inicio))


