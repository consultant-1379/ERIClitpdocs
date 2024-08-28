#!/usr/bin/env python

import sys
import os
import commands
from time import gmtime, strftime

currentDir = os.getcwd()
path3pp = 'target/deps/3pp/'
pathlitp = 'target/deps/litp/'
url3pp = ('https://arm1s11-eiffel004.eiffel.gic.ericsson.se:8443/' +
'nexus/service/local/repositories/prototype/content/com/ericsson/' +
'nms/litp/3pps/core-3pps/1.0.4/')
fileName3pp = 'core-3pps-1.0.4.gz'


def get3pps(path):

#  if not os.path.exists(os.path.abspath(os.path.join(currentDir,path3pp))):
    absPath = os.path.abspath(os.path.join(currentDir, path))
    if not os.path.exists(absPath):
        os.makedirs(absPath)

    options = r'--no-proxy -O ' + absPath + '/' + fileName3pp
    cmd = 'wget ' + options + ' ' + url3pp + fileName3pp
    print "Downloading LITP 3PPs:", fileName3pp
    status = os.system(cmd)
    if status:
        print "Error, can't get LITP 3pp resources:", status
        sys.exit(1)

    os.chdir(absPath)
    cmd = r"tar --wildcards '*.rpm' --transform='s/.*\///' -xvzf" + fileName3pp
    print "Extracting LITP 3PPs:", fileName3pp
    status = os.system(cmd)
    if status:
        print "Error, can't untar LITP 3pp RPMs:", status
        sys.exit(2)
    else:
        os.unlink(fileName3pp)
    os.chdir(currentDir)


def extractRPMs(path):
    absPath = os.path.abspath(os.path.join(currentDir, path))
    os.chdir(absPath)

    files = os.listdir(os.getcwd())
    for f in files:
        print "Extracting RPM:", f, "..."
        if f.lower().find('.rpm') < 0:
            print "Warning: file", f, "is not a RPM file, skipping ...."
            continue
        cmd = "rpm2cpio " + f + r" | cpio -idm"
        status, output = commands.getstatusoutput(cmd)
        if status:
            print "Error, can't extract LITP 3pp RPMs:", output
            sys.exit(3)
#       else:
#           os.unlink(f)
    os.chdir(currentDir)

if __name__ == '__main__':
#    print("\n  ---- Getting 3pps from Nexus [%s] ----\n"
#          % (strftime("%Y-%m-%d %H:%M:%S", gmtime())))
#    get3pps(path3pp)
#    print("\n  ---- Extracting 3PP RPMs [%s] ----\n"
#          % (strftime("%Y-%m-%d %H:%M:%S", gmtime())))
#    extractRPMs(path3pp)
    print("\n  ---- Extracting LITP RPMs [%s] ----\n"
          % (strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    extractRPMs(pathlitp)
