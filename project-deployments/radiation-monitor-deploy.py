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
env.user = 'root'

@task
def deploy():

    # scipy 0.14 already installed as long as we stay on Debian Jessie or newer

    if not exists('/usr/local/radmonitor'):
        run('git clone https://github.com/rascalmicro/radmonitor.git /usr/local/radmonitor')
    with cd('/usr/local/radmonitor'):
        run('cp util/gps.py /usr/local/lib/python2.7/dist-packages/')

    if not exists('/usr/local/emorpho-cpython'):
        run('git clone https://github.com/rascalmicro/emorpho-cpython.git /usr/local/emorpho-cpython')
    with cd('/usr/local/emorpho-cpython'):
        run('git checkout linux')
        run('python ./setup.py build') # api/usb.h:5:21: fatal error: windows.h: No such file or directory
        run('sudo python ./setup.py install')

# add supervisor task to run radmonitor