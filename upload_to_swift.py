#!/usr/bin/python
import subprocess
from source_novarc import source_novarc
import sys
from subprocess import check_output

from date_time import date_time


def upload_to_swift(cont, obj, novarc):
    ONE_GB = 1073741824
    source_novarc(novarc)
    swift_cmd = "swift upload " + cont + " ./ --skip-identical --object-name " + obj + " -S " + str(ONE_GB)
    sys.stderr.write(date_time() + swift_cmd + "\n")
    try:
        check = check_output(swift_cmd, shell=True, stderr=subprocess.PIPE)
    except:
        sys.stderr.write(date_time() + "Upload of " + obj + " to " + cont + " failed\n")
        exit(1)
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Uploads current directory contents to specified object and container')
    parser.add_argument('-c', '--container', action='store', dest='cont',
                        help='Swfit container to upload to.  i.e. PANCAN')
    parser.add_argument('-o', '--object', action='store', dest='obj',
                        help='Swift object name to upload current directory contents to.  i.e. ALIGN/2015-1234')
    parser.add_argument('-n', '--novarc', action='store', dest='novarc', help='.novarc with openstack authentication')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (cont, obj, novarc) = (inputs.cont, inputs.obj, inputs.novarc)
    upload_to_swift(cont, obj, novarc)
