import logging
from sql import DB

class BaseReporter:
	def __init__(self, args):
		self.args =args
		logger = logging.Logger(name= "logging loui")
		logger.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		formatter = logging.Formatter("%(levelname)-5s %(asctime)s: %(message)s","%H:%M:%S")
		ch.setFormatter(formatter)
		logger.addHandler(ch)
		
		self.debug = lambda ret: self.args.verbose and logger.info(ret)
		self.error = lambda ret: logger.error(ret)
	def open(self):
		self.debug("Open db file {0}".format(self.args.dbfile))
		self.db = DB(self.args.dbfile)
	def close(self):
		self.debug("Close db file {0}".format(self.args.dbfile))
		self.db.close()