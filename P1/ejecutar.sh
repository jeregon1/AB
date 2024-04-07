#!/bin/bash

# Script que prueba el programa huf.py

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

    printf "Comprimir archivo de %'d bytes" $(wc -c $archivo | awk '{print $1}')
    time ../huf.py $comprimir $archivo

    # Muevo el archivo comprimido a la carpeta d (descomprimir)
    mv $archivo.huf resultados/$archivo.huf

    echo -n Descomprimir
    time ../huf.py $descomprimir resultados/$archivo.huf

    if cmp $archivo resultados/$archivo; then
        echo -e "\nArchivo $archivo es igual al descomprimido. OK"
    fi
}

calcular_compresion() {
    archivo=$1

    original=$(wc -c $archivo | awk '{print $1}')
    comprimido=$(wc -c resultados/$archivo.huf | awk '{print $1}')
    porcentaje=$(echo "scale=2; ($comprimido * 100 / $original)" | bc)

    echo -e "\nCompresión del archivo $archivo"
    printf "Original:   %'d bytes\n" $original
    printf "Comprimido: %'d bytes\n" $comprimido
    echo -e "El archivo comprimido ocupa un $porcentaje% del original\n"
}

cd pruebas

# Si hay un argumento, se prueba con ese archivo
if [ $# -eq 1 ]; then
    probar_archivo $1
    calcular_compresion $1
    exit 0
fi

archivo1="vacio.txt"
archivo2="uno.txt"
archivo3="quijote.txt"
archivo4="practica1_23-24.pdf"

# Pruebo el programa con los archivos de prueba
probar_archivo $archivo1
probar_archivo $archivo2
probar_archivo $archivo3
probar_archivo $archivo4

calcular_compresion $archivo1
calcular_compresion $archivo2
calcular_compresion $archivo3
calcular_compresion $archivo4
