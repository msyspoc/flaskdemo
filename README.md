Flask App

1. Need to install the Python, Mongodb and Flask in your system.

#Command for installing Python:-
sudo apt-get install python

#Command for installing Mongodb:-
Install MongoDB
Step 1: Import the MongoDB repository:
> sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
Create a source list file for MongoDB
> echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
Update the local package repository
> sudo apt-get update

Step 2: Install the MongoDB packages
Install the latest stable version of MongoDB:
> sudo apt-get install -y mongodb-org
Install a specific release of MongoDB:
> sudo apt-get install -y mongodb-org=3.4 mongodb-org-server=3.4 mongodb-org-shell=3.4 mongodb-org-mongos=3.4 mongodb-org-tools=3.4

Step 3: Launch MongoDB as a service on Ubuntu 16.04
Create a configuration file named mongodb.service in /etc/systemd/system to manage the MongoDB service.
> sudo vim /etc/systemd/system/mongodb.service
Copy the following contents in the file.

" #Unit contains the dependencies to be satisfied before the service is started.
[Unit]
Description=MongoDB Database
After=network.target
Documentation=https://docs.mongodb.org/manual
#Service tells systemd, how the service should be started.
#Key `User` specifies that the server will run under the mongodb user and
#`ExecStart` defines the startup command for MongoDB server.
[Service]
User=mongodb
Group=mongodb
ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf
#Install tells systemd when the service should be automatically started.
#`multi-user.target` means the server will be automatically started during boot.
[Install]
WantedBy=multi-user.target "

Update the systemd service with the command stated below:
> systemctl daemon-reload
Start the service with systemcl.
> sudo systemctl start mongodb
Check if mongodb has been started on port 27017 with netstat command:
> netstat -plntu
Check if the service has started properly.
> sudo systemctl status mongodb
The output to the above command will show `active (running)` status with the PID and Memory/CPU it is consuming.
Enable auto start MongoDB when system starts.
> sudo systemctl enable mongodb
Stop MongoDB
> sudo systemctl stop mongodb
Restart MongoDB
> sudo systemctl restart mongodb
or 
sudo apt install mongodb-server

#Command for installing Flask:-

Step 1:Let’s start by creating a virtual environment -
> cd ~
> sudo apt-get install python-virtualenv 
> sudo apt-get install python-pip
To check if virtualenv is correctly installed, type -
> virtualenv --version
At the time this post was written, the output was -
> 1.11.4

Step 2:Now let’s make a directory flask-application where we will store our project.
> mkdir flaskproject
> cd flaskproject

Step 3:It time to create to virtual environment flask-env, where we will install flask.
> virtualenv flask-env
You will see the following output on the terminal -
> New python executable in flask-env/bin/python
> Installing setuptools, pip...done.

Step 4:We have successfully created our virtual environment, now let’s activate it using the command below -
> source flask-env/bin/activate

Step 5:It is time to install flask. We will use pip to install the package -
pip install Flask

2. Created the Database mydata in Mongodb.

3. Created the Collection userdata in mydata Database.

4. Create the mongo.py file in flaskproject directory.

5. Import Flask, jsonify, request, render_template, session, redirect, url_for, Response, make_response from flask module.

6. Import PyMongo from flask_pymongo.
#Command for installing flask_pymongo:-
> sudo pip install Flask-PyMongo

7. Import MongoClient from pymongo. 
# Using MongoClient, we made the connection with Mongodb database.

8. Import BSON, json_util, ObjectId from bson.
#Command for installing bson:-
> sudo pip install bson

9. Import Template from jinja2.
#Command for installing jinja2:-
> sudo pip install jinja2 

10. Import join, dirname, realpath from os.path.

11. Then, wrote some methods for our user login apllication.

12. For password encryption, import hashlib and salt.

13. Save session and cookies on our apllication for unique users.
