from command import BaseReporter
import orcid
import itertools
import pybtex.database
from bib import joinBibliography,writeHTML
import shutil
from config import Config

class FetchReporeter(BaseReporter):
	def fetch(self):
		self.debug("Read config")
		Config(self.args)
		self.open()
		
		self.debug("Read orchids")
		orcs = self.db.getOrcIds()
		
		self.close()
		
		self.debug("Open API connection")
		api = orcid.API()
		
		self.debug("Get all work summaries")
		alldocs = []
		for orc in orcs:
			docs = api.getWorks(orc)
			alldocs += docs
		
		self.debug("Sort all work summaries")
		alldocs.sort()
		
		self.debug("Make entries uniques")
		uniqdocs = []
		for doc,_ in itertools.groupby(alldocs):
			uniqdocs.append (doc)
		
		self.debug("Get complete works")
		entries = pybtex.database.BibliographyData()
		for doc in uniqdocs:
			ent = api.getWork(doc)
			if ent != None:
				joinBibliography(entries,ent)
		if self.args.bib:
			self.debug("Write bib in {path}{name}.bib".format(**vars(self.args)))
			entries.to_file(open("{path}{name}.bib".format(**vars(self.args)),"w"))
		if self.args.html:
			self.debug("Write html in {path}{name}.html".format(**vars(self.args)))
			writeHTML(entries, path = "{path}{name}.html".format(**vars(self.args)))
		if self.args.jquery:
			jname= "jquery-3.2.1.min.js"
			self.debug("Copy jQuery to {path}{jname}".format(path = self.args.path, jname= jname))
			shutil.copyfile("bib/{jname}".format(jname=jname),"{path}{jname}".format(path = self.args.path, jname= jname))