## Instrucciones de uso del programa "busca"

El programa está escrito en python en un solo fichero busca.py. Para ejecutarlo se debe invocar con el siguiente comando:

```shell
python3 busca.py fich_entrada fich_resultados
# o bien
./busca.py fich_entrada fich_resultados
```

Donde:
- _fich_entrada_: es el fichero de entrada donde recoge los artículos de los distintos bloques
- _fich_resultados_: es el fichero de salida donde se escribirán los resultados de la búsqueda.
Se mostrará por cada bloque: una línea con el área máxima y el tiempo de ejecución de la búsqueda, seguido de tantas lineas como artículos se han seleccionado para la solución.

### Ejecución de los tests

```shell
./ejecutar.sh [fichero_entrada] [fichero_resultados]
```

El script `ejecutar.sh` comprueba el correcto funcionamiento del programa busca.py ejecutando las siguientes tareas:
- Si se le pasa un fichero de entrada: 
    - ejecuta el programa con ese fichero
    - guarda los resultados en un fichero de salida
- Si no:
    - ejecuta el programa con todos los ficheros de prueba (*1_prueba.txt, 2_singleArticle.txt, 3_moreArticles.txt, 4_tricky.txt*)
    - guarda los resultados en un fichero de salida para cada fichero de prueba

Destacar que se imprime por pantalla información relativa a la solución de cada caso de prueba, así como el tiempo de ejecución de cada uno de ellos, comparando el **tiempo requerido** mediante el uso de la solución <u>recursiva vs iterativa</u>. 

A su vez se ha realizado una versión voraz del algoritmo, por lo tanto también aparece el **tiempo requerido** mediante el uso de la solución <u>voraz</u>.

Comentar que en el fichero `experimentacion.txt` se han recogido los resultados de la experimentación realizada con los distintos algoritmos, comparando el tiempo de ejecución de cada uno de ellos, incluso con los de la práctica anterior (<u>backtracking</u>)