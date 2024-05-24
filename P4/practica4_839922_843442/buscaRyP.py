#!/usr/bin/python3

import sys
from time import perf_counter
import heapq
from queue import PriorityQueue, LifoQueue, Queue
# from collections import namedtuple

"""
Autores: Jesús López Ansón, Javier Sin Pelayo
Fichero: busca.py
        Implementa un algoritmo de búsqueda basado en ramificación y poda. Resuelven el problema de 
        la colocación de artículos en una página para maximizar el área ocupada por los artículos. 
        Se imprime el área restante de la página que queda libre, y el tiempo que ha tardado en calcular la solución.
"""



"""
Search algorithm with dynamic programming that, given:
    - The page dimensions (width W and height H)
    - A list of n articles, each with its dimension and position (i.e., width wi,
      height hi and cartesian coordinates (xi, yi) as specified above)

determines the articles to place on the page maximizing the total area occupied by articles and calculate the total space occupied by them
"""

# Entry file format:
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

-->Entry file example:
5 280 400    <-- Block 1
10 10 0 0        <-- Article 1
10 10 15 15      <-- Article 2
10 10 10 10      <-- Article 3
20 10 20 20      <-- Article 4
20 10 25 15      <-- Article 5
6 280 400    <-- Block 2
10 20 30 40     ...
50 60 70 80
20 30 40 50
90 80 70 60
80 70 60 50
50 50 40 40


Assumptions:
    - There is at least one block
    - There is at least one article in each block
    - The coordinates and dimensions of the articles are positive integers
    - The coordinates and dimensions of the articles are such that the article is completely within the page
"""

# Output file format:
"""
A line for each block containing 2 numbers:
    - area remaining not being occupied by the articles that maximize the area covered (in mm)
    - time needed (in milliseconds) to calculate the solution.

-->Output file example:
40 0.1875
"""

"""
Class that represents an article
"""
class Article:
    def __init__(self, w, h, x, y, area = 0):
        self.w = w # width
        self.h = h # height
        self.x = x # 'x' coordinate of the top left corner
        self.y = y # 'y' coordinate of the top left corner
        self.area = w * h # area of the article

    """
    Checks if an article overlaps with any other article in a list
    """
    def overlaps(self, articles):
        for a in articles:
            article_is_left = self.x + self.w <= a.x
            article_is_right = a.x + a.w <= self.x
            article_is_up = self.y + self.h <= a.y
            article_is_down = a.y + a.h <= self.y
            if not (article_is_left or article_is_right or article_is_up or article_is_down):
                return True
        return False
    
    @staticmethod
    def list_area(list) -> int:
        return sum(article.area for article in list)

    """
    String representation of the article
    """
    def __str__(self):
        return "Article with values--> w: {}, h: {}, x: {}, y: {}".format(self.w, self.h, self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, Article) and \
            self.w == other.w and self.h == other.h and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.w, self.h, self.x, self.y))


""" 
Class that represents a block of articles
"""
class Block:
    def __init__(self, n_articles, W, H, articles):
        self.n_articles = n_articles # number of articles
        self.W = W # page width
        self.H = H # page height
        self.articles = articles # list of articles
        self.area = self.W * self.H # area of the block


    """
    Sorts the articles by area (w * h) in descending order
    """
    def sort_articles(self):
        self.articles.sort(key=lambda a: a.area, reverse=True)

    """
    String representation of the block
    """
    def __str__(self):
        articles_str = ""
        for article in self.articles:
            articles_str +=  str(article) + "\n"
        return "n: {}, W: {}, H: {}, articles:\n{}".format(self.n_articles, self.W, self.H, articles_str)


"""
Reads a file containing the blocks and articles and returns a list of blocks
"""
def read_file(file) :
    blocks = []
    with open(file, "r") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            n, W, H = map(int, lines[i].split()) # number of articles, page width, page height
            articles = []
            for j in range(i + 1, i + 1 + n): # iterate over the articles of the block
                w, h, x, y = map(int, lines[j].split()) 
                articles.append(Article(w, h, x, y)) # add article to the list
            blocks.append(Block(n, W, H, articles)) # add block to the list
            i += 1 + n
    return blocks


"""
Class that represents the solution of the search algorithm
"""
class Solution:
    def __init__(self, area, articles, block_area, remaining_articles = set(), time = .0, nodes_generated = 0):
        # assert sum(article.area for article in articles) == area
        # assert area <= block_area

        self.area = area # in mm²
        self.articles = set(articles) # list of articles that maximize the area
        self.block_area = block_area # in mm²
        self.remaining_articles = remaining_articles # set of articles that have been checked
        self.time = time # in ms
        self.nodes_generated = nodes_generated # number of nodes generated

    def remaining_area(self):
        return self.block_area - self.area

    def __lt__(self, other):
        if isinstance(other, Solution):
            return self.remaining_area() < other.remaining_area()
        return NotImplemented


def buscaRyP(block: Block) -> Solution:

    nodes_generated = 0

    # Initialize LIFO queue to store partial solutions
    # pq = Queue()
    pq = LifoQueue()
    # pq = PriorityQueue()

    # The priority is set by the articles area in the solution
    initial_solution = Solution(0, [], block.area, remaining_articles = set(block.articles))
    best_solution = initial_solution
    pq.put(initial_solution)  # Put the initial solution with index 0

    # Branch and Bound search
    while not pq.empty():
        partial_solution = pq.get()  # Partial solution with minimu
        
        # New articles that overlap with the current partial solution
        overlapping_articles = {a for a in partial_solution.remaining_articles if a.overlaps(partial_solution.articles)}

        # Explore all valid placements of articles still not looked at
        for article in partial_solution.remaining_articles - overlapping_articles:

            nodes_generated += 1
            new_solution = Solution(partial_solution.area + article.area, partial_solution.articles | {article}, block.area)
            new_solution.remaining_articles = set(block.articles) - (overlapping_articles | new_solution.articles)
        
            # Check if the partial solution is not promising, 
            if new_solution.area + Article.list_area(new_solution.remaining_articles) <= best_solution.area:
                continue  # Prune this branch

            # Update best solution if needed
            if new_solution.area > best_solution.area:
                best_solution = new_solution

            pq.put(new_solution)  # Put the solution tuple with the index

    best_solution.nodes_generated = nodes_generated

    return best_solution


"""
Function that finds the solution and calculates the time it takes to do so.
"""
def find_solution(block: Block, busca_function) -> Solution:
    time_start = perf_counter()
    solution = busca_function(block)
    time_end = perf_counter()
    solution.time = (time_end - time_start) * 1000
    return solution


"""
Parameters:
    - in_file: file containing the blocks and articles
    - out_file: file to write the results
"""
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 buscaRyP.py <in_file> <out_file>")
        sys.exit(1)

    blocks = read_file(sys.argv[1])
    solutions = [find_solution(block, buscaRyP) for block in blocks]

    # Write solutions to the file
    with open(sys.argv[2], "w") as f:
        for solution in solutions:
            f.write("{} {:.6f}\n".format(solution.remaining_area(), solution.time))
            for article in solution.articles:
                f.write(" {} {} {} {}\n".format(article.w, article.h, article.x, article.y))
