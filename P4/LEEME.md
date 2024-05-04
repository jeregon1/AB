TERMINAR REVISANDO LAS --> 🎃

## Organización del directorio
El directorio está dividido en los siguientes directorios/ficheros de interés:
- **buscaRyP.py**: Programa principal que implementa la búsqueda de un área máxima en un bloque de artículos. Devuelve el área restante sin ocupar por los artúculos.
- **buscaTest.py**: Programa que realiza pruebas adicionales de los algoritmos de las prácticas anteriores junto al de esta: 
    - fuerza bruta 
    - backtracking
    - programación dinámica 
    - ramificación y poda 

    imprimiendo información relativa al tiempo y nodos generados.
- **ejecutar.sh**: Script que ejecuta los tests del programa *buscaRyP.py*, junto a los del programa *buscaTest.py*, donde se aporta información adicional relativa a los nodos generados comparando casos de estudio con los distintos algoritmos mencionados previamente.
- **pruebas**: directorio de tests que contiene: 
    - **6 ficheros de interés** para la realización de las pruebas. 🎃 el 6 peta con RyP (correo Simona?)
    - **ficheros resultado**: un fichero resultado por cada fichero de prueba correspondiente. 

## Instrucciones de ejecución

El programa está escrito en python en un solo fichero buscaRyP.py. Para ejecutarlo se debe invocar con el siguiente comando:

```shell
python3 buscaRyP.py fich_entrada fich_resultados
# o bien
./buscaRyP.py fich_entrada fich_resultados
```

Donde:
- _fich_entrada_: es el fichero de entrada donde recoge los artículos de los distintos bloques.
- _fich_resultados_: es el fichero de salida donde se escribirán los resultados de la búsqueda.
Se mostrará por cada bloque: una línea con el área restante sin ocupar de la página y el tiempo de ejecución de la búsqueda, seguido de tantas lineas como artículos se han seleccionado para la solución.

### Ejecución de los tests

El script `ejecutar.sh` comprueba el correcto funcionamiento del programa buscaRyP.py ejecutando las siguientes tareas:
- Si se pasa un argumento:
    - se ejecuta el script con ese argumento (fichero de entrada)
    - guarda los resultados en un fichero de salida
    - muestra por pantalla el resultado de la ejecución
- Si no:
    - ejecuta el programa con todos los ficheros de prueba (*1_prueba.txt, 2_singleArticle.txt, 3_moreArticles.txt, 4_tricky.txt, 🎃*)
    - guarda los resultados en un fichero de salida para cada fichero de prueba
A su vez, se ejecuta el script de pruebas *buscaTest.py*.

Destacar que se imprime por pantalla información relativa a la solución de cada caso de prueba, así como el tiempo de ejecución de cada uno de ellos, incluyendo también en las comprobaciones de *buscaTest.py* una comparación del **tiempo requerido** mediante el uso de <u>ramificación y poda</u> vs <u>prog dinámica</u> vs <u>búsqueda con retroceso</u> vs <u>fuerza bruta</u>, junto a los **nodos generados** por cada uno de estos algoritmos.


```shell
./ejecutar.sh [fichero_entrada]
```
