from sqlite3 import connect

class DB:
	def __init__(self,path="people.db"):
		self.conn = connect(path)
		self.c = self.conn.cursor()
	
	def getList(self):
		self.c.execute('SELECT * FROM people')
		return self.c.fetchall()
	
	def close(self):
		self.conn.close()

if __name__ == "__main__":
	db = DB()
	print(db.getList())
	db.close()