from pybtex.backends.html import Backend
from pybtex.style.formatting.plain import Style

from pybtex.style.formatting import BaseStyle
from pybtex.richtext import Tag,Text,Symbol,HRef

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

class WorkSummary:
	def __init__(self, path, title, date):
		self.path = path
		self.title = title
		self.date = date
	__lt__ = lambda self, other: self.date.y < other.date.y or (self.date.y == other.date.y and self.title < other.title)
	__eq__ = lambda self, other: self.date.y == other.date.y and self.title == other.title
	__str__ = lambda self: self.title + ": " + str(self.date)

from itertools import count
def itName(name):
	yield name
	for i in count(2):
		yield "{0}_{1}".format(name,i)
def joinBibliography(bib1, bib2):
	for key in bib2.entries:
		for name in itName(key):
			if name not in bib1.entries:
				bib1.entries[name] = bib2.entries[key]
				break

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

class HtmlStyle(BaseStyle):
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
	def write_prologue(self):
		PROLOGUE = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
		<html>
		<head><meta name="generator" content="Pybtex">
		<meta http-equiv="Content-Type" content="text/html; charset=%s">
		<title>Bibliography</title>
		<script src="jquery-3.2.1.min.js"></script>
		<script type="text/javascript">
		$(function(){
			search = $(".filter-input input[type='search']")
			search.keyup(function(){
				inputText = search.val().toLowerCase()
				$('.mix').each(function() {
					var $this = $(this);
					if(($this.attr('class') + $this.text()).toLowerCase().match(inputText) ) {
						$(this).show()
					}
					else {
						$(this).hide()
					}
				});
				$('.year').each(function() {
					if ($("."+$(this).text()+ ".mix").is(":visible")) $(this).show()
					else $(this).hide()
				});
			})
		})
		
		</script>
		</head>
		<body>
		<div class="filter-input">
			<input type="search" placeholder="Try unicorn">
		</div>
		<div id="content">
		"""
		encoding = self.encoding or pybtex.io.get_default_encoding()
		self.output(PROLOGUE % encoding)


def writeHTML(bib, path = "output/out.html"):
	style = HtmlStyle()
	style.sort = lambda x: sorted(x, key = lambda e:-int(e.fields['year']))
	style.format_labels =  lambda x: [int(e.fields['year']) for e in x]
	formatbib = style.format_bibliography(bib)
	HtmlBackend().write_to_file(formatbib,path)


