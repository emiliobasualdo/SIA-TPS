# SIA-TPS

## Setup
Usamos Python 3.x
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Run
Para correr 1 vez simplemente editamos config.cfg según criterio.  
No es necesario borrar las lineas que no se usan.
```
board=maps/easy1.py            # path relativo al mapa, hay algunos de ejemplo ne l carpeta maps
algorithm=bfs                  # algún valor de [bfs, dfs, iddfs, ggs, a_star, ida]
heuristic=euclidean_distance   # (solo aplica para ggs, a_star, ida) algún valor de [euclidean_distance, manhattan_distance, sum_of_manhattan]
iterative_limit= 10            # (solo aplica para iddfs) un entero mayor a 0
```
y luego
```shell
cd TP1
python main.py   
```

También podemos correr todos los algoritmos y heurísticas con algún mapa en particular(recomendamos un mapa simple).  
Esta función correrá todos los algoritmos 10 veces y generará un archivo results.csv con los resultados.  
También imprimirá en pantalla los tiempos promedios de cada algoritmos y heurística.
```shell 
python main.py many maps/easy1.py
```