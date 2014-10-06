#! /usr/bin/python

# This is a fabfile for deploying code with Fabric: http://fabfile.org
#
# You can run this file with a command like this: fab -f radiation-monitor-deploy.py deploy

from __future__ import with_statement
from fabric.api import *
from fabric.colors import green, red
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.operations import reboot
import fabtools

env.hosts = ['root@beaglebone.local']

@task
def deploy():
    pass

    # Need to add:

    # Maybe newer version of Scipy? Current version in apt repos is 0.10.1, need 0.11?

    # gpsd
    
    # git clone https://github.com/rascalmicro/emorpho-cpython.git
    # cd emorpho-cpython
    # git branch linux
    # python ./setup.py build
    # sudo python ./setup.py install
    
    # git clone https://github.com/rascalmicro/radmonitor.git
    # cd radmonitor
    # mv util/gps.py /usr/local/lib/python2.7/dist-packages/
