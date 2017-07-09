from setuptools import setup, find_packages
from  ORCSchlange import __version__

setup(
	name="ORCSchlange",
	version= __version__,
	packages=find_packages(),
	install_requires=['pybtex>=0.21', 'requests>=2.18.1'],
	author="Fabian Gärtner",
	author_email="fabian@bioinf.uni-leipzig.de",
	url= "https://github.com/ScaDS/ORC-Schlange",
	description="Create a nice static publishing websites from ORCIDs.",
	license="Apache 2.0",
	
	classifiers=[
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"License :: OSI Approved :: Apache Software License",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6"
	],
	entry_points={
		'console_scripts': [
			'orcs = ORCSchlange.__main__:main'
		]
	}
)
