##TODO do this in a better way
import sys
sys.path.insert(0, '../')

import os

import pardus_stats
import pardus_strategy

class Cache:
  files = []

  hits = 0
  misses = 0

  def __init__(self):
    pass

  def hit(self):
    self.hits += 1 

  def miss(self):
    self.misses += 1

  def __repr__(self):
    return ("Hits: " + str(self.hits) + " , misses: " + self.misses)

class PrintStrategy(pardus_strategy.Strategy):

  fs_chance = None 

  def __init__(self):
    pass

  def start(self, fs_chance):
    print "FS chance: ", fs_chance
    self.fs_chance = fs_chance

  def isDir(self, p):
    return (p in self.fs_chance.dir_chances)

  def tick(self, record):
    path = record.syscall.arg
    upper_dir = self.fs_chance.get_dir_from_path(path)

    #nonsense query like close(4) that we can
    #just ignore
    if path == "" or upper_dir == None:
      return

    #ignore if its a relative path
    if upper_dir == "../" or upper_dir ==  "..":
      return      

    ##it is a directory
    if self.isDir(path + "/"):
      print "dir: ", path 

    else:
      print "file: ", path
 
    print "upper dir: ", upper_dir, " path: ", path
 
    ##if not already in, add to the chance structure
    if not (path in self.fs_chance.dir_chances[upper_dir].file_chances):
      print "dir chance obj: ", self.fs_chance.dir_chances[upper_dir]

      self.fs_chance.dir_chances[upper_dir].addFile(path)
      
      print "dir chance obj (after mod): ", self.fs_chance.dir_chances[upper_dir]
     
      ##miss or hit it
      #hit the file requested
      self.fs_chance.dir_chances[upper_dir].hitFile(path)

      #miss all of the others
      self.fs_chance.dir_chances[upper_dir].missExcept(path) 

    print "--------------------------"

  def exit(self):
    print self.fs_chance
 
ps = PrintStrategy()
sr = pardus_stats.StrategyRunner(ps, os.getcwd() + "/..")
sr.start()
