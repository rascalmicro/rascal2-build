#!/usr/bin/python

from colorprint import redprint, greenprint
import sh

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

PROGRAMS_TO_TEST = {
    'nginx': '/usr/sbin/nginx',
    'uwsgi': '/usr/local/bin/uwsgi',
    'zsh': '/usr/bin/zsh'
}

def check_programs():
    for program in sorted(PROGRAMS_TO_TEST.keys()):
        try:
            sh.which(program) == PROGRAMS_TO_TEST[program]
        except AssertionError:
            redprint('Binary for {0} not at {1}.'.format(program, PROGRAMS_TO_TEST[program]))
        else:
            greenprint('Binary for {0} found at {1}'.format(program, PROGRAMS_TO_TEST[program]))

def check_python_modules():
    for module in PYTHON_MODULES_TO_TEST_IMPORT:
        try:
            __import__(module)
        except ImportError:
            redprint('Module {0} not installed.'.format(module))
        else:
            greenprint('Successfully imported module {0}.'.format(module))

def main():
    check_python_modules()
    check_programs()

if __name__ == "__main__":
    main()
