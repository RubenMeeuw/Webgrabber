#!/bin/bash
bindDirectory="/etc/bind/"
namedConfFile="named.conf.local"

while getopts "vhe" name ; do
  case $name in
   v)
    echo "Version 1.0 made by Ruben Meeuwissen"
    exit 0;;
   h)
    echo "Usage:"
    echo "./install.sh -h to get this help message"
    echo "./install.sh -v to get the version"
    echo "./install.sh -e to run the installation"
    echo "./install.sh without arguments to do only installation."
    echo "Use sudo for this command"
    exit 0;;
  esac
done

copyDNSFiles () {
  cp db.* $bindDirectory
}

mergeNamedConfFile () {
  originConf=$bindDirectory$namedConfFile
  # If not already merged -> merge
  if grep "$(cat $namedConfFile | sed -n 2p)" -q  $originConf; then # Check if sencond line is in origin
    cat $namedConfFile >> $originConf
  fi
}

restartBindServer () {
  /etc/init.d/bind9 restart
}

copyDNSFiles
mergeNamedConfFile
restartBindServer
