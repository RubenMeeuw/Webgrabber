#!/bin/bash
webfolder='grabbedWebsites'
vhostfolder='virtualHosts'
interfacefile='interfaces'
portsfile='ports.conf'

clean=0
getopts "hvd:w:" name
while [ "$name" != "?" ] ; do
  case $name in
   c) clean=1;;
  esac
  getopts "hvd:w:" name
done

clean () {
	enabledFolderFiles = "$(ls /etc/apache2/sites-enabled)"
	availableFolderFiles = "$(ls /etc/apache2/sites-available)"
	for filename in $enabledFolderFiles
  do
		# remove from enabled websites
		a2dissite $filename
  done

	for filename in $availableFolderFiles
  do
		# remove from available websites
    filename="/etc/apache2/sites-available/$filename"
		rm $filename
  done
}

# Copy all website folders and give correct permission
copyWebsites () {
  webFileList="$(ls $webfolder)"
	for filename in $webFileList
  do
    filename="$webfolder/$filename"
		chmod -R +xr $filename
		cp -r $filename /var/www/
  done
}

# Copy all virtual host files
copyHosts () {
  vhosts="$(ls $vhostfolder)"
	for filename in $vhosts
  do
    filename2="$vhostfolder/$filename"
		cp $filename2 /etc/apache2/sites-available/

		# Add to enabled websites
		a2ensite $filename
  done
}

# Copy the the interface file to the correct spot
copyInterface () {
	cat $interfacefile >> /etc/network/interfaces
}

# Copy the ports file to the correct spot
copyPorts () {
	cp $portsfile /etc/apache2/
}

# Call the functions

if [ $clean -eq 1 ]
then Clean
fi

copyWebsites
copyHosts
copyInterface
copyPorts
