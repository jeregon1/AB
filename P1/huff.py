# coding=utf-8
from heapq import heapify, heappop, heappush
import os, sys, struct

def int_to_4bytes(int_value):
    return struct.pack('>I', int_value)
    

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

    def imprimir_arbol(self, raiz, nivel=0):
        if raiz is not None:
            self.imprimir_arbol(raiz.derecha, nivel + 1)
            if raiz.byte is None: byte = ''
            else: byte = raiz.byte
            print(' ' * nivel * 6 + '->' + byte + ' ' + str(raiz.frecuencia))
            self.imprimir_arbol(raiz.izquierda, nivel + 1)

    '''
        - Este método genera los códigos binarios para cada byte en el árbol de Huffman.
        - Recorre el árbol recursivamente y asigna '0' para el hijo izquierdo y '1' para el hijo derecho, 
          acumulando los códigos para cada byte.
    '''
    def generar_codigos(self, raiz, codigo=''):
        if raiz is None:
            return {}

        if raiz.byte is not None:
            return {raiz.byte: codigo}

        codigos = {}
        codigos.update(self.generar_codigos(raiz.izquierda, codigo + '0'))
        codigos.update(self.generar_codigos(raiz.derecha, codigo + '1'))

        return codigos

# 01a001c1b001f1e1d
    def serialize_huffman_tree(self, node):
        if node is None:
            return ''
        elif node.byte is not None: # Leaf node
            return '1' + byte_to_str(ord(node.byte))
        else: # Internal node
            return '0' + self.serialize_huffman_tree(node.izquierda) + self.serialize_huffman_tree(node.derecha)

    # Function that converts the binary serialized tree into its bits represenntation
    # It receives a string containing only ones and zeros and then it returns the
    def binary_tree_to_bytes (self, node):
        binary = self.serialize_huffman_tree(node)
        bytes = ''
        while binary is not '':
            bits_8 = binary[:8]
            # Needed for the last bits case
            if len(bits_8) is not 8: bits_8 = bits_8 + (8 - len(bits_8)) * '0'
            # Here we convert "01100001" to its byte form
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

    """

        def decompress_tree(self, file):
            # Read the length of the compressed tree from the file
            tree_length = ord(file.read(4))

            # Read that many bytes to get the compressed tree
            compressed_tree = file.read(tree_length)

            # Convert the compressed tree to a binary string
            binary_tree = ''.join(format(ord(byte), '08b') for byte in compressed_tree)

            # Deserialize the Huffman tree
            tree, _ = self.deserialize_huffman_tree(binary_tree)

            return tree

        def deserialize_huffman_tree(self, serialized_tree):
            # If the serialized tree is empty, return None
            if not serialized_tree:
                return None, ''

            # Get the first character of the serialized tree
            first_char = serialized_tree[0]

            # If the first character is '1', this is a leaf node
            if first_char == '1':
                # The next 8 characters are the binary representation of the byte
                byte = chr(int(serialized_tree[1:9], 2))
                # Return the leaf node and the remaining serialized tree
                return Node(byte=byte), serialized_tree[9:]

            # If the first character is '0', this is not a leaf node
            else:
                # Deserialize the left subtree
                left, serialized_tree = self.deserialize_huffman_tree(serialized_tree[1:])
                # Deserialize the right subtree
                right, serialized_tree = self.deserialize_huffman_tree(serialized_tree)
                # Return the node and the remaining serialized tree
                return Node(left=left, right=right), serialized_tree

    """

    # A partir de la tabla de códigos, genera la cabecera que se añadirá al archivo comprimido
    def generar_cabecera(self, root):
        # La cabecera es el árbol serializado con la longitud del árbol al principio
        arbol_serializado = self.binary_tree_to_bytes(root)
        print("arbol serializado:" + arbol_serializado)
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

        # Recorrer el fichero original y escribir los bits comprimidos en el fichero comprimido
        for linea in archivo:
            for byte in linea:
                bits_acumulados += tabla_codigos[byte]

                while len(bits_acumulados) >= 8:
                    byte_to_write = bits_acumulados[:8]   # Tomar los primeros 8 bits
                    bits_acumulados = bits_acumulados[8:] # Eliminar los 8 bits que ya se han escrito
                    archivo_comprimido.write(chr(int(byte_to_write, 2)))

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
    arbol_huffman = compresor.construir_arbol()
    compresor.imprimir_arbol(arbol_huffman)
    tabla_codigos = compresor.generar_codigos(arbol_huffman)
    compresor.comprimir_archivo(ruta_archivo_comprimido, tabla_codigos, arbol_huffman)

# byte_to_str(ord(a)) = "01100001"
# It converts a byte to its str form with all 8 bits, including starting zeros
def byte_to_str(byte):
    binary_str = ''.join(str((byte >> i) & 1) for i in range(7, -1, -1))  # Convert byte to binary string
    padded_str = binary_str.zfill(8)  # Pad the binary string with leading zeros
    return padded_str
    
def str_to_char(s):
    """Convert a binary string to a char."""
    return chr(int(s, 2))


"""     
def reconstruir_arbol(self, serialized_tree):
        # index es una lista para que pueda sea global dentro de reconstruir_arbol.
        # Por ello solo se utiliza la primera componente, como si fuera un tipo int
        index = [0]

        def reconstruir_helper():
            bit = serialized_tree[index[0]]
            index[0] += 1
            if bit == 1:
                byte = serialized_tree[index[0]: index[0] + 8]
                index[0] += 8
                return NodoHuffman(chr(int(byte, 2)))
            else:
                left = reconstruir_helper()
                right = reconstruir_helper()
                return NodoHuffman(frecuencia=left.frecuencia + right.frecuencia, izquierda=left, derecha=right)

        return reconstruir_helper() 
"""
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
        len_tree = struct.unpack('>I', archivo_comprimido.read(4))[0]
        print("len_tree: " + str(len_tree))

        # Leemos el árbol serializado
        serialized_tree_binary = archivo_comprimido.read(len_tree)
        print("serialized_tree: " + serialized_tree_binary)
        serialized_tree_str = string_to_binary(serialized_tree_binary)
        print("binary version:" + serialized_tree_str)

        # Reconstruimos el árbol de Huffman
        arbol_huffman = self.deserialize_huffman_tree(serialized_tree_str)
        CompresorHuffman.imprimir_arbol(CompresorHuffman(''), arbol_huffman)

        # Inicializamos el nodo actual como la raíz del árbol
        nodo_actual = arbol_huffman

        # Leemos el resto del archivo comprimido
        bytes = archivo_comprimido.read()
        bits = string_to_binary(bytes)

        # Abrimos el archivo de salida para escribir los datos descomprimidos
        nombre_archivo, _ = os.path.splitext(self.ruta_archivo_comprimido)
        nombre_archivo = "d/" + nombre_archivo
        archivo_descomprimido = open(nombre_archivo, 'wb')

        # Recorremos los bits y descomprimimos
        for bit in bits:
            if bit == '0':
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha

            if nodo_actual.byte is not None:
                archivo_descomprimido.write(nodo_actual.byte)
                nodo_actual = arbol_huffman

        archivo_comprimido.close()
        archivo_descomprimido.close()

def descomprimir_archivo_huffman(ruta_archivo_comprimido):
    descompresor = DescompresorHuffman(ruta_archivo_comprimido)
    descompresor.descomprimir_archivo()

def string_to_binary(s):
    return ''.join(''.join(str((ord(c) >> i) & 1) for i in range(7, -1, -1)) for c in s)

def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] & (1 << shift)) >> shift

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
    elif sys.argv[1] == '-j':
        print(byte_to_str(ord('a')))
