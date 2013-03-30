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
      raise
   
    self.strategy_points = {}
    self.strategy_caches = {}

    for strategy in self.strategies:
      self.strategy_points[strategy] = 0
      self.strategy_caches[strategy] = None

    self.ticks = 0

  def start(self, fs_chance):
    self.fs_chance = fs_chance
    
    for strategy in self.strategies:
      strategy.start(fs_chance)

  def isDir(self, p):
    return (p in self.fs_chance.dir_chances)

  def is_relative(self, path):
    return (not (path[0] == '/'))

  def is_nonsense(self, path):
    if path == "":
      return True
  
    if self.is_relative(path):
      return True

    if self.isDir(path + "/") or self.isDir(path):
      return True

  def cache_score(self, cache_record):
    misses = float(cache_record[1])

    #hits over misses
    if misses == 0:
      misses = 0.001

    return (cache_record[0]/misses)

  def reset_cache(self):
    max_strategy = max(self.strategy_points, key=lambda x: self.strategy_points[x])  
    print "max strategy: ", max_strategy

    self.cache.files = max_strategy.cache.files

  def tick_strategies(self, record):
    for strategy in self.strategies:

      print "files: ", strategy.cache.files
      print "needle: ", record.syscall.arg

      #tick the strategy - it should hit or miss the cache
      cache_record = strategy.tick(record)

      if cache_record == None:
        continue

      print "Cache record: ", cache_record

      #get the "score" of this cache - should have changed
      cache_score = self.cache_score(cache_record)   

      #plug the score into the points hash
      self.strategy_points[strategy] = cache_score  
  

  def tick(self, record):
    """Central method of all strategies. Passed the records
    one by one by the PardusStats system."""

    #probably not a solution that works in real life
    #takes the cache of one of the strategies and swaps it out
    if self.ticks % 100 == 0:
      pass
      #self.reset_cache()

    path = record.syscall.arg
    #upper_dir = self.fs_chance.get_dir_from_path(path)
    syscall = record.syscall.syscall
    program_path = record.program_path

    self.tick_strategies(record)

    if not (syscall in ["open", "execve", "stat"]):
      return

    if self.is_nonsense(path):
      return

    if self.is_relative(path):
      return

    ##check the cache on the selector strategy itself
    self.cache.check(path)


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
    
    print self.strategy_points
  
    self.ticks += 1

  def exit(self):
    for strategy in self.strategies:
      print strategy, ": ", "hits: ", strategy.cache.hits, "misses: ", strategy.cache.misses

    print "TOTAL HITS: ", self.cache.hits, "TOTAL MISSES: ", self.cache.misses

if __name__ == "__main__":
  sr = pardus_stats.StrategyRunner(os.getcwd() + "/..", "/seer-data/small-sample")
  
  for i in range(100, 101):
    sys.stderr.write(str(i*10) + "...")

    ns = naive_strategy.NaiveStrategy(i*10)
    cs = cd_strategy.CDStrategy(i*10)
 
    ps = SelectorStrategy(i*10, [cs])
    sr.start(ps)

