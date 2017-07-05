from sqlite3 import connect

class DB:
	def __init__(self,path="example/people.db"):
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

class WorkSummary:
	def __init__(self, path, title, date):
		self.path = path
		self.title = title
		self.date = date
	__lt__ = lambda self, other: self.date.y < other.date.y or (self.date.y == other.date.y and self.title < other.title)
	__eq__ = lambda self, other: self.date.y == other.date.y and self.title == other.title
	__str__ = lambda self: self.title + ": " + str(self.date)

from requests import Session
class API:
	auth = "https://sandbox.orcid.org/oauth/token"
	ORC_client_id = "APP-DZ4II2NELOUB89VC"
	ORC_client_secret = "c0a5796e-4ed3-494b-987e-827755174718"
	def __init__(self):
		self.s = Session()
		self.s.headers = {'Accept': 'application/json'}
		data = {"grant_type":"client_credentials", "scope":"/read-public","client_id":self.ORC_client_id, "client_secret":self.ORC_client_secret}
		r = self.s.request(method ="post",url= self.auth, data=data)
		self.s.headers = {'Accept': 'application/json', "Access token":r.json()["access_token"]}
	baseurl = "https://pub.sandbox.orcid.org/v2.0"
	getDate = lambda self,d: Date(d["year"]["value"],d["month"]["value"] if d["month"] else None, d["day"]["value"] if d["day"] else None )
	def getWorks(self,id):
		r = self.s.request(method= "get",url = "{0}/{1}/works".format( self.baseurl, id.getID()))
		for work in (w["work-summary"][0] for w in r.json()["group"]):
			yield WorkSummary(work["path"],work["title"]["title"]["value"],self.getDate(work["publication-date"]))
	def getWork(self, summary):
		r = self.s.request(method= "get",url= self.baseurl + summary.path)
		return r.json()['citation']['citation-value']

import itertools
if __name__ == "__main__":
	db = DB()
	orcs = [OrcID(*t) for t in db.getList()]
	db.close()
	alldocs = []
	api = API()
	for orc in orcs:
		alldocs += [d for d in api.getWorks(orc) if orc.start <= d.date <= orc.stop]
	alldocs.sort()
	uniqdocs = [doc for doc,_ in itertools.groupby(alldocs)]
	for d in uniqdocs:
		print (d)