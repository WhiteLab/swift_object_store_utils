#!/usr/bin/env python
import sys
from source_novarc import source_novarc
from subprocess import call
from date_time import date_time


def download_from_swift_list(cont, fn, novarc):
    source_novarc(novarc)
    deproxy = 'unset http_proxy; unset https_proxy;'
    fh = open(fn, 'r')
    for obj in fh:
        swift_cmd = deproxy + "swift download " + cont + " --skip-identical " + obj + " >> dl_log.txt"
        sys.stderr.write(date_time() + swift_cmd + "\n")
        call(swift_cmd, shell=True)
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Download from swift using container list')
    parser.add_argument('-c', '--container', action='store', dest='cont', help='Swift container, i.e. PANCAN')
    parser.add_argument('-f', '--file', action='store', dest='fn',
                        help='Swift object list - text document one per line')
    parser.add_argument('-n', '--novarc', action='store', dest='novarc', help='.novarc with openstack authentication')


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (cont, fn, novarc) = (inputs.cont, inputs.fn, inputs.novarc)
    download_from_swift_list(cont, fn, novarc)
