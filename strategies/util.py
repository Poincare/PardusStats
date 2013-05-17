def isDir(p):
  return (p in self.fs_chance.dir_chances)

def is_relative(path):
  return (not (path[0] == '/'))

def is_nonsense(path):
  if path == "":
    return True
  
  if is_relative(path):
    return True

  if isDir(path + "/") or isDir(path):
    return True

 
