from src.carga_dataset import cargar, RUTA_DATASET

class K2Tree:
    def __init__(self, filas, columnas, n, k):
        self.filas = filas
        self.columnas = columnas
        self.n = n
        self.k = k
        print("\ninit de K2-Tree")

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


if __name__ == "__main__":
    filas, columnas, n = cargar(RUTA_DATASET)
    arbol = K2Tree(filas, columnas, n)
