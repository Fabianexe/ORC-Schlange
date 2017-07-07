import logging

class BaseReporter:
	def __init__(self, args):
		self.args =args
		FORMAT = "%(levelname)-5s %(asctime)s: %(message)s"
		logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt = "%H:%M:%S")
		
	debug = lambda self,ret: self.args.verbose and logging.info(ret)
	error = lambda self,ret: logging.error(ret)
	