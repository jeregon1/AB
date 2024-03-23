#!/bin/bash

# Script de pruebas de busca.py

# Si se pasan un argumento, se ejecuta el script con ese argumento como fichero de pruebas
# Si no, se ejecutan las pruebas con los archivos de prueba

if [ $# -eq 1 ]; then
    python3 busca.py pruebas/$1 pruebas/res_$1 && cat pruebas/res_$1
    exit 0
fi

cd pruebas

fich_1="1_prueba.txt"
fich_2="2_singleArticle.txt"
fich_3="3_moreArticles.txt"
fich_4="4_tricky.txt"

echo "Pruebas con los archivos de prueba"

for f in $fich_1 $fich_2 $fich_3 $fich_4; do
    echo "Probando con $f"
    python3 ../busca.py $f "res_$f"
    cat "res_$f"
done

echo Tests:
echo
cd ..
python3 buscaTest.py
