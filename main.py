import os
import sys
import time
import zipfile

from src.carga_dataset import cargar, RUTA_DATASET
from src.k2tree import K2Tree
from src.csr import CSR

RUTA_DATASETS = os.path.join(os.path.dirname(__file__), "datasets")
RUTA_ZIP = os.path.join(RUTA_DATASETS, "datasets.zip")
ARCHIVOS_DATASET = ["dataset_minimo.txt", "web-Google.txt", "web-Stanford.txt"]


print("inicia main.py \n")


# uso: python main.py [nombre_dataset.txt]
if len(sys.argv) > 1:
    nombre_dataset = sys.argv[1]
    ruta_dataset = os.path.join(RUTA_DATASETS, nombre_dataset)

    if not os.path.exists(ruta_dataset):
        raise FileNotFoundError(f"no existe el dataset: {ruta_dataset}")
else:
    ruta_dataset = RUTA_DATASET

# carga el dataset
filas, columnas, n = cargar(ruta_dataset)

# instancia CSR
csr = CSR(filas, columnas, n)

inicio = time.perf_counter()
csr.existe_arista_lineal(1, 17793)
fin = time.perf_counter()
print("\ntiempo existe_arista_lineal:", (fin - inicio))

inicio = time.perf_counter()
csr.existe_arista_binaria(1, 17793)
fin = time.perf_counter()
print("tiempo existe_arista_binaria:", (fin - inicio))

print("\nbits_numpy():", csr.bits_numpy())
print("bits_numpy() / m:", csr.bits_numpy() / len(csr.indices))
print("bits_estructura():", csr.bits_estructura())
print("bits_estructura() / m:", csr.bits_estructura() / len(csr.indices))

# instancia K2Tree
arbol = K2Tree(filas, columnas, n, 2)

print("\nadj")

print("adj(0, 4):", arbol.adj(0, 4))  # true
print("adj(0, 2):", arbol.adj(0, 2))  # false

print("\nrank")

print("rank(4):", arbol.rank(4))  # da 3
print("rank(16):", arbol.rank(16))  # da 9


print("\n\nfin desde main.py \n")
