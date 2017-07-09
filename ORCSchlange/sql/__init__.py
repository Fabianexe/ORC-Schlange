from sqlite3 import connect, OperationalError,IntegrityError
from ORCSchlange.orcid import OrcID

class DB:
	def __init__(self,path="output/people.db"):
		self.conn = connect(path)
		self.c = self.conn.cursor()
	def getList(self):
		self.c.execute('SELECT * FROM people')
		return self.c.fetchall()
	def close(self):
		self.conn.close()
	def createDB(self):
		try:
			self.c.execute("CREATE TABLE people (orcid CHARACTER(16) PRIMARY KEY, start DATE, end DATE)")
			self.conn.commit()
			return True
		except OperationalError:
			return False
	def dropDB(self):
		try:
			self.c.execute("DROP TABLE people")
			self.conn.commit()
		except OperationalError:
			pass
	def addUser(self, orchid, start, stop):
		try:
			self.c.execute("INSERT INTO people VALUES (?,?,?)", (orchid, start, stop))
			self.conn.commit()
			return True
		except IntegrityError:
			return False
	getOrcIds = lambda self: [OrcID(*t) for t in self.getList()]
	def createTestDB(self):
		self.dropDB()
		self.createDB()
		self.addUser("0000000219094153","1900-01-01","2016-12-31")
		self.addUser("000000020183570X","1900-01-01","2016-12-31")
		self.addUser("0000000303977442","1900-01-01","2016-12-31")
	def addConfig(self, id, secret, auth, api):
		try:
			self.c.execute("DROP TABLE config")
			self.conn.commit()
		except OperationalError:
			pass
		self.c.execute("CREATE TABLE config (api TEXT, auth TEXT, id TEXT, secret TEXT)")
		self.conn.commit()
		self.c.execute("INSERT INTO config VALUES (?,?,?,?)", (api, auth, id, secret))
		self.conn.commit()
	def readConfig(self):
		self.c.execute('SELECT * FROM config')
		return self.c.fetchone()
	
