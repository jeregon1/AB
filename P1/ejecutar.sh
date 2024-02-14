#!/bin/bash

# Script que prueba el programa huff.py

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
archivo3="practica1_23-24.pdf"

# Pruebo el programa con los archivos de prueba
probar_archivo $archivo1
probar_archivo $archivo2
probar_archivo $archivo3
