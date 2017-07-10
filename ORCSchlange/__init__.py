"""The functions to handle the main function"""
import argparse
from ORCSchlange.command.fetch import FetchReporeter
from ORCSchlange.command.db import DBReporeter

__version__ = "0.7.1"
"""The version of the package"""


def add_global(parser):
    """Add the global arguments to the parser
    :param parser:
    """
    parser.set_defaults(func=lambda x: parser.print_help())
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-v', '--verbose', action='store_true', dest="verbose", help="Create verbose output")


def add_fetch(fetch):
    """Add the fetch arguments to the fetch command"""
    fetch.set_defaults(func=lambda args: FetchReporeter(args).fetch(), config=0)
    fetch.add_argument('--dbfile', action='store', dest="dbfile", help="The SQLite DB file that is used.",
                       default="output/people.db")
    fetch.add_argument('--html', action='store_false', dest="html",
                       help="Is a html output created. (default: %(default)s)")
    fetch.add_argument('--bib', action='store_true', dest="bib", help="Is a bib output created. (default: %(default)s)")
    fetch.add_argument('--path', action='store', dest="path",
                       help="The path where the output is created. (default: %(default)s)", default="output/")
    fetch.add_argument('--name', action='store', dest="name", help="The name of the output. (default: %(default)s)",
                       default="out")
    fetch.add_argument('--jQuery', action='store_true', dest="jquery",
                       help="Copy jQuery version 3.2.1 to the output path. (default: %(default)s)")

    api = fetch.add_argument_group(title="API-Configuration",
                                   description="""To interact with the ORCID-API the client-id and client-secret 
                                   need to set or loaded. The default is the sandbox""")
    api.add_argument("--sandbox", action='store_const', const=0, dest="config",
                     help="Run in the ORCID-Sandbox These need no further options.")
    api.add_argument("--db", action='store_const', const=1, dest="config",
                     help="Load the options out of the SQLite DB.These need that they are added before with db addAPI.")
    api.add_argument("--file", action='store', dest="config",
                     help="""Load the options out of the file that is given. These need that the file is in a json 
                     format that have a field \"client_id\" and \"client_secret\".""")
    api.add_argument("--inline", nargs=2, dest="config", help="Give the data inline. First the id then the secret.")


def add_db(db):
    """Add the db arguments and subcommands to the db command"""
    db.set_defaults(func=lambda args: db.print_help() if not args.test else DBReporeter(args).create_test())
    db.add_argument('--dbfile', action='store', dest="dbfile", help="The SQLite DB file that is used.",
                    default="output/people.db")
    db.add_argument('-t', '--test', action='store_true', help=argparse.SUPPRESS)
    db.add_argument('-h', "--help", action='store_true', help=argparse.SUPPRESS)

    dbsubs = db.add_subparsers(title="db", description="Manage the SQLite DB that contains the orcids",
                               metavar="The databank functions are:")

    add_dbs = dbsubs.add_parser('add', help='Add an new ORCID to the DB')
    add_adddb(add_dbs)

    conf_db = dbsubs.add_parser('addConf', help='Add an new Config to the DB')
    add_conf(conf_db)

    print_db = dbsubs.add_parser('print', help='Print the content of the databank')
    print_db.set_defaults(func=lambda args: DBReporeter(args).prints())

    clean_db = dbsubs.add_parser('clean', help='Reset the databank')
    clean_db.set_defaults(func=lambda args: DBReporeter(args).clean())

    create_db = dbsubs.add_parser('create', help='Create a new databank')
    create_db.set_defaults(func=lambda args: DBReporeter(args).create())


def add_adddb(add_dbs):
    """Add the arguments to the add command"""
    add_dbs.add_argument('orchid', action="store", help="The new added ORCID.")
    add_dbs.add_argument('start', action="store", help="The date after the ORCID data is fetched in form \"YYYY-MM-DD\”.")
    add_dbs.add_argument('stop', action="store", help="The date until the ORCID data is fetched in form \"YYYY-MM-DD\”.",
                         nargs="?")
    add_dbs.set_defaults(func=lambda args: DBReporeter(args).add())


def add_conf(conf_db):
    """Add the arguments to the addConf command"""
    conf_db.add_argument('cliend_id', action="store", help="The client id of you app.")
    conf_db.add_argument('clien_secret', action="store", help="The client secret of you app.")
    conf_db.add_argument('auth', action="store", help="The url to authenticate.", nargs="?",
                         default="https://orcid.org/oauth/token")
    conf_db.add_argument('api', action="store", help="The url of the api.", nargs="?",
                         default="https://pub.orcid.org/v2.0/")
    conf_db.set_defaults(func=lambda args: DBReporeter(args).add_conf())
