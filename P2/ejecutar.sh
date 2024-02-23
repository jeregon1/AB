#!/bin/bash

# Script de pruebas de busca.py

# Si se pasan dos argumentos, se ejecuta el script con esos argumentos
# Si no, se ejecutan las pruebas con los archivos de prueba

if [ $# -eq 2 ]; then
    python3 busca.py $1 $2
    exit 0
fi

cd pruebas

fich_1="1_prueba.txt"
fich_2="2_singleArticle.txt"
fich_3="3_moreArticles.txt"

echo "Pruebas con los archivos de prueba"

# Pruebo con los archivos de prueba
echo Fichero: $fich_1; echo
python3 ../busca.py $fich_1 "res_$fich_1"

echo Fichero: $fich_2; echo
python3 ../busca.py $fich_2 "res_$fich_2"

echo Fichero: $fich_3; echo
python3 ../busca.py $fich_3 "res_$fich_3"
