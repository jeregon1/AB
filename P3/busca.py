#!/mnt/c/Users/jesus/anaconda3/envs/alg/python.exe
#!/opt/csw/bin/python3

import sys
from time import perf_counter

""" Variants:
    👉🏼 Recursive solution is solved using: Recurrent equations
    👉🏼 Iterative solution is solved using: "Memoization" table 
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

Example:
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
        return "Article with values--> w: {}, h: {}, x: {}, y: {}".format(self.w, self.h, self.x, self.y)

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

"""
Calculates the area occupied by a list of articles
"""
def calculate_area(articles):
    area = 0
    for article in articles:
        area += article.w * article.h
    return area

"""
Checks if an article overlaps with any other article in a list
"""
def check_overlap(article, articles):
    for a in articles:
        article_is_left = article.x + article.w <= a.x
        article_is_right = a.x + a.w <= article.x
        article_is_up = article.y + article.h <= a.y
        article_is_down = a.y + a.h <= article.y
        if not (article_is_left or article_is_right or article_is_up or article_is_down):
            return True
    return False

"""
Sorts a list of articles by area (w * h) in descending order
"""
def sort_articles(articles):
    return sorted(articles, key=lambda a: a.w * a.h, reverse=True)


"""
Class that represents the solution of the search algorithm
"""
class Solution:
    def __init__(self, area, articles, time = .0, nodes_generated = 0):
        self.area = area # in mm²
        self.articles = articles
        self.time = time # in ms
        self.nodes_generated = nodes_generated

    def __str__(self):
        articles_str = '\n'.join(str(article) for article in self.articles)
        return "Area: {} mm², Time: {:.6f} ms, Nodes generated: {}\n List of articles: \n-{}".format(
            solution.area, solution.time, solution.nodes_generated, articles_str
        )
    


def busca_recursive(block, index=0, memo={}):
    if index == len(block):
        return Solution(0, [])
    if index in memo:
        return memo[index]
    article = block[index]
    # Exclude the current article
    exclude = busca_recursive(block, index + 1)
    # Include the current article
    include = busca_recursive(block, index + 1)
    include.total_area += article.area
    include.articles.append(article)
    # Choose the solution with the maximum area
    solution = max(include, exclude, key=lambda x: x.total_area)
    memo[index] = solution
    return solution


def busca_iterative(block):
    n = len(block)
    dp = [Solution(0, []) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        article = block[i]
        # Exclude the current article
        exclude = dp[i + 1]
        # Include the current article
        include = Solution(dp[i + 1].total_area + article.area, dp[i + 1].articles + [article])
        # Choose the solution with the maximum area
        dp[i] = max(include, exclude, key=lambda x: x.total_area)
    return dp[0]

# """
# Dynamic programming function that maximizes the area covered by articles in a block and calculates the total space occupied by them.
# Articles can't overlap and must be inside the page.
# Returns the maximum area found and the list of articles that maximize it
# """
# def busca(block):

#     solution = Solution(0, [])


#     return solution


"""  
Parameters:
    - [-r | -i]: option to choose between using recursive or iterative solution
    - in_file: file containing the blocks and articles
    - out_file: file to write the results
"""
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3.3 busca.py [-r | -i] <in_file> <out_file>")
        sys.exit(1)

    option = sys.argv[1]    
    blocks = read_file(sys.argv[2])
    recursive_solutions = []
    iterative_solutions = []
    # Search solution for each block timing it
    for block in blocks:
        if option == "-r":
            time_start = perf_counter()
            recursive_solution = busca_recursive(block) 
            time_end = perf_counter()
            recursive_solution.time = (time_end - time_start) * 1000

            recursive_solutions.append(recursive_solution)
        else:
            time_start = perf_counter()
            iterative_solution = busca_iterative(block)
            time_end = perf_counter()
            iterative_solution.time = (time_end - time_start) * 1000

            iterative_solutions.append(iterative_solution)
    
    # Write recursive and iterative solutions to the file
    with open(sys.argv[3], "w") as f:
        if option == "-r":
            f.write("########## Recursive Solution ##########\n")
            for solution in recursive_solutions:
                f.write("{} {:.6f}".format(solution.area, solution.time))
                for article in solution.articles:
                    f.write("\n{} {} {} {}".format(article.w, article.h, article.x, article.y))

        else:
            f.write("########## Iterative Solution ##########\n")
            for solution in iterative_solutions:
                f.write("{} {:.6f}".format(solution.area, solution.time))
                for article in solution.articles:
                    f.write("\n{} {} {} {}".format(article.w, article.h, article.x, article.y))

