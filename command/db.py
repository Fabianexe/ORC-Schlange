from sql import DB
import sys
from command import BaseReporter

class DBReporeter(BaseReporter):
	def open(self):
		self.debug("Open db file {0}".format(self.args.dbfile))
		self.db = DB(self.args.dbfile)
	def close(self):
		self.debug("Close db file {0}".format(self.args.dbfile))
		self.db.close()
	def add(self):
		self.open()
		self.debug("Validate orchid")
		self.args.orchid = self.args.orchid.replace("-","")
		if len(self.args.orchid) != 16:
			self.error("Invalide orchid")
			self.close()
			sys.exit(1)
		checkDate = lambda d: len(d)!= 10 or len(d.split("-"))!=3 or not d.split("-")[0].isdecimal() or not d.split("-")[1].isdecimal() or not d.split("-")[2].isdecimal()
		self.debug("Validate start")
		if checkDate(self.args.start):
			self.error("Invalide start")
			self.close()
			sys.exit(1)
		if self.args.stop:
			self.debug("Stop found")
			self.debug("Validate stop")
			if checkDate(self.args.stop):
				self.error("Invalide stop")
				sys.exit(1)
			self.debug("Add orcid")
			if not self.db.addUser(self.args.orchid, self.args.start, self.args.stop):
				self.error("Doubled orchid entry. Nothing have been added.")
		else:
			self.debug("Add orcid")
			if not self.db.addUser(self.args.orchid, self.args.start, None):
				self.error("Doubled orchid entry. Nothing have been added.")
		self.close()
	def prints(self):
		self.open()
		for orc in self.db.getOrcIds():
			print(orc)
		self.close()
	def clean(self):
		self.open()
		self.debug("Drop old DB")
		self.db.dropDB()
		self.debug("Create new DB")
		self.db.createDB()
		self.close()
	def create(self):
		self.open()
		self.debug("Create new DB")
		if not self.db.createDB():
			self.error("DB already exists")
		self.close()
	def createTest(self):
		self.open()
		self.debug("Create test DB")
		self.db.createTestDB()
		self.close()