#!/bin/bash

# Script de pruebas de busca.py

# Si se pasan un argumento, se ejecuta el script con ese argumento como fichero de pruebas
# Si no, se ejecutan las pruebas con los archivos de prueba

if [ $# -eq 1 ]; then
    python3 busca.py pruebas/$1 pruebas/res_$1
    exit 0
fi

cd pruebas

fich_1="1_prueba.txt"
fich_2="2_singleArticle.txt"
fich_3="3_moreArticles.txt"
fich_4="4_tricky.txt"

echo "Pruebas con los archivos de prueba"

# Pruebo con los archivos de prueba
python3 ../busca.py $fich_1 "res_$fich_1"
echo Fichero $fich_1 finalizado

python3 ../busca.py $fich_2 "res_$fich_2"
echo Fichero $fich_2 finalizado

python3 ../busca.py $fich_3 "res_$fich_3"
echo Fichero $fich_3 finalizado

python3 ../busca.py $fich_4 "res_$fich_4"
echo Fichero $fich_4 finalizado

echo Tests:
echo
cd ..
python3 buscaTest.py
