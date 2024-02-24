from time import perf_counter
from random import shuffle
import unittest
import itertools
from busca import busca, Block, Article, Solution, calculate_area, check_overlap, read_file

path_tests = 'pruebas/'
test_files = ['1_prueba.txt', '3_moreArticles.txt']

class TestBuscaEfficiency(unittest.TestCase):
    def brute_force(self, block):
        solution = Solution(0, [])
        all_combinations = []
        for r in range(1, len(block.articles) + 1):
            all_combinations.extend(itertools.combinations(block.articles, r))
        
        solution.nodes_generated = len(all_combinations)
        for combination in all_combinations:
            if all(not check_overlap(a, [article for article in combination if article != a]) for a in combination):
                area = calculate_area(list(combination))
                if area > solution.area:
                    solution.area = area
                    solution.articles = combination
        return solution

    def test_busca_efficiency(self):
        articles = [Article(10, 10, i * 15, i * 15) for i in range(10)]
        articles.append(Article(10, 10, 5, 5))
        articles.append(Article(10, 10, 30, 30))
        articles.append(Article(10, 10, 100, 100))
        block = Block(len(articles), 200, 200, articles)

        blocks = [block]
        for test_file in test_files:
            blocks.extend(read_file(path_tests + test_file))

        for block in blocks:
            shuffle(block.articles)
            start = perf_counter()
            busca_result = busca(block)
            busca_time = (perf_counter() - start) * 1000

            start = perf_counter()
            brute_force_result = self.brute_force(block)
            brute_force_time = (perf_counter() - start) * 1000

            print('\nBlock: {}'.format(block))
            print('Backtracking: {:>9.6f}ms'.format(busca_time))
            print('Brute force:  {:>9.6f}ms'.format(brute_force_time))
            print('Nodes generated in backtracking: {}'.format(busca_result.nodes_generated))
            print('Nodes generated in brute force:', brute_force_result.nodes_generated)
            self.assertEqual(busca_result.area, brute_force_result.area)
            self.assertLess(busca_time, brute_force_time)


class TestBusca(unittest.TestCase):
    def test_busca(self):
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
        articles = [Article(10, 10, 0, 0), Article(10, 10, 5, 0)]
        block = Block(2, 20, 10, articles)
        solution = busca(block)
        self.assertEqual(solution.area, 100)

if __name__ == '__main__':
    # Run all tests
    unittest.main()
