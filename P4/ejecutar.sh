#!/bin/bash
# Autores: Jesús López Ansón (839922), Javier Sin Pelayo (843442)
# Funcionamiento: script que realiza pruebas sobre el programa buscaRyP.py.
#                 Realiza una serie de tests sobre unos ficheros de interés, y luego
#                 ejecuta el script de pruebas buscaTest.py, el cual realiza pruebas
#                 adicionales con información relativa a los nodos generados, tiempo
#                 de ejecución, ...

# MODO DE USO 
# ./ejecutar.sh [archivo]
#  - Si se pasa un argumento, se ejecuta el script con ese argumento
#  - Si no, se ejecutan las pruebas con todos los archivos de prueba

if [ $# -eq 1 ];then
    echo "Ejecutando pruebas con $1"
    fich=$1
    python3 buscaRyP.py pruebas/$fich pruebas/res_$fich && cat pruebas/res_$fich
    # exit 0
else
    fich_1="1_prueba.txt"
    fich_2="2_singleArticle.txt"
    fich_3="3_moreArticles.txt"
    fich_4="4_tricky.txt"
    fich_5="5_evenMoreArticles.txt"
    fich_6="6_greaterBlocks.txt"

    for fich in $fich_1 $fich_2 $fich_3 $fich_4; do
        echo -e "########## Ejecutando pruebas con $fich ##########"
        python3 buscaRyP.py pruebas/$fich pruebas/res_$fich
        cat pruebas/res_$fich
    done

    echo Tests adicionales:
    echo
    python3 buscaTest.py
fi
