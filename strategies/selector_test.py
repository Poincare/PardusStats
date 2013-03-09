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

  def test_empty_strategies(self):
    with self.assertRaises(Exception):
      m = selector.SelectorStrategy(100, []) 

  def test_is_relative(self):
    self.assertTrue(self.selector.is_relative(self.relative_path))
  
  def test_is_relative_false(self):
    self.assertFalse(self.selector.is_relative(self.absolute_path))

  def test_is_nonsense(self):
    self.assertTrue(self.selector.is_nonsense(self.nonsense_path))

if __name__ == '__main__':
  unittest.main()
