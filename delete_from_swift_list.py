#!/usr/bin/env python
import sys
import re
from source_novarc import source_novarc
from subprocess import call
from date_time import date_time


def delete_from_swift_list(cont, fn, l, novarc):
    source_novarc(novarc)
    deproxy = 'unset http_proxy; unset https_proxy;'
    fh = open(fn, 'r')
    for obj in fh:
        obj = obj.rstrip('\n')
        if re.match('\W+', obj) or obj == '\n' or obj == '':
            sys.stderr.write(date_time() + 'Object ' + obj + ' looks malformed, skipping for safety reasons!\n')
            continue
        if l == 'y':
            swift_cmd = deproxy + "swift delete --leave-segments " + cont + " " + obj + " >> dl_log.txt 2>> dl_log.txt"
        else:
            swift_cmd = deproxy + "swift delete " + cont + " " + obj + " >> dl_log.txt 2>> dl_log.txt"
        sys.stderr.write(date_time() + swift_cmd + "\n")
        call(swift_cmd, shell=True)
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Delete objects from swift using object list')
    parser.add_argument('-c', '--container', action='store', dest='cont', help='Swift container, i.e. PANCAN')
    parser.add_argument('-f', '--file', action='store', dest='fn',
                        help='Swift object list - text document one per line')
    parser.add_argument('-l', '--leave', action='store', dest='l',
                        help='Flag to leave segments (\'y\') for large objects.  Useful for when a large one was renamed, but the manifest with original anes stays the same')
    parser.add_argument('-n', '--novarc', action='store', dest='novarc', help='.novarc with openstack authentication')


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (cont, fn, l, novarc) = (inputs.cont, inputs.fn, inputs.l, inputs.novarc)
    delete_from_swift_list(cont, fn, l, novarc)
