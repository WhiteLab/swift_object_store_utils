#!/usr/bin/env python
import sys
import re
from source_novarc import source_novarc
from subprocess import check_output
if len(sys.argv) != 2:
    sys.stderr.write('Need .novarc file\n')
    exit(1)


def messy_string2list(line):
    clean_list = line.split('|')
    clean_list.pop(0)
    for i in xrange(0, len(clean_list), 1):
        clean_list[i] = re.sub('^\s+', '', clean_list[i])
        clean_list[i] = re.sub('\s+$', '', clean_list[i])
    return clean_list


novarc = sys.argv[1]
source_novarc(novarc)
cmd = 'cinder list'
cur = check_output(cmd, shell=True)
cur = cur.split('\n')
sys.stdout.write('ID\tstatus\tname\tsize\tattached to\n')
tot_use = 0
for i in xrange(3, (len(cur) - 2), 1):
    info = messy_string2list(cur[i])
    tot_use += int(info[3])
    sys.stdout.write('\t'.join((info[0], info[2], info[3], info[6])) + '\n')
sys.stdout.write('TOTAL\tNA\tNA\t' + str(tot_use) + '\tNA\n')