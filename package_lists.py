PYTHON_MODULES_TO_INSTALL = [
    'gevent',
    'gevent-websocket',
    'Flask-uWSGI-WebSocket',
    'markdown2',
    'redis',
    'uwsgi',
    'pytronics',
    'bitstring',
    'Flask-Login',
    'twilio'
]

DEBIAN_PACKAGES_TO_INSTALL = [
    'avr-libc',
    'autossh',
    'gcc-avr',
    'gpsd-clients',
    'htop',
    'ipython-notebook',
    'libpq-dev',
    'libftdi-dev',
    'lsof',
    'nginx',
    'postgis',
    'postgresql',
    'python-flask',
    'python-matplotlib',
    'python-mpltoolkits.basemap',
    'python-psycopg2',
    'python-requests',
    'python-scipy',
    'python-webcolors',
    'strace',
    'supervisor',
    'vim,'
    'zip'
    #'zsh'
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
    'xserver-common',
    #'libgtk2.0-common', # probably breaks OpenCV. Also, required by gpsd-clients (and maybe also by some Python libs)
    'libgtk-3-common' # removes Gstreamer and Numpy
]

BONESCRIPT_SERVICES = [
    'cloud9',
    'bonescript',
    'bonescript-autorun',
    'apache2'
]
