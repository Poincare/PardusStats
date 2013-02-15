class Cache:
  files = []

  hits = 0
  misses = 0

  def __init__(self):
    pass

  def addFile(self, filepath):
    self.files.append(filepath)

  def hit(self):
    self.hits += 1 

  def miss(self):
    self.misses += 1

  def check(self, filepath):
    if filepath in self.files:
      self.hit()

    else:
      self.miss()
      self.files.append(filepath)

  def clear(self):
    self.files = []

  def __repr__(self):
    return ("Hits: " + str(self.hits) + " , misses: " + str(self.misses))


