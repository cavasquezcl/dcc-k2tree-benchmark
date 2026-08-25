import numpy as np

data = np.loadtxt("../datasets/ca-GrQc.txt", dtype=np.int32)

origenes = data[:, 0]
destinos = data[:, 1]

cant_origenes = len(origenes)
cant_destinos = len(destinos)

print("origenes:", cant_origenes)
print("destinos:", cant_destinos)
print(origenes, destinos)

todos = np.concatenate([origenes, destinos])
unicos = np.unique(todos)  # lista ordenada

cant_destinos = len(unicos)
print("\nunicos:", cant_destinos)
print(unicos)
