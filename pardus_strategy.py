class Strategy:
  """This is meant as a parent class. All strategies to be tested
  subclass this class. Subsequently, they are run against the Seer
  filesystem traces and you can collect data on how your strategy 
  did within this class."""

  def __init__(self):
    pass

  def start(self, fs_chance):
    """The fs_chance argument is an FSChance structure that has
    all of the directories laid out for you."""
    pass

  def tick(self, record):
    """You are passed in a TraceRecord object, which has details
    on what the "user" (i.e. filesystem trace) performed. Use
    these details to predict further events and/or record data.""" 
    pass

      
