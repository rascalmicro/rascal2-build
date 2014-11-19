from __future__ import with_statement
import crypt
from fabric.api import *
from fabric.colors import green, red
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, sed
from fabric.operations import local, reboot
import fabtools
from package_lists import *

env.host = 'beaglebone.local'
env.user = 'root'

# Usage
#         fab predeploy deploy:host=new-rascal-host-name
# or just
#         fab deploy:host=new-rascal-host-name

@task
def predeploy():
    prep_host()
    set_hostname()

@task
def deploy():
    disable_bonescript()
    remove_unneeded_debian_packages()
    install_debian_packages()
    install_python_modules()
    install_rascal_software()
    install_config_files()
    allow_uwsgi_to_control_supervisor()
    set_zsh_as_default_shell()
    reboot()

def prep_host():
    # Set the password. Can't log in to blank-password host with Fabric.
    local('./prep_host.sh')

def set_hostname():
    prompt('Enter new hostname: ', 'hostname', default='rascal2')
    print(green('Setting hostname to: ' + env.hostname))
    run('echo ' + env.hostname + ' > /etc/hostname')
    reboot()

def install_python_modules():
    for module in PYTHON_MODULES_TO_INSTALL:
        print(green('\nInstalling Python module: {0}'.format(module)))
        run('pip install ' + module)

def package_installed(package):
    cmd = 'dpkg-query -l "{0}" | grep -q ^.i'.format(package)
    with settings(warn_only=True):
        result = run(cmd)
    return result.succeeded

def install_debian_packages():
    print(green('\nUpdating package repository lists'))
    run('apt-get update -y', pty=False)

    for package in DEBIAN_PACKAGES_TO_INSTALL:
        if not package_installed(package):
            print(green('\nInstalling package: {0}'.format(package)))
            run('apt-get install -y ' + package, pty=False)
        else:
            print(green('Package ' + package + ' already installed'))

    print(green('\nRemoving unneeded package remnants'))
    run('apt-get autoremove -y', pty=False)

def disable_bonescript():
    print(green('Disabling Bonescript . . .'))
    for service in BONESCRIPT_SERVICES:
        fabtools.systemd.stop_and_disable(service)
    fabtools.utils.run_as_root('systemctl disable bonescript.socket')
    fabtools.utils.run_as_root('systemctl disable cloud9.socket')

def remove_unneeded_debian_packages():
    for package in DEBIAN_PACKAGES_TO_REMOVE:
        if package_installed(package):
            print(green('\nRemoving package: {0}'.format(package)))
            run('apt-get remove -y ' + package, pty=False)
        else:
            print(green('Package ' + package + ' already removed.'))

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
    run('adduser www-data shadow') # just 'read' access so uWSGI can authenticate against /etc/shadow

    if exists('/var/www/editor/static/codemirror'):
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
    put('gitconfig', '/root/.gitconfig')

def allow_uwsgi_to_control_supervisor():
    run('groupadd supervisor')
    run('usermod -a -G supervisor www-data')
    # The lines below might not write to the right section in the config file. This should be tested.
    # Should write to [unix_http_server]
    before = 'chmod=0770 ; socket file mode (default 0700)'
    after = 'chmod=0770\r\n    chown=root:supervisor'
    sed('/etc/supervisor/supervisord.conf', before, after)

def set_zsh_as_default_shell():
    pass
    # chsh
    # Changing the login shell for root
    # Enter the new value, or press ENTER for the default
    # Login Shell [/bin/bash]: /bin/zsh
    # curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh

### END DEPLOY SECTION ###

### START TEST SECTION ###

@task
def test():
    check_debian_packages()
    check_programs()
    check_python_modules()

PROGRAMS_TO_TEST = {
    'nginx': '/usr/sbin/nginx',
    'uwsgi': '/usr/local/bin/uwsgi',
    'zsh': '/usr/bin/zsh',
}

PYTHON_MODULES_TO_TEST_IMPORT = [
    'gevent',
    'geventwebsocket',
    'flask.ext.uwsgi_websocket',
    'redis',
    # uwsgi omitted; not a Python module, though installed with pip
    'pytronics',
    'bitstring',
    'webcolors',
    'flask_login'
]

def check_debian_packages():
    for package in sorted(DEBIAN_PACKAGES_TO_INSTALL):
        if package_installed(package):
            print(green('Package {0} found.'.format(package)))
        else:
            print(red('Package {0} missing!'.format(package)))

def check_programs():
    for program in sorted(PROGRAMS_TO_TEST.keys()):
        try:
            run('which ' + program) == PROGRAMS_TO_TEST[program]
        except:
            print(red('Binary for {0} not at {1}.'.format(program, PROGRAMS_TO_TEST[program])))
        else:
            print(green('Binary for {0} found at {1}'.format(program, PROGRAMS_TO_TEST[program])))

def check_python_modules():
    for module in PYTHON_MODULES_TO_TEST_IMPORT:
        try:
            run('python -c "__import__(\'' + module + '\')"')
        except:
            print(red('Module {0} not installed.'.format(module)))
        else:
            print(green('Successfully imported module {0}.'.format(module)))
