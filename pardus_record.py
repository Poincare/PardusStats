import shlex
import sys

class Syscall:
  def __init__(self, sys_str): 
    self.sys_string = sys_str
    self.parse()

  def parse(self):
    paren_pos = self.sys_string.find("(")
    self.syscall = self.sys_string[0:paren_pos]
    self.arg = self.sys_string[paren_pos:]

    #remove last two characters
    self.arg = self.arg[:-1] 

    #remove first two characters
    self.arg = self.arg[1:]

  def __repr__(self):
    return self.sys_string

class TraceRecord:
  def __init__(self, rs):
    self.record_string = rs
    self.split_string = shlex.split(self.record_string) 

  def parse(self):

    self.id_str = self.split_string[0]
    self.uid = self.split_string[2]
    self.pid = self.split_string[4]
    self.program_path = self.split_string[5]
    #self.syscall = self.split_string[8]
    self.syscall = Syscall(self.split_string[8])
    self.syscall.parse()
  
  def __repr__(self):
    return "Id str: " + self.id_str + ", uid: " + self.uid + ", pid: " + \
    self.pid + " program path: " + self.program_path + " syscall: " + str(self.syscall)

class RecordSet:
  def __init__(self, path):
    self.path = path
    
  def load(self):
    dump = open(self.path, 'r')
    self.records = []

    i = 0 
    for line in dump:
      tr = TraceRecord(line.rstrip())
      if len(tr.split_string) == 11:
        tr.parse()
        self.records.append(tr)
      i += 1

  def __repr__(self):
    return self.records.__repr__()
    

