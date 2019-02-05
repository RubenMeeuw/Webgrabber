import os
import fnmatch
from random import randint
import logging

class LinkConverter:
	"""Class to change all the links in the grabbed folder to point to each other."""

	def __init__(self, config):
		"""Initialise a link converter."""

		self.config = config

		self.website_list = self.config['WEB']['CRAWL_LIST']
		self.output = self.config['WEB']['WEB_OUTPUT']
		self.domain =self.config['NEW_DOMAIN']
		self.crawl_list_new_domain = os.path.join(self.output + "/../",self.website_list.split('.txt')[0] + self.domain)

		logging.getLogger()

	def convertFolder(self, folderName):
		"""Convert all the links in the files in the specified folder and subfolders"""

		self.count = 0
		linksArray = self.createLinksArray()
		for directory, subdirectories, filenames in os.walk(folderName):
			for filename in filenames:
				self.convertFile(os.path.join(directory,filename), linksArray)
		logging.debug("There were {} links converted in {}".format(self.count, os.path.basename(os.path.normpath(folderName))))

	def convertFile(self, input, linksArray):
		"""Substitute all the links in the specified foler with a random fake website"""

		newFile = open(input + ".tmp", "w")
		with open(input, "r") as file:
			for line in file:
				newFile.write(self.convertLine(line, linksArray))
		newFile.close()
		os.rename(input + ".tmp", input)

	def convertLine(self, line, linksArray):
		"""Substitute the http link in the line with a fake website"""

		hrefOptions = ["href=\"http", "href= \"http", "href = \"http", "href=\'http", "href= \'http", "href = \'http"]
		hrefCommaOption = ["\"", "\"", "\"", "\'", "\'", "\'"]
		for i in range(0, len(hrefOptions)):
			elements = line.split(hrefOptions[i])
			if(len(elements) > 1):
				self.count += 1
				head = elements[0]
				link = "href=\"http://" + self.getRandomLink(linksArray) + "\""
				tail = elements[1].split(hrefCommaOption[i], 1)[1]
				newLink = head + link + tail
				return newLink
		return line

	def getRandomLink(self, array):
		"""Get a random fake website"""

		return array[randint(0, len(array)-1)]

	def createLinksArray(self):
		"""Create an array from all possible fake websites"""

		with open(self.crawl_list_new_domain, "r") as web:
			websites = [x.strip("\n") for x in web.readlines()]
		return websites

class UrlConverter:
	"""Class to change url domains"""

	def __init__(self, config):
		"""Initialise a url converter."""

		self.config = config

		self.website_list = self.config['WEB']['CRAWL_LIST']
		self.output = self.config['WEB']['WEB_OUTPUT']
		self.domain = self.config['NEW_DOMAIN']

	def convertUrlsInFile(self):
		"""Convert the list of websites to the new domain urls"""

		# Create a new file to save all new url names
		newFileName = 'output/' + self.website_list.split(".txt")[0] + self.domain
		# Open the nem file
		newFile = open(newFileName, "w")
		# Convert every line and add it to the new file
		with open(self.website_list, "r") as file:
			for line in file:
				line.rstrip("/\n")
				newUrl = self.convertUrl(line) + "\n"
				newFile.write(newUrl)
		newFile.close()
		return newFileName

	def convertUrl(self, url):
		"""Convert the url to the new domain"""

		# Remove 'http://www.' from url
		if "http://" in url:
			url = url.replace("http://", "")
		elif "https://" in url:
			url = url.replace("https://", "")
		if "www." in url:
			url = url.replace("www.", "")

		# Replace domain with your own domain
		url = url.split(".")[0] + self.domain

		return url
