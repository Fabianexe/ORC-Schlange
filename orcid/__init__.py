import time
from requests import Session
import config
import pybtex.database
from bib import Date, WorkSummary

class OrcID:
	def __init__(self, id, start, stop):
		self.id = id
		self.start = Date(*start.split("-"))
		self.stop = Date(*stop.split("-"))
	getID = lambda self: "-".join([self.id[4 * i : 4 * (i + 1)]  for i in range(4)])
	__str__ = lambda self: self.getID() + ": " + str(self.start) + " - " + str(self.stop)

class API:
	authurl = "https://sandbox.orcid.org/oauth/token" if config.OrcSAND else "https://orcid.org/oauth/token"
	baseurl = "https://pub.sandbox.orcid.org/v2.0"  if config.OrcSAND else "https://pub.orcid.org/v2.0/"
	
	def __init__(self):
		self.s = Session()
		self.s.headers = {'Accept': 'application/json'}
		data = {"grant_type":"client_credentials", "scope":"/read-public","client_id":config.ORC_client_id, "client_secret":config.ORC_client_secret}
		r = self.s.request(method ="post",url= self.authurl, data=data)
		self.s.headers = {'Accept': 'application/json', "Access token":r.json()["access_token"]}
	getDate = lambda self,d: Date(d["year"]["value"],d["month"]["value"] if d["month"] else None, d["day"]["value"] if d["day"] else None )
	def getWorks(self,id):
		r = self.s.request(method= "get",url = "{0}/{1}/works".format( self.baseurl, id.getID()))
		for work in (w["work-summary"][0] for w in r.json()["group"]):
			if work["publication-date"] != None:
				d = self.getDate(work["publication-date"])
				if id.start <= d and d <= id.stop:
					yield WorkSummary(work["path"],work["title"]["title"]["value"],d)
	def getWork(self, summary):
		r = self.s.request(method= "get",url= self.baseurl + summary.path)
		json = r.json()
		if json['citation'] != None:
			if json['citation']['citation-type'] == "BIBTEX":
				return pybtex.database.parse_string(json['citation']['citation-value'], "bibtex")
		return None

