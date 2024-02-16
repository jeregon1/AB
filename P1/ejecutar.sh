#!/bin/bash

# Script que prueba el programa huff.py

# MODO DE USO
# ./ejecutar.sh [archivo]
# Si se pasa un argumento, se prueba el programa con ese archivo
# Si no se pasa un argumento, se prueban los archivos de prueba


comprimir="-c"
descomprimir="-d"

# Creo la carpeta d (descomprimir) si no existe
if [ ! -d d ]; then
    mkdir d
fi

probar_archivo() {
    archivo=$1

    ./huff.py $comprimir $archivo
    # Muevo el archivo comprimido a la carpeta d (descomprimir)
    mv $archivo.huf d/$archivo.huf
    ./huff.py $descomprimir d/$archivo.huf

    if cmp $archivo d/$archivo; then
        echo -e "\nArchivo $archivo OK"
    fi
}

# Si hay un argumento, se prueba con ese archivo
if [ $# -eq 1 ]; then
    probar_archivo $1
    exit 0
fi

archivo1="x.txt"
archivo2="uno.txt"
archivo3="quijote.txt"
archivo4="practica1_23-24.pdf"

# Pruebo el programa con los archivos de prueba
probar_archivo $archivo1
probar_archivo $archivo2
probar_archivo $archivo3
probar_archivo $archivo4

# Ahora calculamos la compresión del archivo quijote.txt y practica1_23-24.pdf
echo -e "\nCompresión del archivo quijote.txt"
echo -e "Original: $(wc -c $archivo3 | awk '{print $1}') bytes"
echo -e "Comprimido: $(wc -c d/$archivo3.huf | awk '{print $1}') bytes"

echo -e "\nCompresión del archivo practica1_23-24.pdf"
echo -e "Original: $(wc -c $archivo4 | awk '{print $1}') bytes"
echo -e "Comprimido: $(wc -c d/$archivo4.huf | awk '{print $1}') bytes"
