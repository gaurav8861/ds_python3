

import time
import subprocess
import re
import argparse
from os import path

def run():

    lfs_df = """
    UUID                       bytes        Used   Available Use% Mounted on
    lustre-MDT0000_UUID         3.3G       24.1M        3.0G   1% /lus[MDT:0]
    lustre-OST0000_UUID        39.0G      254.1M       36.7G   2% /lus[OST:0]
    
    filesystem_summary:        39.0G      254.1M       36.7G   1% /lus
    """

    ost_check1 = re.compile(r'.*(OST\d+).*\s+(\d+)%.*')

    # tuplist1 = re.findall(ost_check1, lfs_df)

    ost_list = [y for (x, y) in
                re.findall(ost_check1, str(lfs_df))
                if int(y) > 0]
    print("{0}".format(ost_list))

if __name__== "__main__":
    run()