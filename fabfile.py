from __future__ import with_statement
from package_lists import *
from fabric.api import *
from fabric.colors import green
from fabric.contrib.console import confirm

env.hosts = ['root@beaglebone.local']

def prepare_host():
    run('pip install -U pip')

def deploy():
    pass
#    run('git clone https://github.com/rascalmicro/rascal2-build.git')
#    with cd('rascal2-build'):
#        run('python build-rascal2.py')

    set_passwords()
    disable_bonescript()
    remove_unneeded_debian_packages()
    install_debian_packages()
    install_python_modules()
    #install_rascal_software()
    #install_config_files()
    #allow_uwsgi_to_control_supervisor()
    #set_zsh_as_default_shell()

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
    greenprint('Installing Rascal editor . . .')
    if not (os.path.isdir('/var/www/editor')):
        sh.git.clone('https://github.com/rascalmicro/red.git', '/var/www/editor')
    if not (os.path.isdir('/var/www/public')):
        sh.git.clone('https://github.com/rascalmicro/demos.git', '/var/www/public')
    if not os.path.isdir('/var/log/uwsgi'):
        sh.mkdir('/var/log/uwsgi')
    sh.touch('/var/log/uwsgi/public.log')
    sh.touch('/var/log/uwsgi/emperor.log')
    sh.touch('/var/log/uwsgi/editor.log')
    sh.chown('-R', 'www-data', '/var/log/uwsgi')
    sh.chgrp('-R', 'www-data', '/var/log/uwsgi')

    if os.path.isdir('/var/www/editor/static/codemirror'):
        sh.rm('-rf', '/var/www/editor/static/codemirror')
        sh.wget('https://github.com/marijnh/CodeMirror/archive/4.2.0.tar.gz')
        sh.tar('xzvf', '4.2.0.tar.gz')
        sh.mv('CodeMirror-4.2.0/', '/var/www/editor/static/codemirror')

    sh.systemctl('enable', 'nginx.service')

def install_config_files():
    greenprint('Copying over config files . . .')
    sh.mkdir('-p', '/etc/uwsgi/vassals')
    sh.cp('./emperor.ini', '/etc/uwsgi/emperor.ini')
    sh.cp('./editor.ini', '/etc/uwsgi/vassals/editor.ini')
    sh.cp('./public.ini', '/etc/uwsgi/vassals/public.ini')
    sh.cp('./uwsgi.service', '/etc/systemd/system/uwsgi.service')
    sh.systemctl('enable', 'uwsgi.service')
    sh.cp('./vimrc', '/root/.vimrc')

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
