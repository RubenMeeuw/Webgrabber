# Webgrabber

This python script consist of three elements.
- It searches for defined html websites and will make a copy of all html content possible, and stores it in a folder.
- It creates a webserver package ready to deploy on your webserver.
- It creates a dns-server package ready to deploy on your dns-server.

**Note: use the generated content only for local testing purposes. Do not deploy any of the generated content on the open web. I am not responsible for any negative effects that may result from this.**

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
On your system you will need to have python2 to run the script.

Make sure your webserver has apache2 and ifupdown script:
```
sudo apt-get update;
sudo apt-get install apache2;
sudo apt-get install ifupdown;
```
Your dns-server will need to have a running version of bind9.
```
sudo apt-get update;
sudo apt-get install bind9 bind9utils bind9-doc;
```
### Creating the Packages
Dowload or clone this package to your system.
Go to the root folder of the package and run the following command:
```
python createSetupPackage.py
```
### Install the Webserver Package
Move the package to your webserver with for example the 'scp' command.
Go to the root folder of the package and execute the following command on the webserver:
```
sudo chmod +x install.sh && sudo ./install.sh
```

### Install the DNS Package
Move the package to your dns-server with for example the 'scp' command.
Go to the root folder of the package and execute the following command on the webserver:
```
sudo chmod +x install.sh && sudo ./install.sh
```

## Additional

### Webgrabber Options
You can execute the python script by adding a linkparser which redirects any hyperlink on the website to one of your grabbed websites. Execute the following command:
```
python createSetupPackage.py -l
```
For more options execute:
```
python createSetupPackage.py -h
```

### Webgrabber Settings
- You can add websites by adding their link to the 'websites.txt' file. Note: Their address should be of the form 'www.example.com'.
- Change the config to your liking by changing the domain or ip prefix.

## Built With

* [Atom](https://atom.io/) - The IDE used
* [Python](https://www.python.org/) - Main programming language
* [Wget](https://www.gnu.org/software/wget/) - Command used for grabbing websites

## Authors
- Ruben Meeuwissen

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
**Note: use the generated content only for local testing purposes. Do not deploy any of the generated content on the open web. I am not responsible for any negative effects that may result from this.**
