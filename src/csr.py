import math
import numpy as np

class CSR:
    def __init__(self, filas, columnas, n):
        print("\ninit de CSR")
        self.filas = filas
        self.columnas = columnas
        self.n = n

        # la representación
        self.indptr = None
        self.indices = None

        # construye
        self.construir()

    def construir(self):

        filas = self.filas
        columnas = self.columnas
        n = self.n

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

        # guarda la estructura
        self.indptr = indptr
        self.indices = columnas

    def vecinos(self, nodo):
        return self.indices[self.indptr[nodo]:self.indptr[nodo + 1]]

    def existe_arista_lineal(self, nodo_origen, nodo_destino):
        return nodo_destino in self.vecinos(nodo_origen)

    def existe_arista_binaria(self, nodo_origen, nodo_destino):
        vecinos_origen = self.vecinos(nodo_origen)
        pos_v_origen = np.searchsorted(vecinos_origen, nodo_destino)
        return pos_v_origen < len(vecinos_origen) and vecinos_origen[pos_v_origen] == nodo_destino

    def bits_numpy(self):
        return (self.indptr.nbytes + self.indices.nbytes) * 8

    def bits_estructura(self):
        m = len(self.indices)  # cantidad de aristas
        bits_por_indptr = math.ceil(math.log2(m + 1))
        bits_por_indice = math.ceil(math.log2(self.n))
        return (self.n + 1) * bits_por_indptr + m * bits_por_indice
