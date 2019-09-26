#!/usr/bin/python
import time
import subprocess
import re
import argparse
from os import path


def check_lustre_pool2():
    lustre_pool_list_cmd = ['lctl', 'pool_list', 'lustre']

    while True:
        try:
            pool_list = subprocess.Popen(lustre_pool_list_cmd,
                                         stdout=subprocess.PIPE
                                         ).stdout.read().split()
            pool_lst = pool_list[3]
            print("pool_list found {}".format(pool_lst))
        except IndexError:
            print("pool_list not found")
            time.sleep(5)
            continue

def check_lustre_pool():
    lustre_pool_list_cmd = ['lctl', 'pool_list', 'lustre']
    pool_list = subprocess.Popen(lustre_pool_list_cmd,
                                 stdout=subprocess.PIPE
                                 ).stdout.read().split()
    return pool_list

def check_lustre_pool1():
    while True:
        try:
            # Checking pool_list
            check_lustre_pool()
            print("pool_list found")
            time.sleep(20)
        except IndexError:
            time.sleep(20)
            continue

def check_pool_dir(template_directory):
    lustre_pool_list_cmd = ['lfs', 'getstripe', template_directory, '--pool']
    pool_list = subprocess.Popen(lustre_pool_list_cmd,
                                 stdout=subprocess.PIPE
                                 ).stdout.read().split()[0]
    return pool_list

if __name__== "__main__":
    try:
        # Checking pool_list
        pool_name = check_pool_dir("/lus/templates/FMtarget")
        print("pool_list found {0}".format(pool_name.decode()))
    except IndexError:
        print("pool not found")
