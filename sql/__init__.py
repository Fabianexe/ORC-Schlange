from sqlite3 import connect
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
	
	getOrcIds = lambda self: [OrcID(*t) for t in self.getList()]
	
