from subprocess import call
import shutil
import os
from Converter import ( UrlConverter, LinkConverter )
# import config
import json
import logging

class Grabber:

	def __init__(self, config, linkparser):
		"""Initialise a web grabber."""

		self.config = config
		# Load the necessary variables from the config file
		self.website_list = self.config['WEB']['CRAWL_LIST']
		self.output = self.config['WEB']['WEB_OUTPUT']
		self.output_grabbed_websites = self.output + '/grabbedWebsites'
		self.install_web = self.config['WEB']['WEB_INSTALL_FILE']
		self.ip_prefix = self.config["IP_PREFIX"]

		self.urlConverter = UrlConverter(self.config)
		self.linkConverter = LinkConverter(self.config)

		self.convertLinks = linkparser

		logging.getLogger()


	def getWebsite(self, url):
		"""Use wget command to retrieve recursively all files of website"""

		logging.debug("Crawling {} from the web...".format(url))
		call(['wget', url, '--recursive', '--convert-links',
		'--page-requisites', '--continue', '--tries=5',
		'--directory-prefix=' + self.output_grabbed_websites + "/" + self.urlConverter.convertUrl(url), '--retry-connrefused',
		'--quiet', '-nH', '--no-parent'])

	def getWebsiteFromFile(self):
		"""Read all lines from the website list and execute the getWebsite method"""

		with open(self.website_list, "r") as fp:
	    		for line in fp:
	        		self.getWebsite(line.rstrip('\n'))

	def clearGrabbedFolder(self):
		"""Clear all previous grabbed websites from the folder"""

		logging.debug("Clearing grabbed website folder")
		if os.path.exists(self.output_grabbed_websites):
			shutil.rmtree(self.output_grabbed_websites)

	def execute(self):
		"""Start the grabbing process"""

		# Remove all old files
		self.clearGrabbedFolder()

		# Create new url names for the websites
		self.urlConverter.convertUrlsInFile()

		# Get all website sources from WEBSITES_FILE
		self.getWebsiteFromFile()

		# Optionally convert the links in the grabbed website to point to each otherself.
		if (self.convertLinks):
			logging.debug('Converting links')
			for f in os.listdir(self.output_grabbed_websites):
				self.linkConverter.convertFolder(os.path.join(self.output_grabbed_websites, f))
