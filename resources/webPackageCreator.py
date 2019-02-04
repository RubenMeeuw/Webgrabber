from shutil import copyfile
import os
from subprocess import call
import random

class WebPackageCreator:
	"""This class creates the files needed for the webserver for all grabbed websites"""

	def __init__(self, config):
		"""Initialise a web file creater."""

		self.config = config

		self.domain = self.config['NEW_DOMAIN']
		self.website_list = self.config['WEB']['CRAWL_LIST']
		self.output = self.config['WEB']['WEB_OUTPUT']
		self.output_grabbed_websites = self.output + '/grabbedWebsites'
		self.install_web = self.config['WEB']['WEB_INSTALL_FILE']
		self.default_interface = self.config['WEB']['DEFAULT_INTERFACE']
		self.ip_prefix = self.config['IP_PREFIX']
		self.netmask = self.config['NETMASK']
		self.newWebListFile =  os.path.join(self.output + "/../",self.website_list.split('.txt')[0] + self.domain)

	def writePortsFile(self, file, IP):
		#TODO make port variable
		"""Write the ports.conf file"""

		file.write("Listen " + IP + ":80\n")

	def writeInterfaceFile(self, file, x, IP):
		#TODO make more variables
		"""Write the interface file: add the new ip to the network"""

		file.write("auto ens160:" + str(x) + "\n")
		file.write("iface ens160:" + str(x) + " inet static\n")
		file.write("\taddress " + IP + "\n")
		file.write("\tnetmask " + self.netmask + "\n\n")

	def writeVirtualHostFile(self, fileName, x, IP):
		#TODO make more variables
		"""Write the virtual host file: Assigns website folder to the ip"""

		virtualHostFolder = os.path.join(self.output, "virtualHosts")
		if not os.path.exists(virtualHostFolder):
			os.makedirs(virtualHostFolder)

		with open(os.path.join(virtualHostFolder, fileName + ".conf"), "w") as virtualHostFile:
			virtualHostFile.write("ServerName " + fileName + "\n")
			virtualHostFile.write("<VirtualHost " + IP + ":80>\n")
			virtualHostFile.write("\tServerAdmin webmaster@localhost\n")
			virtualHostFile.write("\tDocumentRoot /var/www/" + fileName + "\n")
			virtualHostFile.write("</VirtualHost>")

	def clearVirtualHostDir(self):
		"""Clear the virtual host directory"""

		for filename in os.listdir(self.output + "/virtualHosts"):
			os.remove(self.output + "/virtualHosts/" + filename)

	def copyWebInstallFileToPackage(self):
		"""Add an install script to the set up folder of the websites"""

		call(['chmod', '+xr', self.install_web])
		copyfile(self.install_web, os.path.join(self.output, "install.sh"))

	# def randomGenerateUniqueIP(self, mask, srange, erange):
	# 	if (mask = 24):
	# 		random.randint(srange, erange)
	# 	if (mask = 18):
	#
	# 	else:
	# 		raise Exception('An invalid mask is used')


	def createFiles(self):
		"""Create all files for the web packages"""

		# Create all the necessary network interface which need to be appended
		# to the server interface
		interfaceDestination = os.path.join(self.output, "interfaces")
		interfaceFile = open(interfaceDestination, "w")

		# Create a new ports file where every website will be appended to
		portsFile = open(os.path.join(self.output, "ports.conf"), "w")

		x = 0

		# Assign a new ip address to every website and create the according files
		with open(self.newWebListFile, "r") as web:
	    		for line in web:
					url = line.rstrip("/\n")
					# Start counting from ip 10
					lastNumber = 10 + x
					# Create IP from prefix and lastNumber
					IP = self.ip_prefix + str(lastNumber)
					# Write the interface file for this IP
					self.writeInterfaceFile(interfaceFile, x, IP)
					# Write the ports file for this IP
					self.writePortsFile(portsFile, IP)
					# Write the virtualhost file for this IP
					self.writeVirtualHostFile(url, x, IP)
					x += 1
		interfaceFile.close()
		portsFile.close()

	def create(self):
		"""Execute the functions to create the web package"""

		self.createFiles()
		self.copyWebInstallFileToPackage()
