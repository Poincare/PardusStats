##TODO do this in a better way
import sys
sys.path.insert(0, '../')

import os

import pardus_stats
import pardus_strategy
from cache import *

class NaiveStrategy(pardus_strategy.Strategy):

  def __init__(self, clear_rate):
    self.cache = Cache()
    self.ticks = 0
    self.clear_rate = clear_rate 

  def start(self, fs_chance):
    self.fs_chance = fs_chance

  def isDir(self, p):
    return (p in self.fs_chance.dir_chances)

  def is_relative(self, path):
    return (not (path[0] == '/'))

  def tick(self, record):
    path = record.syscall.arg
    upper_dir = self.fs_chance.get_dir_from_path(path)

    if path == "" or path == None:
      return

    if self.is_relative(path):
      return

    if self.ticks % self.clear_rate == 0:
      self.cache.clear()
 
    #nonsense query like close(4) that we can
    #just ignore
    if path == "" or upper_dir == None:
      return

    #ignore if its a relative path
    if upper_dir in ["../", "..", ".", "./"]:
      return      

    ##it is a directory
    if self.isDir(path + "/"):
      
      return

    else:
      pass 
    
    self.cache.check(path)
 
    self.ticks += 1

  def exit(self):
    for dc_path in self.fs_chance.dir_chances:
      dc = self.fs_chance.dir_chances[dc_path]
      for fname in dc.file_chances:
        if dc.file_chances[fname][0] > 5:
          pass
          #print dc 

    print str(self.clear_rate) + ": " + str(self.cache)

sr = pardus_stats.StrategyRunner(os.getcwd() + "/..")

for i in range(1, 1000): 
  ps = NaiveStrategy(i * 100)
  sr.start(ps)

