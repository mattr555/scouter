#!/bin/bash

apt-get update
sudo apt-get install -y curl git
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get install -y python-pip nodejs
sudo pip install -r requirements.txt
sudo npm install -g bower
bower install
