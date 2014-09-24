from __future__ import with_statement
from fabric.api import *
from fabric.colors import green
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from package_lists import *
import os

env.hosts = ['root@beaglebone.local']

@task
def deploy():
    set_hostname()
    set_passwords()
    disable_bonescript()
    remove_unneeded_debian_packages()
    install_debian_packages()
    install_python_modules()
    install_rascal_software()
    install_config_files()
    allow_uwsgi_to_control_supervisor()
    set_zsh_as_default_shell()

def set_hostname():
	prompt('Enter hostname: ', 'hostname', default='rascal2')
	print(green('Setting hostname to: ' + env.hostname))
	run('echo ' + env.hostname + ' > /etc/hostname')

def set_passwords():
    print(green('Setting passwords for root and debian accounts'))

def install_python_modules():
    for module in PYTHON_MODULES_TO_INSTALL:
        print(green('\nInstalling Python module: {0}'.format(module)))
        run('pip install ' + module)

def install_debian_packages():
    print(green('\nUpdating package repository lists'))
    run('apt-get update -y', pty=False)

    for package in DEBIAN_PACKAGES_TO_INSTALL:
        print(green('\nInstalling package: {0}'.format(package)))
        run('apt-get install -y ' + package, pty=False)

    print(green('\nRemoving unneeded package remnants'))
    run('apt-get autoremove -y', pty=False)

def disable_bonescript():
    print(green('Disabling Bonescript . . .'))
    for service in BONESCRIPT_SERVICES:
        run('systemctl disable ' + service)

def remove_unneeded_debian_packages():
    for package in DEBIAN_PACKAGES_TO_REMOVE:
        print(green('\nRemoving package: {0}'.format(package)))
        run('apt-get remove -y ' + package, pty=False)

def install_rascal_software():
    print(green('Installing Rascal editor . . .'))
    if not exists('/var/www/editor'):
        run('git clone https://github.com/rascalmicro/red.git /var/www/editor')
    if not exists('/var/www/public'):
        run('git clone https://github.com/rascalmicro/demos.git /var/www/public')
    if not exists('/var/log/uwsgi'):
        run('mkdir /var/log/uwsgi')
    run('touch /var/log/uwsgi/public.log')
    run('touch /var/log/uwsgi/emperor.log')
    run('touch /var/log/uwsgi/editor.log')
    run('chown -R www-data /var/log/uwsgi')
    run('chgrp -R www-data /var/log/uwsgi')

    if os.path.isdir('/var/www/editor/static/codemirror'):
        run('rm -rf /var/www/editor/static/codemirror')
        run('wget https://github.com/marijnh/CodeMirror/archive/4.2.0.tar.gz')
        run('tar xzvf 4.2.0.tar.gz')
        run('mv CodeMirror-4.2.0/ /var/www/editor/static/codemirror')

    run('systemctl enable nginx.service')

def install_config_files():
    print(green('Copying over config files . . .'))
    put('default', '/etc/nginx/sites-available/')
    run('mkdir -p /etc/uwsgi/vassals')
    put('emperor.ini', '/etc/uwsgi/emperor.ini')
    put('editor.ini', '/etc/uwsgi/vassals/editor.ini')
    put('public.ini', '/etc/uwsgi/vassals/public.ini')
    put('uwsgi.service', '/etc/systemd/system/uwsgi.service')
    run('systemctl enable uwsgi.service')
    put('vimrc', '/root/.vimrc')

def allow_uwsgi_to_control_supervisor():
    run('echo "chmod=0770 ; socket file mode (default 0700)" >> /etc/supervisor/supervisor.conf')
    run('echo "chown=root:supervisor" >> /etc/supervisor/supervisor.conf')

def set_zsh_as_default_shell():
    pass
    # chsh
    # Changing the login shell for root
    # Enter the new value, or press ENTER for the default
    # Login Shell [/bin/bash]: /bin/zsh
    # curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh
