from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()
setup(
	name = "DioHash",
	version = "1.0.0",
	description = 'Python Cryptography package for generating DioHash hashing functions',
	py_modules = ['DioHash'],
	package_dir = {"" : "src"},
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/sukreshmanda/DioHash",
	author = "Manda Sukresh",
	author_email = "mandasukresh@gmail.com",
	classifiers = [
		"Programming Language :: Python :: 3"
		"Programming Language :: Python :: 3.6"
		"Programming Language :: Python :: 3.7"
		"License :: OSI Approved :: GNU General Public License v3 or later (GPL v2+)",
		"Operating System :: OS Independent"
	],
)
