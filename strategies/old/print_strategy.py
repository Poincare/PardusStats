##TODO do this in a better way
import sys
sys.path.insert(0, '../')

import os

import pardus_stats
import pardus_strategy

class PrintStrategy(pardus_strategy.Strategy):

  def __init__(self):
    pass

  def start(self, fs_chance):
    print "FS_CHANCE: "
    print fs_chance

  def tick(self, record):
    print "RECORD: ", record 

ps = PrintStrategy()
sr = pardus_stats.StrategyRunner(ps, os.getcwd() + "/..")
sr.start()
