#!/usr/bin/env python
import sys
import re
from source_novarc import source_novarc
from subprocess import check_output
import subprocess
import pdb
from date_time import date_time
if len(sys.argv) != 2:
    sys.stderr.write('Need .novarc file\n')
    exit(1)


def messy_string2list(line):
    line = line.replace('|', '')
    line = line.replace('^\s+', '')
    line = line.replace('\s+$', '')
    clean_list = line.split()
    return clean_list


def get_flavors():
    cmd = 'nova flavor-list'
    flava = check_output(cmd, shell=True)
    flava = flava.split('\n')
    flava_dict = {}
    for i in xrange(3, (len(flava) -2), 1):
        cur = messy_string2list(line=flava[i])
	try:
            flava_dict[cur[1]] = {}
            flava_dict[cur[1]]['mem'] = cur[2]
            flava_dict[cur[1]]['eph'] = cur[4]
            flava_dict[cur[1]]['cpu'] = cur[6]
	except:
	    sys.stderr.write('Flavor list failed at ' + flava[i] + '\n')
	    exit(1)
    return flava_dict


def get_vms():
    cmd = 'nova list'
    vms = check_output(cmd, shell=True)
    vms = vms.split('\n')
    vm_list = []
    for i in xrange(3, (len(vms) - 2), 1):
        cur = messy_string2list(line=vms[i])
        vm_list.append(cur[0])
    return vm_list


def output_usage(flavors, vms):
    for vm in vms:
        cmd = 'nova show ' + vm
        cur = check_output(cmd, shell=True)
        cur = cur.split('\n')
        cdate = messy_string2list(cur[13])
        cdate = cdate[1]
        flavor = messy_string2list(cur[14])
        flavor = flavor[1].split()
        flavor = flavor[0]
        key_name = messy_string2list(cur[18])
        key_name = key_name[1]
        name = messy_string2list(cur[20])
        name = name[1]
        sys.stderr.write('Getting info for ' + '\n')
        sys.stdout.write('\t'.join((name, vm, cdate, key_name, flavor, flavors[flavor]['cpu'], flavors[flavor]['mem'],
                                    flavors[flavor]['eph'])) + '\n')



novarc = sys.argv[1]
source_novarc(novarc)
sys.stderr.write('Getting flavor list\n')
flavors = get_flavors()
sys.stderr.write('Getting vm list\n')
vms = get_vms()
sys.stdout.write('name\tID\tcreate_date\tkey\tflavor\tcpus\tmem\teph\n')
output_usage(flavors, vms)
