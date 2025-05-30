#!/usr/bin/env python3
import os
import sys

def main():
    # Ativar ambiente virtual
    if sys.platform == 'win32':
        activate_script = os.path.join('venv', 'Scripts', 'activate')
        os.system(f'call {activate_script} && python interface/app.py')
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')
        os.system(f'source {activate_script} && python interface/app.py')

if __name__ == '__main__':
    main()
