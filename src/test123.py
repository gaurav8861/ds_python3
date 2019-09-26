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


# checking lustre pool existence
def check_lustre_pool(template_directory):
    lustre_pool_dir_cmd = ['lfs', 'getstripe', template_directory, '--pool']
    pool_name = subprocess.Popen(lustre_pool_dir_cmd,
                                 stdout=subprocess.PIPE
                                 ).stdout.read().split()[0]
    return pool_name.decode()


# Slicing mount point
def slice_mountpoint(target_layout, mountpoint):
    return target_layout.split(mountpoint+'/', 1)[1]


def run(args):
    """ Infinite loop for the daemon to poll every 5 minutes """
    try:

        # Get mountpoint
        # command returns 0 when no client is mounted with an empty output
        # Example mount output
        # [root@cslmoxxxx ~]# mount -t lustre
        # 172.18.1.3@tcp:172.18.1.4@tcp:/lus on /lus type lustre
        target = "/lus/templates/FMtarget"

        mnt_cmd = ['mount', '-t', 'lustre']
        mount_cmd_op = subprocess.Popen(mnt_cmd,
                                        stdout=subprocess.PIPE
                                        ).stdout.read()

        if not mount_cmd_op:
            print("Unable to find lustre client mounted on the system")
            return 1

        try:
            mountpoint = mount_cmd_op.split()[2]
            print("mountpoint : ", mountpoint)
            fsname = mount_cmd_op.decode().split()[0].split('/')[1]
            print("fsname : ", fsname)
        except (ValueError, IndexError):
            print("Error fetching filesystem name")
            return 1

        ost_check = re.compile(r'.(OST\d+).*\s+(\d+)%.*')
        file_check = re.compile(r'.*\n')
        # Sliced target layout
        target_sliced = slice_mountpoint(target,
                                         mountpoint.decode())

        while True:
            if not path.isdir(target):
                print("Target layout directory not found, "
                                "Waiting to detect correct target layout")
                time.sleep(int(20))
                continue

            try:
                # Checking pool_list
                pool_name = check_lustre_pool(target)
                print("pool_list found {0}".format(pool_name))
            except IndexError:
                time.sleep(int(20))
                continue

            # Run lfs df to get the used percentage of all OSTs
            lfs_df_cmd = ['lfs', 'df', '-h', '--pool',
                          '{0}.flash'.format(fsname)]
            lfs_df = subprocess.Popen(lfs_df_cmd,
                                      stdout=subprocess.PIPE).stdout.read()
            if not lfs_df:
                raise LookupError

            ost_list = [x for (x, y) in
                        re.findall(ost_check, lfs_df.decode())
                        if int(y) > 0]
            print(ost_list)

            if not ost_list:
                raise IOError

            ost_ary = []
            for element in ost_list:
                ost_ary.append(element[-1])
            ost_nums = ','.join(ost_ary)
            print("ost_nums : ", ost_nums)
            # Generate lfs find command
            lfs_find_cmd = ['lfs', 'find', mountpoint.decode(),
                            '--type', 'f',
                            '--size', '+{0}M'.format
                            (args.file_size_threshold),
                            '--mtime', '+{0}'.format
                            (args.file_modified_time_threshold),
                            '--ost', '{0}'.format(ost_nums)]
            lfs_find = subprocess.Popen(lfs_find_cmd,
                                        stdout=subprocess.PIPE
                                        ).stdout.read()
            print("lfs_find : ", lfs_find)

            if lfs_find:

                file_list_names = re.findall(file_check,
                                             str(lfs_find.decode()))
                print("file_list_names : ", file_list_names)
                for file_name in file_list_names:
                    print(file_name)
            time.sleep(int(20))

    except LookupError:
        print("OST lookup failed")
        exit(1)
    except IOError:
        print("Unable to fetch lfs output")
        exit(1)
    except Exception as exc:
        print(exc)
        exit(1)


def parse_args():
    """Arg parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity",
                        action="count", dest="verbosity", default=0,
                        help=("Increase verbosity. May specify multiple "
                              "times."))
    # Kafka stuff.
    parser.add_argument("--target_layout",
                        action="store", dest="target_layout",
                        help="The directory containing the layout "
                        "information for the migration destination")
    parser.add_argument("-a", "--broker_address",
                        action="store", dest="dmrqhost",
                        default="0",
                        help=("hostname:port of DMRQ message broker: "
                              "default={0}".
                              format(0)))
    parser.add_argument("-o", "--outgoing_topic",
                        action="store", dest="topic_out",
                        default="d",
                        help=("Name of notifier outgoing topic: default={0}".
                              format(0)))
    # Topic to be Register
    parser.add_argument("-t", "--topic_name",
                        action="store", dest="topic_name",
                        default="BKR.kafka_temp_topic_out_default",
                        help=("Name of topic to be register: default={0}".
                              format("BKR.kafka_temp_topic_out_default")))
    # Priority
    parser.add_argument("-p", "--priority",
                        action="store", dest="priority",
                        default="BKR.priority_default",
                        help=("Priority of outgoing topic: default={0}".
                              format("BKR.priority_default")))
    parser.add_argument("-e", "--expiration",
                        action="store", dest="expiration",
                        help=("Number of days before expiration. Default={0}".
                              format("BKR.default_expiration_date_time")))
    # FILE_SIZE_THRESHOLD
    parser.add_argument("--file_size_threshold",
                        action="store", dest="file_size_threshold",
                        help=("File size threshold. Default={0}".
                              format("BKR.default_file_size_threshold")))
    # FILE_MODIFIED_TIME_THRESHOLD
    parser.add_argument("--file_modified_time_threshold",
                        action="store", dest="file_modified_time_threshold",
                        help=("File modified time threshold. Default={0}".
                              format
                              ("BKR.default_file_modified_time_threshold")))
    # Sleep time
    parser.add_argument("--sleep_time",
                        action="store", dest="sleep_time",
                        help=("Sleep time of daemon. Default={0}".
                              format("BKR.default_sleep_time")))

    args = parser.parse_args()
    return args


def main():
    """
    Main.
    """
    args = parse_args()

    run(args)
if __name__== "__main__":
    main()

