from pybtex.backends.html import Backend
from pybtex.style.formatting.plain import Style

from pybtex.richtext import Tag, Text, Symbol, HRef
from pybtex.io import get_default_encoding

from itertools import count


class Date:
    def __init__(self, y, m, d):
        self.y = int(y)
        self.m = int(m) if m else None
        self.d = int(d) if d else None

    def check(self, other, attr):
        if getattr(self, attr) is None or getattr(other, attr) is None:
            return 1
        if getattr(self, attr) < getattr(other, attr):
            return 1
        if getattr(self, attr) > getattr(other, attr):
            return -1
        return 0

    def __le__(self, other):
        return True if 1 == (self.check(other, "y") or self.check(other, "m") or self.check(other, "d") or 1) else False

    def __str__(self):
        return str(self.y) + "-" + str(self.m) + "-" + str(self.d)


class WorkSummary:
    def __init__(self, path, title, date):
        self.path = path
        self.title = title
        self.date = date

    def __lt__(self, other):
        return self.date.y < other.date.y or (self.date.y == other.date.y and self.title < other.title)

    def __eq__(self, other):
        return self.date.y == other.date.y and self.title == other.title

    def __str__(self):
        return self.title + ": " + str(self.date)


def it_name(name):
    yield name
    for i in count(2):
        yield "{0}_{1}".format(name, i)


def join_bibliography(bib1, bib2):
    for key in bib2.entries:
        for name in it_name(key):
            if name not in bib1.entries:
                bib1.entries[name] = bib2.entries[key]
                break


class HtmlTag(Tag):
    def __init__(self, name, opt, *args):
        super(HtmlTag, self).__init__(name, *args)
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
        ret += HtmlTag("h4", "style=\"margin-bottom: 2px;\"", context.rich_fields['title'])
        ret += Tag("i", context.rich_fields['author']) + Symbol('newblock')
        ret += context.rich_fields['journal']
        if 'volume' in context.fields:
            ret += Symbol("nbsp") + context.rich_fields['volume']
        if 'number' in context.fields:
            ret += Symbol("nbsp") + "(" + context.rich_fields['number'] + ")"
        if 'pages' in context.fields:
            ret = ret + ":" + context.rich_fields['pages']
        if 'doi' in context.fields:
            ret += Symbol('newblock') + HRef('https://doi.org/' + context.fields['doi'], "[ Publishers's page ]")
        return HtmlTag("div", "class=\"" + context.fields['year'] + " mix \"", ret)


class HtmlBackend(Backend):
    symbols = {'ndash': u'&ndash;', 'newblock': u'<br/>\n', 'nbsp': u'&nbsp;'}

    def format_tag(self, tag, text, options=None):
        return u'<{0} {2} >{1}</{0}>'.format(tag, text, options if options else "") if text else u''

    label = None

    def write_entry(self, key, label, text):
        if label != self.label:
            self.output(u'<h3 class=\"{0} year\">{0}</h3>\n'.format(label))
            self.label = label
        self.output(u'%s\n' % text)

    def write_epilogue(self):
        return self.output(u'</div></body></html>\n')

    def write_prologue(self):
        prologue = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
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
        encoding = self.encoding or get_default_encoding()
        self.output(prologue % encoding)


def write_html(bib, path="output/out.html"):
    style = HtmlStyle()
    style.sort = lambda x: sorted(x, key=lambda e: -int(e.fields['year']))
    style.format_labels = lambda x: [int(e.fields['year']) for e in x]
    formatbib = style.format_bibliography(bib)
    HtmlBackend().write_to_file(formatbib, path)
