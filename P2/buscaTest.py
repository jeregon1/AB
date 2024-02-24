import time
import unittest
import itertools
from busca import busca, Block, Article, calculate_area, check_overlap

class TestBuscaEfficiency(unittest.TestCase):
    def brute_force(self, block):
        max_area = 0
        best_combination = None
        all_combinations = []
        for r in range(1, len(block.articles) + 1):
            all_combinations.extend(itertools.combinations(block.articles, r))
        
        for r in range(1, len(block.articles) + 1):
            for combination in all_combinations:
                if all(not check_overlap(a, list(combination)) for a in combination):
                    area = calculate_area(list(combination))
                    if area > max_area:
                        max_area = area
                        best_combination = combination
        return max_area, best_combination

    def test_busca_efficiency(self):
        articles = [Article(10, 10, i * 15, i * 15) for i in range(10)]
        articles.append(Article(10, 10, 5, 5))
        articles.append(Article(10, 10, 10, 10))
        articles.append(Article(10, 10, 30, 30))
        block = Block(len(articles), 200, 200, articles)

        start = time.time()
        busca_result = busca(block)
        busca_time = time.time() - start

        start = time.time()
        brute_force_result = self.brute_force(block)
        brute_force_time = time.time() - start

        self.assertEqual(busca_result.area, brute_force_result[0])
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
