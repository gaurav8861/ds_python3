#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import subprocess
import re
import argparse
import os

from os import path

USED_SPACE_THRESHOLD = 0
FILE_MODIFIED_TIME_THRESHOLD = '1'
FILE_SIZE_THRESHOLD = '1'

# example lfs df output
#
# sms-1:~ # lfs df -h
# UUID                       bytes        Used   Available Use% Mounted on
# lustre-MDT0000_UUID         3.3G       23.3M        3.0G   1% /lus[MDT:0]
# lustre-OST0000_UUID        38.4G       49.0M       36.3G   1% /lus[OST:0]
# lustre-OST0001_UUID        38.4G       49.0M       36.3G   1% /lus[OST:1]
# filesystem_summary:        76.8G       98.1M       72.7G   1% /lus
# lfs find /lus --type f --size +0M --mtime +1 --ost 1

# lfs path2fid /lus/test/p1
def getFid(OUTPUT_FILE_LOCATION):
    path2fid_cmd = ['lfs', 'path2fid', OUTPUT_FILE_LOCATION]
    path2fid = subprocess.Popen(path2fid_cmd,
                                stdout=subprocess.PIPE
                                ).stdout.read().split()[0]
    return str(path2fid.decode())

def seperateout_mountpoint(target_layout):
    #file_check = re.compile(r'.\/*')
    #file_list_names = re.findall(file_check, str(target_layout))
    #print(file_list_names)

    #mnt_cmd = ['mount', '-t', 'lustre']
    #mount_cmd_op = subprocess.Popen(mnt_cmd,
        #                            stdout=subprocess.PIPE
         #                           ).stdout.read()


    #mountpoint = mount_cmd_op.split()[2]
    #print(mountpoint.decode())
    #fsname = mount_cmd_op.decode().split()[0].split('/')[1]
    lus = '/lus'
    test = target_layout.split(lus+'/',1)[1]
    print(test)


def run():
    """ Infinite loop for the daemon to poll every 5 minutes """
    try:
        target_layout = 'cUsers/gauravkumar'
        if target_layout:

            if target_layout[0] is not '/':
                print("Target layout directory path must begin with /")
                return 1
            if path.isdir(target_layout) is False:
                print("Target layout directory not found, please use correct target layout")
                return 1

        # Get mountpoint
        mnt_cmd = ['mount', '-t', 'lustre']
        mountpoint = subprocess.Popen(mnt_cmd,
                                      stdout=subprocess.PIPE
                                      ).stdout.read().split()[2]
        print(mountpoint)
        if not mountpoint:
            raise LookupError

        ost_check = re.compile(r'.*(OST\d+).*\s+(\d+)%.*')
        file_check = re.compile(r'.*\n')

        while True:
            # Run lfs df to get the used percentage of all OSTs
            lfs_df_cmd = ['lfs', 'df', '-h']
            lfs_df = subprocess.Popen(lfs_df_cmd,
                                      stdout=subprocess.PIPE).stdout.read()
            if not lfs_df:
                 raise LookupError

            ost_list = [x for (x, y) in
                        re.findall(ost_check, str(lfs_df))
                        if int(y) > 0]

            if not ost_list:
                raise IOError

            ost_ary = []
            for element in ost_list:
                ost_ary.append(element[-1])
            ost_nums = ','.join(ost_ary)
            # Generate lfs find command
            lfs_find_cmd = ['lfs', 'find', mountpoint.decode(),
                            '--type', 'f',
                            '--size', '+{0}M'.format
                            (FILE_SIZE_THRESHOLD),
                            '--mtime', '-{0}'.format
                            (FILE_MODIFIED_TIME_THRESHOLD),
                            '--ost', '{0}'.format(ost_nums)]
            lfs_find = subprocess.Popen(lfs_find_cmd,
                                        stdout=subprocess.PIPE
                                        ).stdout.read()
            # output result -
            # /lus/test
            # /lus/test1
            if lfs_find:
                file_list_names = re.findall(file_check,
                                             str(lfs_find.decode()))
                for file_name in file_list_names:
                    print(file_name.rstrip())

            time.sleep(5)
    except LookupError:
        print("OST lookup failed")
        exit(1)
    except IOError:
        print("Unable to fetch lfs output")
        exit(1)
    except Exception as exc:
        print(str(exc))
        exit(1)

if __name__== "__main__":
   # run()
   seperateout_mountpoint("/lus/template/file")