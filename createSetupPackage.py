from shutil import copyfile
from subprocess import call
from resources.websiteCrawler import Grabber
from resources.webPackageCreator import WebPackageCreator
from resources.dnsPackageCreator import DNSCreater
from resources.Converter import ( LinkConverter, UrlConverter )
import os
import json
import sys, getopt

linkparser = False

def createOutputFolder():
	""" Create an output folder if does not exit yet """

	newpath = r'output'
	if not os.path.exists(newpath):
		os.makedirs(newpath)

def handleOptions(argv):
   try:
	   opts, args = getopt.getopt(argv,"hvl",[])
   except getopt.GetoptError:
	   print 'Use createSetupPackage.py -h for help of using commands'
	   sys.exit(2)
   for opt, arg in opts:
	   if opt == '-h':
		 print 'Usage:'
		 print '"createSetupPackage.py -h" for help'
		 print '"createSetupPackage.py -v" for version'
		 print '"createSetupPackage.py -l" for using linkconverter'
		 print 'Linkconverter converts all hyperlinks in the webfiles to redirect to each other.'
		 print 'This may take a long time'
		 sys.exit()
	   elif opt == '-v':
		   print 'WebGrabber Version 1.0 created by Ruben Meeuwissen 2018-2019'
		   print 'For questions or additions please write an issue at the git repository:'
		   print 'https://github.com/RubenMeeuw/Webgrabber'
		   sys.exit()
	   elif opt == '-l':
		   global linkparser
		   linkparser = True


def main(argv):
	""" The main function of the program """
	handleOptions(argv)
	# Load the config file
	configfile = 'config.json'
	with open(configfile, 'r') as f:
		config = json.load(f)

	createOutputFolder()

	grabber = Grabber(config, linkparser)
	grabber.execute()

	webPackageCreator = WebPackageCreator(config)
	webPackageCreator.create()

	dnsPackageCreator = DNSCreater(config)
	dnsPackageCreator.create()

if __name__ == '__main__':
	main(sys.argv[1:])
