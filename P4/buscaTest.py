#!/usr/bin/env python3

""" If the imports don't work, try uncommenting these following lines """
# import sys
# from os.path import dirname, abspath

# # Add the parent directory to sys.path
# sys.path.append(dirname(dirname(abspath(__file__))))

from random import shuffle
import unittest
import itertools
from P2.practica2_839922_843442 import busca_backtracking
from P3.practica3_839922_843442 import busca_recursive, busca_iterative
from P4.buscaRyP import Block, Article, Solution, read_file, buscaRyP, find_solution

path_tests = 'pruebas/'
test_files = ['1_prueba.txt','2_singleArticle.txt', '3_moreArticles.txt', '4_tricky.txt', '5_evenMoreArticles.txt']

# def busca_backtracking(block):
#     # Area-based sorting
#     block.sort_articles()
#     nodes_generated = 0

#     def recursive_backtracking(i = 0, solution_in_progress = Solution(0, [])) -> 'tuple[int, list[Article]]': # Devuelve los artículos a añadir a la solución
#         nonlocal nodes_generated
#         best_area = solution_in_progress.area
#         last_added_article = [solution_in_progress.articles[-1]] if solution_in_progress.articles else []

#         # Base case: all articles have been checked
#         if i == block.n_articles:
#             return best_area, last_added_article
        
#         nodes_generated += 1 # Increment the number of nodes generated
#         best_articles_to_add = [] # List of the best articles found in this node among all its children

#         for article in block.articles[i:]: # For each son of the current node

#             if article.overlaps(solution_in_progress.articles): # Pruning predicate (Predicado acotador)
#                 continue

#             solution_in_progress.area += article.area
#             solution_in_progress.articles.append(article)

#             possible_best_area, articles_to_add = recursive_backtracking(i + 1, solution_in_progress) # Recursive call

#             # Undo the changes to solution_in_progress to explore the next son
#             solution_in_progress.area -= article.area
#             solution_in_progress.articles.pop()

#             if possible_best_area > best_area: # Solution predicate (Predicado solución)
#                 best_area = possible_best_area
#                 best_articles_to_add = articles_to_add

#         return best_area, last_added_article + best_articles_to_add

#     solution = Solution(0, [])
#     solution.area, solution.articles = recursive_backtracking()
#     solution.nodes_generated = nodes_generated # Set the number of nodes generated
#     return solution

class TestBuscaEfficiency(unittest.TestCase):
    def brute_force(self, block) -> Solution:
        solution = Solution(0, [])
        all_combinations = []
        for r in range(1, block.n_articles + 1):
            all_combinations.extend(itertools.combinations(block.articles, r))
        
        solution.nodes_generated = len(all_combinations)
        for combination in all_combinations:
            if all(not a.overlaps([article for article in combination if article is not a]) for a in combination):
                area = sum(a.area for a in combination)
                if area > solution.area:
                    solution.area = area
                    solution.articles = combination
        return solution

    def test_busca_efficiency(self):
        articles = [Article(10, 10, i * 15, i * 15) for i in range(6)]
        articles.append(Article(10, 10, 5, 5))
        articles.append(Article(10, 10, 30, 30))
        articles.append(Article(10, 10, 100, 100))
        block = Block(len(articles), 200, 200, articles)

        blocks = [block]
        for test_file in test_files:
            blocks.extend(read_file(path_tests + test_file))

        for block in blocks:
            shuffle(block.articles)
            backtracking = find_solution(block, busca_backtracking)
            shuffle(block.articles)
            iterative = find_solution(block, busca_iterative)
            shuffle(block.articles)
            recursive = find_solution(block, busca_recursive)
            shuffle(block.articles)
            brute_force = find_solution(block, self.brute_force)
            shuffle(block.articles)
            buscaRyP = find_solution(block, buscaRyP)

            # Printing of results from the tests
            print('\nBlock: {}'.format(block))
            print('Backtracking: {:>12.6f}ms'.format(backtracking.time))
            print('Iterative dp: {:>12.6f}ms'.format(iterative.time))
            print('Recursive dp: {:>12.6f}ms'.format(recursive.time))
            print('Branch&Bound: {:>12.6f}ms'.format(buscaRyP.time))
            print('Brute force:  {:>12.6f}ms'.format(brute_force.time))
            print('Nodes generated in backtracking: {:>6}'.format(backtracking.nodes_generated))
            print('Nodes generated in iterative dp: {:>6}'.format(iterative.nodes_generated))
            print('Nodes generated in recursive dp: {:>6}'.format(recursive.nodes_generated))
            print('Nodes generated in brute force: ', brute_force.nodes_generated)

            # Checks that the area of the solutions is calculated correctly
            self.assertEqual(backtracking.area, brute_force.area)
            self.assertEqual(iterative.area, brute_force.area)
            self.assertEqual(recursive.area, brute_force.area)


class TestBusca(unittest.TestCase):
    def test_busca(self):
        for busca in [busca_backtracking, busca_iterative, busca_recursive, buscaRyP]:
            # Test 1: Single article fits perfectly in the block
            articles = [Article(10, 10, 0, 0)]
            block = Block(1, 10, 10, articles)
            solution = busca(block)
            self.assertEqual(solution.area, 100)

            # Test 2: Two non-overlapping articles
            articles = [Article(10, 10, 0, 0), Article(10, 10, 10, 0)]
            block = Block(2, 20, 10, articles)
            solution = busca(block)
            self.assertEqual(solution.area, 200)

            # Test 3: Two overlapping articles
            articles = [Article(10, 10, 0, 0), Article(20, 10, 0, 0)]
            block = Block(2, 20, 10, articles)
            solution = busca(block)
            self.assertEqual(solution.area, 200)

if __name__ == '__main__':
    # Run all tests
    unittest.main()
