build instructions
==================

1. install ucs
2. install necessary packages as root:

		apt-get install build-essential debhelper devscripts univention-config-dev univention-management-console-dev git-core

3. obtain source code from github

		git clone https://github.com/hermanthegerman2/asterisk4ucs.git

4. make changes 
5. create new versions in each modules with
   
		dch -i

6. make release with 
   
		./buildall
7. create release directory

		mkdir release/asterisk4ucs-1.1.0
8. copy all debian packages to release directory

		cp *.deb release/asterisk4ucs-1.1.0
9. enter release directory

		cd release
10. execute release-script

		./release 1.1.0

