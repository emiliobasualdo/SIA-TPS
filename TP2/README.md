# SIA-TP2

## Setup
Usamos Python 3.x
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Run
#### Para graficar en vivo
Existe la opción de correr el websocket para ver en vivo los resultados.  
Por default el WS hostea en ws://localhost:8080. Se puede cambiar el puerto en el .cfg
```
[WEBSOCKET]
enable=true
port=8080
```
Iniciar la página de ReactJs se requiere NodeJs = 14
```shell
cd live-graphs
npm install
npm run start
```

#### Correr sin gráficos realtime
Es necesario apagar el WS
```
[WEBSOCKET]
enable=false
```
El resto del archivo se configura por secciones.

### DEFAULT
Acá se configuran los parámetros generales para el sistema
```
[DEFAULT]
items_directory=allitems
character_class=defensor
seed=100                  <- semilla del random, seed=None para aleatorio
N=600 <- cantidad de individuos en el sistema
k=500 <- cantidad de individuos
graphs=true  <- graficar resultados al final de la corrida
min_h=1.3 <- alturna mínima de los individuos
max_h=2 <- alturna máxima de los individuos
```
Condiciones de corte de ejecución:
- por máxima cantidad de iteraciones/generaciones: gen_quantity
- por máxima cantidad de segundos transcurridos: time
- por objetivo de fitness alcanzado: fitness_goal
- por repetición del mejor fitness: content
- por repetición de cantidad de diversidad objetivo: structure

Solo es necesario uno de los siguientes grupos
```
[STOP_CONDITION]
# posible valores: [gen_quantity, time, fitness_goal, content, structure]
stop_condition=time
time=20

stop_condition=fitness_goal
fitness_goal=10

stop_condition=gen_quantity
gen_quantity=100

stop_condition=content
content=20

stop_condition=structure
structure=20
max_gen_fixed=100
```
Métodos de selección.  
Estos parámetros pueden ser utilizados en ambos la selección de padres para el crossover y para la selección de la nueva generación.

Es importante que se especifiquen 2 métodos con los parámetros `method1` y `method2` seguidos de sus respectivos parámetros.
```
method1=XXX
z=W
method2=YYY
m=p
n=l
```
A continuación se listan algunos ejemplos.
```
[SELECTION]
# opciones [random, elite, roulette, universal, ranking, det_tourn, prob_tourn, boltzmann]
A=0.99
method1=random

method2=elite

method1=boltzmann
t0=100
tc=1

method1=prob_tourn
th=0.6

method2=det_tourn
M=5
```
Métodos de crossover.
```
[CROSS_OVER]
# opciones [one_point, two_points, anular, uniform]
method=one_point
#method=two_points
#method=anular
#method=uniform
#Pc = 0.9
```
Métodos de mutación. 
Algunas opciones lleval listas de valores separadas por comas.
```
[MUTATION]
# opciones [single_gen, multi_gen_lim, multi_gen_uni, complete]
#method=single_gen
#Pm=0.9

#method=multi_gen_lim
#Pm=0.9
#M=2

method=multi_gen_uni
Pms=1.0,0.7,0.7,0.5,0.9,0.2 <- Probabilidades según gen Pms=[ARMA, BOTA, CASCO, GUANTE, PECHERA, ALTURA]

#method=complete
#Pm=0.5
#Pms=0.9, 0.9, 0.9, 0.9, 0.9, 0.9
```
La sección de selección de la nueva generación toma los mismos parámetros que la sección de selección de padres. 
Además se le agregar el parámetro `fill` que puede tomar los valores `all` o`parent`  
```
[NEW_GEN_SELECTION]
# mismas opciones y que SELECTION
A=0.99
method1=random
#M=5
#method1=boltzmann
#t0=10
#tc=0.01
method2=elite
# [all, parent]
fill=parent