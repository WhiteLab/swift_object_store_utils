#!/usr/bin/env python
import sys
from source_novarc import source_novarc
from subprocess import check_output
if len(sys.argv) != 2:
    sys.stderr.write('Need .novarc file\n')
    exit(1)


def messy_string2list(line):
    line = line.replace('^\s+', '')
    line = line.replace('\s+$', '')
    cur = line.split('\|')
    clean_list = cur.split()
    return clean_list


def get_flavors():
    cmd = 'nova flavor-list'
    flava = check_output(cmd, shell=True)
    flava = flava.split('\n')
    flava_dict = {}
    for i in xrange(3, (len(flava) -2), 1):
        try:
            cur = messy_string2list(line=flava[i])
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
    tot_mem = 0
    tot_cpu = 0
    tot_eph = 0
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
        (cpu, mem, eph) = (flavors[flavor]['cpu'], flavors[flavor]['mem'], flavors[flavor]['eph'])
        sys.stdout.write('\t'.join((name, vm, cdate, key_name, flavor, cpu, mem, eph)) + '\n')
        tot_cpu += int(cpu)
        tot_mem += int(mem)
        tot_eph += int(eph)
    sys.stdout.write('TOTAL\tNA\tNA\tNA\tNA\t' + '\t'.join((tot_cpu, tot_mem, tot_eph)) + '\n')


novarc = sys.argv[1]
source_novarc(novarc)
sys.stderr.write('Getting flavor list\n')
flavors = get_flavors()
sys.stderr.write('Getting vm list\n')
vms = get_vms()
sys.stdout.write('name\tID\tcreate_date\tkey\tflavor\tcpus\tmem\teph\n')
output_usage(flavors, vms)
