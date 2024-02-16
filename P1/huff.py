#!/usr/bin/env python2.4
# coding=utf-8

from heapq import heapify, heappop, heappush
import os, sys, struct

def int_to_4bytes(int_value):
    return struct.pack('>I', int_value)

def bytes4_to_int(bytes):
    return struct.unpack('>I', bytes)[0]

def int_to_1byte(int_value):
    return struct.pack('>B', int_value)

def bytes1_to_int(bytes):
    return struct.unpack('>B', bytes)[0]

# byte_to_str(ord(a)) = "01100001"
# Convierte un byte a su forma de cadena con todos los 8 bits, incluyendo los ceros iniciales
def byte_to_str(byte):
    binary_str = ''.join(str((byte >> i) & 1) for i in range(7, -1, -1))  # Convierte byte a cadena binaria
    padded_str = binary_str.zfill(8)  # Rellena con ceros a la izquierda
    return padded_str
    
def str_to_char(s):
    """Convert a binary string to a char."""
    return chr(int(s, 2))

def string_to_binary(s):
    return ''.join(''.join(str((ord(c) >> i) & 1) for i in range(7, -1, -1)) for c in s)
    

"""
    Esta clase representa un nodo en el árbol de Huffman. Cada nodo tiene un byte, su frecuencia
    en el texto y dos referencias a sus nodos hijos (izquierda y derecha).
"""
class NodoHuffman:
    def __init__(self, byte=None, frecuencia=None, izquierda=None, derecha=None):
        self.byte = byte  # Byte del nodo
        self.frecuencia = frecuencia  # Frecuencia del byte
        self.izquierda = izquierda  # Nodo hijo izquierdo
        self.derecha = derecha # Nodo hijo derecho

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
    - Este método cuenta la frecuencia de cada byte en el archivo.
    '''
    def contar_frecuencia(self):
        frecuencia_bytes = {}
        archivo = open(self.ruta_archivo, 'rb')
        for linea in archivo:
            for byte in linea:
                if byte in frecuencia_bytes:
                    frecuencia_bytes[byte] += 1
                else:
                    frecuencia_bytes[byte] = 1
        archivo.close()

        return frecuencia_bytes

    ''' 
    - Este método construye el árbol de Huffman a partir de las frecuencias de los bytes.
    - Utiliza una cola de prioridad para mantener los nodos ordenados por frecuencia.
    - Los nodos con menor frecuencia estarán a la mayor profundidad del árbol mientras que los nodos con mayor
        frecuencia estarán a menor profundidad, de manera que el byte más frecuente tendrá el código más corto.
    '''
    def construir_arbol(self):
        cola_prioridad = [NodoHuffman(byte, frecuencia) for byte, frecuencia in self.contar_frecuencia().items()]
        heapify(cola_prioridad) # Convierte la lista en una cola de prioridad

        while len(cola_prioridad) > 1:
            nodo_izquierda = heappop(cola_prioridad)
            nodo_derecha = heappop(cola_prioridad)
            nodo_padre = NodoHuffman(frecuencia=nodo_izquierda.frecuencia + nodo_derecha.frecuencia)
            nodo_padre.izquierda = nodo_izquierda
            nodo_padre.derecha = nodo_derecha

            heappush(cola_prioridad, nodo_padre)

        return cola_prioridad[0]

    @staticmethod
    def imprimir_arbol(raiz, nivel=0):
        if raiz is not None:
            CompresorHuffman.imprimir_arbol(raiz.derecha, nivel + 1)
            if raiz.byte is None: byte = ''
            else: byte = raiz.byte
            print(' ' * nivel * 6 + '->' + byte + ' ' + str(raiz.frecuencia))
            CompresorHuffman.imprimir_arbol(raiz.izquierda, nivel + 1)

    '''
        - Este método genera los códigos binarios para cada byte en el árbol de Huffman.
        - Recorre el árbol recursivamente y asigna '0' para el hijo izquierdo y '1' para el hijo derecho, 
          acumulando los códigos para cada byte.
    '''
    @staticmethod
    def generar_codigos(raiz, codigo=''):
        if raiz is None:
            return {}

        if raiz.byte is not None:
            return {raiz.byte: codigo or '0'}

        codigos = {}
        codigos.update(CompresorHuffman.generar_codigos(raiz.izquierda, codigo + '0'))
        codigos.update(CompresorHuffman.generar_codigos(raiz.derecha,   codigo + '1'))

        return codigos

    # 01a001c1b001f1e1d
    @staticmethod
    def serialize_huffman_tree(raiz):
        if raiz is None:
            return ''
        elif raiz.byte is not None: # Leaf node
            return '1' + byte_to_str(ord(raiz.byte))
        else: # Internal node
            return '0' + CompresorHuffman.serialize_huffman_tree(raiz.izquierda) + CompresorHuffman.serialize_huffman_tree(raiz.derecha)

    # Función que convierte el árbol serializado en su representación binaria
    # Recibe una cadena que contiene solo unos y ceros y luego devuelve la representación en bytes
    def binary_tree_to_bytes (self, node):
        binary = self.serialize_huffman_tree(node)
        bytes = ''
        while binary is not '':
            bits_8 = binary[:8]
            # Necesario para el caso de los últimos bits
            if len(bits_8) is not 8: bits_8 = bits_8 + (8 - len(bits_8)) * '0'
            # Aquí convertimos "01100001" a su forma de byte
            byte = 0
            for char in bits_8:
                if char == '1': bit = 1
                else:           bit = 0
                byte = byte << 1 | bit
            
            # Transforming 8 bits to its ascii byte representation
            bytes += chr(byte)
            binary = binary[8:]
        return bytes

    #                   01011000 01001011 00011101 10001000 10110011 01011001 01101100 10000000
    # cabecera ejemplo: 01011000 01001011 00011101 10001000 10110011 01011001 01101100 100
    # XK��Yl�


    # A partir de la tabla de códigos, genera la cabecera que se añadirá al archivo comprimido
    def generar_cabecera(self, root):
        # La cabecera es el árbol serializado con la longitud del árbol al principio
        arbol_serializado = self.binary_tree_to_bytes(root)
        len_arbol_serializado_bytes = int_to_4bytes(len(arbol_serializado))
        return len_arbol_serializado_bytes + arbol_serializado

    '''
        - Este método comprime el archivo de entrada utilizando los códigos generados por el árbol de Huffman.
        - Abre el archivo original en modo lectura y el archivo comprimido en modo binario.
        - Recorre el archivo original, reemplazando cada byte por su código binario correspondiente y escribiendo 
          los bytes resultantes en el archivo comprimido.
        - Si al final del archivo aún hay bits por escribir, se añade un byte adicional para completar el último byte 
          y se agrega información sobre el relleno al final del archivo.
    '''
    def comprimir_archivo(self, ruta_archivo_comprimido, tabla_codigos, arbol_huffman):
        archivo = open(self.ruta_archivo, 'r') # Lectura en modo texto
        archivo_comprimido = open(ruta_archivo_comprimido, 'wb') # Escritura en modo binario

        # Generar la cabecera y escribirla en el archivo comprimido
        archivo_comprimido.write(self.generar_cabecera(arbol_huffman))

        bits_acumulados = ''
        content = ''

        # Recorrer el fichero original y escribir los bits comprimidos en el fichero comprimido
        for linea in archivo:
            for byte in linea:
                bits_acumulados += tabla_codigos[byte]

                while len(bits_acumulados) >= 8:
                    byte_to_write = bits_acumulados[:8]   # Tomar los primeros 8 bits
                    bits_acumulados = bits_acumulados[8:] # Eliminar los 8 bits que ya se han escrito
                    content += str_to_char(byte_to_write)


        padding = 0
        # En caso de que queden bits por escribir, se añade un byte adicional para completar el último byte
        if bits_acumulados:
            padding = 8 - len(bits_acumulados)
            bits_acumulados += '0' * padding
            content += str_to_char(bits_acumulados)

        # Escribir en 1 byte la cantidad de bits de relleno del último byte
        archivo_comprimido.write(int_to_1byte(padding))
        archivo_comprimido.write(content)

        archivo.close()
        archivo_comprimido.close()

def info_arbol_huffman(arbol_huffman, show_tree=False):
    if show_tree: print("Arbol"); CompresorHuffman.imprimir_arbol(arbol_huffman)
    profundidad = [0] # Asume que el árbol tiene al menos un nodo
    total_leafs_per_depth = [0]

    def helper(node, depth):
        if node is None:
            return
        if depth > profundidad[0]:
            profundidad[0] = depth
            total_leafs_per_depth.extend([0] * (depth - len(total_leafs_per_depth) + 1))
        if node.byte is not None:
            total_leafs_per_depth[depth] += 1
        helper(node.izquierda, depth + 1)
        helper(node.derecha, depth + 1)

    if arbol_huffman is not None: helper(arbol_huffman, 0)

    hojas = sum(total_leafs_per_depth)
    percentages_per_depth = [total_leafs_per_depth[i] / float(hojas) * 100 for i in range(len(total_leafs_per_depth))]

    for i in range(len(percentages_per_depth)):
        print ("Profundidad %d: %.2f%%" % (i, percentages_per_depth[i]))

    print("Profundidad máxima: " + str(profundidad[0]))


# Crea una instancia del CompresorHuffman, cuenta las frecuencias, construye el árbol, genera los códigos y comprime el archivo.
def comprimir_archivo_huffman(ruta_archivo, ruta_archivo_comprimido):
    compresor = CompresorHuffman(ruta_archivo)
    arbol_huffman = compresor.construir_arbol()
    tabla_codigos = compresor.generar_codigos(arbol_huffman)
    compresor.comprimir_archivo(ruta_archivo_comprimido, tabla_codigos, arbol_huffman)

    info_arbol_huffman(arbol_huffman, show_tree=True)


class DescompresorHuffman:
    def __init__(self, ruta_archivo_comprimido):
        self.ruta_archivo_comprimido = ruta_archivo_comprimido

    # Función para reconstruir el árbol de Huffman a partir de la información serializada
    def deserialize_huffman_tree(self, s):
        """Deserialize a Huffman tree from a string."""
        def helper(bits):
            if len(bits) == 0:
                return None

            bit = bits.pop(0)
            if bit == '1':
                # Convert the next 8 bits to a character
                byte = str_to_char(''.join(bits[:8]))
                del bits[:8]
                return NodoHuffman(byte)
            else: # '0'
                left = helper(bits)
                right = helper(bits)
                return NodoHuffman(izquierda=left, derecha=right)

        # Convert the string to a list of bits
        bits = list(s)
        return helper(bits)

    # Función para descomprimir el archivo comprimido usando el árbol de Huffman reconstruido
    def descomprimir_archivo(self):
        archivo_comprimido = open(self.ruta_archivo_comprimido, 'rb')

        # Leemos la longitud del árbol serializado
        len_tree = bytes4_to_int(archivo_comprimido.read(4))

        # Leemos el árbol serializado
        serialized_tree_binary = archivo_comprimido.read(len_tree)
        # Convertimos el árbol serializado a su representación en cadena
        serialized_tree_str = string_to_binary(serialized_tree_binary)

        # Reconstruimos el árbol de Huffman
        arbol_huffman = self.deserialize_huffman_tree(serialized_tree_str)

        tabla_char_codigo = CompresorHuffman.generar_codigos(arbol_huffman)
        tabla_codigo_char = {}
        # Invertimos la tabla de códigos para poder buscar los códigos en O(1)
        for k, v in tabla_char_codigo.items():
            tabla_codigo_char[v] = k
        
        # Leemos la longitud del relleno del último byte
        len_padding = bytes1_to_int(archivo_comprimido.read(1))

        # Leemos el resto del archivo comprimido
        bytes = archivo_comprimido.read()
        bits = string_to_binary(bytes)
        archivo_comprimido.close()
        
        # Eliminamos los bits de relleno del último byte
        if len_padding > 0:
            bits = bits[ : -len_padding]

        # Abrimos el archivo de salida para escribir los datos descomprimidos
        nombre_archivo, _ = os.path.splitext(self.ruta_archivo_comprimido)
        archivo_descomprimido = open(nombre_archivo, 'wb')

        # Descomprimimos los datos usando la tabla de códigos, cuyas claves son los códigos y los valores son los bytes
        # Y escribimos en batches, para no saturar la memoria
        batch_size = 8000
        content = ''
        codigo = ''
        for bit in bits:
            codigo += bit
            if codigo in tabla_codigo_char:
                content += tabla_codigo_char[codigo]
                if len(content) >= batch_size:
                    archivo_descomprimido.write(content)
                    content = ''
                codigo = ''
        archivo_descomprimido.write(content)
        archivo_descomprimido.close()


def descomprimir_archivo_huffman(ruta_archivo_comprimido):
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
        descomprimir_archivo_huffman(ruta_archivo_comprimido)
    else:
        print("Uso: python huff.py [-c|-d] ruta_archivo")
        sys.exit()
