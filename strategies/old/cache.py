class Cache:
  files = []

  hits = 0
  misses = 0

  def __init__(self, clear_rate):
    self.clear_rate = clear_rate
    self.hit_table = {}
    self.clear_bool = False

  def addFile(self, filepath):
    if self.clear_bool:
      if len(self.files) > self.clear_rate:
        self.clear()

    self.hit_table[filepath] = 0 
    self.files.append(filepath)
    
  def hit(self):
    self.hits += 1 

  def miss(self):
    self.misses += 1

  def check(self, filepath):
    if filepath in self.files:
      if filepath in self.hit_table:
        self.hit_table[filepath] += 1
      else:
        self.hit_table[filepath] = 1

      self.hit()

    else:
      self.miss()
      self.addFile(filepath)

  def clear(self):
    self.files = []

  def __repr__(self):
    return ("Hits: " + str(self.hits) + " , misses: " + str(self.misses))


