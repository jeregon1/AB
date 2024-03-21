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
    def __init__(self, w, h, x, y, area = 0):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.area = w * h

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

    def sort_articles(self):
        self.articles.sort(key=lambda a: a.area, reverse=True)

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
        area += article.area
    return area


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
        articles_str = '\n- '.join(str(article) for article in self.articles)
        return "Area: {} mm², Time: {:.6f} ms, Nodes generated: {}\n List of articles: \n- {}".format(
            self.area, self.time, self.nodes_generated, articles_str
        )

"""
1. Define the state of the dynamic programming solution. In this case, a state can be defined by the index 
   of the current article and the remaining width and height of the page.

2. Define the base case. If there are no more articles to consider or no more space on the page, the maximum area is 0.

3. Define the transition function. For each article, you have two choices: include it or exclude it. 
   If you include it, the remaining width and height of the page decrease by the width and height of the article, 
   and the total area increases by the area of the article. If you exclude it, the remaining width and height of the 
   page and the total area remain the same. The maximum area for the current state is the maximum of the areas obtained 
   by including and excluding the current article.

4. Implement the dynamic programming solution. You can use a 3D array to store the maximum area for each state. 
   Start from the base case and use the transition function to fill in the array.

5. Extract the solution. The maximum area is stored in the array. To find the articles that make up this area, 
   you can backtrack from the final state to the base case, at each step choosing the article that was included 
   in the optimal solution.

   
Recurrence relation:
    - f(i, w, h) = max(f(i + 1, w, h), f(i + 1, w - wi, h - hi) + wi * hi)
    - f(i, w, h) = 0 if i == n or w == 0 or h == 0
"""


"""
Recursive solution that maximizes the area covered by articles in a block and calculates the total space occupied by them.
Articles can't overlap and must be inside the page.
"""
def busca_recursive(block) -> Solution:
    block.sort_articles()

    def busca(index, articlesInSolution) -> Solution:
        # Base case
        if index == -1:
            return Solution(0, [])

        article = block.articles[index]

        # g(j-1, c)
        solution_exclude = busca(index - 1, articlesInSolution)

        if article.overlaps(articlesInSolution):
            return solution_exclude
        else:
            # g(j-1, c - wj, h - hj) + wj * hj
            solution_include = busca(index - 1, articlesInSolution + [article])
            solution_include.area += article.area
            solution_include.articles.append(article)

            solution = max(solution_exclude, solution_include, key=lambda solution: solution.area)
            return solution

    return busca(block.n_articles - 1, [])

"""
Iterative solution that maximizes the area covered by articles in a block and calculates the total space occupied by them.
Articles can't overlap and must be inside the page.
"""
def busca_iterative(block) -> Solution:
    block.sort_articles()
    n = block.n_articles

    # Initialize memoization table
    memo = {0: Solution(0, [])}

    for i in range(1, 2**n):
        memo[i] = Solution(0, [])
        for j in range(n):
            # Check if the j-th article is included in the i-th subset
            article_in_subset = ((i >> j) & 1 != 0)
            if not article_in_subset:
                continue

            article = block.articles[j]
            sol_without_j = memo[i ^ (1 << j)] # This is the solution for the subset i without the j-th article
            # If the article overlaps with any article in the solution
            # then we don't consider it
            if article.overlaps(sol_without_j.articles):
                continue

            # We check if the solution with j is better than the solution without j for the subset i
            temp = Solution(sol_without_j.area + article.area, sol_without_j.articles + [article])
            if temp.area > memo[i].area:
                memo[i] = temp

    # Find the solution with the maximum area
    return max(memo.values(), key=lambda solution: solution.area)

"""
A simple and smart greedy heuristic would be to order the articles by area divided by the number of overlaps with other articles.
Then, we can iterate over the sorted articles and add them to the solution if they don't overlap with any other article in the solution.
"""
def greedy_solution(block) -> Solution:
    # First, we sort the articles by area divided by the number of overlaps with other articles
    # Calculate the number of overlaps for each article
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
A simple Greedy Heuristic could be to sort the articles by their area in descending order and then place each article 
on the page in that order, as long as it doesn't overlap with any previously placed articles and fits within the page. 
This heuristic is based on the idea that placing larger articles first will maximize the total area occupied by the articles.

Here is a pseudocode for the Greedy Heuristic:

function greedy_solution(block):
    sort block.articles by area in descending order
    create an empty list selected_articles
    for each article in block.articles:
        if article does not overlap with any article in selected_articles and fits within the page:
            add article to selected_articles
    return selected_articles
"""
def greedy_solution(block) -> Solution:
    block.sort_articles()
    areaTotal = block.W * block.H
    selected_articles = []
    for article in block.articles:
        if not article.overlaps(selected_articles) and areaTotal >= article.area:
            selected_articles.append(article)
            areaTotal -= article.area
    return Solution(calculate_area(selected_articles), selected_articles)

"""
Parameters:
    - [-r | -i]: option to choose between using recursive or iterative solution
    - in_file: file containing the blocks and articles
    - out_file: file to write the results
"""
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 busca.py [-r | -i] <in_file> <out_file>")
        sys.exit(1)

    option = sys.argv[1]
    if   option == "-r": busca_function = busca_recursive
    elif option == "-i": busca_function = busca_iterative
    elif option == "-g": busca_function = greedy_solution
    else:
        print("Usage: python3 busca.py [-r | -i] <in_file> <out_file>")
        sys.exit(1)

    blocks = read_file(sys.argv[2])
    solutions = []
    # Search solution for each block timing it
    for block in blocks:
        time_start = perf_counter()
        solution = busca_function(block) 
        time_end = perf_counter()
        solution.time = (time_end - time_start) * 1000
        solutions.append(solution)

    # Write recursive and iterative solutions to the file
    with open(sys.argv[3], "w") as f:
        for solution in solutions:
            f.write("{} {:.6f}\n".format(solution.area, solution.time))
            for article in solution.articles:
                f.write("{} {} {} {}\n".format(article.w, article.h, article.x, article.y))
