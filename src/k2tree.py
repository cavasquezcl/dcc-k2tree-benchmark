from src.carga_dataset import cargar, RUTA_DATASET
import numpy as np
class K2Tree:
    def __init__(self, filas, columnas, n, k):
        self.filas = filas
        self.columnas = columnas
        self.n = n
        self.k = k
        print("\ninit de K2-Tree")

        self.construir()

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
            print("h")
            for f_off, c_off, tam, idx in nivel_actual:
                hijo_tam = tam // k
                f_bloque = filas[idx]
                c_bloque = columnas[idx]
                print("tam: ", hijo_tam)
                print("f: ", f_bloque)
                print("c: ", c_bloque)
                for ff in range(k):  #ff -> fila
                    fila_ini = f_off + ff * hijo_tam
                    print("k1: ", fila_ini)
                    for cc in range(k):  # cc -> columna
                        col_ini = c_off + cc * hijo_tam

                        arbol_bits.append(1)
                        hojas_bits.append(0)
                        siguiente_nivel.append((1, 1, 1, 1))
                        print("k2:", col_ini)
            nivel_actual = siguiente_nivel


        print("binarios construidos")
        print(arbol_bits)
        print(hojas_bits)



if __name__ == "__main__":
    filas, columnas, n = cargar(RUTA_DATASET)
    arbol = K2Tree(filas, columnas, n, 2)
