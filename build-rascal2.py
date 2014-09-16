#!/usr/bin/python

import os
import pip
import sh
import subprocess
import sys
import threading

INSTALLATION_TOOLS = [
    'sh'
]

PYTHON_MODULES_TO_INSTALL = [
	'gevent',
	'gevent-websocket',
	'Flask-uWSGI-WebSocket',
	'redis',
	'uwsgi',
	'pytronics',
	'bitstring',
	'webcolors',
	'Flask-Login'
]

DEBIAN_PACKAGES_TO_INSTALL = [
	'nginx',
	'python-flask',
	'supervisor',
	'zsh'
]

DEBIAN_PACKAGES_TO_REMOVE = [
	'apache2',
	'apache2-mpm-worker',
	'apache2-utils',
	'apache2.2-bin',
	'apache2.2-common',
	'nodejs',
	'xscreensaver',
	'xscreensaver-data',
	'xserver-xorg-core',
	'xserver-common'
	'libgtk2.0-common', # probably breaks OpenCV
	'libgtk-3-common' # removes Gstreamer and Numpy
]

BONESCRIPT_SERVICES = [
	'cloud9.service',
	'bonescript.service',
	'bonescript.socket',
	'bonescript-autorun.service'
]

class RepeatingTimer(threading._Timer):
    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                return
            else:
                self.function(*self.args, **self.kwargs)

def status():
    sys.stdout.write('* ')
    sys.stdout.flush()

def set_passwords():
    print('Setting passwords for root and debian accounts')

def install_tools():
    for module in INSTALLATION_TOOLS:
        print('\nInstalling tool: {0}'.format(module))
        pip.main(['install', module])

def install_python_modules():
	for module in PYTHON_MODULES_TO_INSTALL:
        print('\nInstalling Python module: {0}'.format(module))
		pip.main(['install', module])

def install_debian_packages():
	for package in DEBIAN_PACKAGES_TO_INSTALL:
		print('\nInstalling package: {0}'.format(package))
		timer = RepeatingTimer(1.0, status)
		timer.daemon = True # Allows program to exit if only the thread is alive
		timer.start()
		proc = subprocess.Popen('apt-get install -y '+ package, shell=True, stdin=None, stdout=open(os.devnull,"wb"), stderr=subprocess.STDOUT, executable="/bin/bash")
		proc.wait()
		timer.cancel()

def disable_bonescript():
	print('Disabling Bonescript . . .')
	for service in BONESCRIPT_SERVICES:
		sh.systemctl('disable', service)

def remove_unneeded_debian_packages():
	for package in DEBIAN_PACKAGES_TO_REMOVE:
		print('\nRemoving package: {0}'.format(package))
		timer = RepeatingTimer(1.0, status)
		timer.daemon = True # Allows program to exit if only the thread is alive
		timer.start()
		proc = subprocess.Popen('apt-get remove -y '+ package, shell=True, stdin=None, stdout=open(os.devnull,"wb"), stderr=subprocess.STDOUT, executable="/bin/bash")
		proc.wait()
		timer.cancel()
	# then apt-get autoremove?

def install_rascal_software():
	print('Installing Rascal editor . . .')
	sh.git.clone('https://github.com/rascalmicro/red.git', '/var/www/editor')
	sh.git.clone('https://github.com/rascalmicro/demos.git', '/var/www/public')
    sh.mkdir('/var/log/uwsgi')
	sh.touch('/var/log/uwsgi/public.log')
	sh.touch('/var/log/uwsgi/emperor.log')
	sh.touch('/var/log/uwsgi/editor.log')
	sh.chown('-R', 'www-data', '/var/log/uwsgi')
	sh.chgrp('-R', 'www-data', '/var/log/uwsgi')

	sh.rm('rf', '/var/www/editor/static/codemirror')
	sh.wget('https://github.com/marijnh/CodeMirror/archive/4.2.0.tar.gz')
	sh.tar('xzvf', '4.2.0.tar.gz')
	sh.mv('CodeMirror-4.2.0/', '/var/www/editor/static/codemirror')

	sh.systemctl('enable', 'nginx.service')

def install_config_files():
	print('Copying over config files . . .')
	sh.cp('./emperor.ini', '/etc/uwsgi/emperor.ini')
	sh.cp('./editor.ini', '/etc/uwsgi/vassals/editor.ini')
	sh.cp('./public.ini', '/etc/uwsgi/vassals/public.ini')
	sh.cp('./uwsgi.service', '/etc/systemd/system/uwsgi.service')
	sh.systemctl('enable', 'uwsgi.service')

def allow_uwsgi_to_control_supervisor():
	pass
	# Need to add this stuff to /etc/supervisor/supervisor.conf

	#chmod=0770                       ; socket file mode (default 0700)
	#chown=root:supervisor

def set_zsh_as_default_shell():
	pass
	# chsh
    # Changing the login shell for root
    # Enter the new value, or press ENTER for the default
	# Login Shell [/bin/bash]: /bin/zsh
	# curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh

def main():
	set_passwords()
	install_tools()
	disable_bonescript()
	remove_unneeded_debian_packages()
	install_debian_packages()
	install_python_modules()
	install_rascal_software()
	install_config_files()
	allow_uwsgi_to_control_supervisor()
	set_zsh_as_default_shell()

if __name__ == "__main__":
    main()
