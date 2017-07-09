import argparse 

def addGlobal(parser):
	parser.set_defaults(func= lambda x: parser.print_help())
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	parser.add_argument('-v', '--verbose', action='store_true', dest="verbose", help="Create verbose output" )

from command.fetch import FetchReporeter

def addFetch(fetch):
	fetch.set_defaults(func= lambda args: FetchReporeter(args).fetch(), config = 0)
	fetch.add_argument('--dbfile', action='store', dest="dbfile", help="The SQLite DB file that is used.", default="output/people.db" )
	fetch.add_argument( '--html', action='store_false', dest = "html", help="Is a html output created. (default: %(default)s)")
	fetch.add_argument( '--bib', action='store_true', dest = "bib", help="Is a bib output created. (default: %(default)s)")
	fetch.add_argument( '--path', action='store', dest = "path", help="The path where the output is created. (default: %(default)s)", default="output/" )
	fetch.add_argument( '--name', action='store', dest = "name", help="The name of the output. (default: %(default)s)", default="out")
	fetch.add_argument( '--jQuery', action='store_true', dest = "jquery", help="Copy jQuery version 3.2.1 to the output path. (default: %(default)s)")
	
	api = fetch.add_argument_group(title= "API-Configuration", description="To interact with the ORCID-API the client-id and client-secret need to set or loaded. The default is the sandbox")
	api.add_argument("--sandbox",action='store_const',const=0, dest= "config",help="Run in the ORCID-Sandbox These need no further options.")
	api.add_argument("--db",action='store_const',const=1, dest= "config",help="Load the options out of the SQLite DB.These need that they are added before with db addAPI.")
	api.add_argument("--file",action='store', dest= "config",help="Load the options out of the file that is given. These need that the file is in a json format that have a field \"client_id\" and \"client_secret\".")
	api.add_argument("--inline",nargs=2, dest= "config",help="Give the data inline. First the id then the secret.")
	
from command.db import DBReporeter
def addDB(db):
	db.set_defaults(func= lambda x: db.print_help() if not x.test else DBReporeter(args).createTest())
	db.add_argument('--dbfile', action='store', dest="dbfile", help="The SQLite DB file that is used.", default="output/people.db" )
	db.add_argument('-t', '--test', action='store_true', help=argparse.SUPPRESS)
	db.add_argument('-h', "--help", action='store_true', help=argparse.SUPPRESS)
	
	dbsubs = db.add_subparsers(title= "db",description="Manage the SQLite DB that contains the orcids", metavar="The databank functions are:")
	
	ADDdb =  dbsubs.add_parser('add', help='Add an new ORCID to the DB')
	addADB(ADDdb)
	
	CONFdb =  dbsubs.add_parser('addConf', help='Add an new Config to the DB')
	addCONF(CONFdb)
	
	PRINTdb =  dbsubs.add_parser('print', help='Print the content of the databank')
	PRINTdb.set_defaults(func= lambda args: DBReporeter(args).prints())
	
	CLEANdb =  dbsubs.add_parser('clean', help='Reset the databank')
	CLEANdb.set_defaults(func= lambda args: DBReporeter(args).clean())
	
	CREATEdb =  dbsubs.add_parser('create', help='Create a new databank')
	CREATEdb.set_defaults(func= lambda args: DBReporeter(args).create())
	
def addADB(ADDdb):
	ADDdb.add_argument( 'orchid', action="store" , help="The new added ORCID." )
	ADDdb.add_argument( 'start', action="store" , help="The date after the ORCID data is fetched in form \"YYYY-MM-DD\”." )
	ADDdb.add_argument( 'stop', action="store" , help="The date until the ORCID data is fetched in form \"YYYY-MM-DD\”." , nargs = "?")
	ADDdb.set_defaults(func= lambda args: DBReporeter(args).add())

def addCONF(CONFdb):
	CONFdb.add_argument( 'cliend_id', action="store" , help="The client id of you app." )
	CONFdb.add_argument( 'clien_secret', action="store" , help="The client secret of you app." )
	CONFdb.add_argument( 'auth', action="store" , help="The url to authenticate." , nargs = "?", default= "https://orcid.org/oauth/token")
	CONFdb.add_argument( 'api', action="store" , help="The url of the api." , nargs = "?", default="https://pub.orcid.org/v2.0/")
	CONFdb.set_defaults(func= lambda args: DBReporeter(args).addConf())
