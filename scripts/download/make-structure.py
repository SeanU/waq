#!/usr/bin/env python

from os import path
from os import makedirs
import sys

from common import *

def makedir(dirpath):
    if not path.exists(dirpath):
        print('\tcreating ' + dirpath)
        makedirs(dirpath)

def makeWaterDirs(subdir):
    subdir = path.join(subdir, 'water')
    makedir(subdir)

    dirs = [path.join(subdir, ftype) for ftype in water_file_types]

    for d in dirs:
        makedir(d)

def main(root):
    print('Ensuring directory structure exists at ' + root)
    dirs = [path.join(root, state) for state in state_codes]

    for d in dirs:
        makedir(d)
        makeWaterDirs(d)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: make-structure.py [root-dir]')
    else:
        main(sys.argv[1])
