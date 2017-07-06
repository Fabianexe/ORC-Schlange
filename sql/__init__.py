from sqlite3 import connect, OperationalError
from orcid import OrcID

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
		self.c.execute("CREATE TABLE people (orcid CHARACTER(16), start DATE, end DATE)")
		self.conn.commit()
	def dropDB(self):
		try:
			self.c.execute("DROP TABLE people")
			self.conn.commit()
		except OperationalError:
			pass
	def addUser(self, orchid, start, stop):
		self.c.execute("INSERT INTO people VALUES (?,?,?)", (orchid, start, stop))
		self.conn.commit()
	getOrcIds = lambda self: [OrcID(*t) for t in self.getList()]
	def createTestDB(self):
		self.dropDB()
		self.createDB()
		self.addUser("0000000219094153","1900-01-01","2016-12-31")
		self.addUser("000000020183570X","1900-01-01","2016-12-31")
		self.addUser("0000000303977442","1900-01-01","2016-12-31")
	
