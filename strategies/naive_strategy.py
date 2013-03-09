import sys
sys.path.insert(0, '../')

import os

import pardus_stats
import pardus_strategy

from naive_cache import *

class NaiveStrategy(pardus_stats.Strategy):
  def __init__(self, clear_rate):
    self.clear_rate = clear_rate
    self.cache = Cache(clear_rate)
    self.shutoff_rate = 1000
    self.shutoff_switch = True 

  def start(self, fs_chance):
    self.ticks = 0
    self.cache.clear()
    self.fs_chance = fs_chance

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

  def shutoff(self):
    if not self.shutoff_switch:
      return

    else:
      if self.ticks % self.shutoff_rate == 0:
        self.cache.clear()

  def tick(self, record):
    path = record.syscall.arg
    upper_dir = self.fs_chance.get_dir_from_path(path)
    syscall = record.syscall.syscall
    program_path = record.program_path

    self.shutoff()

    if not (syscall in ["open", "execve", "stat"]):
      return

    if self.is_nonsense(path):
      return

    else:
      pass
     
    self.cache.check(path)

    self.ticks += 1


if __name__ == "__main__":
  sr = pardus_stats.StrategyRunner(os.getcwd() + "/..", "/seer-data/small-sample")
  for i in range(1, 100):
    sys.stderr.write(str(i*10) + "...")
    print ""
    ps = NaiveStrategy(i * 10)
    sr.start(ps)

    print i*10, ",", ps.cache.hits, ",", ps.cache.misses
    #print ps.cache.hit_table

