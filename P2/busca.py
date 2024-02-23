#!/mnt/c/Users/jesus/anaconda3/envs/alg/python.exe

import time, sys

""" 
Algotirmo de búsqueda con retroceso que, dados:
    - La dimensión de la página (anchura W y altura H) 
    - Una lista de n artículos, cada uno con su dimensión y posición (es decir, anchura wi,
       altura hi y coordenadas cartesianas (xi, yi) como especificado anteriormente)

determine los artículos a colocar en la página maximizando el área total ocupada por artículos y calcule la cantidad de espacio total ocupada por
los mismos
"""

# Formato fichero de entrada:
"""
Organized by blocks starting with 3 numbers: n (number of articles), W (page width) and L (page height).
The following n lines contain 4 numbers in this order:
    - w, article width
    - h, article height
    - x, article's top left corner x coordinate
    - y, article's top left corner y coordinate

Page example: (x,y)
(0,0)               (W,0)
+-------------------+
|                   |
|                   |
|                   |
|                   |
|                   |
|                   |
|                   |
+-------------------+
(0,H)               (W,H)

Ejemplo:
5 280 400    👈🏼 Block 1
10 10 0 0        👈🏼 Article 1
10 10 15 15      👈🏼 Article 2
10 10 10 10      👈🏼 Article 3
20 10 20 20      👈🏼 Article 4
20 10 25 15      👈🏼 Article 5
6 280 400    👈🏼 Block 2
10 20 30 40
50 60 70 80
20 30 40 50
90 80 70 60
80 70 60 50
50 50 40 40

Asumiciones:
 - Hay al menos un bloque
 - En cada bloque hay al menos un artículo
 - Las coordenadas y dimensiones de los artículos son enteros positivos 
 - Las coordenadas y dimensiones de los artículos son tales que el artículo está completamente dentro de la página
"""

# Formato fichero de salida:
"""
Una línea por cada bloque que contiene 2 números: 
 - área total ocupada por los artículos (en mm)
 - tiempo necesitado (en milisegundos) para calcular la solución.
"""


"""
Class that represents an article
"""
class Article:
    def __init__(self, w, h, x, y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def __str__(self):
        return "w: {}, h: {}, x: {}, y: {}".format(self.w, self.h, self.x, self.y)

""" 
Class that represents a block of articles
"""
class Block:
    def __init__(self, n_articles, W, H, articles):
        self.n_articles = n_articles
        self.W = W
        self.H = H
        self.articles = articles

    def __str__(self):
        articles_str = ""
        for article in self.articles:
            articles_str +=  str(article) + "\n"
        return "n: {}, W: {}, H: {}, articles:\n{}".format(self.n_articles, self.W, self.H, articles_str)


"""
Reads a file containing the blocks and articles and returns a list of blocks
"""
def read_file(file):
    blocks = []
    with open(file, "r") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            n, W, H = map(int, lines[i].split())
            articles = []
            for j in range(i + 1, i + 1 + n):
                w, h, x, y = map(int, lines[j].split())
                articles.append(Article(w, h, x, y))
            blocks.append(Block(n, W, H, articles))
            i += 1 + n
    return blocks

def calculate_area(articles):
    area = 0
    for article in articles:
        area += article.w * article.h
    return area

def check_overlap(article, articles):
    for a in articles:
        article_is_left = article.x + article.w <= a.x
        article_is_right = a.x + a.w <= article.x
        article_is_up = article.y + article.h <= a.y
        article_is_down = a.y + a.h <= article.y
        if not (article_is_left or article_is_right or article_is_up or article_is_down):
            return True
    return False

def sort_articles(articles):
    return sorted(articles, key=lambda a: a.w * a.h, reverse=True)

"""
Backtracking function that maximizes the area covered by articles in a block and calculates the total space occupied by them.
Articles can't overlap and must be inside the page.
Returns the maximum area found and the list of articles that maximize it
"""
def busca(block):
    """ 
     1. Ordenar los artículos por área (w * h) de mayor a menor
     2. Inicializar el área total ocupada por los artículos a 0
     3. Dada la lista de artículos, para cada artículo, hacer:
        - Si el artículo no se solapa con ningún otro artículo y está dentro de la página, entonces:
            - Añadir el área del artículo al área total ocupada por los artículos
            - Marcar el artículo como colocado
            - Si el área total ocupada por los artículos es mayor que el área total ocupada por los artículos mejor hasta el momento, entonces:
                - Actualizar el área total ocupada por los artículos mejor hasta el momento
                - Actualizar la lista de artículos mejor hasta el momento
                - Deshacer el artículo
    4. Devolver el área total ocupada por los artículos mejor hasta el momento
    """
    block.articles = sort_articles(block.articles) # The base solution is the largest article, as we assume all articles fit in the page
    max_articles = [block.articles[0]]
    max_area = calculate_area(max_articles)
    return busca_backtracking(block, 1, max_area, max_articles)
    
"""
Recursive function that looks for the best combination of articles to maximize the area covered by them
Parameters:
    - block: block of articles
    - i: index of the article to check (number of articles checked so far)
    - max_area: maximum area found so far
    - articles: list of articles that maximize the area
"""
def busca_backtracking(block, i, max_area, max_articles):
    if i == block.n_articles: # Base case: all articles have been checked
        return max_area, max_articles
    
    for article in block.articles[i:]:
        if not check_overlap(article, max_articles):
            max_articles.append(article)
            new_area = calculate_area(max_articles)

            if new_area > max_area:
                max_area = new_area
                max_articles = max_articles.copy()
                
            max_area, max_articles = busca_backtracking(block, i + 1, max_area, max_articles)
            max_articles.pop()

    # If no new article has been added, return the current area and articles received as parameters
    return max_area, max_articles


class Solution:
    def __init__(self, area, articles, time):
        self.area = area
        self.articles = articles
        self.time = time

    def __str__(self):
        return "{} {:.6f}".format(self.area, self.time)

"""  
Parameters:
    - in_file: file containing the blocks and articles
    - out_file: file to write the results
"""
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3.3 busca.py <in_file> <out_file>")
        sys.exit(1)

    blocks = read_file(sys.argv[1])
    solutions = []
    # Search solution for each block timing it
    for block in blocks:
        time_start = time.perf_counter()
        area, articles = busca(block)
        time_end = time.perf_counter()

        total_time_ms = (time_end - time_start) * 1000
        solutions.append(Solution(area, articles, total_time_ms))
        print("Area: {} mm², Time: {:.6f} ms".format(area, total_time_ms))
    
    # Write solutions to file
    with open(sys.argv[2], "w") as f:
        for solution in solutions:
            f.write("{}\n".format(solution))
