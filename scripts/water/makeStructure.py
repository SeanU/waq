#!/usr/bin/env python

from os import path
from os import makedirs
import sys

from common import state_to_id, water_file_types

def makedir(dirpath):
    if not path.exists(dirpath):
        print('\tcreating ' + dirpath)
        makedirs(dirpath)

def main(root):
    print('Ensuring directory structure exists at ' + root)
    dirs = [path.join(root, state) for state in state_to_id]

    for d in dirs:
        makedir(d)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: make-structure.py [root-dir]')
    else:
        main(sys.argv[1])
