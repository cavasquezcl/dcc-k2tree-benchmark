import math
import time
import numpy as np
from src.carga_dataset import cargar, RUTA_DATASET

if __name__ == "__main__":
    filas, columnas, n = cargar(RUTA_DATASET)

    print("aristas:", len(filas))

    # verifica que no hayan self-loops ni arists repetidas (dataset ad-hoc)
    pares = np.column_stack([filas, columnas])

    # revisa que no hayan self-loops, debería dar 0
    cant_self_loops = (pares[:, 0] == pares[:, 1]).sum()
    print("\nself-loops:", cant_self_loops)

    # revisa que no hayan repetidos, debería dar 0
    cant_repetidos = len(pares) - len(np.unique(pares, axis=0))
    print("\naristas repetidas:", cant_repetidos)

    # arma el csr

    orden = np.lexsort((columnas, filas))  # ordena por filas y columnas
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

    def existe_arista_lineal(nodo_origen, nodo_destino):
        return nodo_destino in vecinos(nodo_origen)

    def existe_arista_binaria(nodo_origen, nodo_destino):
        vecinos_origen = vecinos(nodo_origen)
        pos_v_origen = np.searchsorted(vecinos_origen, nodo_destino)
        return pos_v_origen < len(vecinos_origen) and vecinos_origen[pos_v_origen] == nodo_destino

    print("\nexiste_arista_lineal(1, 17793):", existe_arista_lineal(1, 17793))
    print("existe_arista_binaria(1, 17793):", existe_arista_binaria(1, 17793))
    print("existe_arista_lineal(1, 0):", existe_arista_lineal(1, 0))
    print("existe_arista_binaria(1, 0):", existe_arista_binaria(1, 0))
    print("existe_arista_lineal(2, 74360):", existe_arista_lineal(2, 74360))
    print("existe_arista_binaria(2, 74360):", existe_arista_binaria(2, 74360))

    # prueba de tiempo

    inicio = time.perf_counter()
    existe_arista_lineal(1, 17793)
    fin = time.perf_counter()
    print("\ntiempo existe_arista_lineal:", (fin - inicio))

    inicio = time.perf_counter()
    existe_arista_binaria(1, 17793)
    fin = time.perf_counter()
    print("tiempo existe_arista_binaria:", (fin - inicio))

    def bits_numpy():
        return (indptr.nbytes + indices.nbytes) * 8

    m = len(indices)  # cantidad de aristas

    def bits_estructura():
        bits_por_indptr = math.ceil(math.log2(m + 1))
        bits_por_indice = math.ceil(math.log2(n))
        return (n + 1) * bits_por_indptr + m * bits_por_indice

    print("\nbits_numpy():", bits_numpy())
    print("bits_numpy() / m:", bits_numpy() / m)
    print("bits_estructura():", bits_estructura())
    print("bits_estructura() / m:", bits_estructura() / m)
