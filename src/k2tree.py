from src.carga_dataset import cargar, RUTA_DATASET

class K2Tree:
    def __init__(self, filas, columnas, n):
        self.filas = filas
        self.columnas = columnas
        self.n = n
        print("\ninit de K2-Tree")


if __name__ == "__main__":
    filas, columnas, n = cargar(RUTA_DATASET)
    arbol = K2Tree(filas, columnas, n)
