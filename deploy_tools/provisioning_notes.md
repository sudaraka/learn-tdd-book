Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.conf
* Replace SITENAME with, eg, example.com
* Replace USER with, eg, www-data

## Upstart Job

* see gunicorn-upstart.conf
* Replace SITENAME with, eg, example.com
* Replace USER with, eg, www-data

## Directory structure:

Assume we have a user account at /home/USER

    /home/USER/
    +-- sites
        +-- SITENAME
            +-- data
            +-- source
            +-- static
            +-- virtualenv
