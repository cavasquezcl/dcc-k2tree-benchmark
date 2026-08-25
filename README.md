# dcc-k2tree-benchmark

Implementa una estructura k2-tree se realizan mediciones

## Config entorno de desarrollo

Requisitos

- python 3.14
- pip

Crear y activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

Instalar dependendencias

```bash
pip install -r requirements.txt
```

Descarga el dataset

```
python src/download_dataset.py
```

Ejecutar

```
python main.py
```

## Paso a paso

- Implemenar estructura k2-tree
- Reperestar con la estructura una matriz de adyacencia de un grafo
- Hacer pruebas con distintos valores de k
- Medir tiempos
- Buscar combinaciones para minimizar el espacio total que se usa
- Analizando el tiempo que resulta para
  - (1) verificar si una arista existe,
  - (2) extraer todos los vecinos de un nodo.
- Hacer comparaciones contra estructurta baseline (arreglo plano de vecinos por nodo)
