import sys
sys.path.insert(0, '../')

import os

import pardus_stats
import pardus_strategy

from cache import *

#import strategies themselves
#instances of these are passed 
#to the Selector Strategy
import chdir_strategy
import naive_strategy
import cd_strategy 
import program_strategy

class SelectorStrategy(pardus_stats.Strategy):
  def __init__(self, clear_rate, strategies):
    """clear_rate is the clear rate of the cache,
    strategies is a list of Strategy objects
    that SelectorStrategy uses in order to build
    an optimal strategy"""

    self.clear_rate = clear_rate
    self.cache = Cache(clear_rate)
    self.strategies = strategies
    
    if strategies == [] or strategies == None:
      raise Exception
    
  def is_relative(self, path):
    return (not (path[0] == '/'))

  def is_nonsense(self, path):
    if path == "":
      return True
     
    return False

  def tick(self, record):
    """Central method of all strategies. Passed the records
    one by one by the PardusStats system."""

    path = record.syscall.arg
    #upper_dir = self.fs_chance.get_dir_from_path(path)
    syscall = record.syscall.syscall
    program_path = record.program_path

    if self.is_nonsense(path):
      return

    if self.is_relative(path):
      return

    #DATA STRUCTURE
    #a dictionary between strategy objects
    #and the number of "points" that they have
    #also, another dictionary between strategy objects
    #and their current prediction that we need to account for

    #ALGORITHM
    #check previous predictions
    #add points to those strategies who were able to predict correctly
    #Call tick on each strategy, see what each of them would predict
    #pick one of the them that has the highest points
    #store their predictions

if __name__ == "__main__":
  sr = pardus_stats.StrategyRunner(os.getcwd() + "/..", "/seer-data/small-sample")
  
  for i in range(1, 100):
    sys.stderr.write(str(i*10) + "...")

    ns = naive_strategy.NaiveStrategy(i*10)

    ps = SelectorStrategy(i*10, [ns])
    sr.start(ps)



