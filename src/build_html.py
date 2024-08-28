#!/usr/bin/env python

import sys
import os
from time import gmtime, strftime

currentDir = os.getcwd()
rstOutput = 'rstFiles/'
htmlOutput = '../target/site'
sphinxPath = 'target/sphinx'

rstOutputISO = 'rstFilesISO/'
htmlOutputISO = '../target/iso_site'


def setupPythonPath(*paths):
    p = []
    for path in paths:
        sphinxAbsPath = os.path.abspath(os.path.join(currentDir, path))
        p.append(sphinxAbsPath)
    sys.path[:0] = p

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'Error: Please specify the documentation version'
        print 'usage:', sys.argv[0], '<Drop version>', '<Project version>'
        sys.exit(1)
    else:
        release = 'release=' + sys.argv[1]
        version = 'version=' + sys.argv[2]

    setupPythonPath(sphinxPath)
    from sphinx import cmdline

    print("\n---- Generating HTML files [%s] for LITP release %s ----\n"
            % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), sys.argv[1]))
    cmdline.main([sys.argv[0], '-a', '-D', release, '-D', version,
                 os.path.abspath(os.path.join(currentDir, rstOutput)),
                 os.path.abspath(os.path.join(currentDir, htmlOutput))])
    cmdline.main([sys.argv[0], '-a', '-D', release, '-D', version,
                 os.path.abspath(os.path.join(currentDir, rstOutputISO)),
                 os.path.abspath(os.path.join(currentDir, htmlOutputISO))])
