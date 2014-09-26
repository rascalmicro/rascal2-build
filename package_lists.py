PYTHON_MODULES_TO_INSTALL = [
    'gevent',
    'gevent-websocket',
    'Flask-uWSGI-WebSocket',
    'redis',
    'uwsgi',
    'pytronics',
    'requests',
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
    'xserver-common',
    'libgtk2.0-common', # probably breaks OpenCV
    'libgtk-3-common' # removes Gstreamer and Numpy
]

BONESCRIPT_SERVICES = [
    'cloud9',
    'bonescript',
    'bonescript-autorun'
]
