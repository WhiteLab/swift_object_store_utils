#!/usr/bin/env python
import sys
from source_novarc import source_novarc
import subprocess
import os
from date_time import date_time


def setup_dirs(flist):
    temp = {}
    for fn in open(flist):
        parts = fn.split('/')
        if parts[1] not in temp:
            mkdir_cmd = 'mkdir -p FASTQC/' + parts[1] + '/QC'
            subprocess.call(mkdir_cmd, shell=True)
            temp[parts[1]] = 1


def get_fqc_stats(bnids, cont, obj, novarc):
    source_novarc(novarc)
    flist = cont + '_fqc.txt'
    get_list_cmd = 'cat ' + bnids + ' | xargs -IBN swift list ' + cont + ' --prefix ' + obj + '/BN/QC | grep  html | ' \
                                                                                            'grep -v report > ' + flist
    sys.stderr.write(date_time() + get_list_cmd + '\n')
    subprocess.call(get_list_cmd, shell=True)
    sys.stderr.write(date_time() + 'Setting up dirs\n')
    setup_dirs(flist)
    for path in flist:
        path = path.rstrip('\n')
        bnid = path.split('/')[1]
        fn = os.path.basename(path)
        dl_cmd = 'swift download ' + cont + ' ' + path + ' --output FASTQC/' + bnid + '/QC/' + fn
        sys.stderr.write(date_time() + dl_cmd + '\n')
        subprocess.call(dl_cmd, shell=True)
    sys.stderr.write('Process complete!\n')

    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Helper script to get fastqc files for variant viewer from object store')
    parser.add_argument('-b', '--bnids', action='store', dest='bnids', help='bnid list')
    parser.add_argument('-c', '--container', action='store', dest='cont', help='Swift container, i.e. PANCAN')
    parser.add_argument('-o', '--object', action='store', dest='obj',
                        help='Swift object name/prefix, i.e. RAW/2015-1234')
    parser.add_argument('-n', '--novarc', action='store', dest='novarc', help='.novarc with openstack authentication')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (bnids, cont, obj, novarc) = (inputs.bnids, inputs.cont, inputs.obj, inputs.novarc)
    get_fqc_stats(bnids, cont, obj, novarc)
