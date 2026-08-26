from src.carga_dataset import cargar, RUTA_DATASET
from src.k2tree import K2Tree

print("inicia main.py \n")

filas, columnas, n = cargar(RUTA_DATASET)

# instancia K2Tree
arbol = K2Tree(filas, columnas, n, 2)

print("fin desde main.py \n")
