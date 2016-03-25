#!/usr/bin/env python
import sys
from source_novarc import source_novarc
from subprocess import check_output
import subprocess

from date_time import date_time


def download_from_swift(cont, obj, novarc):
    source_novarc(novarc)
    swift_cmd = "swift download " + cont + " --skip-identical --prefix " + obj
    sys.stderr.write(date_time() + swift_cmd + "\n")
    try:
        check = check_output(swift_cmd, shell=True, stderr=subprocess.PIPE)
    except:
        sys.stderr.write(date_time() + "Download of " + obj + " from " + cont + " failed\n")
        exit(1)
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Simple download module to get files from swift.  Can use prefix or whole object name')
    parser.add_argument('-c', '--container', action='store', dest='cont', help='Swift container, i.e. PANCAN')
    parser.add_argument('-o', '--object', action='store', dest='obj',
                        help='Swift object name/prefix, i.e. RAW/2015-1234')
    parser.add_argument('-n', '--novarc', action='store', dest='novarc', help='.novarc with openstack authentication')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (cont, obj, novarc) = (inputs.cont, inputs.obj, inputs.novarc)
    download_from_swift(cont, obj, novarc)
