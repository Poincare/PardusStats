from pardus_record import *

class FSChance:

  #path of directory => chance dictionary
  #all of the directories within the FS
  dir_chances = {}

  def __init__(self, record_set):
    self.record_set = record_set

  def build_dirs(self):
    pass

class DirChance:
  path = ""

  #filename => chance dictionary
  #all of the files under a certain directory
  file_chances = {} 

rs = RecordSet("seer-data/observer-0")
