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

from pybtex.database import parse_string, BibliographyData
def joinBibliography(bib1, bib2):
	for key in bib2.entries:
		bib1.entries[key] = bib2.entries[key]


from pybtex.style.formatting.unsrt import Style
from pybtex.backends.html import Backend

from pybtex.richtext import Tag,Text,Symbol,HRef

class HtmlTag(Tag):
	def __init__(self, name, opt, *args):
		super(HtmlTag,self).__init__(name, *args)
		self.options = opt
	def render(self, backend):
		text = super(Tag, self).render(backend)
		try:
			return backend.format_tag(self.name, text, self.options)
		except TypeError:
			return backend.format_tag(self.name, text)

class HtmlStyle(Style):
	def format_article(self, context):
		ret = Text()
		ret += HtmlTag("h4","style=\"margin-bottom: 2px;\"", context.rich_fields['title'])
		ret += Tag("i",context.rich_fields['author']) + Symbol('newblock')
		ret += context.rich_fields['journal']
		if 'volume' in context.fields:
			ret += Symbol("nbsp") + context.rich_fields['volume']
		if 'number' in context.fields:
			ret += Symbol("nbsp") + "(" + context.rich_fields['number'] + ")"
		if 'pages' in context.fields:
			ret = ret + ":" + context.rich_fields['pages']
		if 'doi' in context.fields:
			ret += Symbol('newblock') + HRef('https://doi.org/' + context.fields['doi'],"[ Publishers's page ]")
		return HtmlTag("div","class=\"" + context.fields['year'] +  " mix \"",ret)

class HtmlBackend(Backend):
	symbols = {'ndash': u'&ndash;', 'newblock': u'<br/>\n', 'nbsp': u'&nbsp;'}
	format_tag = lambda self, tag, text, options =None: u'<{0} {2} >{1}</{0}>'.format(tag, text, options if options else "") if text else u''
	label = None
	def write_entry(self, key, label, text):
		if label != self.label:
			self.output(u'<h3 class=\"{0} year\">{0}</h3>\n'.format(label))
			self.label = label
		self.output(u'%s\n' % text)
	write_epilogue = lambda self: self.output(u'</div></body></html>\n')
	prologue = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
		<html>
		<head><meta name="generator" content="Pybtex">
		<meta http-equiv="Content-Type" content="text/html; charset=%s">
		<title>Bibliography</title>
		{HEAD}
		</head>
		<body>
		{BODY}
		<div id="content">
		"""
	def prepout (self, head, body):
		self.prologue = self.prologue.format(HEAD = head, BODY = body)
	def write_prologue(self):
		try:
			self.prepout("","")
		except ValueError:
			pass
		self.output(self.prologue % (self.encoding or pybtex.io.get_default_encoding()))


body = """
<div class="filter-input">
	<input type="search" placeholder="Try unicorn">
</div>
"""

head = """
<script src="jquery-3.2.1.min.js"></script>
<script type="text/javascript">
{javascript}
</script>
"""

js = """
//empty
"""

#js = """
#$(function(){
#	search = $(".filter-input input[type='search']")
#	search.keyup(function(){
#		inputText = search.val().toLowerCase()
#		alert(inputText)
#	})
#})
#"""

#js = """
#$(function(){
#	search = $(".filter-input input[type='search']")
#	search.keyup(function(){
#		inputText = search.val().toLowerCase()
#		$('.mix').each(function() {
#			if($(this).text().toLowerCase().match(inputText) ) {
#				$(this).show()
#			}
#			else {
#				$(this).hide()
#			}
#		});
#	})
#})
#"""

#js = """
#$(function(){
#	search = $(".filter-input input[type='search']")
#	search.keyup(function(){
#		inputText = search.val().toLowerCase()
#		$('.mix').each(function() {
#			if($(this).text().toLowerCase().match(inputText) ) {
#				$(this).show()
#			}
#			else {
#				$(this).hide()
#			}
#		});
#		$('.year').each(function() {
#			if ($("."+$(this).text()+ ".mix").is(":visible")) $(this).show()
#			else $(this).hide()
#		});
#	})
#})
#"""

head = head.format(javascript= js)

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
	bib = BibliographyData()
	for d in uniqdocs:
		joinBibliography (bib,parse_string(api.getWork(d),"bibtex"))
	style = HtmlStyle()
	style.sort = lambda x: sorted(x, key = lambda e:-int(e.fields['year']))
	style.format_labels =  lambda x: [int(e.fields['year']) for e in x]
	formatbib = style.format_bibliography(bib)
	back = HtmlBackend()
	back.prepout(head, body)
	back.write_to_file(formatbib,"out.html")
