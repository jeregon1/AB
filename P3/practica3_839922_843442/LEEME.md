## Organización del directorio
El directorio está dividido en los siguientes directorios/ficheros de interés:
- **busca.py**: Programa principal que implementa la búsqueda de un área máxima en un bloque de artículos.
- **buscaTest.py**: Programa que realiza pruebas adicionales de los algoritmos de programación dinámica, voraz y fuerza bruta, imprimiendo información relativa al tiempo y nodos generados.
- **ejecutar.sh**: Script que ejecuta los tests del programa *busca.py*, junto a otros adicionales 
del programa *buscaTest.py*, donde se comparan casos de estudio con programación dinámica, voraz y fuerza bruta.
- **experimentacion.txt**: Fichero que recoge los resultados de la experimentación realizada con los distintos algoritmos, comparando el tiempo de ejecución de cada uno de ellos, incluso con los de la práctica anterior (<u>backtracking</u>). A su vez se completa el apartado *BOLA EXTRA* presente en el guión de la práctica.
- **pruebas**: directorio de tests que contiene: 
    - **4 ficheros de interés** para la realización de las pruebas.
    - **ficheros resultado**: un fichero resultado por cada fichero de prueba correspondiente. 

## Instrucciones de ejecución

El programa está escrito en python en un solo fichero busca.py. Para ejecutarlo se debe invocar con el siguiente comando:

```shell
python3 busca.py [-r | -i | -g] fich_entrada fich_resultados
# o bien
./busca.py [-r | -i | -g] fich_entrada fich_resultados
```

Donde:
- _-r_, _-i_ o _-g_ es la opción que se pasa al programa para indicar el algoritmo a utilizar:
    - _-r_ para el algoritmo recursivo
    - _-i_ para el algoritmo iterativo
    - _-g_ para el algoritmo voraz
- _fich_entrada_: es el fichero de entrada donde recoge los artículos de los distintos bloques.
- _fich_resultados_: es el fichero de salida donde se escribirán los resultados de la búsqueda.
Se mostrará por cada bloque: una línea con el área máxima y el tiempo de ejecución de la búsqueda, seguido de tantas lineas como artículos se han seleccionado para la solución.

### Ejecución de los tests


El script `ejecutar.sh` comprueba el correcto funcionamiento del programa busca.py ejecutando las siguientes tareas:
- Si se pasan dos argumentos:
    - se ejecuta el script con esos argumentos (opción y fichero de entrada)
    - guarda los resultados en un fichero de salida
    - muestra por pantalla el resultado de la ejecución
- Si no:
    - ejecuta el programa con todos los ficheros de prueba (*1_prueba.txt, 2_singleArticle.txt, 3_moreArticles.txt, 4_tricky.txt*)
    - guarda los resultados en un fichero de salida para cada fichero de prueba
A su vez, se ejecuta el script de pruebas *buscaTest.py*.

Destacar que se imprime por pantalla información relativa a la solución de cada caso de prueba, así como el tiempo de ejecución de cada uno de ellos, incluyendo también en las comprobaciones de *buscaTest.py* una comparación del **tiempo requerido** mediante el uso de <u>prog dinámica vs voraz vs fuerza bruta</u>, junto a los **nodos generados** por cada uno de estos algoritmos.


```shell
./ejecutar.sh [opcion] [fichero_entrada]
```
