#!/bin/bash

# Autores: Jesús López Ansón (839922), Javier Sin Pelayo (843442)
# Funcionamiento: script que realiza pruebas sobre el programa huf.py.
#                 Comprime y descomprime archivos de prueba y muestra el tiempo de ejecución.
#                 Crea una carpeta 'd' para almacenar los archivos descomprimidos.

# MODO DE USO
# ./ejecutar.sh [archivo]
#   - Si se pasa un argumento, se prueba el programa con ese archivo
#   - Si no se pasa un argumento, se prueban los archivos de prueba


comprimir="-c"
descomprimir="-d"

# Cración de la carpeta 'd' (descomprimir) si no existe
if [ ! -d d ]; then
    mkdir d
fi

echo

probar_archivo() {
    archivo=$1

    printf "Comprimiendo archivo %s (%'d bytes)" "$archivo" $(wc -c "$archivo" | awk '{print $1}')
    time ../huf.py $comprimir $archivo

    # Muevo el archivo comprimido a la carpeta d (descomprimir)
    mv $archivo.huf resultados/$archivo.huf

    echo -n Descomprimiendo...
    time ../huf.py $descomprimir resultados/$archivo.huf

    if cmp $archivo resultados/$archivo; then
        echo -e "\nArchivo $archivo es igual al descomprimido. OK"
    else
        echo -e "\nArchivo $archivo es distinto al descomprimido. ERROR"
    fi
    echo
}

calcular_compresion() {
    archivo=$1

    original=$(wc -c $archivo | awk '{print $1}')
    comprimido=$(wc -c resultados/$archivo.huf | awk '{print $1}')
    porcentaje=$(echo "scale=2; ($comprimido * 100 / $original)" | bc)

    echo -e "\nCompresión del archivo $archivo"
    printf "Original:   %'d bytes\n" $original
    printf "Comprimido: %'d bytes\n" $comprimido
    echo -e "El archivo comprimido ocupa un $porcentaje% del original"
}

cd pruebas

# Si hay un argumento, se prueba con ese archivo
if [ $# -eq 1 ]; then
    probar_archivo $1
    calcular_compresion $1
    exit 0
fi

# Si no, se prueban los archivos de prueba
files=("vacio.txt" "uno.txt" "quijote.txt" "practica1_23-24.pdf")

for file in "${files[@]}"; do
    probar_archivo "$file"
done

for file in "${files[@]}"; do
    calcular_compresion "$file"
done
