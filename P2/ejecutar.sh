#!/bin/bash

if [ $# -eq 2 ]; then
    python busca.py $1 $2
    exit 0
fi

cd pruebas

fich_1="1_prueba.txt"
fich_2="2_singleArticle.txt"
fich_3="3_moreArticles.txt"

echo "Pruebas con los archivos de prueba"

# Pruebo con los archivos de prueba
python3 ../busca.py fich_1 "res_$fich_1"
python3 ../busca.py fich_2 "res_$fich_2"
python3 ../busca.py fich_3 "res_$fich_3"
