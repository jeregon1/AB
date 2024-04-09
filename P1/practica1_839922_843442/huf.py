#!/usr/bin/env python2.4
#coding=utf-8

from heapq import heapify, heappop, heappush
import os, sys, struct

"""
Funciones auxiliares de conversión de tipos
"""
# Convierte un entero a su forma de 4 bytes
def int_to_4bytes(int_value):
    return struct.pack('>I', int_value)

# Convierte 4 bytes a su forma de entero
def bytes4_to_int(bytes):
    return struct.unpack('>I', bytes)[0]

# Convierte un entero a su forma de un único byte
def int_to_1byte(int_value):
    return struct.pack('>B', int_value)

# Convierte un byte a su forma de entero
def bytes1_to_int(bytes):
    return struct.unpack('>B', bytes)[0]

# Convierte un byte a su forma de cadena con todos los 8 bits, incluyendo los ceros iniciales
# byte_to_str(ord(a)) = "01100001"
def byte_to_str(byte):
    binary_str = ''.join(str((byte >> i) & 1) for i in range(7, -1, -1))  # Convierte byte a cadena binaria
    padded_str = binary_str.zfill(8)  # Rellena con ceros a la izquierda
    return padded_str
    
# Convierte una cadena binaria a su forma de byte
# Ejemplo: "01100001" -> "a"
def str_to_char(s):
    return chr(int(s, 2))

# Convierte una cadena a su representación binaria.
# Ejemplo: "abc" -> "011000010110001001100011"
def string_to_binary(s):
    return ''.join(''.join(str((ord(c) >> i) & 1) for i in range(7, -1, -1)) for c in s)
    

"""
    Esta clase representa un nodo en el árbol de Huffman. 
    Cada nodo dispone de: 
     - un byte
     - su frecuencia en el texto 
     - referencias a sus nodos hijos (izquierda y derecha).
"""
class NodoHuffman:
    def __init__(self, byte=None, frecuencia=None, izquierda=None, derecha=None):
        self.byte = byte  # Byte del nodo
        self.frecuencia = frecuencia  # Frecuencia del byte
        self.izquierda = izquierda  # Nodo hijo izquierdo
        self.derecha = derecha # Nodo hijo derecho

    # Comparación de nodos por frecuencia
    def __cmp__(self, other):
        if self.frecuencia < other.frecuencia:
            return -1
        elif self.frecuencia > other.frecuencia:
            return 1
        else:
            return 0

""" Clase encargada de realizar la compresión utilizando el algoritmo de Huffman. Incrusta una cabecera
    al archivo comprimido, para posibilitar la posterior descompresión."""
class CompresorHuffman:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo  # Ruta del archivo de entrada

    # Cuenta la frecuencia de cada byte en el archivo.
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
        heapify(cola_prioridad) # Convierte la lista en una cola de prioridad o montículo (heap)

        while len(cola_prioridad) > 1:
            nodo_izquierda = heappop(cola_prioridad)
            nodo_derecha = heappop(cola_prioridad)
            nodo_padre = NodoHuffman(frecuencia=nodo_izquierda.frecuencia + nodo_derecha.frecuencia)
            nodo_padre.izquierda = nodo_izquierda
            nodo_padre.derecha = nodo_derecha

            heappush(cola_prioridad, nodo_padre)

        return cola_prioridad[0]

    # Imprime el árbol de Huffman de izquierda a derecha
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
        # Caso base: si el nodo es nulo, devolver un diccionario vacío
        if raiz is None:
            return {}

        # Caso base: si el nodo es una hoja, devolver un diccionario con el byte y su código
        if raiz.byte is not None:
            return {raiz.byte: codigo or '0'}

        # Caso recursivo: generar los códigos para los hijos izquierdo y derecho
        codigos = {}
        codigos.update(CompresorHuffman.generar_codigos(raiz.izquierda, codigo + '0'))
        codigos.update(CompresorHuffman.generar_codigos(raiz.derecha,   codigo + '1'))

        return codigos
    
    """ 
    Serializa el árbol de Huffman en una cadena de unos y ceros mediante las reglas:
        - Si el nodo es una hoja, se representa con '1' seguido de su byte.
        - Si el nodo es interno, se representa con '0' y se concatenan las representaciones de sus hijos. 
    """
    @staticmethod
    def serializar_arbol_huffman(raiz):
        if raiz is None: # Nodo nulo
            return ''
        elif raiz.byte is not None: # Nodo hoja
            return '1' + byte_to_str(ord(raiz.byte))
        else: # Nodo interno, concatenar representaciones de los hijos
            return '0' + CompresorHuffman.serializar_arbol_huffman(raiz.izquierda) + CompresorHuffman.serializar_arbol_huffman(raiz.derecha)

    """ Convierte el árbol de Huffman en su representación binaria según las reglas de serialización de arriba """
    def binary_tree_to_bytes (self, node):
        binary_tree = self.serializar_arbol_huffman(node)
        bytes_tree = ''
        while binary_tree is not '': # Mientras queden bits por procesar
            bits_8 = binary_tree[:8]
            # Necesario para el caso de los últimos bits
            if len(bits_8) is not 8: bits_8 = bits_8 + (8 - len(bits_8)) * '0'
            # A continuación convertimos los 8 bits (en forma de string) a su forma de byte
            byte = 0
            for char in bits_8:
                if char == '1': bit = 1
                else:           bit = 0
                byte = byte << 1 | bit # Desplazamos los bits a la izquierda y añadimos el bit actual

            bytes_tree += chr(byte) # Concatenamos los 8 bits (en representación de byte) a la cadena de bytes
            binary_tree = binary_tree[8:] # Eliminamos los 8 bits que ya hemos procesado
        return bytes_tree

    """ A partir del árbol de Huffman, genera la cabecera que se añadirá al archivo comprimido.
        La cabecera es el árbol serializado con la longitud del árbol en los primeros 4 bytes,
        necesaria para la hora de deserializar el árbol en la descompresión. """
    def generar_cabecera(self, root):
        arbol_serializado = self.binary_tree_to_bytes(root) # Serializar el árbol de Huffman
        len_arbol_serializado_bytes = int_to_4bytes(len(arbol_serializado)) # Fijar la longitud a 4 bytes
        return len_arbol_serializado_bytes + arbol_serializado # Devolver el árbol con la cabecera incrustada al inicio

    '''
        Comprime el archivo de entrada utilizando los códigos generados por el árbol de Huffman.
        Realiza los siguientes pasos:
         - Abre el archivo original en modo lectura y el archivo comprimido en modo binario.
         - Recorre el archivo original, reemplazando cada byte por su código binario correspondiente y escribiendo 
           los bytes resultantes en el archivo comprimido.
         - Si al final del archivo aún hay bits por escribir, se añade un byte adicional para completar el último byte 
           y se agrega información sobre el relleno al final del archivo.
    '''
    def comprimir_archivo(self, ruta_archivo_comprimido, tabla_codigos, arbol_huffman):
        archivo = open(self.ruta_archivo, 'r') # Lectura en modo texto

        bits_acumulados = ''
        content = ''

        # Recorrer el fichero original y escribir los bits comprimidos en el fichero comprimido
        for linea in archivo:
            for byte in linea:
                bits_acumulados += tabla_codigos[byte] # Añadir el código binario correspondiente al byte

                while len(bits_acumulados) >= 8:
                    byte_to_write = bits_acumulados[:8]   # Tomar los primeros 8 bits
                    content += str_to_char(byte_to_write) # Convertir los 8 bits a su forma de byte y añadir al contenido
                    bits_acumulados = bits_acumulados[8:] # Eliminar los 8 bits que ya se han escrito

        # En caso de que queden bits por escribir, se añade un byte adicional para completar el último byte
        padding = 0
        if bits_acumulados:
            padding = 8 - len(bits_acumulados)
            bits_acumulados += '0' * padding
            content += str_to_char(bits_acumulados) # Añadir el byte de padding

        archivo.close() # Cerrar el archivo original

        archivo_comprimido = open(ruta_archivo_comprimido, 'wb') # Escritura en modo binario

        # Generar la cabecera y escribirla en el archivo comprimido
        archivo_comprimido.write(self.generar_cabecera(arbol_huffman))

        # Escribir en 1 byte la cantidad de bits de relleno del último byte
        archivo_comprimido.write(int_to_1byte(padding))
        archivo_comprimido.write(content)

        archivo_comprimido.close() # Cerrar el archivo comprimido

""" 
Imprime la información del árbol de Huffman, incluyendo:
 - Si "show_tree" es True, imprime el árbol de Huffman
 - Porcentaje de nodos hoja en cada profundidad
 - Profundidad máxima del árbol 
"""
def info_arbol_huffman(arbol_huffman, show_tree=False):

    # Imprimir el árbol de Huffman, si es el caso
    if show_tree: print("Arbol"); CompresorHuffman.imprimir_arbol(arbol_huffman)

    profundidad = [0] # Asume que el árbol tiene al menos un nodo
    total_leafs_per_depth = [0] # Número de nodos hoja en cada profundidad

    """
    Función recursiva que recorre el árbol de Huffman. En cada nodo, verifica la profundidad actual del nodo. 
    La profundidad de un nodo se define como la longitud del camino desde la raíz hasta ese nodo.
    """
    def helper(node, depth):        
        if node is None: # Caso base: nodo nulo
            return
        if depth > profundidad[0]: # Actualizar la profundidad máxima y el número de nodos hoja en cada profundidad
            profundidad[0] = depth
            # extiender la lista total_leafs_per_depth para tener un espacio para contar los nodos hoja en las nuevas profundidades
            total_leafs_per_depth.extend([0] * (depth - len(total_leafs_per_depth) + 1))
        if node.byte is not None: # Si es un nodo hoja, incrementar el número de nodos hoja en esa profundidad
            total_leafs_per_depth[depth] += 1
        helper(node.izquierda, depth + 1)
        helper(node.derecha, depth + 1)

    # Llamada inicial al método helper
    if arbol_huffman is not None: helper(arbol_huffman, 0)

    hojas = sum(total_leafs_per_depth)
    percentages_per_depth = [total_leafs_per_depth[i] / float(hojas) * 100 for i in range(len(total_leafs_per_depth))]

    for i in range(len(percentages_per_depth)):
        print ("Profundidad %d: %.2f%%" % (i, percentages_per_depth[i]))

    print("Profundidad máxima: " + str(profundidad[0]))


""" Crea una instancia del CompresorHuffman, construye el árbol, genera los códigos y comprime el archivo. """
def comprimir_archivo_huffman(ruta_archivo, ruta_archivo_comprimido):
    # Si el archivo está vacío, crear uno vacío con la extensión .huf
    if os.stat(ruta_archivo).st_size == 0:
        open(ruta_archivo_comprimido, 'w').close()
        return

    compresor = CompresorHuffman(ruta_archivo)
    arbol_huffman = compresor.construir_arbol()
    tabla_codigos = compresor.generar_codigos(arbol_huffman)
    compresor.comprimir_archivo(ruta_archivo_comprimido, tabla_codigos, arbol_huffman)

    # Descomentar la siguiente línea si se desea imprimir información relativa al árbol de Huffman generado
    # info_arbol_huffman(arbol_huffman, show_tree=True)

""" Clase encargada de descomprimir un archivo comprimido con el algoritmo de Huffman. Recupera la información necesaria 
    para la descompresión a partir de la cabecera del archivo comprimido. """
class DescompresorHuffman:
    def __init__(self, ruta_archivo_comprimido):
        self.ruta_archivo_comprimido = ruta_archivo_comprimido

    """ Reconstruye el árbol de Huffman a partir de la cadena serializada. """
    def deserializar_huffman_tree(self, s):
        """ Método auxiliar encargado de recorrer la cadena serializada y reconstruir el árbol. """
        def helper(bits):
            if len(bits) == 0:
                return None

            bit = bits.pop(0)
            if bit == '1':
                byte = str_to_char(''.join(bits[:8])) # Convertir los siguientes 8 bits a un carácter
                del bits[:8] # Eliminar los 8 bits que ya hemos procesado
                return NodoHuffman(byte)
            else: # bit =='0'
                left = helper(bits)
                right = helper(bits)
                return NodoHuffman(izquierda=left, derecha=right)

        return helper(list(s)) # Convertir la cadena a una lista de bits

    """ Lee el archivo comprimido y extrae el contenido (bits) y la tabla de códigos. """
    def leer_archivo(self, archivo_comprimido):
        archivo_comprimido = open(self.ruta_archivo_comprimido, 'rb')
        
        len_tree = bytes4_to_int(archivo_comprimido.read(4)) # Leemos la longitud que ocupa el árbol serializado

        serialized_tree_binary = archivo_comprimido.read(len_tree) # Leemos el árbol serializado

        serialized_tree_str = string_to_binary(serialized_tree_binary) # Convertimos el árbol serializado a su representación en cadena
        
        arbol_huffman = self.deserializar_huffman_tree(serialized_tree_str) # Reconstruimos el árbol de Huffman
        
        tabla_char_codigo = CompresorHuffman.generar_codigos(arbol_huffman) # Generamos la tabla de códigos a partir del árbol de Huffman

        # Invertimos la tabla de códigos para poder buscar los códigos en O(1)
        tabla_codigo_char = {}
        for k, v in tabla_char_codigo.items():
            tabla_codigo_char[v] = k
        
        len_padding = bytes1_to_int(archivo_comprimido.read(1)) # Leemos la longitud del relleno del último byte

        # Leemos el resto del archivo comprimido
        bytes = archivo_comprimido.read()
        archivo_comprimido.close()
        bits = string_to_binary(bytes)

        # Eliminamos los bits de relleno del último byte, si los hay
        if len_padding > 0:
            bits = bits[ : -len_padding]

        return bits, tabla_codigo_char


    """ Descomprime el archivo comprimido deserializando el árbol de Huffman de la cabecera. """
    def descomprimir_archivo(self):
        # Leemos el archivo comprimido y extraemos el contenido (bits) y la tabla de códigos
        bits, tabla_codigo_char = self.leer_archivo(self.ruta_archivo_comprimido)

        # Abrimos el archivo de salida para escribir los datos descomprimidos
        nombre_archivo, _ = os.path.splitext(self.ruta_archivo_comprimido)
        archivo_descomprimido = open(nombre_archivo, 'wb')

        # Descomprimimos los datos usando la tabla de códigos, cuyas claves son los códigos y
        # los valores son los bytes, escribiendo en lotes para no saturar la memoria
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

""" Crea una instancia del DescompresorHuffman y descomprime el archivo. """
def descomprimir_archivo_huffman(ruta_archivo_comprimido):
    # Si el archivo comprimido está vacío, crear uno vacío con la extensión original
    if os.stat(ruta_archivo_comprimido).st_size == 0:
        nombre_archivo, _ = os.path.splitext(ruta_archivo_comprimido)
        open(nombre_archivo, 'w').close()
        return
    descompresor = DescompresorHuffman(ruta_archivo_comprimido)
    descompresor.descomprimir_archivo()


""" 
Argumentos recibidos por el programa principal:
 * Flag que indica si se va a comprimir o descomprimir: 
    '-c' para comprimir 
    '-d' para descomprimir
 * Ruta del archivo de entrada 

Si no se reciben los argumentos necesarios, se imprime un mensaje de
error indicando la correcta invocación del programa. 
"""
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python huff.py [-c | -d] ruta_archivo")
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
