#!/usr/bin/python3

import sys
from time import perf_counter
import heapq
from queue import PriorityQueue
from typing import Tuple
# from collections import namedtuple

"""
Autores: Jesús López Ansón, Javier Sin Pelayo
Fichero: busca.py. 
        🎃 Explicar con definición el contenido del fichero 🎃
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


Asumptions:
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

    def area(self):
        return self.W * self.H

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
def read_file(file):
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
    def __init__(self, area, articles, time = .0, nodes_generated = 0):
        self.area = area # in mm²
        self.articles = articles # list of articles that maximize the area
        self.time = time # in ms
        self.nodes_generated = nodes_generated # number of nodes generated

    """
    String representation of the solution. It shows the area, time, and the list of articles
    """
    def __str__(self):
        articles_str = '\n- '.join(str(article) for article in self.articles)
        return "Area: {} mm², Time: {:.6f} ms, Nodes generated: {}\n List of articles: \n- {}".format(
            self.area, self.time, self.nodes_generated, articles_str
        )
    
    def __lt__(self, other):
        if isinstance(other, Solution):
            return self.area < other.area

# 🎃 Optimized solution (original down below commented)
def buscaRyP(block) -> Tuple[Solution, int]:

    # Initialize priority queue to store partial solutions
    pq = PriorityQueue()

    # Initialize best solution
    best_solution = Solution(0, [])

    # Initial partial solution (no articles placed)
    initial_solution = Solution(0, [], 0, 0)
    # The priority is set by the area (negative to get the maximum area first) because priority queue returns the smallest element first
    pq.put((-initial_solution.area, initial_solution)) 

    # Branch and Bound search
    while not pq.empty():
        # Get the partial solution with the maximum potential area
        partial_solution = pq.get()[1]

        # Check if the partial solution is promising
        if partial_solution.area + block.area() <= best_solution.area:
            continue  # Prune this branch

        # Explore all valid placements of articles
        for article in block.articles:
            new_nodes_generated = partial_solution.nodes_generated + 1
            if not article.overlaps(partial_solution.articles):
                new_articles = partial_solution.articles + [article]
                new_area = partial_solution.area + article.area
                new_solution = Solution(new_area, new_articles, partial_solution.time, new_nodes_generated)

                # Update best solution if needed
                if new_solution.area > best_solution.area:
                    best_solution = new_solution

                pq.put((-new_solution.area, new_solution))

    remaining_area = block.area() - best_solution.area

    return best_solution, remaining_area

# def buscaRyP(block) -> Solution:

#     # Initialize priority queue to store partial solutions
#     pq = []
#     heapq.heapify(pq)

#     # Initialize best solution
#     best_solution = Solution(0, [])

#     # Initial partial solution (no articles placed)
#     initial_solution = Solution(0, [], 0, 0)
#     heapq.heappush(pq, initial_solution)

#     # Branch and Bound search
#     while pq:
#         # Get the partial solution with the maximum potential area
#         partial_solution = heapq.heappop(pq)

#         # Check if the partial solution is promising
#         if partial_solution.area + block.area() <= best_solution.area:
#             continue  # Prune this branch

#         # Explore all valid placements of articles
#         for article in block.articles:
#             if not article.overlaps(partial_solution.articles):
#                 new_articles = partial_solution.articles + [article]
#                 new_area = partial_solution.area + article.area
#                 new_nodes_generated = partial_solution.nodes_generated + 1
#                 new_solution = Solution(new_area, new_articles, partial_solution.time, new_nodes_generated)

#                 # Update best solution if needed
#                 if new_solution.area > best_solution.area:
#                     best_solution = new_solution

#                 heapq.heappush(pq, new_solution)

#     remaining_area = block.area() - best_solution.area

#     return best_solution, remaining_area


"""
Function that finds the solution and calculates the time it takes to do so.
"""
def find_solution(block, busca_function):
    time_start = perf_counter()
    if busca_function == buscaRyP:
        solution, remaining_area = busca_function(block)
    else:
        solution = busca_function(block)
    time_end = perf_counter()
    solution.time = (time_end - time_start) * 1000
    if busca_function == buscaRyP:
        return solution, remaining_area    
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
        for solution, remaining_area in solutions:
            area = solution.area
            time, nodes_generated = solution.time, solution.nodes_generated
            # f.write("{} {:.6f}\n".format(area, time))
            f.write("{} {:.6f}\n".format(remaining_area, time))
            for article in solution.articles:
                f.write(" {} {} {} {}\n".format(article.w, article.h, article.x, article.y))