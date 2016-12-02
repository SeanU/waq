
#!/usr/bin/env python

import os
import os.path
import sys

import markdown as md

if len(sys.argv) < 2:
    print('Need a directory to scan')
    sys.exit(-1)

inputSource = sys.argv[1]
print('Converting Markdown files in ' + inputSource + '...')

def getMdFiles(dir):
    for directory, subdirs, files in os.walk(dir):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext == '.md':
                p = os.path.join(directory, file)
                yield os.path.realpath(p)

def convert(path):
    root, _ = os.path.splitext(path)
    outputPath = root + ".html"
    md.markdownFromFile(path, outputPath)
    
for file in getMdFiles(inputSource):
    print('\t' + file)
    convert(file)