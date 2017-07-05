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

class Date:
	def __init__(self, y, m, d):
		self.y = int(y)
		self.m = int(m) if m else None
		self.d = int(d) if d else None
	def check (self, other, attr):
		if getattr(self,attr) == None or getattr(other,attr) == None:
			return 1
		if getattr(self,attr) < getattr(other,attr):
			return 1
		if getattr(self,attr) > getattr(other,attr):
			return -1
		return 0
	__le__ = lambda self, other: True if 1 == (self.check(other,"y") or self.check(other,"m") or self.check(other,"d") or 1) else False
	__str__ = lambda self: str(self.y) + "-" + str(self.m) + "-" + str(self.d)

class OrcID:
	def __init__(self, id, start, stop):
		self.id = id
		self.start = Date(*start.split("-"))
		self.stop = Date(*stop.split("-"))
	getID = lambda self: "-".join([self.id[4 * i : 4 * (i + 1)]  for i in range(4)])
	__str__ = lambda self: self.getID() + ": " + str(self.start) + " - " + str(self.stop)

if __name__ == "__main__":
	db = DB()
	orcs = [OrcID(*t) for t in db.getList()]
	db.close()
	for orc in orcs:
		print("Do something with",orc)

class WorkSummary:
	def __init__(self, path, title, date):
		self.path = path
		self.title = title
		self.date = date
	__lt__ = lambda self, other: self.date.y < other.date.y or (self.date.y == other.date.y and self.title < other.title)
	__eq__ = lambda self, other: self.date.y == other.date.y and self.title == other.title
	__str__ = lambda self: self.title + ": " + str(self.date)