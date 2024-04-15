#!/usr/bin/env python3
from random import shuffle
import unittest
import itertools
from busca import Block, Article, Solution, read_file, busca_recursive, busca_iterative, find_solution

path_tests = 'pruebas/'
test_files = ['1_prueba.txt','2_singleArticle.txt', '3_moreArticles.txt', '4_tricky.txt']

def busca_backtracking(block) -> Solution:
    from copy import copy

    block.sort_articles()
    nodes_generated = 0

    def recursive_backtracking(i = 0, solution_in_progress = Solution(0, [])) -> Solution:
        nonlocal nodes_generated
        if i == block.n_articles:
            return solution_in_progress
        
        nodes_generated += 1
        best_solution_in_node = Solution(solution_in_progress.area, copy(solution_in_progress.articles))

        for article in block.articles[i:]: # Para cada nodo hijo

            if article.overlaps(solution_in_progress.articles): # Predicado acotador
                continue

            solution_in_progress.area += article.area
            solution_in_progress.articles.append(article)

            possible_solution = recursive_backtracking(i + 1, solution_in_progress)

            if possible_solution.area > best_solution_in_node.area: # Predicado solución
                best_solution_in_node = Solution(possible_solution.area, copy(possible_solution.articles))
        
            # Undo the changes to solution_in_progress
            solution_in_progress.area -= article.area
            solution_in_progress.articles.pop()

        return best_solution_in_node

    solution = recursive_backtracking()
    solution.nodes_generated = nodes_generated
    return solution

class TestBuscaEfficiency(unittest.TestCase):
    def brute_force(self, block) -> Solution:
        solution = Solution(0, [])
        all_combinations = []
        for r in range(1, block.n_articles + 1):
            all_combinations.extend(itertools.combinations(block.articles, r))
        
        solution.nodes_generated = len(all_combinations)
        for combination in all_combinations:
            if all(not a.overlaps([article for article in combination if article != a]) for a in combination):
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

            print('\nBlock: {}'.format(block))
            print('Backtracking: {:>12.6f}ms'.format(backtracking.time))
            print('Iterative dp: {:>12.6f}ms'.format(iterative.time))
            print('Recursive dp: {:>12.6f}ms'.format(recursive.time))
            print('Brute force:  {:>12.6f}ms'.format(brute_force.time))
            print('Nodes generated in backtracking: {:>6}'.format(backtracking.nodes_generated))
            print('Nodes generated in iterative dp: {:>6}'.format(iterative.nodes_generated))
            print('Nodes generated in recursive dp: {:>6}'.format(recursive.nodes_generated))
            print('Nodes generated in brute force: ', brute_force.nodes_generated)
            self.assertEqual(backtracking.area, brute_force.area)
            self.assertEqual(iterative.area, brute_force.area)
            self.assertEqual(recursive.area, brute_force.area)


class TestBusca(unittest.TestCase):
    def test_busca(self):
        for busca in [busca_backtracking, busca_iterative, busca_recursive]:
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
