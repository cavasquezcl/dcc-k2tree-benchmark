import time

from src.carga_dataset import cargar, RUTA_DATASET
from src.k2tree import K2Tree
from src.csr import CSR

print("inicia main.py \n")

filas, columnas, n = cargar(RUTA_DATASET)



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



print("\n\nfin desde main.py \n")
