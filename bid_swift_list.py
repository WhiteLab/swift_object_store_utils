#!/usr/bin/env python

import sys
from subprocess import call
from source_novarc import source_novarc
from date_time import date_time


def bid_swift_list(cont, obj, blist, novarc):
    source_novarc(novarc)
    fh = open(blist, 'r')
    for bid in fh:
        bid = bid.rstrip('\n')
        swift_cmd = "swift list " + cont + " --prefix " + obj + "/" + bid
        sys.stderr.write(date_time() + swift_cmd + "\n")
        try:
            call(swift_cmd, shell=True)
        except:
            sys.stderr.write(date_time() + "Lising of " + bid + ' of ' + obj + " from " + cont + " failed\n")
            return 1

    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Helper script to get all files associated with a BID')
    parser.add_argument('-c', '--container', action='store', dest='cont', help='Swift container name, i.e. PANCAN')
    parser.add_argument('-o', '--object', action='store', dest='obj', help='Swift object prefix, i.e. RAW/2015-1234')
    parser.add_argument('-l', '--list', action='store', dest='blist', help='Bionimbus ID list, one per line')
    parser.add_argument('-n', '--novarc', action='store', dest='novarc', help='.novarc with openstack authentication')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (cont, obj, blist, novarc) = (inputs.cont, inputs.obj, inputs.blist, inputs.novarc)
    bid_swift_list(cont, obj, blist, novarc)
