from time import perf_counter
from random import shuffle
import unittest
import itertools
from busca import Block, Article, Solution, read_file, busca_recursive, busca_iterative

path_tests = 'pruebas/'
test_files = ['1_prueba.txt', '2_singleArticle.txt' '3_moreArticles.txt', '4_tricky.txt']

def busca(block):
   
    block.sort_articles()
    solution = Solution(0, [])

    def busca_backtracking(i):
        if i == block.n_articles: # Base case: all articles have been checked
            return 
        
        solution.nodes_generated += 1
        for article in block.articles[i:]:
            if not article.overlaps(solution.articles):

                new_area = calculate_area(solution.articles + [article])
                new_area = solution.area + article.area
                if new_area > solution.area:
                    solution.area = new_area
                    solution.articles.append(article)

                busca_backtracking(i + 1)

    # Start the recursive function in order to find the first combination of articles that maximize the area
    busca_backtracking(0)
    return solution

class TestBuscaEfficiency(unittest.TestCase):
    def brute_force(self, block):
        solution = Solution(0, [])
        all_combinations = []
        for r in range(1, len(block.articles) + 1):
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
