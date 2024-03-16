#!/bin/bash

# Script de pruebas de busca.py

# Si se pasan dos argumentos, se ejecuta el script con esos argumentos
# Si no, se ejecutan las pruebas con los archivos de prueba

if [ $# -eq 2 ]
then
    echo "Ejecutando pruebas con $2"
    opcion=$1
    fich=$2
    python3 busca.py $opcion pruebas/$fich pruebas/res_$fich
    cat pruebas/res_$fich
    exit 0
fi

ficheros="1_prueba.txt 2_singleArticle.txt 3_moreArticles.txt"

for fich in $ficheros
do
    echo -e "########## Ejecutando pruebas con $fich ##########"
    python3 busca.py -r pruebas/$fich pruebas/res_$fich
    cat pruebas/res_$fich
    python3 busca.py -i pruebas/$fich pruebas/res_$fich
    cat pruebas/res_$fich
done
