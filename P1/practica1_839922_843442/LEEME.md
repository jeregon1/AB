## Organización del directrio
En el directorio está dividido en los siguientes directorios/ficheros de interés:
- **huf.py**: Programa principal que implementa la compresión y descompresión de ficheros mediante el algoritmo de Huffman.
- **ejecutar.sh**: Script que ejecuta los tests del programa *huf.py*.
- **pruebas**: directorio de tests que contiene: 
    - **4 ficheros de interés** para la realización de las pruebas
    - **resultados**: directorio donde se almacenan los resultados de la ejecución del algoritmo sobre los 4 archivos que se acaban de mencionar (una vez sometidos a la compresión y posterior descompresión).


## Instrucciones de ejecución

El programa está escrito en python en un solo fichero **huf.py**. Para ejecutarlo se debe invocar con el siguiente comando:

```shell
python2.4 huf.py [-c | -d] fichero_entrada
# o bien
./huf.py [-c | -d] fichero_entrada
```

Donde:
- -c: comprime el fichero de entrada
- -d: descomprime el fichero de entrada

### Ejecución de los tests

El script **ejecutar.sh** comprueba el correcto funcionamiento del programa *huf.py* ejecutando las siguientes tareas:
- Comprimir y descomprimir el fichero de prueba
- Comprobar que el fichero original y el descomprimido son iguales
- Calcula el tiempo de ejecución de la compresión y descompresión
- Calcula el porcentaje de compresión

```shell
./ejecutar.sh [fichero_entrada]
# Si no se especifica fichero_entrada, se ejecutará con todos los ficheros de prueba
```