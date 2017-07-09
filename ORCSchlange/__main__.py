import argparse 
from ORCSchlange.command.fetch import FetchReporeter
from ORCSchlange.command.db import DBReporeter

from ORCSchlange.__init__ import *

def main():
		parser = argparse.ArgumentParser(prog='orcs', description= "A simple tool to interact with the ORICID-Public-API.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
		
		addGlobal(parser)
		
		subparsers = parser.add_subparsers(metavar="The ORC-Schlange commands are:")
		fetch = subparsers.add_parser('fetch', help="Fetch the information from the ORICID-Public-API. Call \"fetch -h\" for more details.")
		
		addFetch(fetch)
		
		db = subparsers.add_parser('db', help='Manage the SQLite DB that contains the orcids. Call \"db -h\" for more details.', add_help=False)
		addDB(db)
		
		args = parser.parse_args()
		args.func(args)

if __name__ == "__main__":
	main()