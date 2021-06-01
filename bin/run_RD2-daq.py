#!/usr/bin/python3

import os, sys
import subprocess
import numpy
import glob
import time


print('run_DAQ.py [datedir]')

args = sys.argv
if len(args) >1:
    sub_dir=args[1]
else:
    sub_dir = datetime.date.today().strftime('%Y%m%d')

    
def runDAQ():

    ## Edit HERE ##

    data_dir = './data/' # with the last slash
#    sub_dir = '20210406' # without the last slash
    entries = 1000  # per 1 subrun

    frequency = 100000000.0 # Hz for radon amp
    #frequency = 5000000.0 # Hz For PMT test
    #frequency = 20000.0 # Hz For He-3
    trigger_level = -0.03 # V
    trigger_type = 'fall' # 'rise' or 'fall'
    #trigger_position = 3.e-4 # s
    trigger_position = 1./frequency*3000.
    
    dynamic_range = 2.0

#    daq_cmd = '/home/msgc/RD2/ad2_daq/bin/daq'
#    copy_script = '/home/msgc/RD2/ad2_daq/bin/autocopy.sh'
    daq_cmd = '/home/msgc/RD2-daq/bin/daq'
    copy_script = '/home/msgc/RD2-daq/bin/autocopy.sh'

    ###############


    subrun_name = find_newrun(data_dir+sub_dir+'/')
    print_cmd(['Manual copy:',copy_script,
        data_dir+sub_dir])

    cmd = [daq_cmd
    ,str(frequency)
    ,str(trigger_level)
    ,trigger_type
    ,str(trigger_position)
    ,str(dynamic_range)
    ,str(entries)
    ,data_dir+sub_dir + '/' + subrun_name 
    ]

    subprocess.run(['mkdir', '-p', data_dir+sub_dir ])
    print_cmd(cmd)
    subprocess.run(cmd)

    # Copy cmd
    print_cmd([copy_script, sub_dir])
    #subprocess.Popen([copy_script, sub_dir])


def print_cmd(cmd):
    for c in cmd:
        print(c, end=' ')
    print()


def find_newrun(dir_name):
    data_header = 'sub'
    files = glob.glob(dir_name+'*.txt')
    if len(files) == 0:
        return data_header+'0'.zfill(4)
    else:
        files.sort(reverse=True)
        num_pos = files[0].find('sub')
        return data_header+str(int(files[0][num_pos+3:num_pos+3+4])+1).zfill(4)


def auto_run():
    while(True):
        runDAQ()
        time.sleep(1)


if __name__ == '__main__':
    auto_run()
 
