## Instrucciones de uso del programa huff

El programa está escrito en python en un solo fichero huff.py. Para ejecutarlo se debe invocar con el siguiente comando:

```shell
python2.4 huff.py [-c|-d] fichero_entrada
# o bien
./huff.py [-c|-d] fichero_entrada
```

Donde:
- -c: comprime el fichero de entrada
- -d: descomprime el fichero de entrada

### Ejecución de los tests

El script ejecutar.sh comprueba el correcto funcionamiento del programa huff.py ejecutando las siguientes tareas:
- Comprimir y descomprimir el fichero de prueba
- Comprobar que el fichero original y el descomprimido son iguales
- Calcula el tiempo de ejecución de la compresión y descompresión
- Calcula el porcentaje de compresión

```shell
./ejecutar.sh [fichero_entrada]
# Si no se especifica fichero_entrada, se ejecutará con todos los ficheros de prueba
```