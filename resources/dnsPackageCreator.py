from shutil import copyfile
import os
from subprocess import call

class DNSCreater:
	"""This class can create the according dns files for a webserver"""

	def __init__(self, config):
		"""Initialises a new DNSCreater"""

		self.config = config
		self.output = self.config['DNS']['DNS_OUTPUT']
		self.default_dns = self.config['DNS']['DEFAULT_DNS']
		self.default_named_conf = self.config['DNS']['DEFAULT_NAMED_CONF']
		self.default_reverse_dns = self.config['DNS']['DEFAULT_REVERSE_DNS']
		self.dns_install_file = self.config['DNS']['DNS_INSTALL_FILE']
		self.domain = self.config['NEW_DOMAIN']
		self.ip_prefix = self.config['IP_PREFIX']
		self.website_list = self.config['WEB']['CRAWL_LIST']
		self.newWebListFile =  os.path.join(self.output + "/../",self.website_list.split('.txt')[0] + self.domain)


	def writeDNSFile(self, dnsFile, url, IP):
		"""Create a domainname for the ip"""

		name = self.removeDomainString(url)
		dnsFile.write("\n;" + name.upper() + " DNS CONFIG\n")
		dnsFile.write(name + "\tIN\tA\t" + IP + "\n")
		dnsFile.write("www." + name + "\tIN\tCNAME\t" + name + "\n")

	def writeReverseDNSFile(self, dnsFile, url, lastIPnumber):
		"""write the reverse dns file"""

		dnsFile.write("\n" + str(lastIPnumber) + "\tIN\tPTR\t" + url + ".")

	def copyDNSInstallFileToPackage(self):
		"""Add an install script to the set up folder of the dns"""

		call(['chmod', '+xr', self.dns_install_file])
		copyfile(self.dns_install_file, os.path.join(self.output, "install.sh"))

	def revertIP(self):
		"""Reverse the order of the ip prefix"""

		sIP = self.ip_prefix.split(".")
		reverseIP = ""
		for x in xrange(len(sIP)-1, 0, -1):
			reverseIP += sIP[x-1] + "."
		return reverseIP

	def createNamedConfExtension(self):
		"""Create the link to the reverse dns in the conf file"""

		with open(os.path.join(self.output, "named.conf.local"), "w") as namedConfFile:
			namedConfFile.write('\nzone "' + self.domain.split(".")[1] + '." {\n')
			namedConfFile.write('\ttype master;\n')
			namedConfFile.write('\tfile "/etc/bind/db' + self.domain + '";\n')
			namedConfFile.write('};\n')

			namedConfFile.write('\nzone "' + self.revertIP() + 'in-addr.arpa" {\n')
			namedConfFile.write('\ttype master;\n')
			namedConfFile.write('\tfile "/etc/bind/db.' + self.ip_prefix[:len(self.ip_prefix)-1] + '";\n')
			namedConfFile.write('};')

	def removeDomainString(self, url):
		"""Remove the ".domain" from the url"""

		return url.split(".")[0]

	def createFiles(self):
		"""Create all files for the dns packages"""

		if not os.path.exists(self.output):
			os.makedirs(self.output)

		# Create the dns file
		dnsFileDestination = os.path.join(self.output, "db" + self.domain)
		dnsFile = open(dnsFileDestination, "w")

		# Create a new reverse dns file
		reverseDNSFile = open(os.path.join(self.output, "db." + self.ip_prefix[:len(self.ip_prefix)-1]), "w")

		x = 0

		# Assign a new ip address to every websites dns
		with open(self.newWebListFile, "r") as web:
	    		for line in web:
					url = line.rstrip("/\n")
					# Start counting from ip 10
					lastNumber = 10 + x
					# Create IP from prefix and lastNumber
					IP = self.ip_prefix + str(lastNumber)
					# Write to the dns file
					self.writeDNSFile(dnsFile, url, IP)
					# Write to the reverse dns file
					self.writeReverseDNSFile(reverseDNSFile, url, lastNumber)
					x += 1
		dnsFile.close()
		reverseDNSFile.close()

	def create(self):
		"""Execute the functions to create the web package"""

		self.createFiles()
		self.createNamedConfExtension()
