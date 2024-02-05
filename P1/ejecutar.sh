#!/bin/bash

# Solo puede haber 2 argumentos
# 1. flag -c o -d para comprimir o descomprimir
# 2. nombre del archivo a comprimir o descomprimir

if [ $# -ne 2 ]; then
    echo "Error: Uso $0 [-c|-d] <nombre_archivo>"
    exit 1
elif [ $1 != "-c" ] && [ $1 != "-d" ]; then
    echo "Error: Uso $0 [-c|-d] <nombre_archivo>"
    exit 1
elif [ ! -f $2 ]; then
    echo "Error: El archivo $2 no existe"
    exit 1
fi

python2.4 huff.py $1 $2
