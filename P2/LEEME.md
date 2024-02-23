## Instrucciones de uso del programa "busca"

El programa está escrito en python en un solo fichero busca.py. Para ejecutarlo se debe invocar con el siguiente comando:

```shell
python3 busca.py fich_entrada fich_resultados
# o bien
./busca.py fich_entrada fich_resultados
```

Donde:
- fich_entrada: es el fichero de entrada donde recoge los artículos de los distintos bloques
- fich_resultados: es el fichero de salida donde se escribirán los resultados de la búsqueda.
Se mostrará una línea por cada bloque con el área máxima y el tiempo de ejecución de la búsqueda.

### Ejecución de los tests

El script ejecutar.sh comprueba el correcto funcionamiento del programa busca.py ejecutando las siguientes tareas:
- Aplicar el algoritmo de búsqueda al fichero de entrada introducido
- Imprimir por pantalla el área máxima de cada bloque y el tiempo de ejecución
- 🎃

```shell
🎃🎃
./ejecutar.sh [fichero_entrada] [fichero_resultados]
# Si no se especifica fichero_entrada, se ejecutará con todos los ficheros de prueba, generando para cada uno de ellos un fichero de resultados
```