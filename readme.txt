How to run:

1. Install docker

	To install required tools(docker) save the bash script below and execute it::
	
	#!/bin/bash

	#Pull in the shell script to install docker
	wget -qO- https://get.docker.com/ | sh

	#Add your current user to docker group to ease process(Logout is needed to bring this in effect)
	sudo usermod -aG docker $(whoami)

	#Install pip
	sudo apt-get -y install python-pip

	#Install docker-compose
	sudo pip install docker-compose

2. Create containers using 
	docker-compose -f local.yml up --build -d

	#This will create all the containers needed, django and postgresql and run them in background

	#if you are not able to see logs then hit ctrl+c and run

	docker-compose -f local.yml logs --tail=0 --follow

3. Make migrations
	docker-compose -f local.yml run django python manage.py makemigrations

4. Migrate 
	docker-compose -f local.yml run django python manage.py migrate