import sys
sys.path.insert(0, '../')

import os

import pardus_stats
import pardus_strategy

from cache import *

class CDStrategy(pardus_stats.Strategy):
  def __init__(self, clear_rate):
    self.clear_rate = clear_rate
    self.cache = Cache(clear_rate)
    self.prefetched = []
    self.ticks = 0

  def start(self, fs_chance):
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

  def get_chance(self, file_tuple):
    if file_tuple[1] == 0:
      return 0

    return (file_tuple[0]/float(file_tuple[1]))


  def get_highest_chancer(self, dir_path):
    dir_chance = self.fs_chance.dir_chances[dir_path]
    max_chance = -1.0
    max_key = None

    for filename in dir_chance.file_chances:
      if self.isDir(filename):
        continue

      chance = self.get_chance(dir_chance.file_chances[filename])
      if chance > max_chance:
        max_key = filename
        max_chance = chance           
 
    return max_key

  def prefetch_highest_chancer(self, upper_dir):
    highest_chancer = self.get_highest_chancer(upper_dir)
    if highest_chancer == None:
      return

    dir_chance = self.fs_chance.dir_chances[upper_dir]
    chance_tuple = dir_chance.file_chances[highest_chancer]

    if chance_tuple[0] > 2:
      if not (highest_chancer in self.prefetched): 
        print "Prefetched: ", highest_chancer
        self.prefetched.append(highest_chancer)
        self.cache.addFile(highest_chancer)

  def update_chances(self, path, upper_dir):
    if not (path in self.fs_chance.dir_chances[upper_dir].file_chances):
      self.fs_chance.dir_chances[upper_dir].addFile(path)
  
    else:
      self.fs_chance.dir_chances[upper_dir].hitFile(path)
    
    self.fs_chance.dir_chances[upper_dir].missExcept(path)

  
  def get_chance_index(self, upper_dir, path):
    dir_chance = self.fs_chance.dir_chances[upper_dir]
    file_tuple = dir_chance.file_chances[path]
    return (file_tuple[0])

  def rebuild_cache(self):
    max_keys = {} 

    #this algorithm is literally O(n^3).
    #it will fall over and die if the 
    #clear_rate > 100
    for upper_dir in self.fs_chance.dir_chances: 
      mi_len = len(max_keys.keys())
      for path in self.fs_chance.dir_chances[upper_dir].file_chances:
        index = self.get_chance_index(upper_dir, path)
        if mi_len < (self.clear_rate)/2:
          max_keys[path] = index
          continue
        for key in max_keys.keys():
          if index > max_keys[key]:
            del max_keys[key]
            max_keys[path] = index  

    for key in max_keys:
      self.cache.addFile(key)
 
  def tick(self, record):
    if self.ticks % 1000 == 0:
      pass

    self.ticks += 1

    path = record.syscall.arg
    upper_dir = self.fs_chance.get_dir_from_path(path)
    syscall = record.syscall.syscall
    program_path = record.program_path

    if not (syscall in ["open", "execve", "stat"]):
      return

    if self.is_nonsense(path):
      return

    #basic, naive algorithm
    self.cache.check(path)

    #we build on that with the predictive algorithm
    self.update_chances(path, upper_dir)
    
    #don't rebuild everytime, because that's insane
    if self.ticks % 100 == 0:
      self.rebuild_cache()


sr = pardus_stats.StrategyRunner(os.getcwd() + "/..", "/seer-data/small-sample")

for i in range(1, 100):
  sys.stderr.write(str(i*10) + "...")
  ps = CDStrategy(i*10)
  sr.start(ps)

  print i*10, ",", ps.cache.hits, ",", ps.cache.misses 

#print ps.cache.hit_table

