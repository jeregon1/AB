#!/bin/bash

# Pruebas con busca.py


if [ $# -eq 2 ]; then
    python busca.py $1 $2
    exit 0
fi

cd pruebas

fich_1="1_prueba.txt"
fich_2="2_singleArticle.txt"
fich_3="3_moreArticles.txt"

# Pruebo con los archivos de prueba
python busca.py fich_1 "($fich_1)_res"
python busca.py fich_2 "($fich_2)_res"
python busca.py fich_3 "($fich_3)_res"
