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
#         fab predeploy
#         <wait for reboot>
#         fab deploy:host=new-rascal-host-name.local
# or just
#         fab deploy:host=new-rascal-host-name.local

@task
def predeploy():
    local('ssh-keygen -R beaglebone.local') # remove host key, if it exists
    prep_host() # # Set the password. Can't log in to blank-password host with Fabric.
    set_hostname()

@task
def deploy():
    disable_bonescript_and_release_http_port()
    update_debian_package_lists()
    remove_unneeded_debian_packages()
    for package in DEBIAN_PACKAGES_TO_INSTALL:
        install_debian_package(package)
    install_python_modules()
    install_rascal_software()
    install_config_files()
    allow_uwsgi_to_control_supervisor()
    allow_uwsgi_to_access_usb_port()
    install_libpruio()
    install_oh_my_zsh()
    autoremove_debian_package_remnants()
    print(green('Rascal 2 deployment complete. Rebooting . . .'))
    reboot()

def prep_host():
    # Set the password. Can't log in to blank-password host with Fabric.
    local('./prep_host.sh')

def set_hostname():
    prompt('Enter new hostname: ', 'hostname', default='rascal2')
    print(green('Setting hostname to: ' + env.hostname))
    run('echo ' + env.hostname + ' > /etc/hostname')
    print(green('Rebooting . . .'))
    reboot()

def disable_bonescript_and_release_http_port():
    print(green('Disabling Bonescript . . .'))
    with settings(warn_only=True):
        for service in BONESCRIPT_SERVICES:
            fabtools.systemd.stop_and_disable(service)
    fabtools.utils.run_as_root('systemctl disable bonescript.socket')
    fabtools.utils.run_as_root('systemctl disable cloud9.socket')
    #reboot() # to get init process to release port 80

def update_debian_package_lists():
    print(green('\nUpdating package repository lists'))
    run('apt-get update -y', pty=False)

def install_python_modules():
    for module in PYTHON_MODULES_TO_INSTALL:
        print(green('\nInstalling Python module: {0}'.format(module)))
        run('pip install ' + module)

def package_installed(package):
    cmd = 'dpkg-query -l "{0}" | grep -q ^.i'.format(package)
    with settings(warn_only=True):
        result = run(cmd)
    return result.succeeded

def install_debian_package(package):
    if not package_installed(package):
        print(green('\nInstalling package: {0}'.format(package)))
        run('apt-get install -y ' + package, pty=False)
    else:
        print(green('Package ' + package + ' already installed'))

def autoremove_debian_package_remnants():
    print(green('\nRemoving unneeded package remnants'))
    run('apt-get autoremove -y', pty=False)

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
    run('chown -R www-data:www-data /var/log/uwsgi')
    run('adduser www-data shadow') # just 'read' access so uWSGI can authenticate against /etc/shadow

    if exists('/var/www/editor/static/codemirror'):
        run('rm -rf /var/www/editor/static/codemirror')
        run('wget https://github.com/marijnh/CodeMirror/archive/4.2.0.tar.gz')
        run('tar xzvf 4.2.0.tar.gz')
        run('mv CodeMirror-4.2.0/ /var/www/editor/static/codemirror')
    run('chown -R www-data:www-data /var/www')

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
    put('issue', '/etc/issue')
    put('issue.sh', '/etc/profile.d/issue.sh')

def allow_uwsgi_to_control_supervisor():
    run('groupadd -f supervisor')
    run('usermod -a -G supervisor www-data')
    put('supervisord.conf', '/etc/supervisor/supervisord.conf')

def allow_uwsgi_to_access_usb_port():
    run('usermod -a -G dialout www-data')

def install_libpruio():
    install_debian_package('am335x-pru-package')

    run('wget http://www.freebasic-portal.de/dlfiles/589/BBB_fbc-1.00.tar.bz2')
    run('tar xjf BBB_fbc-1.00.tar.bz2')
    run('cp  BBB_fbc-1.00/usr/local/bin/fbc /usr/bin/')
    run('cp -r BBB_fbc-1.00/usr/local/lib/freebasic/* /usr/lib/')
    run('rm -rf BBB_fbc-1.00')

    run('wget http://www.freebasic-portal.de/dlfiles/539/FB_prussdrv-0.0.tar.bz2')
    run('tar xjf FB_prussdrv-0.0.tar.bz2')
    run('mkdir -p /usr/include/freebasic/BBB')
    run('cp -r FB_prussdrv-0.0/include/* /usr/include/freebasic/BBB/')
    run('mv FB_prussdrv-0.0/bin/pasm /usr/bin/pasm')
    run('rm -rf FB_prussdrv-0.0')

    run('wget https://github.com/rascalmicro/libpruio/archive/master.zip')
    run('unzip master.zip')
    run('cp libpruio-master/src/c_wrapper/libpruio.so /usr/lib') # directory name is probably wrong
    run('ldconfig')
    run('cp libpruio-master/src/c_wrapper/pruio*.h* /usr/include')
    run('cp libpruio-master/src/config/libpruio-00A0.dtbo /lib/firmware') # note corrected filename 0A00 -> 00A0
    run('cp libpruio-master/src/pruio/pruio*.bi /usr/include/freebasic/BBB')
    run('cp libpruio-master/src/pruio/pruio.hp /usr/include/freebasic/BBB')
    run('echo uio_pruss >> /etc/modules') # load uio_pruss module at boot
    put('libpruio.service', '/etc/systemd/system/libpruio.service')
    run('systemctl enable libpruio.service')

def install_oh_my_zsh():
    run('wget --no-check-certificate http://install.ohmyz.sh -O - | sh')

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
