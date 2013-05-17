import sys
sys.path.insert(0, '../')
import os
import pardus_stats
import pardus_strategy
import math
import random
from cache import *

class ProbabStrategy(pardus_stats.Strategy):
  def __init__(self, clear_rate):
    self.clear_rate = clear_rate
    self.cache = Cache(clear_rate)

  def start(self, fs_chance):
    self.ticks = 0
    self.cache.clear()
    self.fs_chance = fs_chance
    self.shutoff_switch = False
    
    self.previously_accessed = []

  def tick(self, record):
    path = record.syscall.arg
    upper_dir = self.fs_chance.get_dir_from_path(path)
    syscall = record.syscall.syscall
    program_path = record.program_path
    if (not (syscall in ["open", "execve", "stat"])) or self.is_nonsense(path):
      return

    self.previously_accessed.append(path)
    self.cache.check(path)

    return (self.cache.hits, self.cache.misses)

if __name__ == "__main__":
  sr = pardus_stats.StrategyRunner(os.getcwd() + "/..", "/seer-data/small-sample")
  for i in range(1, 2):
    ps = ProbabStrategy(i * 10)
    sr.start(ps)
    print "Hits: ", ps.cache.hits, "Misses: ", ps.cache.misses
