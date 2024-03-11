#!/bin/bash

# Script de pruebas de busca.py

# Si se pasan dos argumentos, se ejecuta el script con esos argumentos
# Si no, se ejecutan las pruebas con los archivos de prueba


opcion=$1
fich=$2

python3 busca.py $opcion pruebas/$fich pruebas/res_$fich
