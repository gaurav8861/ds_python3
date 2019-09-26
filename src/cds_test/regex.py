# Copyright 2019 Cray Inc. All Rights Reserved.
# -*- coding: utf-8 -*-

import time
import subprocess
import re
import argparse
from os import path

def getFid(file_location):
    path2fid_cmd = ['lfs', 'path2fid', file_location]
    path2fid = subprocess.Popen(path2fid_cmd,
                                stdout=subprocess.PIPE
                                ).stdout.read().split()[0]
    return str(path2fid.decode())

def check_lustre_pool(template_directory):
    lustre_pool_dir_cmd = ['lfs', 'getstripe', template_directory, '--pool']
    pool_name = subprocess.Popen(lustre_pool_dir_cmd,
                                 stdout=subprocess.PIPE
                                 ).stdout.read().split()[0]
    return pool_name


# Slicing mount point
def slice_mountpoint(target_layout, mountpoint):
    return target_layout.split(mountpoint+'/', 1)[1]


def run():
    target_layout = "/lus/templates/FMtarget"
    mnt_cmd = ['mount', '-t', 'lustre']
    mount_cmd_op = subprocess.Popen(mnt_cmd,
                                    stdout=subprocess.PIPE
                                    ).stdout.read()

    if not mount_cmd_op:
        print("Unable to find lustre client mounted on the system")
        return 1

    try:
        mountpoint = mount_cmd_op.split()[2]
        fsname = mount_cmd_op.decode().split()[0].split('/')[1]
    except (ValueError, IndexError):
        print("Error fetching filesystem name")
        return 1

    ost_check = re.compile(r'.*(OST\d+).*\s+(\d+)%.*')
    file_check = re.compile(r'.*\n')
    # Sliced target layout
    target_sliced = slice_mountpoint(target_layout,
                                     mountpoint.decode())

    while True:
        if not path.isdir(target_layout):
            print("Target layout directory not found, "
                  "Waiting to detect correct target layout")
            time.sleep(20)
            continue

        try:
            # Checking pool_list
            pool_name = check_lustre_pool(target_layout)
            print("pool_list found {0}".format(pool_name))
        except IndexError:
            time.sleep(20)
            continue

        # Run lfs df to get the used percentage of all OSTs
        lfs_df_cmd = ['lfs', 'df', '-h', '--pool',
                      '{0}.flash'.format(fsname)]
        lfs_df = subprocess.Popen(lfs_df_cmd,
                                  stdout=subprocess.PIPE).stdout.read()
        if not lfs_df:
            raise LookupError

        ost_list = [x for (x, y) in
                    re.findall(ost_check, str(lfs_df))
                    if int(y) > 0]
        print(ost_list)
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
                        (0),
                        '--mtime', '+{0}'.format
                        (1),
                        '--ost', '{0}'.format(ost_nums)]
        lfs_find = subprocess.Popen(lfs_find_cmd,
                                    stdout=subprocess.PIPE
                                    ).stdout.read()

        if lfs_find:
            file_list_names = re.findall(file_check,
                                         str(lfs_find.decode()))
            for file_name in file_list_names:
                print(file_name)
        time.sleep(20)

def main():
    run()
if __name__== "__main__":
    main()