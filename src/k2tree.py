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

        for _ in range(h):
            siguiente_nivel = []

            for f_off, c_off, tam, idx in nivel_actual:
                hijo_tam = tam // k
                f_bloque = filas[idx]
                c_bloque = columnas[idx]

                for ff in range(k):  #ff -> fila
                    f_ini = f_off + ff * hijo_tam
                    f_mascara = (f_bloque >= f_ini) & (f_bloque < f_ini + hijo_tam)

                    for cc in range(k):  # cc -> columna
                        c_ini = c_off + cc * hijo_tam
                        c_masc = f_mascara & (c_bloque >= c_ini) & (c_bloque < c_ini + hijo_tam)
                        hijo_idx = idx[c_masc]
                        hay_arista = hijo_idx.size > 0
                        bit = 1 if hay_arista else 0

                        if hijo_tam == 1:
                            hojas_bits.append(bit)
                        else:
                            arbol_bits.append(bit)
                            if(hay_arista):
                                siguiente_nivel.append((f_ini, c_ini, hijo_tam, hijo_idx))

            nivel_actual = siguiente_nivel

        # se guarda el arbol en la instancia
        self.arbol_bits = np.array(arbol_bits, dtype=np.uint8)
        self.hojas_bits = np.array(hojas_bits, dtype=np.uint8)

        self.arbol_bits_sumado = np.concatenate(([0], np.cumsum(self.arbol_bits, dtype=np.int64)))

    def rank(self, i):
        return self.arbol_bits_sumado[i]

if __name__ == "__main__":
    filas, columnas, n = cargar(RUTA_DATASET)
    arbol = K2Tree(filas, columnas, n, 2)
