from pardus_record import *
from pardus_strategy import *
import json


class FSChance:

  #path of directory => chance dictionary
  #all of the directories within the FS
  dir_chances = {}

  def __init__(self, record_set):
    self.record_set = record_set

  #messy, nonidiomatic code
  #someone should fix this
  def get_dir_from_path(self, path):
    slash_pos = path.rfind("/")
    if slash_pos != -1:

      if slash_pos+1 <= len(path):
        return path[:slash_pos+1]      
      else: 
        return path[:slash_pos] 
  def add_dir(self, path):
    if not (path in self.dir_chances):
      self.dir_chances[path] = DirChance(path)

  def prune(self):
    to_delete = []

    for path in self.dir_chances:
      if path == "../" or path == "./":
        to_delete.append(path)

    for td in to_delete:
      del self.dir_chances[td]

  def load(self):
    rs = self.record_set 
    i = 0
    for record in rs.records:
      path = record.syscall.arg
      upper_dir = self.get_dir_from_path(record.syscall.arg)

      if path != "" and upper_dir != None:  
        self.add_dir(upper_dir)
      i += 1
  
    self.prune()

  def __repr__(self):
    return str(self.dir_chances)

class DirChance:
  """Hold the file probabilities under each directory"""

  #filename => chance dictionary
  #all of the files under a certain directory

  def __init__(self, path):
    self.path = path
    self.file_chances = {}
    
  def __repr__(self):
    return self.path + " : " + str(self.file_chances)

  def addFile(self, filename):
    #tuple format: (hit count, total count)
    self.file_chances[filename] = [0, 0]
  
  def hitFile(self, filename):
    #increment hit count
    self.file_chances[filename][0] += 1
  
    #increment total count
    self.file_chances[filename][1] += 1

  def missExcept(self, ext):
    for fn in self.file_chances:
      if fn == ext:
        continue
      
      self.file_chances[fn][1] += 1   
  

class StrategyRunner:
  record_set = None
  
  def get_rs(self):
    print "Getting rs..."

    if self.record_set == None:
      rs = RecordSet(self.base_path + self.data_path)
      rs.load()
  
      return rs

    else:
      return self.record_set

  def get_fs(self):
    print "getting fs..."

    fs = FSChance(self.get_rs())
    fs.load()
  
    return fs

  def __init__(self, base_path, data_path = "/seer-data/sample"):
    """passed strategy object, subclass of Strategy"""

    #strategy object
    self.strategy = None 
    self.data_path = data_path
    self.base_path = base_path
    self.record_set = self.get_rs()
    self.fs_chance = self.get_fs()

  def start(self, strategy):
    self.strategy = strategy

    self.strategy.start(self.fs_chance)
    for record in self.record_set.records:
      self.strategy.tick(record)
   
    #lets the strategy know that the records are over 
    self.strategy.exit()

