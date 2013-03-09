##TODO do this in a better way
import sys
sys.path.insert(0, '../')

import os

import pardus_stats
import pardus_strategy

from cache import *

class CDStrategy(pardus_strategy.Strategy):

  fs_chance = None 

  def __init__(self, clear_rate):
    self.cache = Cache(clear_rate)
    self.ticks = 0
    self.clear_rate = clear_rate 

  def start(self, fs_chance):
    self.fs_chance = fs_chance

  def isDir(self, p):
    return (p in self.fs_chance.dir_chances)

  def get_chance(self, file_tuple):
    if file_tuple[1] == 0:
      return 0

    return (file_tuple[0]/float(file_tuple[1]))

  def get_highest_chancer(self, dir_path):
    dir_chance = self.fs_chance.dir_chances[dir_path]
    max_chance = -1.0
    max_key = None

    for filename in dir_chance.file_chances:
      chance = self.get_chance(dir_chance.file_chances[filename])
      if chance > max_chance:
        max_key = filename
        max_chance = chance           
 
    return max_key

  def prefetch_highest_chancer(self, upper_dir):
    highest_chancer = self.get_highest_chancer(upper_dir)
    dir_chance = self.fs_chance.dir_chances[upper_dir]
    chance_tuple = dir_chance.file_chances[highest_chancer]

    if chance_tuple[0] > 2:
      self.cache.addFile(highest_chancer)

  def rebuild_cache(self):
    for upper_dir in self.fs_chance.dir_chances:
      self.prefetch_highest_chancer(upper_dir)

  def is_relative(self, path):
    return (not (path[0] == '/'))

  def tick(self, record):
    path = record.syscall.arg
    upper_dir = self.fs_chance.get_dir_from_path(path)
    syscall = record.syscall.syscall
    program_path = record.program_path

    if not (syscall in ["open", "chdir", "execve", "stat"]):
      #print "Skipped call: ", syscall
      return

    if program_path == "??":
      return
   
    if path == None or path == "":
      return

    #don't deal with relative paths
    if self.is_relative(path):
      return

    if self.ticks % self.clear_rate == 0:
      pass
      #self.cache.clear()
      #self.rebuild_cache()
 
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
 
    ##if not already in, add to the chance structure
    if not (path in self.fs_chance.dir_chances[upper_dir].file_chances):

      self.fs_chance.dir_chances[upper_dir].addFile(path)
      
    
    self.cache.check(path)
 
    ##miss or hit it
    #hit the file requested
    self.fs_chance.dir_chances[upper_dir].hitFile(path)

    #miss all of the others
    self.fs_chance.dir_chances[upper_dir].missExcept(path) 
   
    self.ticks += 1

    self.prefetch_highest_chancer(upper_dir); 

  def exit(self):
    for dc_path in self.fs_chance.dir_chances:
      dc = self.fs_chance.dir_chances[dc_path]
      for fname in dc.file_chances:
        if dc.file_chances[fname][0] > 5:
          pass
          #print dc 

    print self.cache 

sr = pardus_stats.StrategyRunner(os.getcwd() + "/..", "/seer-data/small-sample")

if __name__ == "__main__": 
  for i in range(100, 101):
    sys.stderr.write(str(i*100) + "...")
    sys.stdout.write(str(i*100) + "...")
    ps = CDStrategy(i*100)
    sr.start(ps)
    #print ps.cache.hit_table
    #print "-------------------------------------------"
    #print "-------------------------------------------"
    #print ps.fs_chance

