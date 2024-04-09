#!/bin/bash
# Autores: Jesús López Ansón (839922), Javier Sin Pelayo (843442)
# Funcionamiento: script que realiza pruebas sobre el programa busca.py.
#                 Realiza una serie de tests sobre unos ficheros de interés, y luego
#                 ejecuta el script de pruebas buscaTest.py, el cual realiza pruebas
#                 adicionales con información relativa a los nodos generados, tiempo
#                 de ejecución, ...

# MODO DE USO
# ./ejecutar.sh [opcion] [archivo]
#  - Si se pasan dos argumentos, se ejecuta el script con esos argumentos
#  - Si no, se ejecutan las pruebas con todos los archivos de prueba

if [ $# -eq 2 ];then
    echo "Ejecutando pruebas con $2"
    opcion=$1
    fich=$2
    python3 busca.py $opcion pruebas/$fich pruebas/res_$fich && cat pruebas/res_$fich
    exit 0
fi

fich_1="1_prueba.txt"
fich_2="2_singleArticle.txt"
fich_3="3_moreArticles.txt"
fich_4="4_tricky.txt"

for fich in $fich_1 $fich_2 $fich_3 $fich_4; do
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

echo Tests adicionales:
echo
python3 buscaTest.py