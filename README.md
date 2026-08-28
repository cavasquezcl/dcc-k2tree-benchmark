# dcc-k2tree-benchmark

Implementa una estructura k2-tree se realizan mediciones

## Config entorno de desarrollo

Requisitos

- python 3.14
- pip

En winddows

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Crear y activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

Instalar dependendencias

```bash
pip install -r requirements.txt
```

Ejecución

```
python main.py amazon.txt
```

## Paso a paso (para la planificación)

- Descargar datasets desde internet
- Preprocesar el dataset
- Generar el baseline contra lo que va a comparar
    - función vecinos
    - función arista
    - bits
- Implemenar estructura k2-tree
    - reperestar con la estructura una matriz de adyacencia de un grafo
    - ajustar matriz
    - submatrices
    - vecinos
    - arista
    - bits
- Hacer pruebas con distintos valores de k
- Medir tiempos
- Buscar combinaciones para minimizar el espacio total que se usa
- Analizando el tiempo que resulta para
    - (1) verificar si una arista existe,
    - (2) extraer todos los vecinos de un nodo.
- Hacer comparaciones contra estructurta baseline (arreglo plano de vecinos por nodo)
