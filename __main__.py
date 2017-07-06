from sql import DB
import orcid
import itertools
import pybtex.database
from bib import joinBibliography,writeHTML

if __name__ == "__main__":
	#Read OrcIDs
	db = DB()
	orcs = db.getOrcIds()
	db.close()
	#init API
	api = orcid.API()
	#get all work summaries
	alldocs = []
	for orc in orcs:
		docs = api.getWorks(orc)
		alldocs += docs
	#Sort entries
	alldocs.sort()
	#make entries unique
	uniqdocs = []
	for doc,_ in itertools.groupby(alldocs):
		uniqdocs.append (doc)
	#Get complete work
	entries = pybtex.database.BibliographyData()
	for doc in uniqdocs:
		ent = api.getWork(doc)
		if ent != None:
			joinBibliography(entries,ent)
	#Write bib data
	entries.to_file(open("output/out.bib","w"))
	#Write html
	writeHTML(entries)