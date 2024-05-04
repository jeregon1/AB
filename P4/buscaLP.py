"""
Decision variables:
    - x_ij: binary variable indicating whether article j is placed in block i

Coonstraints:
    1 - Page coverage: Ensure that the articles placed on the page do not exceed the page boundaries.

        ∑j=1..n (x_ij * w_j) <= W_i , ∀i
        ∑j=1..n (x_ij * h_j) <= H_i , ∀i

    2 - Overlap: Ensure that no two articles overlap on the page.

        x_ij + x_ik <= 1, ∀i, ∀j, ∀k != j

Objective Function:
    - Maximize the total area covered by the articles:

        max ∑i=1..n ∑j=1..n (x_ij * w_j * h_j)

Given this formalization, we can now implement a program using Python-MIP (Mixed-Integer Programming) to solve the LP problem.

Here's a general outline of how the program would work:

    1 - Read the input file containing the blocks and articles data.
    2 - For each block:
        - Formulate the LP problem using the defined decision variables, constraints, and objective function.
        - Solve the LP problem.
        - Store the results.
    3 - Write the results to an output file.


The implementation is going to be done using Python-MIP (Mixed-Integer Programming) library.    
"""
"""
To formalize this problem as a linear programming problem, we can define binary decision variables x[i] for each article i, where x[i] = 1 if article i is selected, and x[i] = 0 otherwise. The objective is to maximize the total area of the selected articles, subject to the constraints that no two selected articles overlap and that all articles fit within the page
"""
from dataclasses import dataclass
from time import perf_counter
from typing import List, Tuple
from mip import Model, xsum, maximize, BINARY
import sys

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

@dataclass
class Solution:
    selected_articles: List[Article]
    time: float = 0.0

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
            blocks.append((n, W, H, articles)) # add block to the list
            # blocks.append(Block(n, W, H, articles)) # add block to the list
            i += 1 + n
    return blocks

def solve_LP(block) -> Solution:
    n, W, H, articles = block

    model = Model()

    # binary variables indicating if article i is selected
    x = [model.add_var(var_type=BINARY) for i in range(n)]

    # objective function: maximize total area of selected articles
    model.objective = maximize(xsum(article.area * x[i] for i, article in enumerate(articles)))

    # constraint: no two selected articles overlap
    for i in range(n):
        for j in range(i+1, n):
            if not (articles[i].x + articles[i].w <= articles[j].x or 
                    articles[j].x + articles[j].w <= articles[i].x or 
                    articles[i].y + articles[i].h <= articles[j].y or 
                    articles[j].y + articles[j].h <= articles[i].y):
                model += x[i] + x[j] <= 1

    # solve the model
    model.optimize()

    # retrieve the selected articles
    selected_articles = [articles[i] for i in range(n) if x[i].x >= 0.99]

    return Solution(selected_articles)


"""
Function that finds the solution and calculates the time it takes to do so.
"""
def find_solution(block, busca_function):
    time_start = perf_counter()
    solution = busca_function(block)
    time_end = perf_counter()
    solution.time = (time_end - time_start) * 1000
    return solution


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 buscaLP.py <in_file> <out_file>")
        sys.exit(1)

    blocks = read_file(sys.argv[1])

    solutions = [find_solution(block, solve_LP) for block in blocks]

    # time_start = perf_counter()
    # solutions = [solve_LP(block) for block in blocks]
    # time_end = perf_counter()

    # Write solutions to the file
    with open(sys.argv[2], "w") as f:
        for solution in solutions:
            area = sum(article.area for article in solution.selected_articles)
            f.write("{} {:.6f}\n".format(area, solution.time))
            for article in solution.selected_articles:
                f.write("{} {} {} {}\n".format(article.w, article.h, article.x, article.y))