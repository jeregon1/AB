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
Se mostrará una línea por cada bloque con el área máxima y el tiempo de ejecución de la búsqueda

### Ejecución de los tests

```shell
./ejecutar.sh [fichero_entrada] [fichero_resultados]
```

El script `ejecutar.sh` comprueba el correcto funcionamiento del programa busca.py ejecutando las siguientes tareas:
- Si se le pasa un fichero de entrada: 
    - ejecuta el programa con ese fichero
    - guarda los resultados en un fichero de salida
- Si no:
    - ejecuta el programa con todos los ficheros de prueba (*1_prueba.txt, 2_singleArticle.txt, 3_moreArticles.txt*)
    - guarda los resultados en un fichero de salida para cada fichero de prueba
    - lanza el banco de pruebas `buscaTest.py` donde se realizan comprobaciones con casos de estudio específicos   

Destacar que se imprime por pantalla información relativa a la solución de cada caso de prueba, así como el tiempo de ejecución de cada uno de ellos, comparando el **tiempo requerido** mediante el uso de <u>backtracking vs fuerza bruta</u>, junto a los **nodos generados** por cada uno de estos algoritmos.
