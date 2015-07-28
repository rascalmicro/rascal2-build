PYTHON_MODULES_TO_INSTALL = [
    'flask',
    'geopy',
    'gevent',
#    'gevent-websocket',
    'Flask-uWSGI-WebSocket',
    'markdown2',
    'redis',
    'uwsgi',
    'pytronics',
#    'pytumblr', # appears busted for Python 3
    'bitstring',
    'Flask-Login',
    'twilio'
]

# Reformatted Debian package list, as a manual workaround for an annoying apt bug that
# will surely be fixed any day now
#
# avr-libc autossh gcc-avr gpsd-clients htop ipython-notebook libpq-dev libftdi-dev lsof nginx postgis postgresql python-flask python-matplotlib python-mpltoolkits.basemap python-psycopg2 python-requests python-scipy python-webcolors strace supervisor vim zip

DEBIAN_PACKAGES_TO_INSTALL = [
    'avr-libc',
    'autossh',
    'fswebcam',
    'gcc-avr',
    'gpsd-clients',
    'htop',
    'ipython-notebook',
    'ipython3-notebook',
    'libpq-dev',
    'libftdi-dev',
    'lsof',
    'nginx',
    'postgis',
    'postgresql',
    'python-flask',
    'python3-flask',
    'python-matplotlib',
    'python3-matplotlib',
    'python-mpltoolkits.basemap',# No Python 3 version yet
    'python3-pip',
    'python-psycopg2',
    'python3-psycopg2',
    'python-requests',
    'python3-requests',
#    'python3-rpi.gpio',
    'python-scipy',
    'python3-scipy',
    'python3-serial',
    'python3-smbus',
    'python-webcolors',
    'python3-webcolors',
    'strace',
    'supervisor', # Not sure if this supports Python 3 or not
    'vim',
    'zip',
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
    'xserver-common',
    #'libgtk2.0-common', # probably breaks OpenCV. Also, required by gpsd-clients (and maybe also by some Python libs)
    'libgtk-3-common' # removes Gstreamer and Numpy
]
