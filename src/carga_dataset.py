import numpy as np

data = np.loadtxt("../datasets/ca-GrQc.txt", dtype=np.int64)

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
