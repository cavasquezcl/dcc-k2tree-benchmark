import time

from src.carga_dataset import cargar, RUTA_DATASET
import numpy as np

class K2Tree:
    def __init__(self, filas, columnas, n, k):
        self.filas = filas
        self.columnas = columnas
        self.n = n
        self.k = k

        # representacion k2-tree
        self.arbol_bits = None
        self.hojas_bits = None
        self.arbol_bits_sumado = None

        print("\ninit de K2-Tree")

        self.construir()
        print("Post construir")
        print(self.arbol_bits)
        print(self.arbol_bits_sumado)

        """
        k: es lo que varía
        n: potencia de k
        hay que dividir matriz M[1,n][1,n] en k2 areas iguales ->
        matriz: M [(n/k)(r-1)+1, (n/k)r] [(n/k)(c-1)+1, (n/k)c]

        funciones:
        - adj -> revisa arista
        - neigh -> vecinos
        - creport -> es como report
        - rneigh -> vecinos inversos
        - report -> busca arista en uan matriz

        paso a paso:
        1. construir el k2-tree
        2. rank()
        3. adj
        4. neigh -> creport
        """
    def construir(self):
        print(self.filas)
        print(self.columnas)
        print(self.n)
        print(self.k)

        filas = self.filas
        columnas = self.columnas
        n = self.n
        k = self.k

        tamagno = 1
        h = 0
        while tamagno < n:
            tamagno *= k
            h += 1

        print("tamaño:", tamagno)
        print("altura:", h)

        arbol_bits = []
        hojas_bits = []

        # fila_offset, col_offset, tamaño, indices_aristas_del_bloque)
        nivel_actual = [(0, 0, tamagno, np.arange(len(filas)))]

        for nivel in range(h):
            inicio_tiempo_nivel = time.perf_counter()
            print(f"nivel {nivel}/{h}: {len(nivel_actual)} bloques a procesar...")

            siguiente_nivel = []

            for f_off, c_off, tam, idx in nivel_actual:
                hijo_tam = tam // k
                f_bloque = filas[idx]
                c_bloque = columnas[idx]

                for ff in range(k):  # ff -> fila, va afuera
                    f_ini = f_off + ff * hijo_tam
                    f_mascara = (f_bloque >= f_ini) & (f_bloque < f_ini + hijo_tam)

                    for cc in range(k):  # cc -> columna, va adentro
                        c_ini = c_off + cc * hijo_tam
                        c_masc = f_mascara & (c_bloque >= c_ini) & (c_bloque < c_ini + hijo_tam)
                        hijo_idx = idx[c_masc]
                        hay_arista = hijo_idx.size > 0
                        bit = 1 if hay_arista else 0

                        if hijo_tam == 1:
                            # ultimo nivel
                            hojas_bits.append(bit)
                        else:
                            # hace el bit del hijo (ff, cc) en la posicion ff*k + cc
                            arbol_bits.append(bit)
                            if(hay_arista):
                               siguiente_nivel.append((f_ini, c_ini, hijo_tam, hijo_idx))

            nivel_actual = siguiente_nivel

            tiempo_nivel = time.perf_counter() - inicio_tiempo_nivel
            print(f"{tiempo_nivel:.2f}s")

        # se guarda el arbol en la instancia
        self.tamagno = tamagno
        self.h = h
        self.arbol_bits = np.array(arbol_bits, dtype=np.uint8)
        self.hojas_bits = np.array(hojas_bits, dtype=np.uint8)

        self.arbol_bits_sumado = np.concatenate(([0], np.cumsum(self.arbol_bits, dtype=np.int64)))

    def rank(self, i):
        return self.arbol_bits_sumado[i]

    def adj(self, fila, columna):
        k = self.k
        tam = self.tamagno
        h = self.h
        len_arbol = len(self.arbol_bits)
        hojas_bits = self.hojas_bits
        arbol_bits = self.arbol_bits

        nid = 0  # id del nodo actual (ahora es la raiz)

        for _ in range(h):
            tam //= k
            hijo = (fila // tam) * k + (columna // tam)
            pos = nid * k * k + hijo

            if pos < len_arbol:
                if arbol_bits[pos] == 0:
                    return False
                nid = self.rank(pos + 1)
            else:
                return bool(hojas_bits[pos - len_arbol])

            fila %= tam
            columna %= tam

        return False

    def neigh(self, fila):
        if self.h == 0:
            return []

        return self._creport(fila, 0, self.tamagno, 0)

    def _creport(self, r, c0, s, nid):
        k = self.k
        l = s // k
        r1 = r // l
        r = r % l

        len_arbol = len(self.arbol_bits)
        vecinos = []

        for c in range(k):
            hijo = r1 * k + c
            pos = nid * k * k + hijo

            if pos < len_arbol:
                if self.arbol_bits[pos]:
                    nuevo_nid = self.rank(pos + 1)
                    vecinos += self._creport(r, c0 + c * l, l, nuevo_nid)
            elif self.hojas_bits[pos - len_arbol]:
                vecinos.append(c0 + c * l)

        return vecinos

    def bits_numpy(self):
        return (self.arbol_bits.nbytes + self.hojas_bits.nbytes) * 8

    def bits_estructura(self):
        # este es el tamaño mas chico
        return len(self.arbol_bits) + len(self.hojas_bits)
