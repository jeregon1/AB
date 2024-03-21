#!/bin/bash

# Script de pruebas de busca.py

# Si se pasan dos argumentos, se ejecuta el script con esos argumentos
# Si no, se ejecutan las pruebas con todos los archivos de prueba

if [ $# -eq 2 ]
then
    echo "Ejecutando pruebas con $2"
    opcion=$1
    fich=$2
    python3 busca.py $opcion pruebas/$fich pruebas/res_$fich && cat pruebas/res_$fich
    exit 0
fi


for fich in 1_prueba.txt 2_singleArticle.txt 3_moreArticles.txt 4_tricky.txt
do
    echo -e "########## Ejecutando pruebas con $fich ##########"
    echo -e "\tRecursiva"
    python3 busca.py -r pruebas/$fich pruebas/res_$fich
    cat pruebas/res_$fich
    
    echo -e "\tIterativa"
    python3 busca.py -i pruebas/$fich pruebas/res_$fich
    cat pruebas/res_$fich

    echo -e "\tVoraz"
    python3 busca.py -g pruebas/$fich pruebas/res_$fich
    cat pruebas/res_$fich
done
