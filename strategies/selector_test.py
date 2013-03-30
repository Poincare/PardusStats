import unittest
import selector
import naive_strategy

class TestSelectorFunctions(unittest.TestCase):
  def setUp(self):
    self.relative_path = "something/somewhere"
    self.absolute_path = "/etc/something"
    self.nonsense_path = ""
    self.dir_path = "/some/directory/"
    self.file_path = "/some/file"
    self.naive_strat = naive_strategy.NaiveStrategy(100)
    self.selector = selector.SelectorStrategy(100, [self.naive_strat])

  def test_strategy_points(self):
    self.assertTrue(self.naive_strat in self.selector.strategy_points)

  def test_empty_strategies(self):
    self.assertRaises(Exception, selector.SelectorStrategy, 100, [])

  def test_is_relative(self):
    self.assertTrue(self.selector.is_relative(self.relative_path))
  
  def test_is_relative_false(self):
    self.assertFalse(self.selector.is_relative(self.absolute_path))

  def test_is_nonsense(self):
    self.assertTrue(self.selector.is_nonsense(self.nonsense_path))

  def test_cache_score_sanity(self):
    cache_data = [(100, 0), (95, 5), (0, 100)]

    #make sure you don't divide by zero
    #and, more misses makes a cache worse, so, the score should be lower
    self.assertTrue(self.selector.cache_score(cache_data[0]) > self.selector.cache_score(cache_data[1]))
    
    #make sure 0 hits doesn't cause a problem
    self.assertTrue(self.selector.cache_score(cache_data[0]) > self.selector.cache_score(cache_data[2]))

  def test_fschance_start(self):
    self.selector.start({"tree":"frog"})
    self.assertTrue(self.selector.strategies[0].fs_chance == {"tree":"frog"})

if __name__ == '__main__':
  unittest.main()
