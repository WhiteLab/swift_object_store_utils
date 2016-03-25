#!/usr/bin/env python
import re
import sys
from subprocess import call
from subprocess import check_output

from date_time import date_time
from source_novarc import source_novarc


def download_from_swift_list(cont, fn, novarc):
    deproxy = 'unset http_proxy; unset https_proxy;'
    source_novarc(novarc)
    fh = open(fn, 'r')
    for obj in fh:
        obj = obj.rstrip('\n')
        (old, new) = obj.split('\t')
        swift_cmd = deproxy + "swift stat -v " + cont + " " + old
        sys.stderr.write(date_time() + swift_cmd + "\n")
        stat = check_output(swift_cmd, shell=True)
        header = re.search('URL: (\S+)\s+Auth Token: (\S+)\s+', stat)
        url = header.group(1)
        token = header.group(2)
        cp_cmd = 'curl -i ' + url + ' -X  COPY -H "X-Auth-Token: ' + token + '" -H "Destination: ' + new + '"'
        sys.stderr.write(cp_cmd + '\n')
        call(cp_cmd, shell=True)

    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Tool to take a list of swift objects from the same container and copy them server-side using curl commands')
    parser.add_argument('-c', '--container', action='store', dest='cont', help='Swift container, i.e. PANCAN')
    parser.add_argument('-f', '--file', action='store', dest='fn',
                        help='Tab-separated renaming list old <tab> new.  New object must start with container name in the event that ones is trying to also switch containers')
    parser.add_argument('-n', '--novarc', action='store', dest='novarc', help='.novarc with openstack authentication')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (cont, fn, novarc) = (inputs.cont, inputs.fn, inputs.novarc)
    download_from_swift_list(cont, fn, novarc)
