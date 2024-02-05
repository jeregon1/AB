# coding=utf-8
from heapq import heapify, heappop, heappush
import os, sys
import pickle

''' 
    Esta clase representa un nodo en el árbol de Huffman. Cada nodo tiene un carácter, su frecuencia
    en el texto y dos referencias a sus nodos hijos (izquierda y derecha).
'''
class NodoHuffman:
    def __init__(self, caracter=None, frecuencia=None):
        self.caracter = caracter  # Carácter del nodo
        self.frecuencia = frecuencia  # Frecuencia del carácter
        self.izquierda = None  # Nodo hijo izquierdo
        self.derecha = None  # Nodo hijo derecho

    def __cmp__(self, other):
        if self.frecuencia < other.frecuencia:
            return -1
        elif self.frecuencia > other.frecuencia:
            return 1
        else:
            return 0

# Esta clase se encarga de realizar la compresión utilizando el algoritmo de Huffman
class CompresorHuffman:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo  # Ruta del archivo de entrada

    ''' 
    - Este método cuenta la frecuencia de cada carácter en el archivo de entrada y almacena esta información 
      en self.frecuencia_caracteres, un diccionario que mapea los caracteres a sus frecuencias.
    '''
    def contar_frecuencia(self):
        frecuencia_caracteres = {}
        archivo = open(self.ruta_archivo, 'r')
        for linea in archivo:
            for caracter in linea:
                if caracter in frecuencia_caracteres:
                    frecuencia_caracteres[caracter] += 1
                else:
                    frecuencia_caracteres[caracter] = 1
        archivo.close()

        return frecuencia_caracteres

    ''' 
    - Este método construye el árbol de Huffman a partir de las frecuencias de los caracteres.
    - Utiliza una cola de prioridad para mantener los nodos ordenados por frecuencia.
    - Los nodos con menor frecuencia estarán a la mayor profundidad del árbol mientras que los nodos con mayor
        frecuencia estarán a menor profundidad, de manera que el carácter más frecuente tendrá el código más corto.
    '''
    def construir_arbol(self):
        cola_prioridad = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in self.contar_frecuencia().items()]
        heapify(cola_prioridad) # Convierte la lista en una cola de prioridad

        while len(cola_prioridad) > 1:
            nodo_izquierda = heappop(cola_prioridad)
            nodo_derecha = heappop(cola_prioridad)
            nodo_padre = NodoHuffman(frecuencia=nodo_izquierda.frecuencia + nodo_derecha.frecuencia)
            nodo_padre.izquierda = nodo_izquierda
            nodo_padre.derecha = nodo_derecha

            heappush(cola_prioridad, nodo_padre)

        return cola_prioridad[0]

    def imprimir_arbol(self, raiz, nivel=0):
        if raiz is not None:
            self.imprimir_arbol(raiz.derecha, nivel + 1)
            print(' ' * nivel * 8 + '->', raiz.caracter, raiz.frecuencia)
            self.imprimir_arbol(raiz.izquierda, nivel + 1)

    '''
        - Este método genera los códigos binarios para cada carácter en el árbol de Huffman.
        - Recorre el árbol recursivamente y asigna '0' para el hijo izquierdo y '1' para el hijo derecho, 
          acumulando los códigos para cada carácter.
    '''
    def generar_codigos(self, raiz, codigo=''):
        if raiz is None:
            return {}

        if raiz.caracter is not None:
            return {raiz.caracter: codigo}

        codigos = {}
        codigos.update(self.generar_codigos(raiz.izquierda, codigo + '0'))
        codigos.update(self.generar_codigos(raiz.derecha, codigo + '1'))

        return codigos

    # A partir de la tabla de códigos, genera la cabecera que se añadirá al archivo comprimido
    def generar_cabecera(self, tabla_codigos):
        # La cabecera es la tabla de códigos serializada
        # Y los 4 primeros bytes son la longitud en bytes de la tabla serializada
        tabla_serializada = pickle.dumps(tabla_codigos)
        return len(tabla_serializada).to_bytes(4, 'big') + tabla_serializada
            

    '''
        - Este método comprime el archivo de entrada utilizando los códigos generados por el árbol de Huffman.
        - Abre el archivo original en modo lectura y el archivo comprimido en modo binario.
        - Recorre el archivo original, reemplazando cada carácter por su código binario correspondiente y escribiendo 
          los bytes resultantes en el archivo comprimido.
        - Si al final del archivo aún hay bits por escribir, se añade un byte adicional para completar el último byte 
          y se agrega información sobre el relleno al final del archivo.
    '''
    def comprimir_archivo(self, ruta_archivo_comprimido, tabla_codigos):
        archivo = open(self.ruta_archivo, 'r') # Lectura en modo texto
        archivo_comprimido = open(ruta_archivo_comprimido, 'wb') # Escritura en modo binario

        # Generar la cabecera y escribirla en el archivo comprimido
        cabecera = self.generar_cabecera(tabla_codigos)
        archivo_comprimido.write(cabecera)

        bits_acumulados = ''

        # Recorrer el fichero original y escribir los bits comprimidos en el fichero comprimido
        for linea in archivo:
            for caracter in linea:
                bits_acumulados += tabla_codigos[caracter]

                while len(bits_acumulados) >= 8:
                    byte = bits_acumulados[:8]
                    bits_acumulados = bits_acumulados[8:]
                    archivo_comprimido.write(chr(int(byte, 2)))

        # En caso de que queden bits por escribir, se añade un byte adicional para completar el último byte
        if bits_acumulados:
            padding = 8 - len(bits_acumulados)
            bits_acumulados += '0' * padding
            archivo_comprimido.write(chr(int(bits_acumulados, 2)))
            archivo_comprimido.write(chr(padding))

        archivo.close()
        archivo_comprimido.close()


# Crea una instancia del CompresorHuffman, cuenta las frecuencias, construye el árbol, genera los códigos y comprime el archivo.
def comprimir_archivo_huffman(ruta_archivo, ruta_archivo_comprimido):
    compresor = CompresorHuffman(ruta_archivo)
    compresor.contar_frecuencia()
    arbol_huffman = compresor.construir_arbol()
    compresor.imprimir_arbol(arbol_huffman)
    tabla_codigos = compresor.generar_codigos(arbol_huffman)
    compresor.comprimir_archivo(ruta_archivo_comprimido, tabla_codigos)


def int_to_bin(int_value):
    binary = ''
    while int_value:
        int_value, remainder = divmod(int_value, 2)
        binary = str(remainder) + binary
    return binary

class DescompresorHuffman:
    def __init__(self, ruta_archivo_comprimido):
        self.ruta_archivo_comprimido = ruta_archivo_comprimido  # Ruta del archivo comprimido
        self.ruta_archivo_descomprimido = os.path.splitext(ruta_archivo_comprimido)[0]  # Ruta del archivo descomprimido

    '''
        - Este método descomprime el archivo comprimido utilizando el árbol de Huffman.
        - Abre el archivo comprimido en modo binario y el archivo descomprimido en modo escritura.
        - Lee los bytes del archivo comprimido y los convierte a su representación binaria.
        - Recorre el árbol de Huffman y va descendiendo por el árbol hasta llegar a una hoja, escribiendo el carácter 
          correspondiente en el archivo descomprimido.
        - Si se encuentra un byte adicional al final del archivo, se elimina el relleno y se cierra el archivo.
    '''
    def descomprimir_archivo(self):
        archivo_comprimido = open(self.ruta_archivo_comprimido, 'rb')  # Lectura en modo binario
        archivo_descomprimido = open(self.ruta_archivo_descomprimido, 'w')  # Escritura en modo texto

        # Leer la cabecera para obtener la longitud del árbol junto con el árbol serializado
        longitud_tabla_codigos = int.from_bytes(archivo_comprimido.read(4), 'big')

        # Deserializar el árbol
        tabla_codigos_serializada = archivo_comprimido.read(longitud_tabla_codigos)
        tabla_codigos = pickle.loads(tabla_codigos_serializada) # diccionario

        # Recorrer el árbol de Huffman y escribir los caracteres en el archivo descomprimido según la tabla de códigos
        bits_acumulados = ''
        byte = archivo_comprimido.read(1)
        while byte:
            bits_acumulados += int_to_bin(ord(byte)).zfill(8)
            for caracter, codigo in tabla_codigos.items():
                if bits_acumulados.startswith(codigo):
                    archivo_descomprimido.write(caracter)
                    bits_acumulados = bits_acumulados[len(codigo):]

            byte = archivo_comprimido.read(1)

        archivo_comprimido.close()
        archivo_descomprimido.close()


# Crea una instancia del DescompresorHuffman y descomprime el archivo.
def descomprimir_archivo(ruta_archivo_comprimido, ruta_archivo_descomprimido):
    descompresor = DescompresorHuffman(ruta_archivo_comprimido)
    descompresor.descomprimir_archivo()


# Recibe dos argumentos:
# - Flag que indica si se va a comprimir o descomprimir: -c para comprimir, -d para descomprimir
# - Ruta del archivo de entrada
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python huff.py [-c|-d] ruta_archivo")
        sys.exit()

    if sys.argv[1] == '-c':
        ruta_archivo = sys.argv[2]
        ruta_archivo_comprimido = ruta_archivo + '.huf'
        comprimir_archivo_huffman(ruta_archivo, ruta_archivo_comprimido)
    elif sys.argv[1] == '-d':
        ruta_archivo_comprimido = sys.argv[2]
        ruta_archivo_descomprimido = ruta_archivo_comprimido[:-4]
        descomprimir_archivo(ruta_archivo_comprimido, ruta_archivo_descomprimido)
