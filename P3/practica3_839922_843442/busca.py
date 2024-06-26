#!/mnt/c/Users/jesus/anaconda3/envs/alg/python.exe
#!/opt/csw/bin/python3

import sys
from time import perf_counter

"""
Autores: Jesús López Ansón, Javier Sin Pelayo
Fichero: busca.py. 
        Implementa tres algoritmo de búsqueda. Dos de programación dinámica (iterativo y recursivo) y uno voraz, 
        que dadas las dimensiones de una página y una lista de artículos, determina los artículos a colocar en la
        página maximizando el área total ocupada por los artículos y calcula el espacio total ocupado por ellos.

        El algoritmo recursivo se basa en las ecuaciones en recurrencia, mientras que el iterativo se basa en la
        utilización de la tabla de memoización para evitar recalcular los mismos estados múltiples veces.
        Por norma general el algoritmo iterativo es más eficiente que el recursivo, pero en este caso, es más costoso
        debido al cálculo de la tabla de memoización. A pesar de calcular únicamente los estados necesarios, el coste
        de la tabla de memoización es mayor que el coste de la recursión.
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
    - total area occupied by the articles (in mm)
    - time needed (in milliseconds) to calculate the solution.

-->Output file example:
400 0.1875
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

"""
Recursive solution that maximizes the area covered by articles in a block and calculates the total space occupied by them.
This solution is given by the following recurrence relations:
    if i == 0: f(i, w, h) = 0
    else:      f(i, w, h) = max(f(i - 1, w, h), f(i - 1, w - wi, h - hi) + wi * hi)

Comments: 
    - articles can't overlap and must be inside the page.
Return value: Solution with the list of articles that maximize the area and the total area occupied by them.
"""
def busca_recursive(block) -> Solution:
    
    block.sort_articles() # Area-based sorting
    nodes_generated = 0

    """
    Recursive function that calculates the solution using the previously defined recurrence relations.
    """
    def busca(index, articlesInSolution = []) -> Solution:
        nonlocal nodes_generated
        # Base case: no more articles to check
        if index == -1:
            return Solution(0, [])
        
        nodes_generated += 1 # Increment the number of nodes generated
        article = block.articles[index] # Get the article at the current index

        # f(i - 1, w, h)
        solution_exclude = busca(index - 1, articlesInSolution)

        # If the article overlaps with any article in the solution then we don't consider it
        if article.overlaps(articlesInSolution):
            return solution_exclude
        else:
            # f(i - 1, w - wi, h - hi) + wi * hi
            solution_include = busca(index - 1, articlesInSolution + [article])
            solution_include.area += article.area
            solution_include.articles.append(article)

            # f(i, w, h) = max(f(i - 1, w, h), f(i - 1, w - wi, h - hi) + wi * hi)
            solution = max(solution_exclude, solution_include, key=lambda solution: solution.area)
            return solution

    solution = busca(block.n_articles - 1) # Start the search passing by the number of articles
    solution.nodes_generated = nodes_generated # Set the number of nodes generated
    return solution

"""
Iterative solution that maximizes the area covered by articles in a block and calculates the total space occupied by them.
This solution is given by the usage of the memoization table to avoid recalculating the same states multiple times.

Comments:
    - articles can't overlap. 
Return value: Solution with the list of articles that maximize the area and the total area occupied by them.
"""
def busca_iterative(block) -> Solution:
    
    block.sort_articles() # Area-based sorting
    n = block.n_articles # Number of articles
    nodes_generated = 0 # Initialize the number of nodes generated

    memo = {0: Solution(0, [])} # Initialize memoization table

    for i in range(1, 2**n): # Iterate over all the subsets of articles (2^n). 
        # Each subset is represented by an integer 'i', where the 'j-th' bit of 'i' is 1 if the 'j-th' article is included in the subset, and 0 otherwise.

        memo[i] = Solution(0, [])
        for j, article in enumerate(block.articles):

            article_in_subset = ((i >> j) & 1 != 0) # Check if the j-th article is included in the i-th subset
            if not article_in_subset:
                continue

            sol_without_j = memo[i ^ (1 << j)] # This is the solution for the subset i without the j-th article
            
            # If the article overlaps with any article in the solution then we don't consider it
            if article.overlaps(sol_without_j.articles): 
                continue

            # We check if the solution with j is better than the solution without j for the subset i
            new_area = sol_without_j.area + article.area
            if new_area > memo[i].area: 
                memo[i] = Solution(new_area, sol_without_j.articles + [article]) # Update the solution
                nodes_generated += 1 # Only count the nodes generated when it overwrites the memoization table 

    # Find the solution with the maximum area
    solution = max(memo.values(), key=lambda solution: solution.area)
    solution.nodes_generated = nodes_generated
    return solution



"""
A simple and smart greedy heuristic would be to order the articles by area divided by the number of overlaps with other articles.
Then, we can iterate over the sorted articles and add them to the solution if they don't overlap with any other article in the solution.
"""
def busca_greedy(block) -> Solution:
    # First, we sort the articles by area divided by the number of overlaps with other articles
    overlaps = {}
    for i, article_i in enumerate(block.articles):
        overlaps[article_i] = 1 # We count the overlap with itself (avoiding division by 0 later on)
        for j, article_j in enumerate(block.articles):
            if i != j and not article_i.overlaps([article_j]):
                overlaps[article_i] += 1

    block.articles.sort(key=lambda a: a.area / overlaps[a], reverse=True)

    # Then, we iterate over the sorted articles and add them to the solution if they don't overlap with any other article in the solution
    solution = Solution(0, [])
    for article in block.articles:
        if not article.overlaps(solution.articles):
            solution.area += article.area
            solution.articles.append(article)

    return solution

"""
Function that finds the solution and calculates the time it takes to do so.
"""
def find_solution(block, busca_function):
    time_start = perf_counter()
    solution = busca_function(block) 
    time_end = perf_counter()
    solution.time = (time_end - time_start) * 1000
    return solution


"""
Parameters:
    - [-r | -i | -g]: option to choose between using recursive, iterative, or greedy solution
    - in_file: file containing the blocks and articles
    - out_file: file to write the results
"""
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 busca.py [-r | -i | -g] <in_file> <out_file>")
        sys.exit(1)

    option = sys.argv[1]
    if   option == "-r": busca_function = busca_recursive
    elif option == "-i": busca_function = busca_iterative
    elif option == "-g": busca_function = busca_greedy
    else:
        print("Usage: python3 busca.py [-r | -i | -g] <in_file> <out_file>")
        sys.exit(1)

    blocks = read_file(sys.argv[2])
    solutions = [find_solution(block, busca_function) for block in blocks]

    # Write recursive and iterative solutions to the file
    with open(sys.argv[3], "w") as f:
        for solution in solutions:
            f.write("{} {:.6f}\n".format(solution.area, solution.time))
            for article in solution.articles:
                f.write(" {} {} {} {}\n".format(article.w, article.h, article.x, article.y))
