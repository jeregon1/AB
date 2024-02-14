#!/bin/bash

# Script que prueba el programa huff.py

comprimir="-c"
descomprimir="-d"

# Creo la carpeta d (descomprimidos) si no existe
if [ ! -d d ]; then
    mkdir d
fi

probar_archivo() {
    archivo=$1
    ./huff.py $comprimir $archivo
    # Muevo el archivo comprimido a la carpeta d (descomprimidos)
    mv $archivo1.huf d/$archivo.huf 
    ./huff.py d/$descomprimir $archivo.huf
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
