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
Iniciar la página de ReactJs se requiere NodeJs = 11
```shell
cd live-graphs
npm install
npm run start
```

#### Correr sin gráficos
Es necesario apagar el WS
```
[WEBSOCKET]
enable=false
```
El resto del archivo se configura por secciones.