ORCSchlange
===========
.. image:: https://github.com/ScaDS/ORC-Schlange/raw/master/orcschlange.png

Introduction
------------
The project try to create nice publishing websites as static-sites from the ORCID data.
To do these you only need the ORCIDs of your staff and there works must be public visible in ORCID.


Features
--------
- Use the ORCID public api and can be used from *everyone* that have a ORCID
- Easy to configure
- Easy to use
- Creates bib files
- Creates html files that can be filtered with jQuery
- For every ORCID an interval is defined in that works are considered
- The Website is static so no chance for attackers
- Optimize to minimize load of ORCID

Installation
------------
The simples way to install is using pip::

   pip install ORCSchlange

.. _`setuptools`: https://pypi.python.org/pypi/setuptools

You can also download the source from https://github.com/ScaDS/ORC-Schlange and run the make script to install the package.
These needs that `setuptools`_ are installed.

Usage
-----
To use the program first a SQLite db must be created with::

   orcs db create --dbfile *path*

When the file is created you can add the basic configuration::

   orcs db addConf *id* *secret* --dbfile *path*

How to get these secrets can be read here:  https://support.orcid.org/knowledgebase/articles/343182

The last thing to configure is to add the orchids of the user. It takes a date after that the publications are taken in account::

  orcs db add *id* *date*  --dbfile *path*

Now the configuration is complete. The last step is to fetch the actually data::

  orcs fetch --dbfile *path* --path *outpath*

These write a "index.html" file that contains all works that are found. 

Now the usual steps are:

- make the html available from the internet
- integrate it in your institute website
- create a cronjob that fetch the data (once a week or so) and keep the html up to date

Here are only the basic options are shown. For a more detailed look at the options use "-h" in the different commands.


.. _`Static Publications Site-Tutorial`: https://www.scads.de/de/aktuelles/blog/347

Background Story
----------------
These project started as a tutorial on how to interact with a REST-API in python and write a static site with the data. You can find these tutorial here:
`Static Publications Site-Tutorial`_.

