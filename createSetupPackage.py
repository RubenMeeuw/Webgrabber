from shutil import copyfile
from subprocess import call
from resources.websiteCrawler import Grabber
from resources.webPackageCreator import WebPackageCreator
from resources.dnsPackageCreator import DNSCreater
from resources.Converter import ( LinkConverter, UrlConverter )
import os
import json

def createOutputFolder():
	""" Create an output folder if does not exit yet """
	
	newpath = r'output'
	if not os.path.exists(newpath):
		os.makedirs(newpath)

def main():
	""" The main function of the program """

	# Load the config file
	configfile = 'config.json'
	with open(configfile, 'r') as f:
		config = json.load(f)

	createOutputFolder()

	grabber = Grabber(config)
	grabber.execute()

	webPackageCreator = WebPackageCreator(config)
	webPackageCreator.create()

	dnsPackageCreator = DNSCreater(config)
	dnsPackageCreator.create()

if __name__ == '__main__':
	main()
