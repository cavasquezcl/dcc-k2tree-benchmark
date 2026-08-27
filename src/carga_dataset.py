import os
import numpy as np

RUTA_DATASET = os.path.join(os.path.dirname(__file__), "../datasets/dataset_minimo.txt")

def cargar(ruta_dataset):
    """
    Ej: origenes = [A, B], destinos = [C, A]

    todos = [A, B, C, A]
    unicos = [A, B, C] --> índices 0, 1, 2
    todos_idx = [0, 1, 2, 0]
    origenes_idx = todos_idx[:2] = [0, 1] --> índices densos de A y B
    destinos_idx = todos_idx[2:] = [2, 0] --> índices densos de C y A
    """
    data = np.loadtxt(ruta_dataset, dtype=np.int64)

    origenes = data[:, 0]
    destinos = data[:, 1]

    todos = np.concatenate([origenes, destinos])

    # unicos: la lista ordenada
    # todos_idx: posicion de "todos" en "únicos"
    unicos, todos_idx = np.unique(todos, return_inverse=True)

    origenes_idx = todos_idx[:len(origenes)]
    destinos_idx = todos_idx[len(origenes):]

    n = len(unicos)  # cantidad de nodos
    filas = origenes_idx
    columnas = destinos_idx

    return filas, columnas, n


if __name__ == "__main__":
    filas, columnas, n = cargar(RUTA_DATASET)
    print("n:", n)
    print("aristas:", len(filas))
